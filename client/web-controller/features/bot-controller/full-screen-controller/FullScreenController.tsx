import React, { memo, useEffect } from 'react';
import { FullScreenEventBus } from '../../../event-buses/fullscreen.event-bus';

export interface IFullScreenControllerProps {
  targetId: string;
}
const FullScreenControllerComponent = (props: IFullScreenControllerProps) => {
  const { targetId } = props;

  useEffect(() => {
    const handleRequestFullScreen = () => {
      const element = document.getElementById(targetId);
      if (element && element.requestFullscreen) {
        element.requestFullscreen();
      }
    }
    const handleExitFullScreen = () => {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
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
