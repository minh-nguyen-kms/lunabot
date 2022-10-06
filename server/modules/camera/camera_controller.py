import json
from threading import Thread

from libs.event_bus.event_bus import EventBus
from .stream_server import StreamServer
from libs.event_bus.event_names import EventNames

class CameraController():
    def __init__(self, event_bus: EventBus, host_name='localhost', port=9000):
        self.host_name = host_name
        self.port = port

        self.streamer = None
        self.thread = None

        self.event_bus = event_bus
        event_bus.on(EventNames.CAMERA_START_STREAMING, self.on_camera_start_streaming)
        event_bus.on(EventNames.CAMERA_STOP_STREAMING, self.on_camera_stop_streaming)
        event_bus.on(EventNames.CAMERA_IS_STREAMING, self.on_camera_is_streaming)
    
    def __del__(self):
        self.event_bus.off(EventNames.CAMERA_START_STREAMING, self.on_camera_start_streaming)
        self.event_bus.off(EventNames.CAMERA_STOP_STREAMING, self.on_camera_stop_streaming)
        self.event_bus.off(EventNames.CAMERA_IS_STREAMING, self.on_camera_is_streaming)

    def on_camera_start_streaming(self, *args):
        self.start_streaming()

    def on_camera_stop_streaming(self, *args):
        self.stop_streaming()

    def on_camera_is_streaming(self, data):
        self.event_bus.emit(EventNames.SOCKET_BROAD_CAST, {
            "event": EventNames.CAMERA_IS_STREAMING,
            "data": data
        })

    def start_streaming(self):
        print('Start streaming thread')
        if self.streamer is None:
            self.streamer = StreamServer(event_bus=self.event_bus, host_name=self.host_name, port=self.port)
        self.thread = Thread(target=self.streamer.start_streaming,args=())
        self.thread.daemon = True
        self.thread.start()

        return self.thread

    def stop_streaming(self):
        print('Stop streaming thread')
        if self.streamer is not None:
            self.streamer.stop_streaming()
            self.streamer = None 