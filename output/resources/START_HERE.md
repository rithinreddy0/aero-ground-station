# Aero Ground Station - project resource pack

Prepared 26 October 2026 for the disaster-management drone project.

## Files

- **Aero_Hardware_Implementation_Manual.pdf** - 40-page implementation manual with 37 sections, contents, wiring and parameter registers, workflow, troubleshooting and linked references.
- **Aero_System_Architecture_Presentation.pptx** - 38-slide editable presentation. Open the speaker notes for the detailed explanations, implementation evidence and source links.
- **Aero_Hardware_Implementation_Source.md** - editable text version of the complete manual.
- **editable-diagrams/** - 13 Mermaid source files: end-to-end architecture, aircraft wiring, deployment, use cases, application components, classes, telemetry sequence, command sequence, uploaded-video sequence, mission activity, mission states, storage and motor layout.
- **source/project_content.json** - structured content and diagram coordinates for future revisions.

## Reading order

Start with the evidence/status section, hardware inventory and system architecture. Read the interface register alongside the board's manufacturer manual. Continue through radio modes, motor mapping, MAVLink and video acquisition, then the application and AI workflows. Finish with the acceptance matrix, limitations and references.

The PDF is intended for the project report and detailed review. Use the PowerPoint for presentation or viva preparation. Edit diagrams directly in PowerPoint, or edit the Mermaid text in a Mermaid-compatible editor.

## Evidence boundaries

The pack uses the application code, commissioning records, this conversation and linked technical documentation. User-reported bench checks, implemented software, pending hardware tests and proposed additions are identified separately.

The historical parameter exports are not a complete current FC readback. GPS fix, battery calibration, actual RF bridge, video-capture hardware and flight behavior still require evidence. No automatic arming/takeoff/landing, onboard AUTO mission upload, confirmed-survivor identification or precise victim geolocation is claimed for the current application.

The ZIP is the documentation pack. It does not include private flight logs, uploaded videos, local incident evidence, model weights or the full application source. The public code repository is linked in the manual.
