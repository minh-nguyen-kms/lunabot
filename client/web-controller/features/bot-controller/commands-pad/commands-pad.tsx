import { SpeedDial } from '@mui/material';
import SpeedDialIcon from '@mui/material/SpeedDialIcon';
import SpeedDialAction from '@mui/material/SpeedDialAction';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import NestCamWiredStandIcon from '@mui/icons-material/NestCamWiredStand';
import { useEffect, useState } from 'react';
import { SOCKET_EVENT_NAMES, useSocket } from '../../../hooks/use-socket';
import ReconnectingWebSocket from 'reconnecting-websocket';
import { useRouter } from 'next/router';

export const CommandsPad = () => {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const { waitSocketConnect, socketEmit } = useSocket();
  useEffect(() => {
    let socket: ReconnectingWebSocket;
    const onSocketMessage = (ev: MessageEvent<any>) => {
      const msg = JSON.parse(ev.data ?? '{}');
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
    // <Box sx={{ opacity: 0.3, height: 320, transform: 'translateZ(0px)', flexGrow: 1 }}>
    <SpeedDial
      ariaLabel="Commands"
      sx={{ opacity: 0.4, position: 'absolute', top: 16, left: 16 }}
      icon={<SpeedDialIcon />}
      onClose={handleClose}
      onOpen={handleOpen}
      open={open}
      direction="down"
    >
      <SpeedDialAction
        icon={<RestartAltIcon />}
        tooltipTitle="Restart"
        onClick={() => {
          socketEmit(SOCKET_EVENT_NAMES.COMMANDS.SYSTEM_RESTART);
          handleClose();
        }}
      />
      <SpeedDialAction
        icon={<NestCamWiredStandIcon />}
        tooltipTitle="Camera Pan-Tilt"
        onClick={() => {
          router.push('/camera-pantilt');
        }}
      />
    </SpeedDial>
    // </Box>
  );
};
