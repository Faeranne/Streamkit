# Streaming Gear

## Elements
Capture Box: RPi4 w/hdmi to csi and display.
Camera Box: RPi4 with RPi HQ and display
Mic Box: XLR and/or RCA capture.
Mixer Box: Nvidia Jetson.  maybe merge with mic box.

## Stats
Camera: 200ms latency to stream, 0 to display.

## Notes:

~~Setup Rpi to stream Input and display on screen.~~ ~~Can be handled with picamera python module, or raspivid~~  Raspivid works great, just use that where you can.

~~Python program to control display? Display controls on-screen?~~ ~~picamera~~ Raspivid plus PIL for overlay.  ~~picamera~~ Raspivid has built in overlay support, but not sure if that is better than using omxplayer, or a custom screen via PIL. Handle touch input seperatly?  ~~Look into omxh264dec for gstreamer~~ Use new V4L2 decoder and encoder.

~~Can CSI to HDMI detect cable disconnect?~~ No, but a wire mod adds the feature.  Look into alternatives.

~~Hdmi splitter? Or just forward from Hdmi port?~~ Straight.  Raspivid is very good.  Integrate audio there?  XLR adapter is right there, but can pi handle the latency?

Timestamp signals and sync with master?  Would require a custom network handler, may or may not work.

~~Identfy Latency of CSI to HDMI.~~ Very Low!  Looks like a good option.

~~Nvidia Jetson as host?  Maybe...  Intel NUC as host? Yes.  Can use USB capture cards for single box support. Look into custom printed case for NUC.~~ ~~RPi capture is very solid, Will probably pair well with NUC. Single box might look more like a CM4 with dual HDMI, or RPi HQ + HDMI.  Alternativly, drop box, and use a laptop with dual ethernet.  would need high core count for stream encoding.~~ Jetson has proved to be perfect for the job.  Starting research into scene building and switching using gstreamer.

~~Use RPi HQ Cam for capture?  It's a thought.~~  Yes use RPi HQ.  It works a treat.

Command an Control... looks like udp sockets on python is fine... is json acceptable here?  Also, how do we handle resend?  I think a simple syn ack is fine, since each side is asking to trigger something on the other side that is gonna be one way anyways.  ie:  It's safe for the camera to start streaming once it recieves the command.  The mixer only cares that the stream has indeed started, then it does it's own thing.  Same for switching scenes after an hdmi disconnect, the capture box only wants to ensure the mixer has made the switch, it doesn't care what happens after.

Look into custom circuit for compute module, and jetson.

## Parts List:

* CSI to HDMI - [[https://www.amazon.com/dp/B0899L6ZXZ]]
* Raspberry Pi 
* RPi HQ Camera
* Nvidia Jetson Nano (1GB version)
* PoE raspi board
* PoE Switch
* Raspberry Pi Official Screen
* 3.5 in DSI screen for Pi
~~* Intel NUC~~
