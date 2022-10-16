import { memo, useEffect, useState } from 'react';
import ReconnectingWebSocket from 'reconnecting-websocket';
import { SOCKET_EVENT_NAMES, useSocket } from '../../../hooks/use-socket';
import styles from './camera-pad.module.scss';

export interface ICameraPadProps {
  defaultValue?: string;
}
const CameraPadComponent = ({ defaultValue }: ICameraPadProps) => {
  const [streamUrl, setStreamUrl] = useState('');
  const [isLoadingCamera, setIsLoadingCamera] = useState(false);
  const { waitSocketConnect, socketEmit } = useSocket();
  useEffect(() => {
    let socket: ReconnectingWebSocket;
    const onSocketMessage = (ev: MessageEvent<any>) => {
      const msg = JSON.parse(ev.data ?? '{}');
      if (msg?.event === SOCKET_EVENT_NAMES.CAMERA.CAMERA_IS_STREAMING) {
        const hostName = window.location.hostname;
        const data = JSON.parse(msg.data ?? '{}');
        const url = `http://${hostName ?? data?.host}:${data?.port}`;
        setStreamUrl(url);
        setIsLoadingCamera(false);
      }
    };
    const loadSocket = async () => {
      socket = await waitSocketConnect();
      socket.addEventListener('message', onSocketMessage);
    };
    loadSocket();

    return () => {
      if (socket) {
        socket.removeEventListener('message', onSocketMessage);
      }
    };
  }, [waitSocketConnect]);
  return (
    <>
      {streamUrl ? (
        <>
          <iframe className={styles.videoContainer} src={streamUrl} />
        </>
      ) : (
        <div className="screen-center">
          {isLoadingCamera && <div className="lds-dual-ring"></div>}
        </div>
      )}
      <div className={styles.commandBar}>
        {!streamUrl && !isLoadingCamera ? (
          <button
            onClick={() => {
              socketEmit(SOCKET_EVENT_NAMES.CAMERA.CAMERA_START_STREAMING);
              setIsLoadingCamera(true);
            }}
          >
            Turn On camera
          </button>
        ) : (
          <button
            onClick={() => {
              socketEmit(SOCKET_EVENT_NAMES.CAMERA.CAMERA_STOP_STREAMING);
              setStreamUrl('');
            }}
          >
            Turn Off camera
          </button>
        )}
      </div>
    </>
  );
};

export const CameraPad = memo(CameraPadComponent);
