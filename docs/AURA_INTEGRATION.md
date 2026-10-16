# AURA detection integration

Integrated from the team's [7-Azhar/major_project](https://github.com/7-Azhar/major_project)
at commit `d50829119b598e5b32b352f384fdd25aca367f08`.

## Run on Windows

Use Python 3.11 and the project virtual environment. CPU-only PyTorch avoids downloading a CUDA runtime on laptops without a compatible NVIDIA setup:

One-command setup: `powershell -ExecutionPolicy Bypass -File scripts/setup-aura.ps1 -IncludeSample`.

```powershell
.\.venv\Scripts\python.exe -m pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -r requirements-ai.txt
.\.venv\Scripts\python.exe scripts/setup_aura.py --model both --sample
powershell -ExecutionPolicy Bypass -File scripts/start.ps1
```

The regular default config opens the simulated aircraft. In the left sidebar, use
**Test AI on your video**, choose a recording and detector, then **Upload & detect**.
MP4/H.264 is recommended; MOV, AVI, MKV, WEBM and M4V are accepted if OpenCV can
decode them. Maximum upload is 500 MB. Uploaded files remain in `data/uploads/`;
delete recordings manually when no longer needed. Files and weights are ignored by Git.

The flight telemetry is simulated and MAVLink is not opened in this test mode.
Uploading while the station is in live mode is rejected. Recording must be stopped
before changing the source. Source changes pause any simulated mission and clear
the control lease and person tracks. The existing authentication and same-origin
checks protect uploads.

Uploads loop at their native frame rate; inference consumes the newest available
frame and skips frames when processing is slower than capture. The annotated stream
uses the exact frame that was inferred, not boxes painted on a newer raw frame.
It reports processing time and source frame sequence. Uncheck **Show annotated
detection video** to inspect the raw input. Throughput depends on CPU/GPU, model and
resolution; this is continuous detection playback, not a guarantee of full-rate inference.
The saved AVI recorder and incident snapshots preserve the raw capture, not annotated AI frames.

To start immediately with the downloaded sample instead:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start.ps1 -Config config.aura-playback.json
```

## What was brought across

- The team's recovered YOLOv8m VisDrone checkpoint, plus their lightweight YOLO26n
  checkpoint as a faster alternative. Setup downloads are pinned and SHA-256 checked
  using the team's `assets-manifest.json` values. Models are not downloaded during inference.
- `ML/hardware.py`, `ML/osd_filter.py` and `ML/detection_modes.py` are included under
  `groundstation/aura/` with source attribution here.
- The classical CLAHE and FPV hybrid processors and their base interface were
  adapted from `feeed enhancement/app/`; imports were made package-relative.
- The source video's OSD profile is included at `config/aura-user-flight-osd.json`.
  It is disabled by default, is specific to the original 640x480 recording, and
  must not be reused on a different OSD layout without calibration. Exclusion can
  hide real targets. Dimensions are validated rather than silently scaled.
- VisDrone `pedestrian` and `people` are normalized to the station's `person`
  policy label while preserving the original class name in the UI and API.

This integration does not claim CBAM inference: the upstream experiment metadata
explicitly identifies the recovered VisDrone checkpoint as having no CBAM.
Neural Zero-DCE enhancement, training and the separate upstream dashboard are not
part of this integration. The optional classical enhancements affect the detector's
input; raw capture remains available for operator comparison.

## Configuration

Existing `yolo_model` selects a local checkpoint. Additional options are
`yolo_device` (`cpu`, `auto`, `cuda` or `cuda:N`), `yolo_precision` (`fp32` or `auto`),
`yolo_imgsz`, `yolo_iou`, `detection_enhancement` (`identity`, `clahe`, `fpv_hybrid`),
`detection_mode` (`original`, `exclude25`, `exclude50`), `detection_osd_profile` and
`video_loop`. OSD exclusion requires a calibrated profile. Upload testing defaults
to original detections at confidence 0.25, with no OSD exclusions.

If a selected model fails to load or infer, the application reports the error rather
than silently switching to the HOG baseline. HOG remains available when no YOLO
model is selected. Synthetic demo video continues to use clearly labelled synthetic
annotations and does not load a heavyweight detector unnecessarily.

The source repository had no root LICENSE in the inspected tree. Attribution is
preserved; the team's permission and upstream model/library licenses still govern
redistribution. Ultralytics/model terms must be reviewed for deployment or commercial use.

## Validation limits

Automated tests cover VisDrone-to-person policy mapping, malformed-box rejection,
OSD opt-in and size checks, explicit model failure, authenticated uploads, invalid
video cleanup, short-video looping, decodable frame-matched annotations and rejection
of video substitution in live mode. The real VisDrone checkpoint has also been run
on the team's sample. Neither detection counts nor a successful smoke test establish
precision, recall, victim coordinates, real aerial accuracy or camera-to-display latency.
