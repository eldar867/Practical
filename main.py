class CoffeeOrder:
    # Константы, лимиты
    ALLOWED_BASES = ("espresso", "americano", "latte", "cappuccino")
    ALLOWED_SIZES = ("small", "medium", "large")
    ALLOWED_MILKS = ("none", "whole", "skim", "oat", "soy")

    BASE_PRICES = {"espresso": 200.0, "americano": 250.0, "latte": 300.0, "cappuccino": 320.0}
    SIZE_MULTIPLIERS = {"small": 1.0, "medium": 1.2, "large": 1.4}
    MILK_PRICES = {"none": 0.0, "whole": 30.0, "skim": 30.0, "oat": 60.0, "soy": 50.0}
    SYRUP_PRICE = 40.0
    ICED_COEFF = 0.2  # фиксированный коэффициент 0.2 к базовой стоимости при iced=True
    MAX_SYRUPS = 4
    MAX_SUGAR = 5

    def __init__(
        self,
        base: str,
        size: str,
        milk: str = "none",
        syrups: tuple[str, ...] = (),
        sugar: int = 0,
        iced: bool = False,
    ) -> None:
        # Валидация входных данных
        if not base or base not in self.ALLOWED_BASES:
            raise ValueError(f"Недопустимая основа: '{base}'. Допустимые: {self.ALLOWED_BASES}")
        if not size or size not in self.ALLOWED_SIZES:
            raise ValueError(f"Недопустимый размер: '{size}'. Допустимые: {self.ALLOWED_SIZES}")
        if milk not in self.ALLOWED_MILKS:
            raise ValueError(f"Недопустимый тип молока: '{milk}'. Допустимые: {self.ALLOWED_MILKS}")
        if not (0 <= sugar <= self.MAX_SUGAR):
            raise ValueError(f"Количество сахара должно быть в диапазоне 0-{self.MAX_SUGAR}")
        if len(syrups) > self.MAX_SYRUPS:
            raise ValueError(f"Превышен лимит сиропов. Максимум: {self.MAX_SYRUPS}")

        self.base: str = base
        self.size: str = size
        self.milk: str = milk
        self.syrups: tuple[str, ...] = tuple(syrups)
        self.sugar: int = sugar
        self.iced: bool = iced

        # Расчет цены и описания выполняется в самом конце инициализации
        self.price: float = self._calculate_price()
        self.description: str = self._generate_description()

    def _calculate_price(self) -> float:
        base_cost = self.BASE_PRICES[self.base] * self.SIZE_MULTIPLIERS[self.size]
        milk_cost = self.MILK_PRICES[self.milk]
        syrup_cost = len(self.syrups) * self.SYRUP_PRICE
        iced_cost = base_cost * self.ICED_COEFF if self.iced else 0.0
        return round(base_cost + milk_cost + syrup_cost + iced_cost, 2)

    def _generate_description(self) -> str:
        parts: list[str] = [f"{self.size} {self.base}"]
        if self.milk != "none":
            parts.append(f"with {self.milk} milk")
        if self.syrups:
            parts.append(", ".join(f"+{s}" for s in self.syrups))
        if self.iced:
            parts.append("(iced)")
        if self.sugar > 0:
            parts.append(f"{self.sugar} tsp sugar")
        return " ".join(parts)

    def __str__(self) -> str:
        return self.description or f"Order price: {self.price}"


if __name__ == "__main__":
    print("Создание базового заказа")
    order = CoffeeOrder(
        base="latte",
        size="medium",
        milk="oat",
        syrups=("vanilla", "caramel"),
        sugar=2,
        iced=True
    )

    # 1. Проверка правильности типов
    assert isinstance(order.base, str), "base должен быть строкой"
    assert isinstance(order.size, str), "size должен быть строкой"
    assert isinstance(order.milk, str), "milk должен быть строкой"
    assert isinstance(order.syrups, tuple), "syrups должен быть кортежем"
    assert isinstance(order.sugar, int), "sugar должен быть целым числом"
    assert isinstance(order.iced, bool), "iced должен быть булевым значением"
    assert isinstance(order.price, float), "price должен быть вещественным числом"
    print("Типы всех полей корректны")

    # 2. Проверка непустой цены
    assert order.price > 0, "Цена должна быть строго положительной"
    print(f"Цена успешно рассчитана: {order.price}")

    # 3. Наличие опций в объекте заказа
    assert order.milk == "oat"
    assert order.syrups == ("vanilla", "caramel")
    assert order.sugar == 2
    assert order.iced is True
    print("Опции сохранены и доступны через атрибуты")

    # 4. Проверка __str__ и description
    print(f"Description: {order.description}")
    print(f"str(order): {order}")

    # 5. Тестирование валидации (пустой base)
    try:
        CoffeeOrder(base="", size="small")
    except ValueError as e:
        print(f"Валидация пустого base: {e}")

    # 6. Тестирование валидации (недопустимый size)
    try:
        CoffeeOrder(base="espresso", size="xlarge")
    except ValueError as e:
        print(f"Валидация недопустимого size: {e}")

    # 7. Тестирование лимита сиропов
    try:
        CoffeeOrder(base="americano", size="large", syrups=("a", "b", "c", "d", "e"))
    except ValueError as e:
        print(f"Валидация лимита сиропов: {e}")

    print("\nВсе проверки пройдены успешно")