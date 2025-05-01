import time
import random
import threading


class Buyer:
    def __init__(self, sale_manager, user_id, components, interval):
        """Инициализация покупателя.
        """
        self.sale_manager = sale_manager
        self.user_id = user_id
        self.components = components
        self.interval = interval
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
            else:
                print("Не удалось совершить покупку.")
        else:
            print(f"Комплектующее {component.name} не в наличии.")
