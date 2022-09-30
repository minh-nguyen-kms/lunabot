import React, { memo, useEffect, useRef } from 'react';
import {
  EventData,
  JoystickManager,
  JoystickManagerOptions,
  JoystickOutputData,
} from 'nipplejs';

export interface JoyStickProps {
  joyStickId: string;
  managerListeners: {
    move: (ev: EventData, data: JoystickOutputData) => void;
    end: (ev: EventData, data: JoystickOutputData) => void;
  };
  options?: JoystickManagerOptions;
  containerStyle?: React.CSSProperties;
}

const JoyStickComponent = ({
  joyStickId,
  options,
  managerListeners,
  containerStyle,
}: JoyStickProps) => {
  const containerRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (typeof window === 'undefined') {
      return;
    }

    const windowObject = window as any;
    windowObject.nipples = windowObject.nipples ?? {};
    windowObject.isLoadingNipple = windowObject.isLoadingNipple ?? {};

    const loadData = async () => {
      if (!containerRef) {
        return;
      }
      if (typeof window === 'undefined') {
        return;
      }

      let manager: JoystickManager = windowObject.nipples[joyStickId];
      if (manager) {
        manager.destroy();
      }
      const isLoading = windowObject.isLoadingNipple[joyStickId];
      if (!manager && !isLoading) {
        windowObject.isLoadingNipple[joyStickId] = true;
        const nipplejs = await import('nipplejs');
        const zone = containerRef.current as HTMLElement;
        manager = nipplejs.create({
          mode: 'static',
          shape: 'circle',
          position: { left: '50%', top: '50%' },
          size: 150,
          catchDistance: 200,
          color: 'red',
          zone,
          ...options,
        });
        windowObject.nipples[joyStickId] = manager;
      }
      if (!manager) {
        return;
      }
      windowObject.nipples[joyStickId].on('move', managerListeners.move);
      windowObject.nipples[joyStickId].on('end', managerListeners.end);
    };
    loadData();
    return () => {
      const manager: JoystickManager = windowObject.nipples[joyStickId];
      if (manager) {
        manager.destroy();
      }
    };
  }, [options, managerListeners, joyStickId]);

  const styles: React.CSSProperties = {
    ...containerStyle,
    position: 'relative',
  };

  return <div ref={containerRef} style={styles} />;
};

export const JoyStick = memo(JoyStickComponent);
