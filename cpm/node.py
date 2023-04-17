import copy
from typing import Hashable


class Activity:
    """

    Specific id_'s:
        "START" - start node
        "FINISH" - final node
        "*_apparent_*" - apparent task.
    """

    def __init__(self, id_: str, prev_activity_id: [Hashable, ], duration: float):
        self.id_: str = id_
        self.prev_activity: [Hashable, ] = copy.deepcopy(prev_activity_id)
        self.duration: float = duration


class Event:
    def __init__(self, early_start: float = None, early_final: float = None,
                 late_start: float = None, late_final: float = None,
                 possible_delay: float = None):
        self.early_start: float = early_start
        self.early_final: float = early_final
        self.late_start: float = late_start
        self.late_final: float = late_final
        self.possible_delay: float = possible_delay


class Node:
    def __init__(self, activity_id_: str, prev_activity_id: [Hashable, ], duration: float, event: Event = None):
        """ Activity + event that finishes that activity. """

        self.activity: Activity = Activity(id_=activity_id_, prev_activity_id=prev_activity_id, duration=duration)
        self.event: Event = event or Event()

    def asdict(self):
        return {
            "id_": self.activity.id_, "prev_activity": self.activity.prev_activity, "duration": self.activity.duration,
            "early_start": self.event.early_start, "early_final": self.event.early_final,
            "late_start": self.event.late_start, "late_final": self.event.late_final,
            "possible_delay": self.event.possible_delay
        }

    def __repr__(self):
        return str(self.asdict())


class ApparentNode(Node):
    """ No activity, zeroed event. """

    def __init__(self, activity_name: str = "apparent",
                 prev_activity_id: [Hashable, ] = None, duration: float = 0, event: Event = None):
        super().__init__(activity_name, prev_activity_id or [], duration, event or Event(0, 0, 0, 0, 0))


class StartNode(ApparentNode):
    def __init__(self):
        super().__init__(activity_name="START")


class FinalNode(ApparentNode):
    def __init__(self, last_event: Event):
        super().__init__(activity_name="FINISH", event=copy.deepcopy(last_event))
        self.event.early_start = self.event.late_start = self.event.late_final = self.event.early_final
        self.event.possible_delay = 0
