import json
import threading
import time
from types import SimpleNamespace

import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient

from groundstation.config import Config
from groundstation.detection import normalize_detections
from groundstation.intelligence import Intelligence
from groundstation.aura.osd_filter import OsdFilter
from groundstation.aura.detection_modes import select_detections
from groundstation.video import Video
import groundstation.main as main


def test_visdrone_people_reach_rescue_policy():
    raw = [dict(class_id=0, label='pedestrian', confidence=.8, xyxy=[10, 20, 50, 80]),
           dict(class_id=1, label='people', confidence=.7, xyxy=[60, 20, 90, 80]),
           dict(class_id=3, label='car', confidence=.9, xyxy=[1, 1, 10, 10])]
    detections = normalize_detections(raw, 100, 100)
    assert [x['label'] for x in detections] == ['person', 'person', 'car']
    assert [x['source_label'] for x in detections] == ['pedestrian', 'people', 'car']
    policy = Intelligence()
    for sequence in range(3):
        policy.update(dict(age_s=.1, detection_sequence=sequence, detections=detections), now=sequence * .1)
    assert policy.snapshot(now=.3)['confirmed_count'] == 2


def test_invalid_boxes_and_scores_are_not_exposed():
    raw = [dict(class_id=0, label='people', confidence=.8, xyxy=[-5, 0, 120, 100]),
           dict(class_id=0, label='people', confidence=.8, xyxy=[float('nan'), 0, 1, 1]),
           dict(class_id=0, label='people', confidence=float('nan'), xyxy=[0, 0, 1, 1]),
           dict(class_id=0, label='people', confidence=.8, xyxy=[10, 10, 2, 2])]
    result = normalize_detections(raw, 100, 100)
    assert len(result) == 1 and result[0]['box'] == [0, 0, 1, 1]


def test_osd_exclusions_are_opt_in_and_dimension_specific(tmp_path):
    profile = tmp_path / 'profile.json'
    profile.write_text(json.dumps(dict(reference_size=[100, 100], regions=[
        dict(name='timer', xyxy=[0, 0, 20, 20], max_box_size=[20, 20])])), encoding='utf-8')
    osd = OsdFilter(profile, 100, 100)
    raw = [dict(label='people', confidence=.9, xyxy=[1, 1, 10, 10])]
    assert select_detections(raw, 0, osd)[0] == [0]
    assert select_detections(raw, 1, osd)[1][0]['excluded_by'] == 'timer'
    with pytest.raises(ValueError):
        OsdFilter(profile, 200, 100)
    with pytest.raises(ValueError):
        Config(detection_mode='exclude25')


def test_failed_selected_model_does_not_run_hog(monkeypatch):
    def fail(_):
        raise RuntimeError('test model unavailable')
    monkeypatch.setattr('groundstation.video.YoloDetector', fail)
    video = Video(Config(video_source='not-demo.mp4', yolo_model='missing.pt'))
    video.frame = np.zeros((240, 320, 3), dtype=np.uint8)
    video.frame_at, video.sequence = time.monotonic(), 1
    thread = threading.Thread(target=video.analyze)
    thread.start()
    time.sleep(.15)
    video.stop_event.set()
    thread.join(2)
    assert video.ai_status == 'AI unavailable: test model unavailable'
    assert video.detections == []


def make_video(path):
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*'MJPG'), 10, (320, 240))
    assert writer.isOpened()
    for value in range(4):
        writer.write(np.full((240, 320, 3), 50 + value * 20, dtype=np.uint8))
    writer.release()


@pytest.fixture
def upload_dependencies(tmp_path, monkeypatch):
    weights = tmp_path / 'weights.pt'
    weights.write_bytes(b'test fake weights; never loaded')
    monkeypatch.setattr(main, 'AI_MODELS', {'visdrone': weights, 'nano': weights})
    monkeypatch.setattr(main, 'ai_available', lambda: True)
    class FakeDetector:
        def __init__(self, config):
            self.path = weights
            self.hardware = SimpleNamespace(device='cpu')
            self.last_details = {'model': 'test', 'enhancement': 'identity', 'filter_mode': 'original', 'excluded_count': 0}
        def predict(self, frame):
            return [{'label': 'person', 'source_label': 'pedestrian', 'confidence': .9,
                     'box': [.2, .2, .6, .8], 'class_id': 0, 'detector': 'AURA YOLO'}]
    monkeypatch.setattr('groundstation.video.YoloDetector', FakeDetector)
    path = tmp_path / 'input.avi'
    make_video(path)
    return path.read_bytes()


def test_upload_playback_and_frame_matched_annotations(tmp_path, upload_dependencies):
    with TestClient(main.create_app(Config(), tmp_path / 'store')) as client:
        token = client.get('/api/session').json()['token']
        auth = {'x-station-token': token, 'content-type': 'application/octet-stream',
                'x-filename': '..%2Fexample%20clip.avi'}
        assert client.get('/api/video/models').json()['models'][0]['ready']
        response = client.post('/api/video/upload?model=visdrone', content=upload_dependencies, headers=auth)
        assert response.status_code == 200, response.text
        assert response.json()['name'] == 'example clip.avi'
        station = client.app.state.station
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline and not station.video.ai_jpeg:
            time.sleep(.05)
        assert station.video.ai_jpeg[:2] == b'\xff\xd8'
        decoded = cv2.imdecode(np.frombuffer(station.video.ai_jpeg, np.uint8), cv2.IMREAD_COLOR)
        assert decoded.shape[:2] == (240, 320)
        state = client.get('/api/status').json()
        assert state['video']['processed_video']
        assert state['mode'] == 'demo'
        assert station.telemetry.connection is None
        assert station.config.live_control is False and station.config.live_missions is False
        time.sleep(.6)  # Source is shorter than this: explicit looping must keep capture alive.
        assert station.video.snapshot()['age_s'] < 1


def test_upload_rejects_invalid_file_and_preserves_source(tmp_path, upload_dependencies):
    with TestClient(main.create_app(Config(), tmp_path / 'store')) as client:
        token = client.get('/api/session').json()['token']
        auth = {'x-station-token': token, 'content-type': 'application/octet-stream', 'x-filename': 'fake.mp4'}
        response = client.post('/api/video/upload', content=b'not a video', headers=auth)
        assert response.status_code == 422
        assert client.app.state.station.config.video_source == 'demo'
        assert not list((tmp_path / 'store' / 'uploads').iterdir())
        assert client.post('/api/video/upload', content=b'x').status_code == 403


def test_upload_cannot_replace_live_aircraft_input(tmp_path):
    config = Config(mode='live', video_source='missing.mp4', mavlink_endpoint='udpin:127.0.0.1:14998')
    with TestClient(main.create_app(config, tmp_path)) as client:
        token = client.get('/api/session').json()['token']
        response = client.post('/api/video/upload', headers={'x-station-token': token})
        assert response.status_code == 409
