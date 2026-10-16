# Mission planner and AI behaviour

## Interface

The reference image's navigation/map/action/waypoint layout has been adapted into a responsive local browser workspace. Flight instruments and video occupy the left sidebar; the interactive map and waypoint table occupy the centre; mission actions, copilot and grid planner occupy the right. The bottom dock contains event history, notes, simulation scenarios and software performance.

Map interaction: drag to pan, wheel/buttons to zoom, Add waypoint then click to insert, click/drag markers to select/move, Fit route to frame the plan, and Centre on aircraft to recenter. Map editing is disabled during execution. Waypoints can be reordered, deleted and changed in the table. Undo keeps the latest 30 draft changes.

The default layer is an offline coordinate grid, without terrain. Optional satellite tiles use Esri World Imagery; street tiles use OpenStreetMap. These require internet and send viewed tile areas to the provider. They are background context, not an obstacle or terrain-height measurement. Attribution is visible; tiles are requested only for the current viewport and held in a bounded in-memory cache.

## Plan lifecycle

Draft → validate/apply → ready → running → paused/completed/cancelled. Editing a paused route creates a new plan starting at waypoint one. Start restarts from point one; Resume continues at the paused point. Manual movement, release, person policy or a failed prerequisite pauses execution. Clearing a fault never resumes automatically.

Plans contain 1–100 WGS84 waypoints, relative altitude and hold duration. Every point must be inside the configured home radius, between 1 m and the altitude ceiling, and contain finite values. The route planner does not evaluate obstacles or terrain. Flight-fence enforcement and loss-of-link handling must also be configured onboard.

Mission save/load persists in SQLite. JSON exports preserve names and hold times; GeoJSON LineString import uses the UI's default altitude/hold. QGC WPL 110 exports contain a configured-home row and relative-altitude WAYPOINT rows. WPL import accepts those rows only, skipping an explicit home row; takeoff, landing, absolute-altitude and unsupported commands are rejected, not silently converted. Import does not automatically validate, arm, upload or execute a route.

## Navigation

The local navigator computes north/east/vertical error to the next GPS point, caps the vector magnitude to the configured speed, slows near the target, rotates horizontal velocity into the current aircraft heading, and sends BODY_NED velocity. Arrival requires horizontal error below 0.6 m and altitude error below 0.4 m; then the hold timer runs. This is a software prototype controller, not a tuned or flight-validated navigator. Velocity requests have no execution acknowledgement; observed telemetry provides feedback.

Demo missions can run at 1×, 5× or 10× time with generated telemetry. Live execution is disabled by default. Enabling it requires `live_control=true`, `live_missions=true`, the active operator lease and all original freshness/flight-envelope gates. Position and heading come from the flight controller. The pilot must establish a safe hover and choose GUIDED independently.

## AI

The copilot is a deterministic bounded intent parser and route generator. It does not call an LLM, infer arbitrary intent or execute free-form prompts. Supported patterns include lawnmower search, rectangular perimeter, a twelve-sided orbit, cardinal/body-relative/vertical measured movements, and return home. Body-relative planning requires heading. Supported phrases are shown in README. A proposal becomes a draft only when the operator selects Use proposed route; execution is a separate action.

Actual person detections are produced by HOG or a configured YOLO model. A small image-space tracker associates boxes by intersection-over-union and requires at least three distinct detector frames. Candidate tracks expire; stale video clears them. This reduces single-frame triggers but does not establish ground truth. Advisory mode presents evidence. Auto-pause policy pauses a running mission and logs an incident, with a 30-second incident cooldown. The drone's position is recorded as aircraft location; pixel boxes do not become person GPS coordinates.

Simulation's Person enters scene creates an explicitly labelled synthetic annotation. The simulation proves application policy transitions only. Real-world detector accuracy, camera latency and physical control response remain unverified.

## Performance changes

Inference skips duplicate capture sequences. OpenCV is limited to two worker threads to reduce contention with telemetry and recording. The map draws on demand rather than on a continuous animation loop; waypoint controls rebuild only after plan/state transitions or edits. Video remains independent from inference. Software timing is shown in Performance, not represented as end-to-end camera/RF latency.

Primary references: [ArduCopter Guided commands](https://ardupilot.org/dev/docs/copter-commands-in-guided-mode.html), [MAVLink file format](https://mavlink.io/en/file_formats/), [OSM tile policy](https://operations.osmfoundation.org/policies/tiles/), [Esri TileLayer service](https://developers.arcgis.com/javascript/latest/references/core/layers/TileLayer/).
