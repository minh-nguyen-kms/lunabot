import { createEventBus } from "../utils/event-bus.helper";

type SocketEventBusType = MessageEvent;
const eventBus = createEventBus<SocketEventBusType>();
export const SocketEventBus = {
    onMessage: (callback: (event: CustomEvent<SocketEventBusType>) => void) => eventBus?.on('message', callback),
    offMessage: (callback: (event: CustomEvent<SocketEventBusType>) => void) => eventBus?.off('message', callback),
    emitMessage: (data: SocketEventBusType) => eventBus?.emit('message', data),
};
