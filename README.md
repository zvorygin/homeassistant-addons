# Samsung Frame Art Add on for Home Assistant

![TV with some art on it ](https://i.imgur.com/BunHdwb.jpeg)

This add-on uses the awesomework of https://github.com/ow/samsung-frame-art . It adds the ability to place images in "Media" (it creates a specific directory for it under MyMedia called "TheFrame" where you can place your images).

By starting the add-on it will randomly pick a image from te folder and put it on your frame; after the image is placed the add-on will automatically stop again. This for instance can be triggered via an automation to it on a daily basis. Please find an example below.

The only configuration option is setting the IP adress of your Samsung The Frame

```
description: ""
mode: single
trigger:
  - platform: time
    at: "23:00:00"
condition: []
action:
  - service: hassio.addon_start
    data:
      addon: local_hass-frame-changer
```
