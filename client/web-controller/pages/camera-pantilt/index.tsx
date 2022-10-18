import type { NextPage } from 'next';
import { EventData, JoystickOutputData } from 'nipplejs';
import { useMemo } from 'react';
import { CameraPanTilt } from '../../features/bot-controller/camera-pan-tilt/camera-pan-tilt';
import { MovingPad } from '../../features/bot-controller/moving-pad/moving-pad';
import { SOCKET_EVENT_NAMES, useSocket } from '../../hooks/use-socket';
import styles from './camera-pantilt.module.scss';

const MOVING_STREAMING_TIME_FRAME = 500; //milisecond

export interface IPanTiltDirection {
  x?: number;
  y?: number;
}

let movingTimer: NodeJS.Timer | null;
let nextMovingTime: number = 0;
const streamMovingSignal = (
  socketEmit: <T>(event: string, data?: T) => void,
  dir: IPanTiltDirection,
) => {
  if (!socketEmit) {
    return;
  }
  

  const currentTime = (new Date()).getTime();
  const timeLeftToNextTick = nextMovingTime - currentTime;
  if (timeLeftToNextTick <= 0) {
    // there is no moving signal already
    // -> Emit immediately
    socketEmit(SOCKET_EVENT_NAMES.CAMERA_PANTILT, dir);
    nextMovingTime = currentTime + MOVING_STREAMING_TIME_FRAME;
  } else {
    // delay for next tick to emit moving signal
    if (movingTimer) {
      clearTimeout(movingTimer);
    }
    movingTimer = setTimeout(() => {
      socketEmit(SOCKET_EVENT_NAMES.CAMERA_PANTILT, dir);
      nextMovingTime = currentTime + MOVING_STREAMING_TIME_FRAME;
    }, timeLeftToNextTick);
  }
};

const CameraPanTiltPage: NextPage = () => {
  const { socketEmit } = useSocket();
  const rightPadListeners = useMemo(
    () => ({
        move: (ev: EventData, data: JoystickOutputData) => {
            const vector = data.vector;
            streamMovingSignal(socketEmit, vector);
        },
        end: () => {
            console.log('end');
        },
    }),
  [],
  );

  const rightOptions = useMemo(() => ({ restJoystick: false, dynamicPage: true }), []);
  return (
    <div className={styles.container}>
      <CameraPanTilt />
      <div className={styles.movingPadContainer}>
        <div></div>
        <MovingPad
          joyStickId="rightPad"
          managerListeners={rightPadListeners}
          options={rightOptions}
        />
      </div>
    </div>
  );
};

export default CameraPanTiltPage;
