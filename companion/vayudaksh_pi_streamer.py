"""
VAYUDAKSH Raspberry Pi Zero 2 W Video Streamer
Runs on the onboard companion computer with Raspberry Pi Camera Module V3.
Streams low-latency MJPEG video over local Wi-Fi / hotspot to the Command Center.
"""
import sys
import time
import argparse
import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

# Global frame buffer
current_frame = None

class VideoCaptureThread:
    def __init__(self, width=640, height=480, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
        self.cap = None
        self._init_camera()

    def _init_camera(self):
        # Try libcamera / OpenCV V4L2 backend for Camera Module V3
        print(f"[VAYUDAKSH PI] Initializing Pi Camera Module V3 ({self.width}x{self.height} @ {self.fps}fps)...")
        try:
            self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        except Exception as e:
            print(f"[VAYUDAKSH PI] V4L2 fallback: {e}")
            self.cap = cv2.VideoCapture(0)

    def read_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None

class StreamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', '0')
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    if current_frame is not None:
                        ret, jpeg = cv2.imencode('.jpg', current_frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                        if ret:
                            self.wfile.write(b'--FRAME\r\n')
                            self.send_header('Content-Type', 'image/jpeg')
                            self.send_header('Content-Length', str(len(jpeg)))
                            self.end_headers()
                            self.wfile.write(jpeg.tobytes())
                            self.wfile.write(b'\r\n')
                    time.sleep(1.0 / 30.0)
            except Exception:
                pass
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>VAYUDAKSH Pi Camera Online</h1><img src='/stream.mjpg' /></body></html>")

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def main():
    global current_frame
    parser = argparse.ArgumentParser(description="VAYUDAKSH Pi Streamer")
    parser.add_argument("--port", type=int, default=8080, help="Streaming port (default 8080)")
    parser.add_argument("--width", type=int, default=640, help="Frame width")
    parser.add_argument("--height", type=int, default=480, help="Frame height")
    parser.add_argument("--fps", type=int, default=30, help="Target FPS")
    args = parser.parse_args()

    cam = VideoCaptureThread(args.width, args.height, args.fps)
    server = ThreadedHTTPServer(('0.0.0.0', args.port), StreamHandler)
    print(f"[VAYUDAKSH PI] Stream active at http://0.0.0.0:{args.port}/stream.mjpg")

    try:
        import threading
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        while True:
            frame = cam.read_frame()
            if frame is not None:
                current_frame = frame
            time.sleep(1.0 / (args.fps * 1.5))
    except KeyboardInterrupt:
        print("\n[VAYUDAKSH PI] Stopping streamer...")
        server.shutdown()

if __name__ == '__main__':
    main()
