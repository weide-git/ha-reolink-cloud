ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache \
    python3 \
    py3-pip

RUN pip3 install --no-cache-dir --break-system-packages pyneolink==0.4.0

COPY run.sh /run.sh
COPY reolink_raw_udp_test.py /data/reolink_raw_udp_test.py

RUN chmod a+x /run.sh

CMD ["/run.sh"]
