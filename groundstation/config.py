import json
import os
import math
from dataclasses import dataclass, field, fields
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Config:
    mode: str = "demo"
    video_source: str | int = "demo"
    video_width: int = 960
    video_height: int = 540
    video_fps: int = 30
    jpeg_quality: int = 75
    mavlink_endpoint: str = "udpin:0.0.0.0:14550"
    mavlink_baud: int = 460800
    target_system: int = 1
    target_component: int = 1
    live_control: bool = False
    live_missions: bool = False
    max_speed_mps: float = 0.5
    max_altitude_m: float = 30
    geofence_radius_m: float = 50
    minimum_battery_percent: int = 25
    home_latitude: float = 17.385
    home_longitude: float = 78.4867
    yolo_model: str = ""
    yolo_device: str = "cpu"
    yolo_precision: str = "fp32"
    yolo_imgsz: int = 640
    yolo_iou: float = 0.7
    detection_enhancement: str = "identity"
    detection_mode: str = "original"
    detection_osd_profile: str = ""
    video_loop: bool = False
    detection_interval_s: float = 0.3
    confidence_threshold: float = 0.5
    ocr_interval_s: float = 1.0
    tesseract_cmd: str = ""
    osd_regions: list = field(default_factory=list)

    def __post_init__(self):
        import re
        if self.yolo_device not in ('auto', 'cpu', 'cuda') and not re.fullmatch(r'cuda:\d+', self.yolo_device):
            raise ValueError('YOLO device must be auto, cpu, cuda, or cuda:N')
        if self.yolo_precision not in ('auto', 'fp32'):
            raise ValueError('YOLO precision must be auto or fp32')
        if type(self.yolo_imgsz) is not int or not 160 <= self.yolo_imgsz <= 1280 or self.yolo_imgsz % 32:
            raise ValueError('YOLO image size must be a multiple of 32 between 160 and 1280')
        if not math.isfinite(self.yolo_iou) or not 0 < self.yolo_iou <= 1:
            raise ValueError('Invalid YOLO IoU threshold')
        if self.detection_enhancement not in ('identity', 'clahe', 'fpv_hybrid'):
            raise ValueError('Unsupported detection enhancement')
        if self.detection_mode not in ('original', 'exclude25', 'exclude50'):
            raise ValueError('Unsupported detection mode')
        if self.detection_mode != 'original' and not self.detection_osd_profile:
            raise ValueError('OSD exclusion requires a calibrated detection_osd_profile')
        if type(self.video_loop) is not bool:
            raise ValueError('video_loop must be boolean')
        if not all(math.isfinite(v) for v in (self.home_latitude,self.home_longitude,self.max_speed_mps,self.max_altitude_m,self.geofence_radius_m)):
            raise ValueError('Navigation configuration must be finite')
        if not -85<=self.home_latitude<=85 or not -180<=self.home_longitude<=180:
            raise ValueError('Invalid configured home coordinates')
        if self.mode not in ("demo", "live"):
            raise ValueError("mode must be demo or live")
        if not 0 < self.max_speed_mps <= 2 or not 0 < self.geofence_radius_m <= 500:
            raise ValueError("Invalid control limits")
        if not 0 < self.max_altitude_m <= 120 or not 0 <= self.minimum_battery_percent <= 100:
            raise ValueError("Invalid altitude or battery limit")
        if not 1 <= self.video_fps <= 60 or not 160 <= self.video_width <= 1920 or not 120 <= self.video_height <= 1080:
            raise ValueError("Invalid video settings")
        if self.detection_interval_s < 0.1 or self.ocr_interval_s < 0.2:
            raise ValueError("Processing intervals too short")
        if not 0 <= self.confidence_threshold <= 1:
            raise ValueError("Invalid confidence threshold")
        if self.mode == "live" and self.video_source == "demo":
            raise ValueError("Live mode requires a real video source index or file")

    @classmethod
    def load(cls):
        path = Path(os.environ.get("GS_CONFIG", str(ROOT / "config.json")))
        raw = json.loads(path.read_text()) if path.exists() else {}
        allowed = {f.name for f in fields(cls)}
        unknown = raw.keys() - allowed
        if unknown:
            raise ValueError(f"Unknown settings: {sorted(unknown)}")
        return cls(**raw)
