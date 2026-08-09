FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

RUN pip install --no-cache-dir pyneolink==0.4.0

WORKDIR /data

COPY reolink_raw_udp_test.py /data/reolink_raw_udp_test.py
COPY run.sh /run.sh

RUN echo "=== BUILD CHECK ===" && 
ls -la /data && 
ls -la /run.sh && 
test -f /data/reolink_raw_udp_test.py && 
echo "=== PYTHON DATEI IM IMAGE VORHANDEN ===" && 
chmod 755 /run.sh

ENTRYPOINT ["/run.sh"]
