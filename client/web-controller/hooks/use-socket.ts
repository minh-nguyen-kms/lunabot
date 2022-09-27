import { useCallback, useEffect, useState } from 'react';

let globalSocket: WebSocket;

const SOCKET_SERVER = 'ws://192.168.1.151:9102';

export const SOCKET_EVENT_NAMES = {
  DISCONNECT: 'DISCONNECT',
  MOVING: 'MOVING',
  CAMERA: {
    CAMERA_START_STREAMING: 'CAMERA_START_STREAMING',
    CAMERA_STOP_STREAMING: 'CAMERA_STOP_STREAMING',
    CAMERA_IS_STREAMING: 'CAMERA_IS_STREAMING',
  },
};

export const useSocket = () => {
  const [socket, setSocket] = useState<WebSocket>(globalSocket);
  useEffect(() => {
    if (globalSocket) {
      setSocket(globalSocket);
    } else {
      const currentSocket = new WebSocket(SOCKET_SERVER);
      globalSocket = currentSocket;
    }
  }, []);

  const waitSocketConnect = useCallback(
    async (): Promise<WebSocket> =>
      new Promise((resolve, reject) => {
        if (!globalSocket) {
          return;
        }
        if (globalSocket.readyState === WebSocket.OPEN) {
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
