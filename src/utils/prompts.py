from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined


class PromptLoader:
    def __init__(self, prompts_dir: str = "prompts"):
        self.env = Environment(
            loader=FileSystemLoader(prompts_dir),
            undefined=StrictUndefined,       # ошибка, если переменная не передана
            trim_blocks=True,                 # убрать перенос после {% %}
            lstrip_blocks=True,               # убрать отступы перед {% %}
        )

    def render(self, name: str, **kwargs) -> str:
        return self.env.get_template(name).render(**kwargs)