from pathlib import Path
import yaml


class SourceCategories:
    def __init__(self, path: str = "config/source_categories.yaml"):
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        self.tech = data.get("tech_sources", [])
        self.exec = data.get("exec_sources", [])
    