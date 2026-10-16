"""AURA/Ultralytics adapter for the station's normalized detection contract."""
import math
import os
from pathlib import Path
import time

from .config import ROOT
from .aura.detection_modes import select_detections
from .aura.osd_filter import OsdFilter


def prepare_runtime():
    """Import native AI libraries before starting video/inference worker threads."""
    (ROOT / 'data' / 'ultralytics').mkdir(parents=True, exist_ok=True)
    os.environ.setdefault('YOLO_CONFIG_DIR', str(ROOT / 'data' / 'ultralytics'))
    os.environ.setdefault('YOLO_AUTOINSTALL', 'false')
    import torch
    import ultralytics
    return torch, ultralytics


def local_path(value):
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def normalize_detections(detections, width, height):
    """VisDrone person classes must feed the existing rescue-candidate policy."""
    output = []
    for item in detections:
        coordinates = item['xyxy']
        if len(coordinates) != 4 or not all(math.isfinite(float(x)) for x in coordinates):
            continue
        x1, y1, x2, y2 = [max(0.0, min(1.0, float(x) / size))
                           for x, size in zip(coordinates, (width, height, width, height))]
        score = float(item['confidence'])
        if x2 <= x1 or y2 <= y1 or not math.isfinite(score) or not 0 <= score <= 1:
            continue
        label = item['label']
        output.append({'label': 'person' if label.lower() in ('person', 'pedestrian', 'people') else label,
                       'source_label': label, 'confidence': score, 'class_id': item['class_id'],
                       'detector': 'AURA YOLO', 'box': [x1, y1, x2, y2]})
    return output


class YoloDetector:
    def __init__(self, config):
        torch, ultralytics = prepare_runtime()
        YOLO = ultralytics.YOLO
        from .aura.hardware import Hardware
        from .aura.pipeline import IdentityProcessor
        from .aura.clahe import ClaheEnhancer
        from .aura.fpv_hybrid import FpvHybridEnhancer

        path = local_path(config.yolo_model)
        if not path.is_file():
            raise ValueError(f'Model file missing: {path}. Run scripts/setup_aura.py first.')
        torch.set_num_threads(2)
        self.hardware = Hardware(torch, config.yolo_device, config.yolo_precision)
        self.model = YOLO(str(path), task='detect').to(self.hardware.device)
        self.config, self.path = config, path
        self.enhancer = {'identity': IdentityProcessor, 'clahe': ClaheEnhancer,
                         'fpv_hybrid': FpvHybridEnhancer}[config.detection_enhancement]()
        self.osd = None
        self.osd_size = None
        self.last_details = {}

    def predict(self, frame):
        started = time.monotonic()
        self.hardware.activate()
        enhanced, _ = self.enhancer.process(frame.copy())
        enhancement_ms = (time.monotonic() - started) * 1000
        h, w = frame.shape[:2]
        if enhanced.shape != frame.shape:
            raise ValueError('Enhancer changed frame dimensions')
        if self.config.detection_osd_profile and self.osd_size != (w, h):
            # Profiles are recording-specific; do not silently rescale to another layout.
            self.osd = OsdFilter(local_path(self.config.detection_osd_profile), w, h)
            self.osd_size = (w, h)
        self.hardware.synchronize()
        tick = time.monotonic()
        result = self.model.predict(enhanced, conf=self.config.confidence_threshold,
                                    imgsz=self.config.yolo_imgsz, iou=self.config.yolo_iou,
                                    device=self.hardware.predict_device, quantize=16 if self.hardware.fp16 else 32,
                                    verbose=False, max_det=300)[0]
        self.hardware.synchronize()
        inference_ms = (time.monotonic() - tick) * 1000
        boxes = result.boxes
        raw = [dict(class_id=int(c), label=result.names[int(c)], confidence=float(s), xyxy=b)
               for b, s, c in zip(boxes.xyxy.cpu().tolist(), boxes.conf.cpu().tolist(),
                                  boxes.cls.cpu().tolist())]
        mode = {'original': 0, 'exclude25': 1, 'exclude50': 2}[self.config.detection_mode]
        keep, excluded = select_detections(raw, mode, self.osd)
        self.last_details = {'model': self.path.name, 'hardware': self.hardware.report(),
                             'enhancement': self.config.detection_enhancement,
                             'enhancement_ms': round(enhancement_ms, 1),
                             'inference_ms': round(inference_ms, 1),
                             'filter_mode': self.config.detection_mode,
                             'raw_count': len(raw), 'excluded_count': len(excluded),
                             'excluded': excluded}
        return normalize_detections([raw[i] for i in keep], w, h)
