import cv2 as cv
import os
from os import path

class ImageManager:

    def __init__(self, image_data_folder) -> None:
        super().__init__()
        extensions = (".jpg", ".jpeg", ".png")
        self.image_data_folder = image_data_folder
        self.file_list = sorted([file for file in os.listdir(image_data_folder) if file.endswith(extensions)])
        self._current_image_idx = 0

    def _read(self, image_idx, resize_size):
        filename = self.file_list[image_idx]
        full_filename = path.join(self.image_data_folder, filename)
        image = cv.imread(full_filename)
        if resize_size is None:
            image = cv.resize(image, (1280, 768))
        else:
            image = cv.resize(image, resize_size)
        imgbytes = cv.imencode('.png', image)[1].tobytes()
        return filename, imgbytes

    def get_image(self, selected_image_idx, resize_size):
        if selected_image_idx < self.total_images():
            filename, image = self._read(selected_image_idx, resize_size)
            self._current_image_idx = selected_image_idx
            self._current_filename = filename

            return image

        self._current_image_idx = 0
        self._current_filename = ""

        return None

    def previous_image(self, resize_size):
        previous_image_idx = ((self._current_image_idx + self.total_images()) - 1) % self.total_images()
        return self.get_image(previous_image_idx, resize_size)

    def next_image(self, resize_size):
        next_image_index = (self._current_image_idx + 1 ) % self.total_images()
        return self.get_image(next_image_index, resize_size)

    def current_image_idx(self):
        return self._current_image_idx

    def current_filename(self):
        return self._current_filename

    def total_images(self):
        return len(self.file_list)

