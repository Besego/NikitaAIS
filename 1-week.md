# 1.1 Задача линейного алгоритма
## Условие:
##### Два программиста вместе пишут код за 8 часов. Первый делает это на 12 часов быстрее второго. За сколько часов каждый напишет код отдельно?

#### решение:
```
def solve_coding_time():
    a, b, c = 1, -28, 96
    discriminant = b**2 - 4*a*c
    y1 = (-b + discriminant**0.5) / (2*a)
    y2 = (-b - discriminant**0.5) / (2*a)
    y = y1 if y1 > 12 else y2
    x = y - 12
    return x, y
x, y = solve_coding_time()
print(f"Первый программист: {x} часов")
print(f"Второй программист: {y} часов")
```

# 1.2 Задача разветвляющегося алгоритма
## Условие:
##### Проверка PIN-кода.
PIN должен состоять ровно из 4 или 6 цифр. Выведите "Valid" или "Invalid" (например, "1234" → Valid, "a234" → Invalid).

#### решение:
```
def check_pin(pin):
    if len(pin) != 4 and len(pin) != 6:
        return "Invalid"
    if not pin.isdigit():
        return "Invalid"
    return "Valid"
pin = input("Введите PIN-код: ")
print(check_pin(pin))
```

# 1.3 Задача циклического алгоритма
## Условие:
##### Арифметическая прогрессия. Выведите последовательность: начальное число A, шаг D, количество элементов N.

#### решение:
```
def arithmetic_progression(a, d, n):
    result = []
    for i in range(n):
        result.append(a + i * d)
    return result
a = int(input("Введите начальное число A: "))
d = int(input("Введите шаг D: "))
n = int(input("Введите количество элементов N: "))
sequence = arithmetic_progression(a, d, n)
print("Арифметическая прогрессия:", *sequence)
```

# 1.4 Задача на проектирование классов
## Условие:
##### Класс "Магазин".
Разработайте класс Store для управления товарами. Добавьте методы для добавления, удаления и обновления товаров.

#### решение:
```
class Store:
    def __init__(self):
        self.inventory = {}
    def add_product(self, product_id, name, price, quantity):
        if product_id in self.inventory:
            return "Товар с таким ID уже существует"
        self.inventory[product_id] = {"name": name, "price": price, "quantity": quantity}
        return "Товар успешно добавлен"
    def remove_product(self, product_id):
        if product_id not in self.inventory:
            return "Товар с таким ID не найден"
        del self.inventory[product_id]
        return "Товар успешно удалён"
    def update_product(self, product_id, name=None, price=None, quantity=None):
        if product_id not in self.inventory:
            return "Товар с таким ID не найден"
        if name is not None:
            self.inventory[product_id]["name"] = name
        if price is not None:
            self.inventory[product_id]["price"] = price
        if quantity is not None:
            self.inventory[product_id]["quantity"] = quantity
        return "Товар успешно обновлён"
    def get_inventory(self):
        return self.inventory
store = Store()
print(store.add_product(1, "Яблоки", 0.5, 100))
print(store.add_product(2, "Бананы", 0.8, 50))
print(store.update_product(1, quantity=150))
print(store.remove_product(2))
print(store.get_inventory())
```

# 1.5 Задача с графическим интерфейсом
## Условие:
##### Онлайн-магазин. 
##### Разработайте приложение для онлайн-магазина с графическим интерфейсом.

#### решение:
```
import flet as ft
class StoreApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Онлайн-магазин"
        self.cart = []
        self.products = [
            {"id": 1, "name": "Яблоки", "price": 0.5, "quantity": 100},
            {"id": 2, "name": "Бананы", "price": 0.8, "quantity": 50},
            {"id": 3, "name": "Апельсины", "price": 0.6, "quantity": 80},
        ]
        self.setup_ui()
    def setup_ui(self):
        self.page.views.clear()
        self.page.views.append(
            ft.View(
                route="/catalog",
                controls=[
                    ft.AppBar(title=ft.Text("Каталог товаров"), bgcolor=ft.colors.BLUE_200),
                    ft.Column(
                        controls=[self.create_product_card(product) for product in self.products],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),
                    ft.ElevatedButton("Перейти в корзину", on_click=self.go_to_cart),
                ]
            )
        )
        self.page.update()
    def create_product_card(self, product):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(product["name"], size=20, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Цена: ${product["price"]:.2f}"),
                        ft.Text(f"В наличии: {product["quantity"]}"),
                        ft.ElevatedButton(
                            "Купить",
                            on_click=lambda e: self.add_to_cart(product),
                            bgcolor=ft.colors.GREEN_200,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=10,
            ),
            elevation=5,
        )
    def add_to_cart(self, product):
        for item in self.cart:
            if item["id"] == product["id"]:
                if item["quantity"] < product["quantity"]:
                    item["quantity"] += 1
                return
        self.cart.append({"id": product["id"], "name": product["name"], "price": product["price"], "quantity": 1})
        self.page.snack_bar = ft.SnackBar(ft.Text(f"{product["name"]} добавлен в корзину!"))
        self.page.snack_bar.open = True
        self.page.update()
    def go_to_cart(self, e):
        self.page.views.append(
            ft.View(
                route="/cart",
                controls=[
                    ft.AppBar(title=ft.Text("Корзина"), bgcolor=ft.colors.BLUE_200),
                    ft.Column(
                        controls=self.create_cart_items(),
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),
                    ft.ElevatedButton("Оформить заказ", on_click=self.checkout, bgcolor=ft.colors.ORANGE_200),
                    ft.ElevatedButton("Вернуться в каталог", on_click=self.go_to_catalog),
                ]
            )
        )
        self.page.go("/cart")
    def create_cart_items(self):
        if not self.cart:
            return [ft.Text("Корзина пуста", size=20)]
        return [
            ft.Card(
                content=ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(f"{item["name"]} (x{item["quantity"]})", size=16),
                            ft.Text(f"${item["price"] * item["quantity"]:.2f}", size=16),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=10,
                ),
                elevation=3,
            )
            for item in self.cart
        ]
    def checkout(self, e):
        if not self.cart:
            self.page.snack_bar = ft.SnackBar(ft.Text("Корзина пуста!"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        self.cart.clear()
        self.page.snack_bar = ft.SnackBar(ft.Text("Заказ успешно оформлен!"))
        self.page.snack_bar.open = True
        self.page.views.pop()
        self.go_to_cart(None)
    def go_to_catalog(self, e):
        self.page.views.pop()
        self.page.go("/catalog")
def main(page: ft.Page):
    StoreApp(page)
ft.app(target=main)
```
