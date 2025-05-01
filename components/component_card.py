import flet as ft
from styles.colors import PINK_LIGHT, YELLOW_LIGHT, TEXT, PINK_MEDIUM, PINK_DARK


class ComponentCard:
    def __init__(self, component_name, quantity, price):
        super().__init__()
        self.component_name = component_name
        self.quantity = quantity
        self.price = price

    # def _get_control_name(
    #     self,
    # ):
    #     return self.__repr__()

    def build(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.COMPUTER, color=PINK_DARK),
                            title=ft.Text(
                                self.component_name,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT,
                            ),
                            subtitle=ft.Text(
                                f"Количество: {self.quantity}\nЦена: {self.price:.2f} руб.",
                                color=TEXT,
                            ),
                        ),
                        # Можно добавить кнопки действий сюда, если нужно
                        # ft.Row(
                        #     [ft.TextButton("Действие 1"), ft.TextButton("Действие 2")],
                        #     alignment=ft.MainAxisAlignment.END,
                        # ),
                    ]
                ),
                width=280,  # Фиксированная ширина для единообразия
                padding=10,
                border_radius=ft.border_radius.all(10),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[PINK_LIGHT, YELLOW_LIGHT],
                ),
            ),
            elevation=4,
            margin=5,
        )
