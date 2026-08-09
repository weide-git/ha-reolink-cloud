FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir pyneolink==0.4.0

COPY reolink_raw_udp_test.py /app/reolink_raw_udp_test.py
COPY run.sh /run.sh

RUN chmod +x /run.sh

ENTRYPOINT ["/run.sh"]
