import { useCallback, useEffect, useState } from 'react';
import ReconnectingWebSocket from 'reconnecting-websocket';

let globalSocket: ReconnectingWebSocket;

// const SOCKET_SERVER = 'ws://192.168.1.19:9102';

export const SOCKET_EVENT_NAMES = {
  DISCONNECT: 'DISCONNECT',
  MOVING: 'MOVING',
  CAMERA: {
    CAMERA_START_STREAMING: 'CAMERA_START_STREAMING',
    CAMERA_STOP_STREAMING: 'CAMERA_STOP_STREAMING',
    CAMERA_IS_STREAMING: 'CAMERA_IS_STREAMING',
  },
  COMMANDS: {
    SYSTEM_RESTART: 'SYSTEM_RESTART',
  },
  CAMERA_PANTILT: 'CAMERA_PANTILT',
};

export const useSocket = () => {
  const [socket, setSocket] = useState<ReconnectingWebSocket>(globalSocket);
  useEffect(() => {
    if (typeof window == undefined) {
      return;
    }
    const socketServer = `ws://${window.location.hostname}:9102`;
    if (globalSocket) {
      setSocket(globalSocket);
    } else {
      const currentSocket = new ReconnectingWebSocket(socketServer);
      globalSocket = currentSocket;
    }
  }, []);

  const waitSocketConnect = useCallback(
    async (): Promise<ReconnectingWebSocket> =>
      new Promise((resolve, reject) => {
        if (!globalSocket) {
          reject('No Websocket instance');
          return;
        }
        if (globalSocket.readyState === ReconnectingWebSocket.OPEN) {
          resolve(globalSocket);
          return;
        }
        globalSocket.onopen = () => {
          resolve(globalSocket);
        };
        globalSocket.onerror = (error) => {
          reject(error);
        };
      }),
    [],
  );

  const socketEmit = useCallback(<T>(event: string, data?: T) => {
    globalSocket?.send(
      JSON.stringify({
        event,
        data,
      }),
    );
  }, []);

  return {
    socket,
    socketEmit,
    waitSocketConnect,
  };
};
