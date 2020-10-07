import PySimpleGUI as sg
import json as json

from utils import utils


class MarkerManager:

    def __init__(self, labels_path) -> None:
        super().__init__()
        self.labels_path = labels_path
        self.markers: dict = self._load_from_file(self.labels_path)

    def save(self):
        self._save_to_file(self.labels_path)

    def _save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.markers, file)

    def add_marker_for_file(self, image_filename, marker):
        actual_marker_list = self.markers.get(image_filename, [])
        actual_marker_list.append(marker)
        self.markers.update({image_filename: actual_marker_list})

    def remove_marker_for_file_at(self, image_filename, position):
        actual_marker_list = self.markers.get(image_filename, [])

        clicked_elements = [marker for marker in actual_marker_list if
                            marker["type"] in ["RECTANGLE", "OVAL"] and
                            marker["def"][0] < position[0] < (marker["def"][0] + marker["def"][2]) and
                            marker["def"][1] < position[1] < (marker["def"][1] + marker["def"][3])]
        if len(clicked_elements) > 0:
            for element in clicked_elements:
                actual_marker_list.remove(element)
        else:
            # test for points
            clicked_elements = [marker for marker in actual_marker_list if
                                marker["type"] in ["POINT"] and
                                (marker["def"][0] - (32 / 1280)) < position[0] < (marker["def"][0] + (32 / 1280)) and
                                (marker["def"][1] - (32 / 768)) < position[1] < (marker["def"][1] + (32 / 768))]

            for element in clicked_elements:
                actual_marker_list.remove(element)

        self.markers.update({image_filename: actual_marker_list})

    def draw(self, overlay: sg.Graph, filename):
        markers = self.markers.get(filename, [])

        color = "#00ff00"
        ow, oh = overlay.get_size()
        for marker in markers:
            marker_type = marker.get("type", "None")
            marker_class = marker.get("class", "Unknown")

            if marker_type in ["RECTANGLE", "OVAL"]:
                marker_def = marker.get("def", [])
                x, y, w, h = marker_def
                tl = (x * ow, y * oh)
                br = ((x + w) * ow, (y + h) * oh)

                if marker_type == "RECTANGLE":
                    utils.draw_rectangle(overlay, tl, br, line_color=color, line_width=4)
                if marker_type == "OVAL":
                    utils.draw_oval(overlay, tl, br, line_color=color, line_width=4)
                overlay.draw_rectangle(tl, ((x + w * .75) * ow, (y * oh) + 16), line_color=color, fill_color=color)
                overlay.draw_text(marker_class, tl, text_location=sg.TEXT_LOCATION_TOP_LEFT)

            if marker_type in ["POINT"]:
                marker_def = marker.get("def", [])
                x, y = marker_def
                w, h = (32, 32)
                center = (x * ow, y * oh)
                tl = ((x * ow)-w, (y * oh)-h)

                utils.draw_cross(overlay, center, (w, h), "#00ff00", 4)
                overlay.draw_rectangle(tl, ((x + ((2*w)/ow) * .75) * ow, (y * oh) - h + 16), line_color=color, fill_color=color)
                overlay.draw_text(marker_class, tl, text_location=sg.TEXT_LOCATION_TOP_LEFT)

        pass

    def _load_from_file(self, filename):

        with open(filename, 'r') as file:
            data = json.load(file)

        return data
