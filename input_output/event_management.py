import json as json

class EventManager:
    def __init__(self, labels_path) -> None:
        super().__init__()
        self.labels_path = labels_path
        self.labels: dict = self._load_from_file(self.labels_path)

    def save(self):
        self._save_to_file(self.labels_path)

    def _save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.labels, file)

    def add_event_for_file(self, image_filename, eventgroup, event):
        if eventgroup in self.labels.get(image_filename, {}):
            if event == self.labels.get(image_filename, {}).get(eventgroup, ""):
                return False

        events = self.labels.get(image_filename, {})
        events.update({eventgroup: event})
        self.labels.update({image_filename: events})

        return True

    def remove_event_for_file(self, image_filename, eventgroup, event):
        if eventgroup in self.labels.get(image_filename, {}):
            if event == self.labels.get(image_filename, {}).get(eventgroup, ""):
                self.labels.update({image_filename: {k: v for k, v in self.labels.get(image_filename, {}).items() if v != event}})
                return True

        return False

    def get_event_table_for_file(self, image_filename):
        result = self.labels.get(image_filename, {})
        if len(result) > 0:
            return [[k, v] for k, v in result.items()]
        return [["", ""]] # empty row

    def _load_from_file(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)

        return data
