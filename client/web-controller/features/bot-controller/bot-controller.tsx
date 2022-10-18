import { MovingPad } from './moving-pad/moving-pad';
import styles from './bot-controller.module.scss';
import { EventData, JoystickOutputData } from 'nipplejs';
import { memo, useCallback, useMemo, useRef } from 'react';
import { SOCKET_EVENT_NAMES, useSocket } from '../../hooks/use-socket';
import { CameraPad } from './camera-pad/camera-pad';
import { CommandsPad } from './commands-pad/commands-pad';

const MOVING_STREAMING_TIME_FRAME = 100; //milisecond
const MOVING_EMITING_TIME_FRAME = 900; //milisecond

export interface IMovingDirection {
  x: string;
  y: string;
  xSpeed?: number;
  ySpeed?: number;
}

let movingTimer: NodeJS.Timer | null;
let nextMovingTime = 0;
const streamMovingSignal = (
  socketEmit: <T>(event: string, data?: T) => void,
  dir: IMovingDirection,
) => {
  if (!socketEmit) {
    return;
  }

  const isMoving = dir.y !== '';
  const isRotating = dir.x !== '';

  // there is no moving
  if (!isMoving && !isRotating) {
    // Emit stop signal
    socketEmit(SOCKET_EVENT_NAMES.MOVING, dir);
    if (movingTimer) {
      clearTimeout(movingTimer);
      movingTimer = null;
    }
    return;
  }

  const currentTime = new Date().getTime();
  const timeLeftToNextTick = nextMovingTime - currentTime;
  if (timeLeftToNextTick <= 0) {
    // there is no moving signal already
    // -> Emit immediately
    socketEmit(SOCKET_EVENT_NAMES.MOVING, dir);
    nextMovingTime = currentTime + MOVING_STREAMING_TIME_FRAME;
  } else {
    // delay for next tick to emit moving signal
    if (movingTimer) {
      clearTimeout(movingTimer);
    }
    movingTimer = setTimeout(() => {
      socketEmit(SOCKET_EVENT_NAMES.MOVING, dir);
      nextMovingTime = currentTime + MOVING_STREAMING_TIME_FRAME;
    }, timeLeftToNextTick);
  }
};

let emitMovingTimer: NodeJS.Timer | null;
// const continuesEmitMoving = streamMovingSignal;
const continuesEmitMoving = (
  socketEmit: <T>(event: string, data?: T) => void,
  dir: IMovingDirection,
) => {
  if (!!emitMovingTimer) {
    clearInterval(emitMovingTimer);
  }

  if (!socketEmit) {
    return;
  }
  const isMoving = dir.y !== '';
  const isRotating = dir.x !== '';

  streamMovingSignal(socketEmit, dir);
  if (!isMoving && !isRotating) {
    return;
  }

  emitMovingTimer = setInterval(() => {
    streamMovingSignal(socketEmit, dir);
  }, MOVING_EMITING_TIME_FRAME);
};

const BotControllerComponent = () => {
  const verticalDirection = useRef('');
  const verticalSpeed = useRef(0);
  const horizontalDirection = useRef('');
  const horizontalSpeed = useRef(0);
  const { socketEmit } = useSocket();

  const onDirection = useCallback(() => {
    const dir: IMovingDirection = {
      y: verticalDirection.current,
      x: horizontalDirection.current,
      xSpeed: horizontalSpeed.current,
      ySpeed: verticalSpeed.current,
    };
    continuesEmitMoving(socketEmit, dir);
  }, [socketEmit]);

  const leftPadListeners = useMemo(
    () => ({
      move: (ev: EventData, data: JoystickOutputData) => {
        const dir = data?.direction?.y?.toUpperCase();
        verticalDirection.current = dir;
        verticalSpeed.current = data?.vector?.y;
        onDirection();
      },
      end: () => {
        verticalDirection.current = '';
        verticalSpeed.current = 0;
        onDirection();
      },
    }),
    [onDirection],
  );

  const rightPadListeners = useMemo(
    () => ({
      move: (ev: EventData, data: JoystickOutputData) => {
        const dir = data?.direction?.x?.toUpperCase();
        horizontalDirection.current = dir;
        horizontalSpeed.current = data?.vector?.x;
        onDirection();
      },
      end: () => {
        horizontalDirection.current = '';
        horizontalSpeed.current = 0;
        onDirection();
      },
    }),
    [onDirection],
  );

  const leftOptions = useMemo(() => ({ lockY: true }), []);
  const rightOptions = useMemo(() => ({ lockX: true }), []);

  return (
    <div className={styles.botController}>
      <CommandsPad />
      <CameraPad />
      <div className={styles.movingPadContainer}>
        <MovingPad
          joyStickId="leftPad"
          managerListeners={leftPadListeners}
          options={leftOptions}
        />
        <MovingPad
          joyStickId="rightPad"
          managerListeners={rightPadListeners}
          options={rightOptions}
        />
      </div>
    </div>
  );
};

export const BotController = memo(BotControllerComponent);
