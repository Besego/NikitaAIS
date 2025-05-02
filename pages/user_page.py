import flet as ft
import asyncio
from buyer import Buyer
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
from models.models import User, Sale, Component
import datetime


def user_view(page: ft.Page, user_id_str: str):
    # --- Проверка авторизации ---
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        user_id = None
        if page.session.contains_key("user_id"):
            user_id = page.session.get("user_id")

    if not user_id:
        return ft.View(
            "/user",
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
            bgcolor=VERY_LIGHT_BLUE,
        )
        
    def is_mobile(page):
        return page.width < 600
    
    def is_tablet(page):
        return 600 <= page.width < 1024

    # --- Функции для загрузки данных ---
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
        return cards

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
        return rows

    def load_sales_history(user_id):
        session = db_manager.Session()
        try:
            sales = session.query(Sale).filter(Sale.user_id == user_id).all()
            rows = []
            if sales:
                for sale in sales:
                    component_name = sale.component.name if sale.component else "N/A"
                    sale_date_str = (
                        sale.sale_date.strftime("%Y-%m-%d %H:%M")
                        if sale.sale_date
                        else "N/A"
                    )
                    rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(component_name, color=TEXT)),
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
                            ft.DataCell(ft.Text("")),
                            ft.DataCell(ft.Text("")),
                            ft.DataCell(ft.Text("")),
                        ]
                    )
                )
            return rows
        finally:
            session.close()

    # --- Контейнеры для динамического контента ---
    components_grid = ft.GridView(
        runs_count=5,
        max_extent=300,
        child_aspect_ratio=1.8,
        spacing=10,
        run_spacing=10,
        controls=load_user_components(user_id),
        expand=True,
    )

    # Обертка GridView для вертикальной прокрутки с ListView
    scrollable_components = ft.ListView(
        controls=[components_grid],
        expand=True,
        spacing=10,
        auto_scroll=False,
    )

    # Таблица рейтинга пользователей
    ranking_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Место", weight=ft.FontWeight.BOLD, color=DARK_BLUE)),
            ft.DataColumn(
                ft.Text("Пользователь", weight=ft.FontWeight.BOLD, color=DARK_BLUE)
            ),
            ft.DataColumn(
                ft.Text("Кол-во продаж", weight=ft.FontWeight.BOLD, color=DARK_BLUE),
                numeric=True,
            ),
        ],
        rows=load_user_ranking(),
        expand=True,
        border=ft.border.all(1, MEDIUM_BLUE),
        border_radius=ft.border_radius.all(10),
        heading_row_color=LIGHT_BLUE,
        data_row_color={"hovered": MEDIUM_BLUE},
        column_spacing=10,
    )

    # Таблица истории продаж
    sales_table = ft.DataTable(
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
            ft.DataColumn(ft.Text("Дата", weight=ft.FontWeight.BOLD, color=DARK_BLUE)),
        ],
        rows=load_sales_history(user_id),
        expand=True,
        border=ft.border.all(1, MEDIUM_BLUE),
        border_radius=ft.border_radius.all(10),
        heading_row_color=LIGHT_BLUE,
        data_row_color={"hovered": MEDIUM_BLUE},
        column_spacing=10,
    )

    # --- Обертка таблиц для прокрутки ---
    def create_scrollable_table(page, table, title=None, description=None):
        """Создает адаптивную таблицу с прокруткой вверх-вниз и влево-вправо.

        """
        # Определяем тип устройства
        is_mob = is_mobile(page)
        is_tab = is_tablet(page)

        # Заголовок и описание (если переданы)
        header = []
        if title:
            header.append(ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=DARK_BLUE))
        if description:
            header.append(ft.Text(description, color=TEXT))

        # Настраиваем таблицу
        table.border = ft.border.all(1, ft.colors.BLACK12)
        table.heading_row_color = ft.colors.BLACK12

        # Контейнер для таблицы с визуальными улучшениями
        table_container = ft.Container(
            width=600,
            content=table,
            padding=10,
            bgcolor=WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.colors.with_opacity(0.15, ft.colors.BLACK)
            ),
        )

        # Логика для мобильных устройств
        if is_mob:
            # Индикаторы прокрутки для мобильных
            scroll_indicators = ft.Row([
                ft.Icon(ft.icons.SWIPE, color=DARK_BLUE, size=18),
                ft.Text("Прокрутите влево-вправо для просмотра всей таблицы",
                        color=TEXT, size=12),
            ], alignment=ft.MainAxisAlignment.CENTER)

            # Горизонтальная прокрутка
            horizontal_scroll = ft.Row(
                [table_container],
                scroll=ft.ScrollMode.AUTO,
                vertical_alignment=ft.CrossAxisAlignment.START
            )

            # Вертикальная прокрутка с ограничением высоты
            return ft.Column(
                [
                    *header,
                    scroll_indicators,
                    ft.Container(
                        content=horizontal_scroll,
                    )
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO  # Включаем вертикальную прокрутку
            )

        # Логика для планшетов
        elif is_tab:
            # Горизонтальная прокрутка
            horizontal_scroll = ft.Row(
                [table_container],
                scroll=ft.ScrollMode.AUTO,
                vertical_alignment=ft.CrossAxisAlignment.START
            )

            return ft.Column(
                [
                    *header,
                    horizontal_scroll
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
            )

        # Логика для десктопов
        else:
            # Горизонтальная прокрутка
            horizontal_scroll = ft.Row(
                [table_container],
                scroll=ft.ScrollMode.AUTO,
                vertical_alignment=ft.CrossAxisAlignment.START
            )

            return ft.Column(
                [
                    *header,
                    horizontal_scroll
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
            )

    # --- Функции обновления ---
    def update_components():
        components_grid.controls = load_user_components(user_id)
        page.update()

    def update_ranking():
        ranking_table.rows = load_user_ranking()
        page.update()

    def update_sales():
        sales_table.rows = load_sales_history(user_id)
        page.update()

    # --- Асинхронное автообновление ---
    async def start_auto_update():
        while True:
            update_components()
            update_ranking()
            update_sales()
            await asyncio.sleep(6)  # Синхронизация с интервалом Buyer

    # Запускаем автообновление
    page.run_task(start_auto_update)

    # --- Запуск Buyer ---
    components = db_manager.get_components_by_user(user_id)
    buyer = Buyer(
        sale_manager=db_manager,
        user_id=user_id,
        components=components,
        interval=6,  # Интервал в секундах
        page=page,  # Передаем объект страницы
    )
    buyer.start_buying()

    # --- Компоненты UI ---
    def logout(e):
        page.session.remove("user_id")
        page.session.remove("user_name")
        page.session.remove("user_role")
        page.go("/login")

    logout_button = ft.IconButton(
        icon=ft.icons.LOGOUT, tooltip="Выйти", on_click=logout, icon_color=DARK_BLUE
    )

    user_name = page.session.get("user_name") or "Пользователь"

    app_bar = ft.AppBar(
        title=ft.Row(
            [
                ft.Icon(ft.icons.PERSON_2, color=WHITE),
                ft.Text(f"Личный кабинет: {user_name}", color=WHITE, size=20, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=MEDIUM_BLUE,
        actions=[logout_button],
        center_title=True,
        toolbar_height=60,
        elevation=4,
    )

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Мой склад",
                icon=ft.icons.STORE,
                content=ft.Container(scrollable_components, padding=10, expand=True),
            ),
            ft.Tab(
                text="Рейтинг пользователей",
                icon=ft.icons.LEADERBOARD,
                content=create_scrollable_table(page,ranking_table,"Рейтинг пользователей")
            ),
            ft.Tab(
                text="История продаж",
                icon=ft.icons.HISTORY,
                content=create_scrollable_table(page,sales_table,"История продаж",),
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

    # --- View ---
    return ft.View(
        f"/user/{user_id}",
        [tabs],
        appbar=app_bar,
        bgcolor=VERY_LIGHT_BLUE,
        padding=0,
        floating_action_button=ft.FloatingActionButton(
            icon=ft.icons.ADD,
            tooltip="Добавить комплектующее",
            on_click=go_to_create_component,
            bgcolor=MEDIUM_BLUE,
        ),
        floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
    )