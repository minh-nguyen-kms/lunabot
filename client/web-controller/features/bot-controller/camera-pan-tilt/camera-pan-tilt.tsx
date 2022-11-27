import type { NextPage } from 'next';
import { EventData, JoystickOutputData } from 'nipplejs';
import { useMemo } from 'react';
import CloseIcon from '@mui/icons-material/Close';
import styles from './camera-pan-tilt.module.scss';
import { IconButton } from '@mui/material';
import { useRouter } from 'next/router';
import { CameraPad } from '../camera-pad/camera-pad';
import { MovingPad } from '../moving-pad/moving-pad';
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
    </div>
  );
};
