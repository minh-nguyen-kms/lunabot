export const createEventBus = <T>() => {
    if (typeof (document) === 'undefined') {
      return;
    }
    // utilize dom element to create event bus
    const eventBus = document.createElement('div');
  
    const on = (eventName: string, callback: (event: CustomEvent<T>) => void) => {
      eventBus.addEventListener(eventName, callback as EventListener);
    };
  
    const off = (eventName: string, callback: (event: CustomEvent<T>) => void) => {
      eventBus.removeEventListener(eventName, callback as EventListener);
    };
  
    const emit = (eventName: string, detail: T) => {
      eventBus.dispatchEvent(new CustomEvent(eventName, { detail }));
    };
  
    return {
      on,
      off,
      emit,
    };
  };
  