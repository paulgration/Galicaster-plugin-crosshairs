Crosshairs Plugin
=================

Adds the ability to draw crosshairs onto pipeline previews to assist with positioning
cameras.

Dependencies
------------

The plugin depends on the following package(s):
::

    python-gi-cairo

Loading
-------

To activate the plugin, add the line in the `plugins` section of your configuration file
::

    [plugins]
    crosshairs = True

True: Enables plugin
False: Disables plugin

Recording pipelines need to include a `cairooverlay` element named `crosshair-overlay`.
Rather than modify existing Galicaster recorder bins, it is possible to specify the
`cairooverlay` element as part of the `caps-preview` configuration for a profile.
Example Presenter profile:
::

    [data]
    name = Presenter

    [track1]
    caps = video/x-raw,framerate=30/1,width=1280,height=720
    device = v4l2
    file = CAMERA.avi
    flavor = presenter
    location = /dev/video0
    name = Presenter
    caps-preview = cairooverlay name=crosshair-overlay ! videoconvert

    [track2]
    device = pulse
    file = sound.mp3
    flavor = presenter
    location = default
    name = Audio