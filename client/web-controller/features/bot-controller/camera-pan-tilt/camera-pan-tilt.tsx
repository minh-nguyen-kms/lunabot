import type { NextPage } from 'next';
import { EventData, JoystickOutputData } from 'nipplejs';
import { useMemo, useState } from 'react';
import CloseIcon from '@mui/icons-material/Close';
import styles from './camera-pan-tilt.module.scss';
import { IconButton, SpeedDial, SpeedDialAction } from '@mui/material';
import { useRouter } from 'next/router';
import { CameraPad } from '../camera-pad/camera-pad';
import { MovingPad } from '../moving-pad/moving-pad';
import CenterFocusStrongIcon from '@mui/icons-material/CenterFocusStrong';
import SpeedDialIcon from '@mui/material/SpeedDialIcon';
import { SOCKET_EVENT_NAMES, useSocket } from '../../../hooks/use-socket';

const MOVING_STREAMING_TIME_FRAME = 500; //milisecond

export interface IPanTiltDirection {
  x?: number;
  y?: number;
}

let movingTimer: NodeJS.Timer | null;
let nextMovingTime = 0;
const streamMovingSignal = (
  socketEmit: <T>(event: string, data?: T) => void,
  dir: IPanTiltDirection,
) => {
  if (!socketEmit) {
    return;
  }

  const currentTime = new Date().getTime();
  const timeLeftToNextTick = nextMovingTime - currentTime;
  if (timeLeftToNextTick <= 0) {
    // there is no moving signal already
    // -> Emit immediately
    socketEmit(SOCKET_EVENT_NAMES.CAMERA_PANTILT.CAMERA_PANTILT_MOVE, dir);
    nextMovingTime = currentTime + MOVING_STREAMING_TIME_FRAME;
  } else {
    // delay for next tick to emit moving signal
    if (movingTimer) {
      clearTimeout(movingTimer);
    }
    movingTimer = setTimeout(() => {
      socketEmit(SOCKET_EVENT_NAMES.CAMERA_PANTILT.CAMERA_PANTILT_MOVE, dir);
      nextMovingTime = currentTime + MOVING_STREAMING_TIME_FRAME;
    }, timeLeftToNextTick);
  }
};

export const CameraPanTilt: NextPage = () => {
  const router = useRouter();
  const { socketEmit } = useSocket();

  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const rightPadListeners = useMemo(
    () => ({
      move: (ev: EventData, data: JoystickOutputData) => {
        const vector = data.vector;
        streamMovingSignal(socketEmit, vector);
      },
      end: () => {
        if (movingTimer) {
          clearTimeout(movingTimer);
        }
        socketEmit(SOCKET_EVENT_NAMES.CAMERA_PANTILT.CAMERA_PANTILT_STOP);
      },
    }),
    [socketEmit],
  );

  const rightOptions = useMemo(
    () => ({ restJoystick: false, dynamicPage: true }),
    [],
  );
  return (
    <div className={styles.container}>
      <IconButton
        className={styles.closeButton}
        style={{ position: 'fixed', top: 0, left: 0 }}
        onClick={() => {
          // TODO: use react route
          window.location.href = '/';
          // router.back();
        }}
      >
        <CloseIcon htmlColor="#fff" />
      </IconButton>
      <CameraPad />
      <div className={styles.movingPadContainer}>
        <div></div>
        <MovingPad
          joyStickId="camerapantilt"
          managerListeners={rightPadListeners}
          options={rightOptions}
        />
      </div>
      <SpeedDial
        ariaLabel="Commands"
        sx={{ opacity: 0.4, position: 'absolute', top: 16, right: 16 }}
        icon={<SpeedDialIcon />}
        onClose={handleClose}
        onOpen={handleOpen}
        open={open}
        direction="left"
      >
        <SpeedDialAction
          icon={<CenterFocusStrongIcon />}
          tooltipTitle="Center View"
          // tooltipOpen
          onClick={() => {
            socketEmit(SOCKET_EVENT_NAMES.CAMERA_PANTILT.CAMERA_PANTILT_CENTER_VIEW);
          }}
        />
      </SpeedDial>
    </div>
  );
};
