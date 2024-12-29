import os
import sys
from dotenv import load_dotenv, find_dotenv
import panel as pn

pn.extension()


class Utils:
    def __init__(self):
        pass

    def get_dlai_api_key(self):
        _ = load_dotenv(find_dotenv())
        return os.getenv("DLAI_API_KEY")

    def get_dlai_url(self):
        _ = load_dotenv(find_dotenv())
        return os.getenv("DLAI_API_URL")


class upld_file:
    def __init__(self):
        self.widget_file_upload = pn.widgets.FileInput(
            accept=".pdf,.ppt,.png,.html,.jpg", multiple=False
        )
        self.widget_file_upload.param.watch(self.save_filename, "filename")

    def save_filename(self, _):
        if len(self.widget_file_upload.value) > 2e6:
            print("file too large. 2 M limit")
        else:
            self.widget_file_upload.save(
                "./example_files/" + self.widget_file_upload.filename
            )
        # print(f"filename_ = {self.widget_file_upload.filename}")
        # print(f"length of value {len(self.widget_file_upload.value)}")
