import PySimpleGUI as sg

from input_output.api_facade import ManagerFacade
from tools.marker_tools import NoneTool, AddRectangleTool, AddOvalTool, RemoveLabelTool, AddPointTool
from ui_components.component import UIComponent
import ui_keys as uk


class Toolbar(UIComponent):
    def __init__(self, api: ManagerFacade) -> None:
        super().__init__()
        self.api = api

        self.button_images = {
            uk.SELECT_ADD_RECTANGLE: self.button_image_entry("images/shape-rectangle-plus"),
            uk.SELECT_ADD_OVAL: self.button_image_entry("images/shape-oval-plus"),
            uk.SELECT_ADD_POINT: self.button_image_entry("images/shape-plus-plus"),
            uk.SELECT_ADD_POLYGON: self.button_image_entry("images/shape-polygon-plus"),
            uk.SELECT_REMOVE_LABEL: self.button_image_entry("images/magnify-remove-cursor")
        }

        self.selected_tool = NoneTool()
        self.buttons = {
            uk.SELECT_ADD_RECTANGLE: self.create_button(uk.SELECT_ADD_RECTANGLE, False),
            uk.SELECT_ADD_OVAL: self.create_button(uk.SELECT_ADD_OVAL, False),
            uk.SELECT_ADD_POINT: self.create_button(uk.SELECT_ADD_POINT, False),
            uk.SELECT_ADD_POLYGON: self.create_button(uk.SELECT_ADD_POLYGON, True),
            uk.SELECT_REMOVE_LABEL: self.create_button(uk.SELECT_REMOVE_LABEL, False)
        }

    def button_image_entry(self, base_image):
        return {"active": f"{base_image}-a.png",
                "inactive": f"{base_image}.png"}

    def create_button(self, key, disabled):
        return sg.Button("", disabled=disabled, image_filename=self.button_images[key]["inactive"], key=key)

    def get_layout(self):
        return [[button] for _, button in self.buttons.items()]

    def activate_button(self, event):
        if event in self.buttons:
            for key, button in self.buttons.items():
                images = self.button_images[key]
                image = images["active"] if key == event else images["inactive"]
                button.update(image_filename=image)
        pass


    def process_event(self, window, event, values):

        if event == uk.SELECT_ADD_RECTANGLE:
            self.selected_tool = AddRectangleTool()
            self.activate_button(event)
        elif event == uk.SELECT_ADD_OVAL:
            self.selected_tool = AddOvalTool()
            self.activate_button(event)
        elif event == uk.SELECT_ADD_POINT:
            self.selected_tool = AddPointTool()
            self.activate_button(event)
        elif event == uk.SELECT_REMOVE_LABEL:
            w, h = window[uk.IMAGE_GRAPH].get_size()
            self.selected_tool = RemoveLabelTool(self.api, w, h)
            self.activate_button(event)

        if event.startswith(uk.IMAGE_GRAPH):
            point = values[uk.IMAGE_GRAPH]
            self.selected_tool.process(event, point)

        if event.startswith("Return"):
            image_graph: sg.Graph = window[uk.IMAGE_GRAPH]

            w, h = image_graph.get_size()
            marker_state:dict = self.selected_tool.commit_current_state(w, h)
            selected_class = values[uk.CLASSES_LISTBOX]

            if marker_state is not None and selected_class is not None and len(selected_class) == 1:
                marker_state.update({"class": selected_class[0]})
                self.api.add_marker_for_current_file(marker_state)
                self.api.save_marker_file()
        pass

