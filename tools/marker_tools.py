import PySimpleGUI as sg
from abc import ABC, abstractmethod
import numpy as np
from utils import utils as utils

from input_output.api_facade import ManagerFacade


class Tool(ABC):
    def __init__(self, name_identifier) -> None:
        super().__init__()
        self.name_identifier = name_identifier

    @abstractmethod
    def reset(self):
        pass

    def commit_current_state(self, frame_width, frame_height):
        res = self._commit_current_state(frame_width, frame_height)
        self.reset()
        return res

    @abstractmethod
    def _commit_current_state(self, frame_width, frame_height):
        pass

    @abstractmethod
    def process(self, event, point):
        pass

    @abstractmethod
    def draw(self, overlay: sg.Graph):
        pass


class NoneTool(Tool):
    def __init__(self) -> None:
        super().__init__("NONE")

    def _commit_current_state(self, frame_width, frame_height):
        pass

    def reset(self):
        pass

    def process(self, event, point):
        pass

    def draw(self, overlay: sg.Graph):
        pass


class DraggableTool(Tool):
    def __init__(self, name_identifier) -> None:
        super().__init__(name_identifier)
        print("init {}".format(name_identifier))
        self.is_dragging = False
        self.start_point = (0, 0)
        self.end_point = (0, 0)

    def reset(self):
        self.is_dragging = False
        self.start_point = (0, 0)
        self.end_point = (0, 0)

    def start_drag(self, image_point):
        self.is_dragging = True
        self.start_point = image_point
        self.end_point = image_point

    def stop_drag(self, image_point):
        self.end_point = image_point
        self.is_dragging = False

    def move_drag(self, image_point):
        self.end_point = image_point
        pass

    def process(self, event, image_point):
        if self.is_dragging:
            if event.endswith("+UP"):
                self.stop_drag(image_point)
            else:
                self.move_drag(image_point)
        else:
            self.start_drag(image_point)

    def _commit_current_state(self, frame_width, frame_height):
        l = min(self.start_point[0], self.end_point[0])
        r = max(self.start_point[0], self.end_point[0])
        u = min(self.start_point[1], self.end_point[1])
        d = max(self.start_point[1], self.end_point[1])
        w = (r - l) / frame_width
        h = (d - u) / frame_height
        clipped_def = np.clip([l / frame_width, u / frame_height, w, h], 0, 1)

        return {
            "type": self.name_identifier,
            "def": clipped_def.tolist()
        }

    @abstractmethod
    def draw(self, overlay: sg.Graph):
        pass


class AddRectangleTool(DraggableTool):
    def __init__(self) -> None:
        super().__init__("RECTANGLE")

    def draw(self, overlay: sg.Graph):
        # red while drawing. dark red if released and not commited
        color = "#ff0000" if self.is_dragging else "#990000"
        utils.draw_rectangle(overlay, self.start_point, self.end_point, line_color=color, line_width=2)


class AddOvalTool(DraggableTool):
    def __init__(self) -> None:
        super().__init__("OVAL")

    def draw(self, overlay: sg.Graph):
        color = "#ff0000" if self.is_dragging else "#990000"
        utils.draw_oval(overlay, self.start_point, self.end_point, line_color=color, line_width=2)

class AddPointTool(Tool):
    def __init__(self) -> None:
        super().__init__("POINT")
        self.dragging = False
        self.point = (0, 0)
        self.ghost_size = (32, 32)

    def reset(self):
        self.point = (0, 0)
        pass

    def _commit_current_state(self, frame_width, frame_height):

        clipped_def = np.clip([self.point[0] / frame_width,
                               self.point[1] / frame_height], 0, 1)

        return {
            "type": self.name_identifier,
            "def": clipped_def.tolist()
        }

    def process(self, event, image_point):
        if self.dragging:
            if event.endswith("+UP"):
                self.dragging = False
        else:
            self.dragging = True

        self.point = image_point

    def draw(self, overlay: sg.Graph):
        color = "#ff0000" if self.dragging else "#990000"
        utils.draw_cross(overlay, self.point, self.ghost_size, line_color=color, line_width=2)


class RemoveLabelTool(Tool):

    def __init__(self, api: ManagerFacade, w, h) -> None:
        super().__init__("REMOVELABEL")
        self.api = api
        self.w = w
        self.h = h

    def reset(self):
        pass

    def _commit_current_state(self, frame_width, frame_height):
        pass

    def process(self, event, point):
        if event.endswith("+UP"):
            self.api.remove_marker_at((point[0] / self.w, point[1] / self.h))
            self.api.save_marker_file()

    def draw(self, overlay: sg.Graph):
        pass