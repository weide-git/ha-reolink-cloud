ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-python:3.12-alpine3.20

FROM ${BUILD_FROM}

WORKDIR /data

RUN pip install --no-cache-dir pyneolink==0.4.0

COPY run.sh /run.sh
COPY reolink_raw_udp_test.py /data/reolink_raw_udp_test.py

RUN chmod a+x /run.sh

CMD ["/run.sh"]
