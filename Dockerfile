ARG BUILD_FROM
FROM $BUILD_FROM

RUN \
  apk add --no-cache \
    python3 py3-pip
RUN \
    pip3 install samsungtvws[async,encrypted]
# Copy data for add-on
COPY run.sh /
COPY art.py /

ADD /images /images


RUN chmod a+x /run.sh

CMD [ "/run.sh" ]