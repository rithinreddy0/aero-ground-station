"""Download hash-verified AURA model assets from a pinned teammate commit."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request
import urllib.parse

ROOT = Path(__file__).resolve().parent.parent
REVISION = 'd50829119b598e5b32b352f384fdd25aca367f08'
BASE = f'https://raw.githubusercontent.com/7-Azhar/major_project/{REVISION}/'
ASSETS = {
    'visdrone': ('ML/models/yolov8m_visdrone_recovered.pt', 'models/aura/yolov8m_visdrone_recovered.pt',
                 '200f73fd846db1ceb46a55614dc90081b4ecfa1393f3f4cfd6152dd93a5928c9'),
    'nano': ('ML/models/yolo26n.pt', 'models/aura/yolo26n.pt',
             '9b09cc8bf347f0fc8a5f7657480587f25db09b34bf33b0652110fb03a8ad4fef'),
    'sample': ('feeed enhancement/samples/fpv/real_fpv_user_flight.mp4', 'data/aura/real_fpv_user_flight.mp4',
               '324d6a436a897d25e145df141b6cbf08198ef874d490b792682f3cdaca08428f'),
}


def download(key):
    source, target, expected = ASSETS[key]
    path = ROOT / target
    if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == expected:
        print(f'Already verified: {target}', flush=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_suffix(path.suffix + '.partial')
    request = urllib.request.Request(BASE + urllib.parse.quote(source), headers={'User-Agent': 'Aero-AURA-setup'})
    digest = hashlib.sha256()
    try:
        with urllib.request.urlopen(request, timeout=60) as response, partial.open('wb') as output:
            while block := response.read(1024 * 1024):
                digest.update(block)
                output.write(block)
        if digest.hexdigest() != expected:
            raise RuntimeError(f'Checksum mismatch: {key}; refusing asset')
        partial.replace(path)
        print(f'Downloaded and verified: {target}', flush=True)
    finally:
        partial.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', choices=('visdrone', 'nano', 'both'), default='visdrone')
    parser.add_argument('--sample', action='store_true')
    args = parser.parse_args()
    for key in (('visdrone', 'nano') if args.model == 'both' else (args.model,)):
        download(key)
    if args.sample:
        download('sample')
    profile = dict(mode='demo', video_source='data/aura/real_fpv_user_flight.mp4', video_loop=True,
                   yolo_model=ASSETS['nano' if args.model == 'nano' else 'visdrone'][1],
                   confidence_threshold=0.25, detection_interval_s=0.3,
                   live_control=False, live_missions=False, detection_mode='original',
                   detection_enhancement='identity', yolo_device='cpu', yolo_precision='fp32')
    (ROOT / 'config.aura-playback.json').write_text(json.dumps(profile, indent=2) + '\n', encoding='utf-8')
    print('Wrote config.aura-playback.json (real video, simulated flight, no RF output).')


if __name__ == '__main__':
    main()
