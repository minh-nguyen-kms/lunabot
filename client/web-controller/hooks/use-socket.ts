import { useCallback, useEffect, useState } from 'react';

let globalSocket: WebSocket;

const SOCKET_SERVER = 'ws://192.168.1.151:9102';

export const SOCKET_EVENT_NAMES = {
  DISCONNECT: 'DISCONNECT',
  MOVING: 'MOVING',
  CAMERA: {
    CAMERA_START_STREAMING: 'CAMERA_START_STREAMING',
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
        if (!socket) {
          return;
        }
        if (socket.readyState === WebSocket.OPEN) {
          resolve(socket);
          return;
        }
        socket.onopen = () => {
          resolve(socket);
        };
        socket.onerror = (error) => {
          reject(error);
        };
      }),
    [socket],
  );

  const socketEmit = useCallback(
    <T>(event: string, data?: T) => {
      socket?.send(
        JSON.stringify({
          event,
          data,
        }),
      );
    },
    [socket],
  );

  return {
    socket,
    socketEmit,
    waitSocketConnect,
  };
};
