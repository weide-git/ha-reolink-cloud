FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

RUN pip install --no-cache-dir pyneolink==0.4.0

COPY run.sh /run.sh
COPY reolink_raw_udp_test.py /data/reolink_raw_udp_test.py

RUN chmod +x /run.sh

CMD ["/run.sh"]
