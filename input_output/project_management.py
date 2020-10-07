from os import path
import PySimpleGUI as sg
import json as json


class ProjectManager:
    def __init__(self, project_folder) -> None:
        super().__init__()
        self.project_folder = project_folder
        self.project_file = path.join(self.project_folder, "projectPaths.json")

    def _create_empty_json_file(self, path):
        with open(path, 'w') as file:
            file.write("{}")

    def _setup_project_file(self) -> dict:
        if not path.exists(self.project_file):
            self._create_empty_json_file(self.project_file)
            sg.popup_timed("No project file found."
                           "\nCreated new project in {}".format(self.project_folder),
                           auto_close_duration=3,
                           button_type=sg.POPUP_BUTTONS_NO_BUTTONS,
                           no_titlebar=True,
                           background_color="black",
                           text_color="white")

        with open(self.project_file) as file:
            try:
                project_data:dict = json.load(file)
            except:
                return {}


        return project_data

    def save_project(self):
        with open(self.project_file, 'w') as file:
            json.dump(self.project_data, file)

    def data_path(self):
        return self.project_data.get("data_path")

    def class_labels_path(self):
        return  self.project_data.get("class_labels_path")

    def event_labels_path(self):
        return  self.project_data.get("event_labels_path")

    def class_list_path(self):
        return self.project_data.get("class_list_path")

    def event_list_path(self):
        return self.project_data.get("event_list_path")

    def load_project(self):
        self.project_data = self._setup_project_file()

        if self.data_path() is None:
            selected_folder = sg.popup_get_folder("Select data folder", "Missing data folder", self.project_folder)
            self.project_data["data_path"] = selected_folder
        if self.class_list_path() is None:
            self.project_data["class_list_path"] = path.abspath(path.join(self.project_folder, "classList.json"))
            self._create_empty_json_file(self.class_list_path())
        if self.class_labels_path() is None:
            self.project_data["class_labels_path"] = path.abspath(path.join(self.project_folder, "classLabels.json"))
            self._create_empty_json_file(self.class_labels_path())
        if self.event_list_path() is None:
            self.project_data["event_list_path"] = path.abspath(path.join(self.project_folder, "eventList.json"))
            self._create_empty_json_file(self.event_list_path())
        if self.event_labels_path() is None:
            self.project_data["event_labels_path"] = path.abspath(path.join(self.project_folder, "eventLabels.json"))
            self._create_empty_json_file(self.event_labels_path())

        self.save_project()

