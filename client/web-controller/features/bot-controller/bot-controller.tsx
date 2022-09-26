import { MovingPad } from './moving-pad/moving-pad';
import styles from './bot-controller.module.scss';
import { EventData, JoystickOutputData } from 'nipplejs';
import { memo, useCallback, useMemo, useRef } from 'react';
import { SOCKET_EVENT_NAMES, useSocket } from '../../hooks/use-socket';
import { CameraPad } from './camera-pad/camera-pad';

const MOVING_STREAMING_TIMEOUT = 500;

export interface IMovingDirection {
  x: string;
  y: string;
  xSpeed?: number;
  ySpeed?: number;
}

let movingTimeOut: NodeJS.Timer | null;
const continuesEmitMoving = (
  socketEmit: <T>(event: string, data?: T) => void,
  dir: IMovingDirection,
) => {
  if (!socketEmit) {
    return;
  }

  // emit first event
  socketEmit(SOCKET_EVENT_NAMES.MOVING, dir);

  const isMoving = dir.y !== '';
  const isRotating = dir.x !== '';

  // stop streaming moving event
  if (!isMoving && !isRotating && movingTimeOut) {
    clearInterval(movingTimeOut);
    movingTimeOut = null;
    return;
  }

  // clear last streaming
  if (movingTimeOut) {
    clearInterval(movingTimeOut);
  }

  // start streaming moving events
  movingTimeOut = setInterval(() => {
    socketEmit(SOCKET_EVENT_NAMES.MOVING, dir);
  }, MOVING_STREAMING_TIMEOUT);
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
      <CameraPad />
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
  );
};

export const BotController = memo(BotControllerComponent);
