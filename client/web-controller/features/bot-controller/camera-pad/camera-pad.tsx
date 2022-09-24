import { memo, useEffect } from 'react';
import { SOCKET_EVENT_NAMES, useSocket } from '../../../hooks/use-socket';

export interface ICameraPadProps {
  defaultValue?: string;
}
const CameraPadComponent = ({ defaultValue }: ICameraPadProps) => {
  const { waitSocketConnect, socketEmit } = useSocket();
  useEffect(() => {
    let socket: WebSocket;
    const onSocketMessage = (ev: MessageEvent<any>) => {
      console.log('ev.data', ev.data);
    };
    const loadSocket = async () => {
      socket = await waitSocketConnect();
      socket.addEventListener('message', onSocketMessage);

      socketEmit(SOCKET_EVENT_NAMES.CAMERA.CAMERA_START_STREAMING);
    };
    loadSocket();

    return () => {
      if (socket) {
        socket.removeEventListener('message', onSocketMessage);
      }
    };
  }, [socketEmit, waitSocketConnect]);
  return <></>;
};

export const CameraPad = memo(CameraPadComponent);
