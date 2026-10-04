import asyncio
from src.pipeline.orchestrator import run_full_pipeline

async def main():
    markdown, stats = await run_full_pipeline(
        audience="tech",
        progress_callback=lambda stage: print(f"[stage] {stage}"),
    )
    print("---")
    print(f"Собрано: {stats.collected}")
    print(f"После дедупа: {stats.after_dedup}")
    print(f"После фильтра: {stats.after_relevance}")
    print(f"В дайджесте: {stats.final}")
    print("---")
    print(markdown[:500])

if __name__ == "__main__":
    asyncio.run(main())