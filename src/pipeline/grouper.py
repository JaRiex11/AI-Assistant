from src.models.publication import Publication


# Порядок разделов в дайджесте. Изменяется здесь — влияет на вывод.
SECTION_ORDER = ["Атака", "Уязвимость", "Инфо"]

SECTION_TITLES = {
    "Атака": "🔴 Атаки",
    "Уязвимость": "🟡 Уязвимости",
    "Инфо": "🔵 Новости",
}


def group_by_type(pubs: list[Publication]) -> dict[str, list[Publication]]:
    """
    Раскладывает публикации по типу с сортировкой по impact_score
    (от высокого к низкому). Игнорирует публикации без type
    и с rejection_reason (упавшие при классификации).
    """
    # 1. Фильтруем: оставляем только успешно классифицированные
    valid = [
        p for p in pubs
        if p.type in SECTION_ORDER and not p.rejection_reason
    ]

    # 2. Группируем по типу
    groups: dict[str, list[Publication]] = {t: [] for t in SECTION_ORDER}
    for pub in valid:
        groups[pub.type].append(pub)

    # 3. Сортируем внутри каждой группы по impact_score (по убыванию)
    for t in groups:
        groups[t].sort(key=lambda p: p.impact_score or 0, reverse=True)

    return groups