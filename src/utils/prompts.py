from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined


class PromptLoader:
    def __init__(self, prompts_dir: str = "prompts"):
        # корень проекта: src/utils/prompts.py → parents[2]
        project_root = Path(__file__).resolve().parents[2]
        templates_path = project_root / prompts_dir

        # быстрая проверка, что папка реально существует — 
        # иначе Jinja2 упадёт позже с менее понятной ошибкой
        if not templates_path.is_dir():
            raise FileNotFoundError(
                f"Папка с промптами не найдена: {templates_path}"
            )

        self.env = Environment(
            loader=FileSystemLoader(str(templates_path)),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, name: str, **kwargs) -> str:
        return self.env.get_template(name).render(**kwargs)