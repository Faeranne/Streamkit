Below is a more concise set of notes and rationals for why choices in the stream kit project were made.  These should help guide future decisions, as well as help you decide if alternative parts or setups make more sense for your use.

# Overal Structure:
The system is structured as a few unique pieces.  Each piece is included as a functional unit, with some being duplicatable, and some either removable, or combindable.

## Camera:
Uses a dedicated Raspberry Pi to read the Raspberry Pi HQ camera, and bother record, and stream, the view.  Optionally, if a display is connected as well, the camera can also show the current viewpoint.  The display can easily double the cost of the unit, so it is made option, but is easily enabled.

### Rational:
Seperating the camera as a unit was done so that it can be easily used in a standalone capacity.  Being able to simply record footage is one possible use, and makes this unit alone the most adaptable piece.  It also allows for capturing multiple angles of the talk, if desired.

## Capture Box:
A rapsberry Pi connected to a toshiba Hdmi to Csi converter.this is the unit i have done the lease experimentation on.  There are still some outstanding questions around it, and it may change form in the future.  The unit can be combine with a 7in screen to allow the presenter to easily see what they are showing to the audiance, as well as allow for a MC to start and stop recorsing and streaming.  In the future, it could also allow online participation by providing twitch chat to the speaker.  As with the camera, being able to capture locally was a focus, and can be done on an external usb device.

### Rational:
This part is seperated due to the distancw between the camera and the speaker, as well as to allow the positioning of the projector connection, though this is a weaker point, and it may make sense to simply use the hdmi out from this box.  It may also make sense in the future to combine this with the mixer box, so long as the thermals are managable, as fan noise would not be acceptable.

## Audio Box:
This would handle mixing the caputre audio with the wireless kmic, and pushing all that to the audio output of whatever PA is being used.  This part is probably the most undertain piece, and will probably get combind with either the mixer or the capture box, though being able to use a seperate box can be a huge boost in certain layouts 

### Rational:
This part has 0 research so far, so I am unsure of if it will remain a physically seperate piece, or if it will become just a logically seperate piece.

## Mixer:
The brains of the system.  This handles mixing the camera, capture box, and audio into 2 feeds.  One for the live stream (and recording), and one for the projection.  This part requires some tight timing, so a Jetson is employed due to it's hardware capabilites with regard to compositing.

### Rational:
A jetson was chosen over a Pi due to the pi's several second delay when compositing just the two streams.  Since multiple mixers are needed at once to run this system, the jetson's power was an ibvious requirement.  The provided carrier does not expose the DSI ports, so it can't easily be used with a local screen, but it does posess an hdmi port to be able to be used with the projector possibly.

## Video Output:
Not included as a seperate physical box by default due to anything else being able to manage this, but in certain situations, it would make sense to provide a seperate display output as needed.

# Signaling
Everything is intended to be used with an IP based signaling system.  Basically, a single unit is marked as the controller (likely the mixer), and everything else becomes a periphrial.  Probably using mdns for automatic setup. Then the preferials can be configured as needed, setting both primarly and ancilary functions.  For example, take the following units:
* Mixer
* Capture box
* Camera
* Camera
* Video output

This system might have the projector input far away from the presenter, and need an audiance camera for cutaway.  the mixer would be the controller, and would tell the cameras to function as cameras, to record their content locally (if possible), and their streaming groups.  it would then tell the capture box to function as a capture box, to present the presenters screen on it's local display, to record locally, and what streaming group to use.  finally, it would tell the display box to be a display box, and to stream the given streaming group to display.

this might be an example setup for a large event, while for a small group, you might only need the following:

* Camera
* Mixer
* Capture Box

in this case, the camera and capture box would be instructed the same as above, with the mixer handling hsmi output.  Or the capture box could handle the outptu, and the mixer only handles streaming.

Or maybe you have a record only event.  In that case you might only need the following:

* Camera
* Capture Box

In this case the camera or capture box could act as the controller, and both set to record only.  either could be set to be the hdmi output, and in the event the camera is, the caputre box would stream directly to it.  in either case, both would be in record only mode. 

# Software

The system is expected to be python, which builds and runs GStreamer pipelines.  Gstreamer was picked due to it's flexability, speed, and level of integration.  In theory, due to how gstreamer is setup, it should be possible to acheve everything OBS can do, but in a command line format.  Python was picked due to it's integration with pil, a popular image manipulation library, and it's ability to run without an X server, for managing interfaces on both the capture and camera systems.

In addition tor managing the gstreamer pipelines, it will also handle the network signaling, which includes the above features, as well as allowing remote control of the scene transitions, and allowing the capture box to remotely signal a scene change when the hdmi cable is removed.

## Libraries

There are several libraries currently expected to be in use.  The following are what I currently use:

* picamera
* gi
* flask

Each was selected for a particual reason.

Picamera was piced due to itt's ability to handle overlays on the display, as well as manage multiple video destinations, namely record and stream.  These allow for a simple interface to be made, and for capture to start locally when a usb drive is provided.

Gi is to allow loading the Gstreamer system, which makes controlling the pipeline possible.

Flask was picked due to it's lightweight nature, and allowing for a web interface on each device to be built.  This might be replaced with a simple tornado interface everywhere except on the controller... we'll see what works best.

# Outstanding issues

Currently, the python code is untouched, and no testing for the capture box has been done besides a preliminary test.  Signaling, pipeline construction, switching, and web interface, are all still up in the air.

# Overall rational

In essence, this design was acheve 3 major points:
* Be cheap, at lease under $1000, which is the last price I put on a streaming PC (without hdmi capture)
* Be compact, the more portable, the better
* Be easy to use, everything needed to be simple plug-and-play, at least as far as the event itself

All three should be easily acheveable within the scope of this project, as well as having the following benifites:

* Modular, not all parts are needed all the tiem, so why do more than ya have to?
* stable, The capture boxes handle 100 meter ethernet runs better than any hdmi extender I have seen, with significantly lower latence.  
* Powerful, the system manages to do most of what the existing systems cab, as well as foing it with fewer cables.

By using hardware encoding (through the pis), and udp streams, everything runs way smoother, and with fewer cables.  Why use 4 ethernet cables to send a signal to the front of house and back again, when 1 manages just fine?

# Final notes:
Of course everything in here is subject to change.  I know these things aren't perfect, but the final part of this that makes me so confident about it is: Modularity.  Every piece does its own job, which makes it easy to replace with another piece when something better is found.  no one system is perfect for everything, so instead I found making the parts modular, and laying out what you need on-site makes the most sense.
