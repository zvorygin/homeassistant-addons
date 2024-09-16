# Samsung Frame TV Art Changer add-on for Home Assistant

![TV with some art on it ](https://i.imgur.com/BunHdwb.jpeg)

This add-on is built on the awesome work of <https://github.com/ow/samsung-frame-art> and <https://github.com/gijsvdhoven/homeassistant-addons>. 
It adds the ability to push images from different sources to your Samsung Frame TV, currently supported are Google Art and Culture, Bing Wallpapers and Local Media folder. 

By starting the add-on it will randomly pick an image based on your configuration and put it on your frame; after the image is placed the add-on will automatically stop again. This for instance can be triggered via an automation to run on a daily basis. Please find an example below.

# Local Media Folder
It adds the ability to place images in "Media" and it will randomly change the image on your Samsung the Frame

# Google Art
*NEW* By default the addon configuration has "Google Art" mode enabled which instead of taking images from the "media" folder takes random images from the Google Arts and Culture site and pushes it to the Samsung Frame TV. 

# Bing Wallpaper
*NEW* The addon now also supports "Bing Wallpapers" mode, which allows you to display random high-quality wallpapers from Bing on your Samsung Frame TV.


## Configuration Options

1. **IP Address**: Set the IP address of your Samsung The Frame TV.
2. **Google Art**: Enable to use random images from Google Arts and Culture.
3. **Bing Wallpapers**: Enable to use random high-quality wallpapers from Bing.
4. **High Res**: (For Google Art only) Enable to get high-resolution images using dezoomify.

When you start the addon for the first time it creates a specific directory Media/ MyMedia called "frame" where you can place your custom images.

Please note (I've found this the hard way!) you must upload pictures with a lower-case extension and only .png and .jpg are supported.

## Installation

Install this addon by adding the repository:

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fvivalatech%2Fhomeassistant-addons)

## Example Automation

Here's an example of how to set up an automation to change the image daily at 23:00:

```yaml
description: "Change Samsung Frame TV Art Daily"
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

You can customize this automation based on your preferences and the configuration options you've chosen in the addon.

## Debugging

For debugging purposes, you can use the `--debugimage` parameter when running the addon. This will save both the original downloaded image and the resized image to the filesystem for inspection.
