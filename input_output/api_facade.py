from input_output.argument_parser import ApplicationSettings
from input_output.event_management import EventManager
from input_output.image_management import ImageManager
from input_output.marker_management import MarkerManager
from input_output.project_management import ProjectManager


class ManagerFacade:
    def __init__(self, app_settings: ApplicationSettings) -> None:
        super().__init__()

        self._project_manager = ProjectManager(app_settings.project_folder())
        self._project_manager.load_project()

        self._image_manager = ImageManager(self._project_manager.data_path())
        self._marker_manager = MarkerManager(self._project_manager.class_labels_path())
        self._event_manager = EventManager(self._project_manager.event_labels_path())

    def project_folder(self):
        return self._project_manager.project_folder

    def add_marker_for_current_file(self, marker_state):
        self._marker_manager.add_marker_for_file(self._image_manager.current_filename(), marker_state)

    def save_marker_file(self):
        self._marker_manager.save()

    def total_images(self):
        return self._image_manager.total_images()
        pass

    def next_image(self, resize_size=None):
        return self._image_manager.next_image(resize_size)

    def current_filename(self):
        return self._image_manager.current_filename()

    def class_list_path(self):
        return self._project_manager.class_list_path()

    def current_image_idx(self):
        return self._image_manager.current_image_idx()

    def previous_image(self, resize_size=None):
        return self._image_manager.previous_image(resize_size)

    def get_image(self, selected_location, resize_size: tuple = None):
        return self._image_manager.get_image(selected_location, resize_size)

    def draw_markers_to_graph(self, graph):
        self._marker_manager.draw(graph, self.current_filename())

    def remove_marker_at(self, point):
        self._marker_manager.remove_marker_for_file_at(self.current_filename(), point)

    def event_list_path(self):
        return self._project_manager.event_list_path()

    def insert_event(self, group_name, event_name):
        success = self._event_manager.add_event_for_file(self.current_filename(), group_name, event_name)
        if success:
            self.save_events_file()
        return success

    def save_events_file(self):
        self._event_manager.save()

    def remove_event(self, group_name, event_name):
        success = self._event_manager.remove_event_for_file(self.current_filename(), group_name, event_name)
        if success:
            self.save_events_file()
        return success

    def get_event_table(self):
        return self._event_manager.get_event_table_for_file(self.current_filename())

    def current_version_string(self):
        return "1.0.0"

    def get_annotated_classes(self):
        res = list(set([item["class"] for elem in [v for _, v in self._marker_manager.markers.items()] for item in elem]))
        return sorted(res)

    def file_iterator(self):
        def iterator():
            for k, v in self._marker_manager.markers.items():
                yield k, v
        return iterator
