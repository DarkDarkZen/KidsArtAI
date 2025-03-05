def process_payment(user_id: int, amount: float) -> bool:
    """Обрабатывает платёж для пользователя. Возвращает True, если платёж успешен, иначе False."""
    # Заглушка: здесь должна быть интеграция с платежным сервисом
    print(f"Processing payment for user {user_id} of amount {amount}")
    return True


def get_tariff_options() -> dict:
    """Возвращает доступные тарифы."""
    tariffs = {
        'single': 100,         # 100 рублей за анализ 1 рисунка
        'monthly': 1000,       # 1000 рублей за месяц использования
        'yearly': 10000        # 10000 рублей за год использования
    }
    return tariffs


if __name__ == '__main__':
    # Пример использования функций
    options = get_tariff_options()
    print("Доступные тарифы:", options)
    result = process_payment(user_id=12345, amount=options['single'])
    if result:
        print("Платёж успешно обработан")
    else:
        print("Ошибка при обработке платежа") 