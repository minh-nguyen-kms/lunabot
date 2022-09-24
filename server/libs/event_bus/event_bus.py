import awebus

class EventBus:
    
    def __init__(self):
        self.bus = awebus.Bus()

    def __str__(self):
        return 'EventBus'

    def on(self, event_name, handler):
        self.bus.on(event_name, handler)

    def off(self, event_name, handler):
        self.bus.off(event_name, handler)
    
    def emit( self, event, *args, **kwargs ):
        self.bus.emit(event, *args, **kwargs)
    
    def emitAsync( self, event, *args, **kwargs ):
        self.bus.emitAsync(event, *args, **kwargs)