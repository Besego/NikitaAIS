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
from components.component_card import ComponentCard
from models.models import (
    User,
    Sale,
    Component,
)  # Импортируем модели для типизации и доступа к данным
import datetime


def user_view(page: ft.Page, user_id_str: str):
    # --- Проверка авторизации --- (остается без изменений)
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        user_id = None
        if page.session.contains_key("user_id"):
            user_id = page.session.get("user_id")

    if not user_id:
        # Возвращаем View с сообщением о необходимости входа
        return ft.View(
            "/user",  # Маршрут для этого View
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Для доступа к этой странице необходимо войти в систему",
                                size=16,
                                color=DARK_BLUE,
                            ),
                            ft.ElevatedButton(
                                "Войти",
                                on_click=lambda _: page.go("/login"),
                                style=ft.ButtonStyle(
                                    bgcolor=MEDIUM_BLUE,
                                    color=VERY_LIGHT_BLUE,
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20,
                    expand=True,
                    alignment=ft.alignment.center,
                    bgcolor=VERY_LIGHT_BLUE,
                )
            ],
            bgcolor=VERY_LIGHT_BLUE,  # Устанавливаем фон для View
        )

    # --- Настройка страницы (перенесено в View) ---
    # page.padding = 0 # Управляется View
    # page.bgcolor = VERY_LIGHT_BLUE # Управляется View

    # --- Функции --- (остаются без изменений)
    def logout(e):
        page.session.remove("user_id")
        page.session.remove("user_name")
        page.session.remove("user_role")
        page.go("/login")

    def load_user_components(user_id):
        components = db_manager.get_components_by_user(user_id)
        cards = []
        if components:
            for comp in components:
                cards.append(
                    ComponentCard(
                        component_name=comp.name,
                        quantity=comp.quantity,
                        price=comp.price,
                    ).build()
                )
        else:
            cards.append(ft.Text("У вас пока нет комплектующих на складе.", color=TEXT))

        return ft.GridView(
            runs_count=5,
            max_extent=300,
            child_aspect_ratio=1.8,
            spacing=10,
            run_spacing=10,
            controls=cards,
            expand=True,
        )

    def load_user_ranking():
        users_ranking = db_manager.get_users_by_sales_count()
        rows = []
        if users_ranking:
            for rank, (user, sales_count) in enumerate(users_ranking, start=1):
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(rank), color=TEXT)),
                            ft.DataCell(ft.Text(user.username, color=TEXT)),
                            ft.DataCell(ft.Text(str(sales_count), color=TEXT)),
                        ]
                    )
                )
        else:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text("Нет данных о продажах.", color=TEXT, colspan=3)
                        )
                    ]
                )
            )

        return ft.DataTable(
            columns=[
                ft.DataColumn(
                    ft.Text("Место", weight=ft.FontWeight.BOLD, color=DARK_BLUE)
                ),
                ft.DataColumn(
                    ft.Text("Пользователь", weight=ft.FontWeight.BOLD, color=DARK_BLUE)
                ),
                ft.DataColumn(
                    ft.Text(
                        "Кол-во продаж", weight=ft.FontWeight.BOLD, color=DARK_BLUE
                    ),
                    numeric=True,
                ),
            ],
            rows=rows,
            expand=True,
            border=ft.border.all(1, MEDIUM_BLUE),
            border_radius=ft.border_radius.all(10),
            heading_row_color=LIGHT_BLUE,
            data_row_color={"hovered": MEDIUM_BLUE},
        )

    def load_sales_history(user_id):
        sales = db_manager.get_sales_by_user(user_id)
        rows = []
        if sales:
            for sale in sales:
                sale_date_str = (
                    sale.sale_date.strftime("%Y-%m-%d %H:%M")
                    if sale.sale_date
                    else "N/A"
                )
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(
                                    sale.component.name if sale.component else "N/A",
                                    color=TEXT,
                                )
                            ),
                            ft.DataCell(ft.Text(str(sale.quantity), color=TEXT)),
                            ft.DataCell(ft.Text(f"{sale.total_price:.2f}", color=TEXT)),
                            ft.DataCell(ft.Text(sale_date_str, color=TEXT)),
                        ]
                    )
                )
        else:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text("История продаж пуста.", color=TEXT, italic=True)
                        ),
                        ft.DataCell(ft.Text("")),  # Пустая ячейка для Кол-во
                        ft.DataCell(ft.Text("")),  # Пустая ячейка для Сумма
                        ft.DataCell(ft.Text("")),  # Пустая ячейка для Дата
                    ]
                )
            )

        return ft.DataTable(
            columns=[
                ft.DataColumn(
                    ft.Text("Комплектующее", weight=ft.FontWeight.BOLD, color=DARK_BLUE)
                ),
                ft.DataColumn(
                    ft.Text("Кол-во", weight=ft.FontWeight.BOLD, color=DARK_BLUE),
                    numeric=True,
                ),
                ft.DataColumn(
                    ft.Text("Сумма", weight=ft.FontWeight.BOLD, color=DARK_BLUE),
                    numeric=True,
                ),
                ft.DataColumn(
                    ft.Text("Дата", weight=ft.FontWeight.BOLD, color=DARK_BLUE)
                ),
            ],
            rows=rows,
            expand=True,
            border=ft.border.all(1, MEDIUM_BLUE),
            border_radius=ft.border_radius.all(10),
            heading_row_color=LIGHT_BLUE,
            data_row_color={"hovered": MEDIUM_BLUE},
        )

    # --- Компоненты UI --- (остаются без изменений)
    logout_button = ft.IconButton(
        icon=ft.icons.LOGOUT, tooltip="Выйти", on_click=logout, icon_color=DARK_BLUE
    )

    user_name = page.session.get("user_name") or "Пользователь"

    # AppBar создается здесь, но будет добавлен в View
    app_bar = ft.AppBar(
        title=ft.Text(f"Личный кабинет: {user_name}", color=TEXT),
        bgcolor=MEDIUM_BLUE,
        actions=[logout_button],
    )

    # Tabs создаются здесь и будут основным контентом View
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Мой склад",
                icon=ft.icons.STORE,
                content=ft.Container(
                    load_user_components(user_id), padding=10, expand=True
                ),
            ),
            ft.Tab(
                text="Рейтинг пользователей",
                icon=ft.icons.LEADERBOARD,
                content=ft.Container(load_user_ranking(), padding=10, expand=True),
            ),
            ft.Tab(
                text="История продаж",
                icon=ft.icons.HISTORY,
                content=ft.Container(
                    load_sales_history(user_id), padding=10, expand=True
                ),
            ),
        ],
        expand=True,
        label_color=DARK_BLUE,
        unselected_label_color=TEXT,
        indicator_color=DARK_BLUE,
        divider_color=MEDIUM_BLUE,
    )

    def go_to_create_component(e):
        page.go("/create_component")

    # return ft.View(
    #     "/user",  # Маршрут для этого View
    #     [tabs],  # Основной контент страницы
    #     appbar=app_bar,  # Устанавливаем AppBar для View
    #     padding=0,  # Убираем отступы View
    #     bgcolor=VERY_LIGHT_BLUE,  # Устанавливаем фон для View
    # )
    # --- View --- (остается без изменений, кроме добавления FAB)
    return ft.View(
        f"/user/{user_id}",
        [tabs],  # Основной контент страницы
        appbar=app_bar,  # Устанавливаем AppBar для View
        bgcolor=VERY_LIGHT_BLUE,  # Устанавливаем фон для View
        padding=0,
        floating_action_button=ft.FloatingActionButton(
            icon=ft.icons.ADD,
            tooltip="Добавить комплектующее",
            on_click=go_to_create_component,
            bgcolor=MEDIUM_BLUE,
        ),
        floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
    )
