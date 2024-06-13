import { SpeedDial } from '@mui/material';
import SpeedDialIcon from '@mui/material/SpeedDialIcon';
import SpeedDialAction from '@mui/material/SpeedDialAction';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import FitScreenIcon from '@mui/icons-material/FitScreen';
import NestCamWiredStandIcon from '@mui/icons-material/NestCamWiredStand';
import VideocamIcon from '@mui/icons-material/Videocam';
import VideoCameraBackIcon from '@mui/icons-material/VideoCameraBack';
import VideocamOffIcon from '@mui/icons-material/VideocamOff';
import { useEffect, useState } from 'react';
import { SOCKET_EVENT_NAMES, useSocket } from '../../../hooks/use-socket';
import ReconnectingWebSocket from 'reconnecting-websocket';
import { useRouter } from 'next/router';
import { FullScreenEventBus } from '../../../event-buses/fullscreen.event-bus';

export const CommandsPad = () => {
  const router = useRouter();
  const [isFullScreen, setIsFullScreen] = useState(false);
  const [open, setOpen] = useState(false);
  const [cameraUrl, setCameraUrl] = useState('');
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const { waitSocketConnect, socketEmit } = useSocket();
  useEffect(() => {
    let socket: ReconnectingWebSocket;
    const onSocketMessage = (ev: MessageEvent<any>) => {
      const msg = JSON.parse(ev.data ?? '{}');
      if (msg?.event === SOCKET_EVENT_NAMES.CAMERA.CAMERA_IS_STREAMING) {
        const data = JSON.parse(msg.data ?? '{}');
        const hostName = window.location.hostname;
        const url = `http://${hostName ?? data?.host}:${data?.port}`;
        setCameraUrl(url);
      }
    };
    const loadSocket = async () => {
      socket = await waitSocketConnect();
      socket.addEventListener('message', onSocketMessage);
      socketEmit(SOCKET_EVENT_NAMES.CAMERA.CAMERA_GET_STATUS);
    };
    setTimeout(() => {
      loadSocket();
    }, 1000);

    return () => {
      if (socket) {
        socket.removeEventListener('message', onSocketMessage);
      }
    };
  }, [waitSocketConnect]);

  return (
    // <Box sx={{ opacity: 0.3, height: 320, transform: 'translateZ(0px)', flexGrow: 1 }}>
    <SpeedDial
      ariaLabel="Commands"
      sx={{ opacity: 0.4, position: 'absolute', top: 16, right: 16 }}
      icon={<SpeedDialIcon />}
      onClose={handleClose}
      onOpen={handleOpen}
      open={open}
      direction="left"
    >
      {!cameraUrl && 
        <SpeedDialAction
          icon={<VideocamIcon />}
          tooltipTitle="Camera SD"
          // tooltipOpen
          onClick={() => {
            socketEmit(SOCKET_EVENT_NAMES.CAMERA.CAMERA_START_STREAMING, { dimensions: 'SD' });
          }}
        />
      }
      {!cameraUrl &&     
        <SpeedDialAction
          icon={<VideoCameraBackIcon />}
          tooltipTitle="Camera HD"
          // tooltipOpen
          onClick={() => {
            socketEmit(SOCKET_EVENT_NAMES.CAMERA.CAMERA_START_STREAMING, { dimensions: 'HD' });
          }}
        />
      } 
      {cameraUrl && 
        <SpeedDialAction
          icon={<VideocamOffIcon />}
          tooltipTitle="Turn Off Camera"
          // tooltipOpen
          onClick={() => {
            socketEmit(SOCKET_EVENT_NAMES.CAMERA.CAMERA_STOP_STREAMING);
            setCameraUrl('');
          }}
        />
      }
      
      <SpeedDialAction
        icon={<NestCamWiredStandIcon />}
        tooltipTitle="Camera Pan-Tilt"
        onClick={() => {
          router.push('/camera-pantilt');
        }}
      />
      <SpeedDialAction
        icon={<FitScreenIcon />}
        tooltipTitle="Full Screen"
        onClick={() => {
          if(!isFullScreen) {
            FullScreenEventBus.emitFullScreenRequest();
          } else {
            FullScreenEventBus.emitFullScreenExit();
          }
          setIsFullScreen(!isFullScreen);
        }}
      />
      <SpeedDialAction
        icon={<RestartAltIcon />}
        tooltipTitle="Restart"
        onClick={() => {
          socketEmit(SOCKET_EVENT_NAMES.COMMANDS.SYSTEM_RESTART);
          handleClose();
        }}
      />
    </SpeedDial>
    // </Box>
  );
};
