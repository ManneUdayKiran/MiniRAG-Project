import json
import os

KB_INDEX_PATH = os.path.join(os.path.dirname(__file__), "kb_index.json")

class KBIndex:
    def __init__(self):
        self.data = {"files": [], "urls": []}
        self.load()

    def load(self):
        if os.path.exists(KB_INDEX_PATH):
            with open(KB_INDEX_PATH, "r", encoding="utf-8") as f:
                self.data = json.load(f)

    def save(self):
        with open(KB_INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def add_file(self, filename):
        if filename not in self.data["files"]:
            self.data["files"].append(filename)
            self.save()

    def remove_file(self, filename):
        if filename in self.data["files"]:
            self.data["files"].remove(filename)
            self.save()

    def add_url(self, url):
        if url not in self.data["urls"]:
            self.data["urls"].append(url)
            self.save()

    def remove_url(self, url):
        if url in self.data["urls"]:
            self.data["urls"].remove(url)
            self.save()

    def get_files(self):
        return list(self.data["files"])

    def get_urls(self):
        return list(self.data["urls"])

kb_index = KBIndex()
