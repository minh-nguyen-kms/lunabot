import { memo, useEffect, useState } from 'react';
import ReconnectingWebSocket from 'reconnecting-websocket';
import { SOCKET_EVENT_NAMES, useSocket } from '../../../hooks/use-socket';
import styles from './camera-pad.module.scss';
import { SocketEventBus } from '../../../event-buses/socket.event-bus';

export interface ICameraPadProps {
  defaultValue?: string;
}
const CameraPadComponent = ({ defaultValue }: ICameraPadProps) => {
  const [streamUrl, setStreamUrl] = useState('');
  const [audioUrl, setAudioUrl] = useState('');
  const [isLoadingCamera, setIsLoadingCamera] = useState(false);
  const { waitSocketConnect, socketEmit } = useSocket();

  useEffect(() => {
    let socket: ReconnectingWebSocket;
    const onSocketMessage = (ev: MessageEvent<any>) => {
      SocketEventBus.emitMessage(ev);
      const msg = JSON.parse(ev.data ?? '{}');
      if (msg?.event === SOCKET_EVENT_NAMES.CAMERA.CAMERA_IS_STREAMING) {
        const data = JSON.parse(msg.data ?? '{}');
        const hostName = window.location.hostname;
        const url = `http://${hostName ?? data?.host}:${data?.port}`;
        setStreamUrl(url);
        setIsLoadingCamera(false); 
      } else if (msg?.event === SOCKET_EVENT_NAMES.CAMERA.CAMERA_IS_NOT_STREAMING) {
        setStreamUrl('');
        setIsLoadingCamera(false); 
      }
    };
    const loadSocket = async () => {
      socket = await waitSocketConnect();
      socket.addEventListener('message', onSocketMessage);
      socketEmit(SOCKET_EVENT_NAMES.CAMERA.CAMERA_GET_STATUS);
    };
    loadSocket();

    return () => {
      if (socket) {
        socket.removeEventListener('message', onSocketMessage);
      }
    };
  }, [waitSocketConnect, socketEmit]);

  useEffect(() => {
    const hostName = window.location.hostname;
    const url = `http://${hostName}:9103/audio`;
    setAudioUrl(url);
  }, []);

  return (
    <>
      {streamUrl ? (
        <>
          <iframe className={styles.videoContainer} src={streamUrl} />
          {audioUrl && (
            <audio controls autoPlay className={styles.audio}>
              <source src={audioUrl} />
            </audio>
          )}
        </>
      ) : (
        <div className="screen-center">
          {isLoadingCamera && <div className="lds-dual-ring"></div>}
        </div>
      )}
      
    </>
  );
};

export const CameraPad = memo(CameraPadComponent);
