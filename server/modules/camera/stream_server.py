# Part 01 using opencv access webcam and transmit the video in HTML
import json
import cv2

from libs.event_bus.event_names import EventNames
from . import streamer as ps

from libs.network import utils as network


HTML="""
<html>
	<head>
		<title>Lunabot camera</title>
	</head>

	<body style="height:100%; padding:0; margin:0">
		<img src="stream.mjpg" autoplay playsinline style="width:100%; height:100%">
	</body>
</html>
"""
class StreamServer():
    def __init__(self, event_bus, host_name, port=9000):
        self.event_bus = event_bus
        self.port = port
        self.host_name = host_name

        self.capture = None
        self.server = None
    
    def stop_streaming(self):
        print('Stop camera streaming')
        if self.capture is not None:
            print('Release capture')
            self.capture.release()
            self.capture = None

        if self.server is not None:
            print('Close streaming server socket')
            self.server.socket.close()
            self.server.server_close()
            self.server = None

    def emit_camera_is_streaming(self):
        self.event_bus.emit(EventNames.CAMERA_IS_STREAMING, json.dumps({
            "host": self.host_name,
            "port": self.port,
        }))

    def start_streaming(self):
        if self.server is not None:
            self.emit_camera_is_streaming()
            return

        StreamProps = ps.StreamProps
        StreamProps.set_Page(StreamProps, HTML)

        address = (self.host_name, self.port) # Enter your IP address

        try:
            StreamProps.set_Mode(StreamProps,'cv2')
            capture = cv2.VideoCapture(0)
            self.capture = capture
            capture.set(cv2.CAP_PROP_BUFFERSIZE,4)
            capture.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
            capture.set(cv2.CAP_PROP_FPS,10)
            StreamProps.set_Capture(StreamProps,capture)
            StreamProps.set_Quality(StreamProps,80)
            
            server = ps.Streamer(address,StreamProps)
            self.server = server

            print('Camera streaming server started at','http://'+address[0]+':'+str(address[1]))
            self.emit_camera_is_streaming()
            server.serve_forever()
        except:
            pass
