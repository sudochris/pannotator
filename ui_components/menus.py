import PySimpleGUI as sg

from input_output.api_facade import ManagerFacade
from ui_components.component import UIComponent
import ui_keys as uk
from os import path as path
import os
import numpy as np

class MainMenu(UIComponent):

    def __init__(self, api: ManagerFacade) -> None:
        super().__init__()
        self.api = api
        self.export_window = None

    def get_layout(self):
        return [
                ["File", [f"Save::{uk.MENU_FILE_SAVE}", f"Exit::{uk.MENU_FILE_EXIT}"]],
                ["Export", [f"YoloV4::{uk.MENU_EXPORT_YOLOV4}"]],
                ["Help", [f"About...::{uk.MENU_HELP_ABOUT}"]]]

    def process_event(self, window, event, values):

        if event.endswith(uk.MENU_HELP_ABOUT):
            sg.Popup("License GNU GPLv3",
                     f"Version: {self.api.current_version_string()}",
                     keep_on_top=True,
                     title="About PANNotator")

        if event.endswith(uk.MENU_FILE_SAVE):
            self.api.save_marker_file()
            self.api.save_events_file()

        if event.endswith(uk.MENU_EXPORT_YOLOV4):
            export_path = sg.PopupGetFolder("Exportpath", "Select ExportPath",
                                       default_path=self.api.project_folder())

            obj_names_file = path.join(export_path, "obj.names")
            obj_data_file = path.join(export_path, "obj.data")
            data_folder = path.join(export_path, "data")
            obj_folder = path.join(data_folder, "obj")
            train_txt_file = path.join(data_folder, "train.txt")
            valid_txt_file = path.join(data_folder, "valid.txt")
            backup_folder = "backup/"
            annotated_classes = self.api.get_annotated_classes()
            num_classes = len(annotated_classes)
            class_idx_from_name = lambda name: annotated_classes.index(name) if name in annotated_classes else -1

            # 1. yolo-obj.cfg
            print(R"yolo-obj.cfg not implementd yet. See:"
                  R"https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects"
                  R"for instructions")
            # 2. obj.names
            with open(obj_names_file, 'w') as file:
                file.writelines("\n".join(annotated_classes))

            # 3. obj.data
            obj_data_lines = [
                f"classes={num_classes}",
                f"train={train_txt_file}",
                f"valid={valid_txt_file}",
                f"names={obj_names_file}",
                f"backup={backup_folder}"
            ]
            with open(obj_data_file, 'w') as file:
                file.writelines("\n".join(obj_data_lines))

            # 4. put images in data/obj
            os.makedirs(path.join(export_path, "data", "obj"), exist_ok=True)

            # 5. create marker txt files for images
            iterator = self.api.file_iterator()
            for img_filename, marker_list in iterator():
                base_filename = img_filename[:-4]
                txt_file = path.join(obj_folder, f"{base_filename}.txt")
                txt_rows = []
                for marker in marker_list:
                    class_idx = class_idx_from_name(marker["class"])
                    if marker["type"] in ["RECTANGLE", "OVAL"]:
                        x, y, w, h = marker["def"]
                        x_center = x + (w / 2)
                        y_center = y + (h / 2)

                    else:
                        x_center, y_center = marker["def"]
                        w, h = 0.03, 0.06 # approx 64x64 on full hd

                    width = w
                    height = h
                    txt_rows.append(f"{class_idx} {x_center} {y_center} {width} {height}")

                with open(txt_file, 'w') as file:
                    file.writelines("\n".join(txt_rows))

            # 6. Test / train split
            train_split = 0.8 # 80% training data
            iterator = self.api.file_iterator()
            train_files, valid_files = [], []

            for img_filename, marker_list in iterator():
                if np.random.rand() < train_split:
                    train_files.append(img_filename)
                else:
                    valid_files.append(img_filename)

            with open(train_txt_file, 'w') as file:
                file.write("\n".join([f"{path.join(obj_folder, line)}" for line in train_files]))

            with open(valid_txt_file, 'w') as file:
                file.writelines("\n".join([f"{path.join(obj_folder, line)}" for line in valid_files]))

            sg.PopupOK("Export finished.",
                       "",
                       "Next steps:",
                       "1. Move images to data/obj/",
                       "2. Create yolo-obj.cfg",
                       "3. Start training", title="Export")