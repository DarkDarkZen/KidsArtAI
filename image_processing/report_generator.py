def generate_report(analysis: dict) -> str:
    """Генерирует подробный отчёт на основе анализа рисунка."""
    report = (
        f"Психологический возраст: {analysis.get('psychological_age', 'N/A')}\n"
        f"Уровень воображения: {analysis.get('imagination_level', 'N/A')}\n"
        f"Эмоциональный интеллект: {analysis.get('emotional_intelligence', 'N/A')}\n"
        f"Физическое состояние: {analysis.get('physical_condition', 'N/A')}\n"
        "Рекомендуется провести анализ нескольких рисунков для более точных выводов."
    )
    return report


if __name__ == '__main__':
    sample_analysis = {
        'psychological_age': 7,
        'imagination_level': 'средний',
        'emotional_intelligence': 'высокий',
        'physical_condition': 'хорошее'
    }
    print(generate_report(sample_analysis)) 