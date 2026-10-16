# Verification record — 9 October 2026

Environment: Windows, Python 3.11.4. Base dependencies installed in the project-local `.venv`; exact resolved packages are captured in `requirements-lock.txt`.

## Passed

`python -m pytest -q`: **39 tests passed**. The environment emits one upstream Starlette/httpx TestClient deprecation warning; no test failure.

Covered: independent heartbeat/position/GPS/battery/EKF freshness, flight-state rejection, lease/video gates, strict command parsing, BODY_NED velocity frame/mask, aircraft isolation, real pymavlink position/GPS packet decode, manual expiry/zero setpoint, pilot takeover, route validation/fence/finite values, north-to-body heading rotation, waypoint hold/completion, copilot search/perimeter/orbit/measured movement grammar, persistent distinct-frame person tracking, AI incident/pause, latched GPS/video/battery pauses and explicit recovery, mission persistence/API gates, same-origin/token/Host protection, incident JPEGs and decodable AVI recording.

`node --check web/app.js` and Python `compileall` passed.

Browser verification covered the Mission Planner-style layout at desktop width and the narrow app-panel layout; satellite tiles rendered with numbered route markers and attribution. The copilot generated a 10-point search, the operator applied it, and simulation followed GPS waypoints. Injecting a synthetic person under auto-pause policy produced a persistent candidate, paused the mission and logged an incident. Mission saving and fault gates were also checked in the UI. Earlier video/notes/recording verification remains valid. Browser error logs were empty during the checked mission flow. Synthetic scenarios are application-policy tests, not real detector or flight benchmarks.

## Not yet verified

No capture card, FPV receiver video, GPS receiver, RadioMaster MAVLink link, ArduPilot SITL instance or physical aircraft was connected. The unit test decodes real MAVLink packet structures but is not an autopilot integration test. Optional YOLO/Tesseract dependencies and models have not been installed or benchmarked. No real aerial detection accuracy or RF/camera-to-browser latency has been measured. Exact firmware migration, wiring, receiver compatibility, pilot takeover and loss-of-link behaviour require the commissioning procedure and connected hardware.

See `COMMISSIONING.md` for the hardware acceptance sequence. Software test success is not physical-flight certification.
