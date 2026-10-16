"""Read-only USB commissioning audit. Close Mission Planner first."""
import argparse
import json
import time
from datetime import datetime
from pathlib import Path

from pymavlink import mavutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="COM16")
    parser.add_argument("--timeout", type=float, default=30)
    args = parser.parse_args()
    connection = mavutil.mavlink_connection(args.port, baud=115200)
    try:
        heartbeat = connection.wait_heartbeat(timeout=10)
        if heartbeat is None:
            raise RuntimeError("No heartbeat received")
        if heartbeat.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED:
            raise RuntimeError("Aircraft is armed; stop commissioning")
        connection.mav.param_request_list_send(
            connection.target_system, connection.target_component
        )
        params = {}
        expected = None
        deadline = time.monotonic() + args.timeout
        while time.monotonic() < deadline:
            message = connection.recv_match(type="PARAM_VALUE", blocking=True, timeout=1)
            if message is None:
                continue
            name = message.param_id
            if isinstance(name, bytes):
                name = name.decode("ascii").rstrip("\0")
            params[name] = message.param_value
            expected = message.param_count
            if len(params) >= expected:
                break
        output = Path("data/commissioning")
        output.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        report = {
            "port": args.port,
            "system": connection.target_system,
            "component": connection.target_component,
            "expected_parameters": expected,
            "received_parameters": len(params),
            "complete": expected is not None and len(params) == expected,
            "parameters": params,
        }
        target = output / f"parameters-{stamp}.json"
        target.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"Saved {len(params)}/{expected} parameters: {target.resolve()}")
        for name in sorted(params):
            if name.startswith(("FRAME_", "SERIAL", "OSD_TYPE", "MOT_PWM_TYPE", "ESC_CALIBRATION", "AHRS_ORIENTATION", "GPS1_TYPE", "COMPASS_USE", "ARMING_CHECK", "INS_ACC")):
                print(f"{name} = {params[name]:g}")
        if not report["complete"]:
            raise RuntimeError("Incomplete backup; retry before changing settings")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
