import asyncio
import flet as ft
from flet import Colors

# Импортируем цвета
from styles.colors import (
    TEXT,
    LIGHT_BLUE,
    MEDIUM_BLUE,
    DARK_BLUE,
    WHITE,
    VERY_LIGHT_BLUE,
)
from db import db_manager
from concurrent.futures import ThreadPoolExecutor

def admin_view(page: ft.Page):
    # --- Проверка авторизации и роли админа ---
    user_role = page.session.get("user_role")
    if user_role != "ADMIN":
        return ft.View(
            "/admin",
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Доступ только для администраторов",
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
    def load_users():
        users = db_manager.get_all_users()
        rows = []
        if users:
            for user in users:
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(user.user_id), color=TEXT)),
                            ft.DataCell(ft.Text(user.username, color=TEXT)),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_color=Colors.RED_400,
                                    tooltip="Удалить пользователя",
                                    on_click=lambda e, uid=user.user_id: show_delete_user_dialog(uid),
                                )
                            ),
                        ]
                    )
                )
        else:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text("Нет пользователей.", color=TEXT, colspan=3)
                        )
                    ]
                )
            )
        return rows

    def load_components():
        components = db_manager.get_all_components()
        rows = []
        if components:
            for comp in components:
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(comp.component_id), color=TEXT)),
                            ft.DataCell(ft.Text(comp.name, color=TEXT)),
                            ft.DataCell(ft.Text(str(comp.quantity), color=TEXT)),
                            ft.DataCell(ft.Text(f"{comp.price:.2f}", color=TEXT)),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_color=Colors.RED_400,
                                    tooltip="Удалить комплектующее",
                                    on_click=lambda e, cid=comp.component_id: show_delete_component_dialog(cid),
                                )
                            ),
                        ]
                    )
                )
        else:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text("Нет комплектующих.", color=TEXT, colspan=5)
                        )
                    ]
                )
            )
        return rows

    def load_sales():
        sales = db_manager.get_all_sales()
        rows = []
        if sales:
            for sale in sales:
                component_name = sale.component.name if sale.component else "N/A"
                username = sale.user.username if sale.user else "N/A"
                sale_date_str = (
                    sale.sale_date.strftime("%Y-%m-%d %H:%M")
                    if sale.sale_date
                    else "N/A"
                )
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(sale.sale_id), color=TEXT)),
                            ft.DataCell(ft.Text(username, color=TEXT)),
                            ft.DataCell(ft.Text(component_name, color=TEXT)),
                            ft.DataCell(ft.Text(str(sale.quantity), color=TEXT)),
                            ft.DataCell(ft.Text(f"{sale.total_price:.2f}", color=TEXT)),
                            ft.DataCell(ft.Text(sale_date_str, color=TEXT)),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_color=Colors.RED_400,
                                    tooltip="Удалить продажу",
                                    on_click=lambda e, sid=sale.sale_id: show_delete_sale_dialog(sid),
                                )
                            ),
                        ]
                    )
                )
        else:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text("Нет продаж.", color=TEXT, colspan=7)
                        )
                    ]
                )
            )
        return rows

    # --- Функции для отображения диалогов подтверждения ---
    def show_delete_user_dialog(user_id):
        def close_dialog(e):
            page.close(dialog)
            page.update()

        def confirm_delete(e):
            success = db_manager.delete_user(user_id)
            page.close(dialog)
            page.update()
            if success:
                users_table.rows = load_users()
            else:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Ошибка при удалении пользователя"),
                    bgcolor=Colors.RED_400,
                )
                page.snack_bar.open = True
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Подтверждение удаления"),
            content=ft.Text("Вы уверены, что хотите удалить этого пользователя? Это действие нельзя отменить."),
            actions=[
                ft.TextButton("Отмена", on_click=close_dialog),
                ft.TextButton("Подтвердить", on_click=confirm_delete),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dialog)
        page.update()

    def show_delete_component_dialog(component_id):
        def close_dialog(e):
            page.close(dialog)
            page.update()

        def confirm_delete(e):
            success = db_manager.delete_component(component_id)
            page.close(dialog)
            page.update()
            if success:
                components_table.rows = load_components()
            else:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Ошибка при удалении комплектующего"),
                    bgcolor=Colors.RED_400,
                )
                page.snack_bar.open = True
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Подтверждение удаления"),
            content=ft.Text("Вы уверены, что хотите удалить это комплектующее? Это действие нельзя отменить."),
            actions=[
                ft.TextButton("Отмена", on_click=close_dialog),
                ft.TextButton("Подтвердить", on_click=confirm_delete),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dialog)
        page.update()

    def show_delete_sale_dialog(sale_id):
        def close_dialog(e):
            page.close(dialog)
            page.update()

        def confirm_delete(e):
            success = db_manager.delete_sale(sale_id)
            page.close(dialog)
            page.update()
            if success:
                sales_table.rows = load_sales()
            else:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Ошибка при удалении продажи"),
                    bgcolor=Colors.RED_400,
                )
                page.snack_bar.open = True
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Подтверждение удаления"),
            content=ft.Text("Вы уверены, что хотите удалить эту продажу? Это действие нельзя отменить."),
            actions=[
                ft.TextButton("Отмена", on_click=close_dialog),
                ft.TextButton("Подтвердить", on_click=confirm_delete),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dialog)
        page.update()

    # --- Таблицы ---
    users_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, color=DARK_BLUE)),
            ft.DataColumn(ft.Text("Имя пользователя", weight=ft.FontWeight.BOLD, color=DARK_BLUE)),
            ft.DataColumn(ft.Text("Действия", weight=ft.FontWeight.BOLD, color=DARK_BLUE)),
        ],
        rows=load_users(),
        expand=True,
        border=ft.border.all(1, MEDIUM_BLUE),
        border_radius=ft.border_radius.all(10),
        heading_row_color=LIGHT_BLUE,
        data_row_color={"hovered": MEDIUM_BLUE},
        column_spacing=10,
    )

    components_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, color=DARK_BLUE)),
            ft.DataColumn(ft.Text("Название", weight=ft.FontWeight.BOLD, color=DARK_BLUE)),
            ft.DataColumn(ft.Text("Кол-во", weight=ft.FontWeight.BOLD, color=DARK_BLUE), numeric=True),
            ft.DataColumn(ft.Text("Цена", weight=ft.FontWeight.BOLD, color=DARK_BLUE), numeric=True),
            ft.DataColumn(ft.Text("Действия", weight=ft.FontWeight.BOLD, color=DARK_BLUE)),
        ],
        rows=load_components(),
        expand=True,
        border=ft.border.all(1, MEDIUM_BLUE),
        border_radius=ft.border_radius.all(10),
        heading_row_color=LIGHT_BLUE,
        data_row_color={"hovered": MEDIUM_BLUE},
        column_spacing=10,
    )

    sales_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, color=DARK_BLUE)),
            ft.DataColumn(ft.Text("Пользователь", weight=ft.FontWeight.BOLD, color=DARK_BLUE)),
            ft.DataColumn(ft.Text("Комплектующее", weight=ft.FontWeight.BOLD, color=DARK_BLUE)),
            ft.DataColumn(ft.Text("Кол-во", weight=ft.FontWeight.BOLD, color=DARK_BLUE), numeric=True),
            ft.DataColumn(ft.Text("Сумма", weight=ft.FontWeight.BOLD, color=DARK_BLUE), numeric=True),
            ft.DataColumn(ft.Text("Дата", weight=ft.FontWeight.BOLD, color=DARK_BLUE)),
            ft.DataColumn(ft.Text("Действия", weight=ft.FontWeight.BOLD, color=DARK_BLUE)),
        ],
        rows=load_sales(),
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
    def update_users():
        users_table.rows = load_users()
        page.update()

    def update_components():
        components_table.rows = load_components()
        page.update()

    def update_sales():
        sales_table.rows = load_sales()
        page.update()

    # --- Асинхронное автообновление ---
    async def start_auto_update():
        while True:
            update_users()
            update_components()
            update_sales()
            await asyncio.sleep(6)

    # Запускаем автообновление
    page.run_task(start_auto_update)

    # --- Компоненты UI ---
    def logout(e):
        page.session.remove("user_id")
        page.session.remove("user_name")
        page.session.remove("user_role")
        page.go("/login")

    logout_button = ft.IconButton(
        icon=ft.icons.LOGOUT, tooltip="Выйти", on_click=logout, icon_color=DARK_BLUE
    )

    app_bar = ft.AppBar(
        title=ft.Row(
            [
                ft.Icon(ft.icons.ADMIN_PANEL_SETTINGS, color=WHITE),
                ft.Text("Панель администратора", color=WHITE, size=20, weight=ft.FontWeight.BOLD),
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
                text="Пользователи",
                icon=ft.icons.PEOPLE,
                content=create_scrollable_table(page,users_table,"Пользователи"),
            ),
            ft.Tab(
                text="Комплектующие",
                icon=ft.icons.STORE,
                content=create_scrollable_table(page,components_table,"Комплектующие"),
            ),
            ft.Tab(
                text="Продажи",
                icon=ft.icons.HISTORY,
                content=create_scrollable_table(page,sales_table,"Продажи"),
            ),
        ],
        expand=True,
        label_color=DARK_BLUE,
        unselected_label_color=TEXT,
        indicator_color=DARK_BLUE,
        divider_color=MEDIUM_BLUE,
    )

    # --- View ---
    return ft.View(
        "/admin",
        [tabs],
        appbar=app_bar,
        bgcolor=VERY_LIGHT_BLUE,
        padding=0,
    )