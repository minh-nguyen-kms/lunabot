from threading import Thread
import pyaudio
import logging

from libs.event_bus.event_bus import EventBus
from libs.event_bus.event_names import EventNames

from .mic_streamer import start_server

class MicController():
    def __init__(self, event_bus: EventBus, host_name='localhost', port=9103):
        self.log = logging.getLogger(self.__class__.__name__)
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
        if (self.thread is not None):
            return
        print('Start MIC streaming thread')
        self.thread = Thread(target=start_server,args=())
        self.thread.daemon = True
        self.thread.start()



        # # print devices
        # audio = pyaudio.PyAudio()
        # info = audio.get_host_api_info_by_index(0)
        # numdevices = info.get('deviceCount')
        # for i in range(0, numdevices):
        #     if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        #         self.log.info("i = " + str(i) + ". Input Device id = " + str(i) + " - " + audio.get_device_info_by_host_api_device_index(0, i).get('name'))
            
        

        return self.thread

    def stop_streaming(self):
        print('MIC Streaming doesn\'t support stoping')
        