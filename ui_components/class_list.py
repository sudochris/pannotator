import PySimpleGUI as sg
import json as json

from input_output.api_facade import ManagerFacade
from ui_components.component import UIComponent

import ui_keys as uk

class ClassList(UIComponent):
    def __init__(self, api: ManagerFacade) -> None:
        super().__init__()
        self.api = api
        self.class_list_path = self.api.class_list_path()

        class_list = self._load_class_list_from_file(self.class_list_path)

        self.listbox = sg.Listbox(class_list,
                        key=uk.CLASSES_LISTBOX,
                        select_mode=sg.SELECT_MODE_SINGLE,
                        size=(100, 20))

        self.inputbox = sg.Input("", key=uk.CLASSES_INPUT_CLASS)
        self._save_class_list_to_file(self.class_list_path, self.listbox.get_list_values())

    def _load_class_list_from_file(self, file_path):
        with open(file_path, 'r') as file:
            result:dict = json.load(file)
        return result.get("classList", [])

    def _save_class_list_to_file(self, file_path, class_list):
        with open(file_path, 'w') as file:
            json.dump({"classList": class_list}, file)

    def get_layout(self):
        return [
            [self.listbox],
            [sg.Text("Classname:"), self.inputbox],
            [sg.Button("+", key=uk.CLASSES_ADD_CLASS),
             sg.Button("-", key=uk.CLASSES_REMOVE_CLASS),
             sg.Button("Clear All", key=uk.CLASSES_REMOVE_ALL_CLASSES)]
        ]

    def process_event(self, window, event, values):

        if event == uk.CLASSES_ADD_CLASS:
            new_classname = values[uk.CLASSES_INPUT_CLASS]
            new_class_list = self.listbox.get_list_values()
            if new_classname != "" and new_classname not in new_class_list:
                self.inputbox.update("")
                new_class_list.append(new_classname)
                self.listbox.update(new_class_list)
                self._save_class_list_to_file(self.class_list_path, self.listbox.get_list_values())

        if event == uk.CLASSES_REMOVE_CLASS:
            selected_values = values[uk.CLASSES_LISTBOX]
            new_class_list = self.listbox.get_list_values()
            for selected_value in selected_values:
                new_class_list.remove(selected_value)

            self.listbox.update(new_class_list)
            self._save_class_list_to_file(self.class_list_path, self.listbox.get_list_values())

        if event == uk.CLASSES_REMOVE_ALL_CLASSES:
            res = sg.popup_yes_no("Do you want to remove all classes?", title="Confirm")
            if res == "Yes":
                self.listbox.update([])
                self._save_class_list_to_file(self.class_list_path, self.listbox.get_list_values())

        pass
