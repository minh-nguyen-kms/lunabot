import logging
import asyncio
import websockets
import json

from libs.event_bus.event_bus import EventBus
from libs.event_bus.event_names import EventNames

class WebsocketServer():
    def __init__(self, event_bus: EventBus, host_name = 'localhost', port = 9001):
        self.log = logging.getLogger(self.__class__.__name__)
        self.host_name = host_name
        self.port = port
        self.event_bus = event_bus

        self.clients = {}
        self.clientsSet = set()
        self.server = None        
        
        event_bus.on(EventNames.SOCKET_BROAD_CAST, self.on_socket_broad_cast)

    async def start(self):
        self.server = websockets.serve(self.handle_ws, self.host_name, self.port)
        async with self.server:
            await asyncio.Future()  # run forever

    async def handle_ws(self, ws, path):
        self.on_new_client(ws)
        try:
            while True:
                msg = await ws.recv()
                self.on_message_received(ws, msg)
        except websockets.ConnectionClosedOK:
            pass
        except Exception as e:
            self.log.error(e)
        self.on_client_left(ws)

    def on_new_client(self, ws):
        addr = ws.remote_address
        self.log.info(f'{addr}: OPEN')

        self.clients[addr] = ws
        self.clientsSet.add(ws)

    def on_client_left(self, ws):
        addr = ws.remote_address
        self.log.info(f'{addr}: CLOSE')

        del self.clients[addr]
        self.clientsSet.remove(ws)

    def on_message_received(self, ws, message):
        addr = ws.remote_address
        self.log.debug(f'{addr}: "{message}"')

        msg = json.loads(message);
        event = msg.get('event', None);
        if event is not None:
            self.event_bus.emit(event, msg.get('data', None))

    def on_socket_broad_cast(self, data):
        self.log.info(f'SOCKET_BROAD_CAST: "{data}"')
        websockets.broadcast(self.clientsSet, json.dumps(data))