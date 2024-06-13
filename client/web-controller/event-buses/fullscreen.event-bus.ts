import { createEventBus } from '../utils/event-bus.helper';

const eventBus = createEventBus<void>();
export const FullScreenEventBus = {
    onFullScreenRequest: (callback: (event: CustomEvent<void>) => void) => eventBus?.on('fullscreen-request', callback),
    offFullScreenRequest: (callback: (event: CustomEvent<void>) => void) => eventBus?.off('fullscreen-request', callback),
    emitFullScreenRequest: () => eventBus?.emit('fullscreen-request'),

    onFullScreenExit: (callback: (event: CustomEvent<void>) => void) => eventBus?.on('fullscreen-exit', callback),
    offFullScreenExit: (callback: (event: CustomEvent<void>) => void) => eventBus?.off('fullscreen-exit', callback),
    emitFullScreenExit: () => eventBus?.emit('fullscreen-exit'),
}

