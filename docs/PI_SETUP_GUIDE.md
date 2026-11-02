# Raspberry Pi Zero 2 W — Quick Setup Guide

## 1. Network Setup
Ensure the Raspberry Pi and the Ground Station laptop are on the exact same Wi-Fi network.

## 2. The Streaming Command
We rely on a hyper-optimized UDP stream utilizing the hardware encoder on the Pi.
SSH into your Pi and run this exact command:

```bash
rpicam-vid -t 0 --inline --width 640 --height 480 --framerate 15 --bitrate 800000 --intra 3 --output - | ffmpeg -fflags nobuffer -f h264 -i - -c:v copy -f mpegts -flush_packets 1 udp://<LAPTOP_IP_ADDRESS>:5000?pkt_size=1316
```

**Replace `<LAPTOP_IP_ADDRESS>`** with the IPv4 address of the computer running the Vayudaksh backend.

## Why this command?
- `rpicam-vid`: Uses the Pi's native ISP and hardware H.264 encoder.
- `--inline`: Injects SPS/PPS headers into every I-frame so the receiver can decode the stream instantly if it connects late.
- `ffmpeg ... -f mpegts`: Wraps the raw H264 stream in an MPEG-TS container, which OpenCV's UDP receiver can parse flawlessly without packet loss errors.
