import re
from datetime import datetime, timedelta
from pathlib import Path

from src.utils.prompts import PromptLoader
from src.providers.ollama import OllamaProvider


class MonthlyDigest:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)

    def _collect_digests(self, audience: str, days: int = 30) -> list[dict]:
        """Собирает все daily-дайджесты за последние N дней."""
        cutoff = datetime.now() - timedelta(days=days)
        digests = []

        # формат имени: digest_{audience}_YYYY-MM-DD_HH-MM.md
        pattern = re.compile(rf"digest_{audience}_(\d{{4}}-\d{{2}}-\d{{2}})_(\d{{2}}-\d{{2}})\.md$")

        for path in sorted(self.output_dir.glob(f"digest_{audience}_*.md")):
            match = pattern.search(path.name)
            if not match:
                continue    # пропускаем latest, monthly и прочее

            date_str = f"{match.group(1)} {match.group(2).replace('-', ':')}"
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            except ValueError:
                continue

            if dt < cutoff:
                continue

            digests.append({
                "date": dt.strftime("%Y-%m-%d"),
                "filename": path.name,
                "content": path.read_text(encoding="utf-8"),
                "dt": dt,
            })

        return digests

    async def build(
        self,
        audience: str,
        llm: OllamaProvider,
        loader: PromptLoader,
        days: int = 30,
    ) -> Path | None:
        digests = self._collect_digests(audience, days)
        if not digests:
            print(f"[monthly] нет дайджестов за {days} дней для '{audience}'")
            return None

        print(f"[monthly] собрано {len(digests)} дайджестов за {days} дней")

        first = digests[0]["dt"].strftime("%Y-%m-%d")
        last = digests[-1]["dt"].strftime("%Y-%m-%d")
        period = f"{first} — {last}"

        prompt = loader.render(
            "monthly_summary.jinja2",
            digests=digests,
            period=period,
        )

        print(f"[monthly] отправляем в LLM ({len(prompt)} символов)...")
        summary = await llm.complete(prompt)

        # сохраняем
        month_str = digests[-1]["dt"].strftime("%Y-%m")
        out_path = self.output_dir / f"digest_{audience}_monthly_{month_str}.md"
        out_path.write_text(summary, encoding="utf-8")
        print(f"[monthly] сохранено: {out_path}")

        return out_path