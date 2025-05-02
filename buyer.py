import time
import random
import threading
import flet as ft

class Buyer:
    def __init__(self, sale_manager, user_id, components, interval, page):
        """Инициализация покупателя.

        Args:
            sale_manager: Объект менеджера продаж.
            user_id: ID пользователя, у которого покупают.
            components: Список комплектующих для покупки.
            interval: Интервал между покупками в секундах.
            page: Объект страницы Flet для обновления UI.
            buyer_name: Имя покупателя (по умолчанию "Покупатель").
        """
        self.sale_manager = sale_manager
        self.user_id = user_id
        self.components = components
        self.interval = interval
        self.page = page  # Для обновления UI
        self.buyer_names = [
            "Геральт из Ривии",
            "Лара Крофт",
            "Кратос",
            "Мастер Чиф",
            "Том Рейдер",
            "Элли",
            "Натан Дрейк",
            "Соник",
            "Марио",
            "Луиджи",
            "Покемон",
            "Пикачу",
            "Супермен",
            "Бэтмен",
            "Человек-паук",
            "Железный человек",
            "Капитан Америка",
            "Тор",
            "Халк",
            "Чудо-женщина",
            "Бэтгерл",
            "Робин",
            "Флэш",
            "Зелёная стрела",
            "Аквамен",
            "Человек-муравей",
            "Человек-факел",
            "Дэдпул",
            "Веном",
            "Доктор Стрэндж",
            "Локи",
            "Танос",
            "Гарри Поттер",
            "Гермиона Грейнджер",
            "Рон Уизли",
            "Дамблдор",
            "Снегг",
            "Волдеморт",
            "Хагрид",
            "Луна Лавгуд",
            "Невилл Долгопупс",
            "Сириус Блэк",
            "Ремус Люпин",
            "Долорес Амбридж",
            "Драко Малфой",
            "Гринготтс",
            "Грюм",
            "Снегг",
            "Люциус Малфой",
            "Беллатрикс Лестрейндж",
            "Нарцисса Малфой",
            "Гринготтс",
        ]
        self.running = False
        self.thread = None

    def start_buying(self):
        """Запуск процесса периодических покупок в отдельном потоке."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._buy_loop)
            self.thread.start()

    def stop_buying(self):
        """Остановка процесса покупок."""
        self.running = False
        if self.thread:
            self.thread.join()

    def _buy_loop(self):
        """Цикл покупок, выполняющийся в отдельном потоке."""
        while self.running:
            self._make_purchase()
            time.sleep(self.interval)

    def _make_purchase(self):
        """Выполнение одной покупки."""
        if not self.components:
            print("Нет комплектующих для покупки.")
            return

        # Выбираем случайное комплектующее
        component = random.choice(self.components)

        # Проверяем наличие
        if component.quantity > 0:
            # Покупаем 1 единицу
            quantity = 1
            sale = self.sale_manager.create_sale(
                component.component_id, self.user_id, quantity
            )
            if sale:
                print(f"Куплено: {quantity} x {component.name}")
                # Показываем уведомление о покупке
                self._show_purchase_notification(component, quantity)
            else:
                print("Не удалось совершить покупку.")
        else:
            print(f"Комплектующее {component.name} не в наличии.")

    def _show_purchase_notification(self, component, quantity):
        """Показывает уведомление о совершенной покупке."""
        total_price = component.price * quantity
        message = f"{self.buyer_names[random.randint(0,len(self.buyer_names)-1)]} купил: {quantity} x {component.name} за {total_price:.2f}"
        snack_bar = ft.SnackBar(content=ft.Text(message))
        self.page.open(snack_bar)
        self.page.update()