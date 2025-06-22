# Samsung Frame TV Art Changer add-on for Home Assistant

![TV with some art on it ](https://i.imgur.com/BunHdwb.jpeg)

This add-on is built on the awesome work of <https://github.com/ow/samsung-frame-art> and <https://github.com/gijsvdhoven/homeassistant-addons>. 
It adds the ability to push images from different sources to your Samsung Frame TV, currently supported are Google Art and Culture, Bing Wallpapers, Google Photos, and Local Media folder. 

By starting the add-on it will randomly pick an image based on your configuration and put it on your frame; after the image is placed the add-on will automatically stop again. This for instance can be triggered via an automation to run on a daily basis. Please find an example below.

If multiple sources are enabled it will randomly choose a source on each run. 

# Google Art
By default the addon configuration has "Google Art" mode enabled which instead of taking images from the "media" folder takes random images from the Google Arts and Culture site and pushes it to the Samsung Frame TV. 

# Bing Wallpaper
The addon now also supports "Bing Wallpapers" mode, which allows you to display random high-quality wallpapers from Bing on your Samsung Frame TV.

# Google Photos
The addon now supports "Google Photos" mode, which allows you to display random images from a specific Google Photos album on your Samsung Frame TV. To use this feature, you'll need to set up Google Photos API credentials and specify the album name in the configuration.

## Setting up Google Photos Integration

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Photos Library API
4. Create OAuth 2.0 credentials (Desktop Application type)
5. Copy the Client ID and Client Secret from your credentials
6. In the Home Assistant addon configuration:
   - Enable "Google Photos"
   - Enter your album name in "Google Photos Album"
   - Paste your Client ID in "Google Photos Client ID"
   - Paste your Client Secret in "Google Photos Client Secret"
7. The first time you run the addon with Google Photos enabled, it will prompt you to authenticate via a web browser
8. After authentication, a token file will be created automatically for future use

# Local Media Folder
Looks for images in the /media/frame folder and randomly pushes an image to your Samsung Frame TV. When you start the addon for the first time it creates a specific directory in Media called "frame" where you can place your custom images.

Please note you must upload pictures with a lower-case extension and only .png and .jpg are supported.


## Installation

Install this addon by adding the repository:

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fvivalatech%2Fhomeassistant-addons)


## Configuration Options

1. **IP Address**: Set the IP address of your Samsung The Frame TV.
2. **Google Art**: Enable to use random images from Google Arts and Culture.
3. **Bing Wallpapers**: Enable to use random high-quality wallpapers from Bing.
4. **Google Photos**: Enable to use images from a specific Google Photos album.
5. **Google Photos Album**: Name of the Google Photos album to use (only used when Google Photos is enabled).
6. **Google Photos Client ID**: OAuth 2.0 Client ID from Google Cloud Console (only used when Google Photos is enabled).
7. **Google Photos Client Secret**: OAuth 2.0 Client Secret from Google Cloud Console (only used when Google Photos is enabled).
8. **Media Folder**: Enable to use images from the local media folder (/media/frame).
9. **Same Image**: Use the same image across multiple TVs (if you have multiple Frame TVs configured).
10. **High Res**: (For Google Art only) Enable to get high-resolution images using dezoomify.


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
      addon: local_hass-frametv-artchanger
```

## TODO

Here's some ideas for stuff to implement
- [ ] Delete old N images on TV, e.g. configurable to keep last 100 uploaded images and delete an older image everytime a new one is uploaded
- [ ] More sources, especially something for high res contemporary art would be awesome or other curated sources
- [ ] Dashboard card that shows currently active art and maybe allows selection of other art