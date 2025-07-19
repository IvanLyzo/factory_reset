from map.triggers.trigger import Trigger

# DEPRECATED: maybe just use triggers with a map to store id, no reason to create a whole class so similar
class Door(Trigger):

    def __init__(self, rect, id, on_enter):
        super().__init__(rect, on_enter)

        self.id = id