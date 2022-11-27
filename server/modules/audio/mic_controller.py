import json
from threading import Thread

from libs.event_bus.event_bus import EventBus
from libs.event_bus.event_names import EventNames

from .mic_streamer import start_server

class MicController():
    def __init__(self, event_bus: EventBus, host_name='localhost', port=9103):
        self.host_name = host_name
        self.port = port
        self.thread = None        

        self.event_bus = event_bus
        event_bus.on(EventNames.MIC_START_STREAMING, self.on_mic_start_streaming)
        event_bus.on(EventNames.MIC_STOP_STREAMING, self.on_mic_stop_streaming)
        event_bus.on(EventNames.MIC_IS_STREAMING, self.on_mic_is_streaming)
        event_bus.on(EventNames.MIC_GET_STATUS, self.on_mic_get_status)
    
    def __del__(self):
        self.event_bus.off(EventNames.MIC_START_STREAMING, self.on_mic_start_streaming)
        self.event_bus.off(EventNames.MIC_STOP_STREAMING, self.on_mic_stop_streaming)
        self.event_bus.off(EventNames.MIC_IS_STREAMING, self.on_mic_is_streaming)

    def on_mic_start_streaming(self, *args):
        self.start_streaming()

    def on_mic_stop_streaming(self, *args):
        self.stop_streaming()

    def on_mic_is_streaming(self, data):
        self.streaming_data = data
        self.event_bus.emit(EventNames.SOCKET_BROAD_CAST, {
            "event": EventNames.MIC_IS_STREAMING,
            "data": data
        })

    def on_mic_get_status(self, *args):
        if self.streamer is not None:
            self.event_bus.emit(EventNames.SOCKET_BROAD_CAST, {
                "event": EventNames.MIC_IS_STREAMING,
                "data": self.streaming_data
            })

    def start_streaming(self):
        print('Start MIC streaming thread')
        self.thread = Thread(target=start_server,args=())
        self.thread.daemon = True
        self.thread.start()
        

        return self.thread

    def stop_streaming(self):
        print('MIC Streaming doesn\'t support stoping')
        