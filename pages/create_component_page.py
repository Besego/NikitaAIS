# create_component_page.py
import flet as ft
from styles.colors import (
    TEXT,
    LIGHT_BLUE,
    MEDIUM_BLUE,
    DARK_BLUE,
    WHITE,
    VERY_LIGHT_BLUE,
)
from db import db_manager
from models.models import Component


def create_component_view(page: ft.Page):
    # --- Проверка авторизации ---
    user_id = page.session.get("user_id")
    if not user_id:
        # Если пользователь не авторизован, перенаправляем на страницу входа
        page.go("/login")
        # Возвращаем пустой View, чтобы избежать рендеринга до перенаправления
        return ft.View("/create_component", [])

    # --- Элементы управления ---
    name_field = ft.TextField(label="Название", width=300, border_color=MEDIUM_BLUE)
    description_field = ft.TextField(
        label="Описание", multiline=True, width=300, border_color=MEDIUM_BLUE
    )
    quantity_field = ft.TextField(
        label="Количество",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300,
        border_color=MEDIUM_BLUE,
    )
    price_field = ft.TextField(
        label="Цена",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300,
        border_color=MEDIUM_BLUE,
    )
    error_text = ft.Text(color=ft.colors.RED)
    success_text = ft.Text(color=ft.colors.GREEN)

    def create_component_click(e):
        error_text.value = ""
        success_text.value = ""
        name = name_field.value
        description = description_field.value
        quantity_str = quantity_field.value
        price_str = price_field.value

        if not all([name, quantity_str, price_str]):
            error_text.value = "Пожалуйста, заполните все обязательные поля (Название, Количество, Цена)."
            page.update()
            return

        try:
            quantity = int(quantity_str)
            price = float(price_str)
            if quantity <= 0 or price <= 0:
                raise ValueError(
                    "Количество и цена должны быть положительными числами."
                )
        except ValueError as ve:
            error_text.value = f"Ошибка ввода: {ve}"
            page.update()
            return

        # Вызов метода для создания компонента
        new_component = db_manager.create_component(
            user_id=user_id,
            name=name,
            description=description,
            quantity=quantity,
            price=price,
        )

        if new_component:
            success_text.value = f"Комплектующее '{name}' успешно добавлено!"
            # Очистка полей
            name_field.value = ""
            description_field.value = ""
            quantity_field.value = ""
            price_field.value = ""
        else:
            error_text.value = "Произошла ошибка при добавлении комплектующего."

        page.update()

    def go_back(e):
        page.go(f"/user/{user_id}")  # Возвращаемся на страницу пользователя

    return ft.View(
        "/create_component",
        [
            ft.AppBar(
                title=ft.Text("Добавить комплектующее", color=WHITE),
                bgcolor=DARK_BLUE,
                leading=ft.IconButton(
                    ft.icons.ARROW_BACK,
                    tooltip="Назад",
                    on_click=go_back,
                    icon_color=WHITE,
                ),
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Введите данные нового комплектующего:",
                            size=18,
                            color=DARK_BLUE,
                        ),
                        name_field,
                        description_field,
                        quantity_field,
                        price_field,
                        ft.ElevatedButton(
                            "Добавить",
                            on_click=create_component_click,
                            style=ft.ButtonStyle(
                                bgcolor=MEDIUM_BLUE,
                                color=VERY_LIGHT_BLUE,
                            ),
                        ),
                        error_text,
                        success_text,
                    ],
                    spacing=15,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
                alignment=ft.alignment.center,
                expand=True,
            ),
        ],
        bgcolor=VERY_LIGHT_BLUE,
        padding=0,
    )
