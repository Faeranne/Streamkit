Camera:
Does:
Runs `picamera` through python to output a h264 file, and a udp stream.

Needs:
Recieve network commands to start/stop recording and streaming.

Capture:
Does:
Nothing

Needs:
Run `picamera` to record and stream based on network commands.  Also needs to monitor hotplug status to alert upstream, as well as restart `picamera`.

Mixer:
Does:
Static rtp stream of two udp streams from the camera.

Needs:
Python integration of this stream, with switching handled by `input-switch` feature of gstreamer.  confirm if entire pipeline must be setup first, or if only one switch needs to be up before starting.  Output screen feed to hdmi for projection.

Host web interface that exports hst of each feed, as well as hst of output, and handles incoming requests to control device settings and pass them to the correct device.
