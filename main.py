import argparse
import asyncio

from src.utils.profile import ProfileLoader
from src.pipeline.orchestrator import run_full_pipeline
from src.pipeline.exporter import Exporter


async def cli_daily(audience: str):
    markdown, stats = await run_full_pipeline(audience=audience)

    exporter = Exporter()
    path = exporter.save(markdown, audience=audience)
    exporter.update_index()

    print(f"✅ {path}")
    print(f"Собрано: {stats.collected} | "
          f"После дедупа: {stats.after_dedup} | "
          f"После фильтра: {stats.after_relevance} | "
          f"В дайджесте: {stats.final}")


def main():
    parser = argparse.ArgumentParser(description="Генератор ИТ/ИБ дайджестов")
    parser.add_argument("--audience", "-a", choices=["tech", "exec"], default=None)
    parser.add_argument("--monthly", "-m", action="store_true")
    parser.add_argument("--days", "-d", type=int, default=30)
    args = parser.parse_args()

    if args.audience is None:
        audience = ProfileLoader("config/profile.yaml").audience
    else:
        audience = args.audience

    if args.monthly:
        from src.pipeline.monthly import MonthlyDigest
        from src.providers.ollama import OllamaProvider
        from src.utils.prompts import PromptLoader

        llm = OllamaProvider(
            model="gpt-oss:120b-cloud",
            config={"temperature": 0, "seed": 42},
        )
        monthly = MonthlyDigest("output")
        path = asyncio.run(
            monthly.build(
                audience=audience,
                llm=llm,
                loader=PromptLoader("prompts"),
                days=args.days,
            )
        )
        if path:
            print(f"✅ Месячный дайджест: {path}")
        else:
            print("⚠️ Дайджестов за период не найдено")
        return

    asyncio.run(cli_daily(audience))


if __name__ == "__main__":
    main()