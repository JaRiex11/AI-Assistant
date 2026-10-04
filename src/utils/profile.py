from pathlib import Path
import yaml


class ProfileLoader:
    def __init__(self, path: str = "config/profile.yaml"):
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        self.active = data["active"]
        self.profile = data["profiles"][self.active]

    @property
    def audience(self) -> str:
        """security → tech, management → exec."""
        return "tech" if self.active == "security" else "exec"