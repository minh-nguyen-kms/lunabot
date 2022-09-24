import { MovingPad } from './moving-pad/moving-pad';
import styles from './bot-controller.module.scss';
import { JoystickManager } from 'nipplejs';
import { useCallback, useRef } from 'react';
import { Socket } from 'socket.io-client';
import { SOCKET_EVENT_NAMES, useSocket } from '../../hooks/use-socket';
import { CameraPad } from './camera-pad/camera-pad';

const MOVING_STREAMING_TIMEOUT = 500;

export interface IMovingDirection {
  x: string;
  y: string;
}

let movingTimeOut: NodeJS.Timer | null;
const continuesEmitMoving = (
  socket: Socket | undefined,
  dir: IMovingDirection,
) => {
  if (!socket) {
    return;
  }

  // emit first event
  socket.emit(SOCKET_EVENT_NAMES.MOVING, dir);

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
    socket.emit(SOCKET_EVENT_NAMES.MOVING, dir);
  }, MOVING_STREAMING_TIMEOUT);
};

export const BotController = () => {
  const verticalDirection = useRef('');
  const horizontalDirection = useRef('');
  const socket = useSocket();

  const onDirection = useCallback(() => {
    const dir: IMovingDirection = {
      y: verticalDirection.current,
      x: horizontalDirection.current,
    };
    // continuesEmitMoving(socket, dir);
  }, []);

  const leftPadListener = useCallback(
    (manager: JoystickManager) => {
      manager.on('plain:up', () => {
        verticalDirection.current = 'FORWARD';
        onDirection();
      });
      manager.on('plain:down', () => {
        verticalDirection.current = 'BACKWARD';
        onDirection();
      });
      manager.on('end', () => {
        verticalDirection.current = '';
        onDirection();
      });
    },
    [onDirection],
  );

  const rightPadListener = useCallback(
    (manager: JoystickManager) => {
      manager.on('plain:left', () => {
        horizontalDirection.current = 'LEFT';
        onDirection();
      });
      manager.on('plain:right', () => {
        horizontalDirection.current = 'RIGHT';
        onDirection();
      });
      manager.on('end', () => {
        horizontalDirection.current = '';
        onDirection();
      });
    },
    [onDirection],
  );

  return (
    <div className={styles.botController}>
      <CameraPad />
      <MovingPad managerListener={leftPadListener} options={{ lockY: true }} />
      <MovingPad managerListener={rightPadListener} options={{ lockX: true }} />
    </div>
  );
};
