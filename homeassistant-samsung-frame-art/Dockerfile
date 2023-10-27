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


RUN chmod a+x /run.sh

CMD [ "/run.sh" ]


LABEL \
    io.hass.name="Home Assistant Samsung the Frame changer for ${BUILD_ARCH}" \
    io.hass.description="Home Assistant Add-on: ${BUILD_ARCH} Home Assistant Samsung the Frame changer" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="base" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="Gijs van den Hoven" \
    org.opencontainers.image.title="Home Assistant Samsung the Frame changer for ${BUILD_ARCH}" \
    org.opencontainers.image.description="Home Assistant Community Add-on: ${BUILD_ARCH} Python base image" \
    org.opencontainers.image.vendor="Home Assistant Add-ons from Gijsvdhoven" \
    org.opencontainers.image.authors="Gijs van den Hoven" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.url="https://github.com/gijsvdhoven/homeassistant-addons" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.documentation="https://github.com/${BUILD_REPOSITORY}/blob/master/README.md" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}
