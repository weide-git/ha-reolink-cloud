# Reolink P2P Raw UDP Test

Vollständiger Home-Assistant-App-Test.

Der Dockerfile verwendet absichtlich `python:3.12-slim`, damit der bisherige
Fehler `base name ($BUILD_FROM) should be blank` nicht mehr auftreten kann.

Enthalten:
- config.yaml
- Dockerfile
- run.sh
- reolink_raw_udp_test.py
