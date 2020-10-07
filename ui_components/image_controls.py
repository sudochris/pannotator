import PySimpleGUI as sg

from input_output.api_facade import ManagerFacade
from ui_components.component import UIComponent
import ui_keys as uk


class ImageControls(UIComponent):
    def __init__(self, api: ManagerFacade) -> None:
        super().__init__()
        self.api = api

    def get_layout(self):
        self.slider = sg.Slider((0, self.api.total_images() - 1), 0,
                          orientation="h",
                          enable_events=True, change_submits=True,
                          key=uk.IMAGE_SLIDER)

        return [sg.Button("Previous", key=uk.PREVIOUS_IMAGE),
                sg.Button("Next", key=uk.NEXT_IMAGE),
                self.slider]

    def process_event(self, window, event, values):
        frame = None
        new_frame = False
        if event == uk.NEXT_IMAGE or event.startswith("Right"):
            frame = self.api.next_image()
            self.slider.update(self.api.current_image_idx())
            new_frame = True

        if event == uk.PREVIOUS_IMAGE or event.startswith("Left"):
            frame = self.api.previous_image()
            self.slider.update(self.api.current_image_idx())
            new_frame = True

        if event.startswith(uk.IMAGE_SLIDER):
            selected_location = int(values[uk.IMAGE_SLIDER])
            frame = self.api.get_image(selected_location)
            new_frame = True

        return new_frame, frame

