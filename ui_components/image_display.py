import PySimpleGUI as sg

from input_output.api_facade import ManagerFacade
from ui_components.component import UIComponent
from ui_components.image_controls import ImageControls

import ui_keys as uk

class ImageDisplay(UIComponent):

    def __init__(self, api: ManagerFacade) -> None:
        super().__init__()
        self.api = api
        self.image_controls = ImageControls(self.api)
        self.graph = sg.Graph((1280, 768), (0, 768), (1280, 0), key=uk.IMAGE_GRAPH, enable_events=True, drag_submits=True)
        self._current_frame = None

    def get_layout(self):
        return [[self.graph],
                self.image_controls.get_layout()]

    def process_event(self, window, event, values):
        new_frame, frame = self.image_controls.process_event(window, event, values)

        if new_frame:
            self._current_frame = frame


        self.graph.erase()
        self.graph.draw_image(data=self._current_frame, location=(0, 0))
        self.api.draw_markers_to_graph(self.graph)



