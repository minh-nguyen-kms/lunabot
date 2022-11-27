import ipaddress
import sys
import os

sys.path.insert(0, '/home/pi/ntm/lunabot/server')

import logging
import asyncio
import time
from libs.network import utils as network
from libs.event_bus.event_bus import EventBus
from libs.event_bus.event_names import EventNames
from modules.camera.camera_controller import CameraController
from modules.websocket.websocket_server import WebsocketServer
from modules.mortor.motor_controller import MotorController
from modules.system.system_controller import SystemController
from modules.camera_pan_tilt.camera_pan_tilt_controller import CameraPanTiltController
from modules.ultra_sonic.ultra_sonic_controller import UltraSonicController

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

async def main():
    event_bus = EventBus()
    ipAddr = network.get_ip_address()
    print("Your Computer IP Address is:" + ipAddr)

    # Start pigpiod service
    os.system('sudo pigpiod')
    time.sleep(1)

    #init systemcontroller
    systemCtrl = SystemController(event_bus=event_bus)
    systemCtrl.start_listening()

    #init camera
    camera = CameraController(event_bus=event_bus, host_name=ipAddr, port=9101)
    # event_bus.emit(EventNames.CAMERA_START_STREAMING)

    #init camera pan tilt
    pantilt = CameraPanTiltController(event_bus=event_bus)
    pantilt.start_listening()

    # #init ultra sonic
    # ultraSonic = UltraSonicController(event_bus=event_bus)
    # await ultraSonic.start_listening()

    #init motor
    motor = MotorController(event_bus=event_bus)
    motor.start_listening()

    #init websocket
    websocket = WebsocketServer(event_bus=event_bus, host_name=ipAddr, port=9102)
    await websocket.start()


if __name__=='__main__':
    asyncio.run(main())