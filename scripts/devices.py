"""Run with .venv/Scripts/python scripts/devices.py; no aircraft commands."""
import json
import os
import cv2
from serial.tools import list_ports

print("Serial ports:")
print(json.dumps([{ "port": p.device, "description": p.description, "hardware": p.hwid}
                  for p in list_ports.comports()], indent=2))
print("Checking video indices 0–4. Close OBS/other camera applications first.")
for index in range(5):
    capture = cv2.VideoCapture(index, cv2.CAP_DSHOW if os.name == "nt" else cv2.CAP_ANY)
    try:
        if capture.isOpened():
            ok, frame = capture.read()
            print(f"Video {index}: {'frame '+str(frame.shape) if ok else 'opens but no frame'}")
    finally:
        capture.release()
