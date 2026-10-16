# Delivery stages and advanced work

## Implemented software baseline

Mission Planner-style workspace, interactive offline/satellite/street map, editable waypoint table, saved missions and file exchange, local intent copilot, GPS-feedback Guided route execution, persistent person tracking, optional automatic mission pause, simulation fault lab, video capture/recording, optional YOLO/OCR, telemetry and logging. Demo and API/control/mission tests exercise these functions. Hardware integration is pending.

## Next: physical observation

Buy and verify composite capture against the actual receiver; identify GPS/compass and receiver; migrate/calibrate ArduCopter if needed; establish ELRS MAVLink downlink; verify live sensor freshness and video latency. This is the immediate milestone, because current hardware information is incomplete.

## Next: measured supervised control

Run ArduPilot SITL integration with actual MAVLink decode and response, then a controlled test environment with an experienced pilot. Prove link failure, browser closure, telemetry staleness, manual takeover and FC timeout. Add automated desired-versus-observed movement feedback. No field trial is implied by passing unit tests.

## Advanced vision

Train/evaluate an aerial search person model with an appropriate licensed dataset, annotated false positives/negatives and flight-condition splits. Temporal image-space tracking is implemented; add better identity association, time alignment and adjustable OSD masks. Calibrate OCR regions and units; store extracted values with confidence/freshness, never as control authority. Develop geo-projection only after camera intrinsics/extrinsics, time synchronization and terrain/ranging are available.

## Advanced operations

Bounded recording, online map layers, incident logs and simulator-verified Guided route execution are implemented. Add total storage retention, WebRTC if measured MJPEG performance is insufficient, replay, licensed offline imagery, richer incident workflow, and onboard MAVLink mission upload/download with acknowledgements. Add motion/depth sensors before obstacle avoidance or visual following; define and validate the estimator's operating envelope.

## Autonomy boundary

Mission planning and AI remain on the laptop, while stabilization and loss-of-link failsafes remain on the aircraft. Vision can advise or pause a reviewed mission; it cannot choose an obstacle-free path from a single FPV camera. The complete plan/follow/detect/pause workflow works in simulation. Physical autonomous rescue search remains an integration and validation stage. Public hosting, remote operators, authentication, signed telemetry and multi-aircraft identity need separate architecture before expansion beyond a local single-operator station.
