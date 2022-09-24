import React, { useEffect, useRef } from 'react';
import { JoystickManager, JoystickManagerOptions } from 'nipplejs';

export interface JoyStickProps {
  managerListener: (manager: JoystickManager) => void;
  options?: JoystickManagerOptions;
  containerStyle?: React.CSSProperties;
}

export const JoyStick = (props: JoyStickProps) => {
  const containerRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const loadData = async () => {
      if (!containerRef) {
        return;
      }

      const nipplejs = await import('nipplejs');

      const zone = containerRef.current as HTMLElement;
      const manager = nipplejs.create({
        mode: 'static',
        position: { left: '50%', top: '50%' },
        catchDistance: 150,
        color: 'red',
        zone,
        ...props.options,
      });
      props.managerListener(manager);
    };
    loadData();
  }, [props]);

  const styles: React.CSSProperties = {
    ...props.containerStyle,
    position: 'relative',
  };

  return <div ref={containerRef} style={styles} />;
};
