import React, { memo, useEffect } from 'react';
import { FullScreenEventBus } from '../../../event-buses/fullscreen.event-bus';

export interface IFullScreenControllerProps {
  targetId: string;
}
const FullScreenControllerComponent = (props: IFullScreenControllerProps) => {
  const { targetId } = props;

  useEffect(() => {
    const handleRequestFullScreen = () => {
      const target = document.getElementById(targetId);
      if (target) {
        target.requestFullscreen();
      }
    }
    const handleExitFullScreen = () => {
      document.exitFullscreen();
    }

    FullScreenEventBus.onFullScreenRequest(handleRequestFullScreen);
    FullScreenEventBus.onFullScreenExit(handleExitFullScreen);


    return () => {
      FullScreenEventBus.offFullScreenRequest(handleRequestFullScreen);
      FullScreenEventBus.offFullScreenExit(handleExitFullScreen);
    }
  }, []);

  return <></>;
};

export const FullScreenController = memo(
  FullScreenControllerComponent,
);
