FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

RUN pip install --no-cache-dir pyneolink==0.4.0

WORKDIR /data

COPY reolink_raw_udp_test.py /data/reolink_raw_udp_test.py
COPY run.sh /run.sh

RUN ls -la /data
RUN ls -la /run.sh
RUN test -f /data/reolink_raw_udp_test.py
RUN chmod 755 /run.sh

ENTRYPOINT ["/run.sh"]
