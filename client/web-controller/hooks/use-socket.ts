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
    CAMERA_IS_NOT_STREAMING: 'CAMERA_IS_NOT_STREAMING',
    CAMERA_GET_STATUS: 'CAMERA_GET_STATUS',
  },
  MIC: {
    MIC_START_STREAMING: 'MIC_START_STREAMING',
    MIC_STOP_STREAMING: 'MIC_STOP_STREAMING',
    MIC_IS_STREAMING: 'MIC_IS_STREAMING',
    MIC_GET_STATUS: 'MIC_GET_STATUS',
  },
  COMMANDS: {
    SYSTEM_RESTART: 'SYSTEM_RESTART',
  },
  CAMERA_PANTILT: {
    CAMERA_PANTILT_MOVE: 'CAMERA_PANTILT_MOVE',
    CAMERA_PANTILT_STOP: 'CAMERA_PANTILT_STOP',
    CAMERA_PANTILT_CENTER_VIEW: 'CAMERA_PANTILT_CENTER_VIEW',
  },
  SWITCHS: {
    SWITCH_LIGHT_ON: 'SWITCH_LIGHT_ON',
    SWITCH_LIGHT_OFF: 'SWITCH_LIGHT_OFF',
  },
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
