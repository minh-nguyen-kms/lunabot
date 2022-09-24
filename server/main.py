import ipaddress
import sys
sys.path.insert(0, '/home/pi/ntm/lunabot/server')

import logging
import asyncio
import time
from libs.network import utils as network
from libs.event_bus.event_bus import EventBus
from libs.event_bus.event_names import EventNames
from modules.camera.camera_controller import CameraController
from modules.websocket.websocket_server import WebsocketServer

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

async def main():
    event_bus = EventBus()
    ipAddr = network.get_ip_address()
    print("Your Computer IP Address is:" + ipAddr)

    #init camera
    camera = CameraController(event_bus=event_bus, host_name=ipAddr, port=9101)
    # event_bus.emit(EventNames.CAMERA_START_STREAMING)

    #init websocket
    websocket = WebsocketServer(event_bus=event_bus, host_name=ipAddr, port=9102)
    await websocket.start()


if __name__=='__main__':
    asyncio.run(main())