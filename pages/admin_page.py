import flet as ft

# Импортируем цвета
from styles.colors import (
    TEXT,
    PINK_LIGHT,
    YELLOW_LIGHT,
    PINK_MEDIUM,
    YELLOW_DARK,
    PINK_DARK,
)
from db import db_manager
from concurrent.futures import ThreadPoolExecutor


def admin_view(page: ft.Page):
    """Создает представление страницы администратора, адаптированное для мобильных устройств."""

    # Создаем ThreadPoolExecutor для асинхронной загрузки данных
    executor = ThreadPoolExecutor(max_workers=3)

    cached_data = {"clients": None, "products": None, "orders": None}

    # Установка свойств страницы
    page.padding = 0
    page.bgcolor = YELLOW_LIGHT

    # Функция для проверки размера экрана
    def is_mobile(page):
        return page.width < 600

    def is_tablet(page):
        return 600 <= page.width < 1024

    # Переменная для хранения текущего активного контента
    current_content = ft.Ref[ft.Container]()

    def load_data(data_type):
        """Загружает данные указанного типа из БД"""
        page.splash = ft.ProgressBar()
        page.update()

        try:
            if data_type == "clients" and cached_data["clients"] is None:
                cached_data["clients"] = db_manager.get_all_clients()
            elif data_type == "products" and cached_data["products"] is None:
                cached_data["products"] = db_manager.get_all_products()
            elif data_type == "orders" and cached_data["orders"] is None:
                cached_data["orders"] = db_manager.get_all_orders()
        except Exception as e:
            print(f"Ошибка загрузки данных {data_type}: {e}")
        finally:
            page.splash = None
            page.update()

    # Функция для показа диалога подтверждения удаления
    def show_delete_confirmation(item_type, item_id, item_name, on_confirm):
        """
        Показывает диалог подтверждения удаления
        """

        # Создаем обработчик закрытия для кнопки "Отмена"
        def handle_cancel(e):
            page.close(dialog)

        # Создаем обработчик для кнопки "Удалить"
        def handle_delete(e):
            page.close(dialog)
            on_confirm(item_id)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Удаление {item_type}"),
            content=ft.Text(
                f"Вы действительно хотите удалить {item_type} '{item_name}'? Это действие нельзя отменить."
            ),
            actions=[
                ft.TextButton("Отмена", on_click=handle_cancel),
                ft.TextButton(
                    "Удалить",
                    on_click=handle_delete,
                    style=ft.ButtonStyle(color=ft.colors.RED_500),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Открываем диалог
        page.open(dialog)
        return dialog

    # Функция для показа сообщения об успехе/ошибке
    def show_message(title, message, is_error=False):
        """Показывает информационное сообщение"""
        color = ft.colors.RED_500 if is_error else PINK_DARK

        # Обработчик закрытия для кнопки "ОК"
        def handle_ok(e):
            page.close(dialog)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, color=color),
            content=ft.Text(message),
            actions=[
                ft.TextButton("ОК", on_click=handle_ok),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.open(dialog)
        return dialog

    # Функции для удаления записей

    def delete_client_handler(e):
        """Обработчик нажатия на кнопку удаления клиента"""
        client_id = e.control.data  # ID клиента хранится в data кнопки

        # Находим информацию о клиенте для отображения в диалоге
        client = next((c for c in cached_data["clients"] if c["id"] == client_id), None)
        if not client:
            return

        def confirm_delete(client_id):
            # Выполняем удаление
            success, message = db_manager.delete_client(client_id)

            # Показываем результат
            title = "Успешно" if success else "Ошибка"
            show_message(title, message, not success)

            # Если успешно, обновляем данные
            if success:
                cached_data["clients"] = None  # Сбрасываем кэш
                executor.submit(load_data, "clients")  # Перезагружаем данные

        show_delete_confirmation(
            "клиента", client_id, client["full_name"], confirm_delete
        )

    def delete_product_handler(e):
        """Обработчик нажатия на кнопку удаления товара"""
        product_id = e.control.data  # ID товара хранится в data кнопки

        # Находим информацию о товаре для отображения в диалоге
        product = next(
            (p for p in cached_data["products"] if p["id"] == product_id), None
        )
        if not product:
            return

        def confirm_delete(product_id):
            # Выполняем удаление
            success, message = db_manager.delete_product(product_id)

            # Показываем результат
            title = "Успешно" if success else "Ошибка"
            show_message(title, message, not success)

            # Если успешно, обновляем данные
            if success:
                cached_data["products"] = None  # Сбрасываем кэш
                executor.submit(load_data, "products")  # Перезагружаем данные

        show_delete_confirmation("товар", product_id, product["name"], confirm_delete)

    def delete_order_handler(e):
        """Обработчик нажатия на кнопку удаления заказа"""
        order_id = e.control.data  # ID заказа хранится в data кнопки

        # Находим информацию о заказе для отображения в диалоге
        order = next((o for o in cached_data["orders"] if o["id"] == order_id), None)
        if not order:
            return

        def confirm_delete(order_id):
            # Выполняем удаление
            success, message = db_manager.delete_order(order_id)

            # Показываем результат
            title = "Успешно" if success else "Ошибка"
            show_message(title, message, not success)

            # Если успешно, обновляем данные
            if success:
                cached_data["orders"] = None  # Сбрасываем кэш
                executor.submit(load_data, "orders")  # Перезагружаем данные

        order_name = f"#{order['id']} от {order['order_date']}"
        show_delete_confirmation("заказ", order_id, order_name, confirm_delete)

    # Функция для создания таблиц или карточек в зависимости от размера экрана
    def create_adaptive_data_view(title, description, columns, rows):
        is_mob = is_mobile(page)
        is_tab = is_tablet(page)

        # Заголовок и описание одинаковы для всех представлений
        header = ft.Column(
            [
                ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=PINK_DARK),
                ft.Text(description, color=TEXT),
            ],
            spacing=5,
        )

        # Создание таблицы с учетом устройства
        if is_mob:
            # Создаем стандартную таблицу
            table = ft.DataTable(
                columns=columns,
                rows=rows,
                column_spacing=10,  # Расстояние между колонками
                border=ft.border.all(1, ft.colors.BLACK12),  # Добавляем рамку
                heading_row_color=ft.colors.BLACK12,  # Цвет строки заголовка
            )

            # Создаем индикаторы прокрутки
            scroll_indicators = ft.Row(
                [
                    ft.Icon(ft.icons.SWIPE, color=PINK_DARK, size=18),
                    ft.Text(
                        "Прокрутите влево-вправо для просмотра всей таблицы",
                        color=TEXT,
                        size=12,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )

            # Для горизонтальной прокрутки используем Row со scroll=True
            table_row = ft.Row(
                [
                    ft.Container(
                        content=table,
                        padding=10,
                        bgcolor=ft.colors.WHITE,
                        border_radius=10,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=5,
                            color=ft.colors.with_opacity(0.15, ft.colors.BLACK),
                        ),
                        width=800,  # Фиксированная большая ширина для активации скроллинга
                    )
                ],
                scroll=ft.ScrollMode.AUTO,  # Горизонтальный скроллинг
                vertical_alignment=ft.CrossAxisAlignment.START,
            )

            # Используем Column со scroll для вертикальной прокрутки
            return ft.Column(
                [
                    header,
                    scroll_indicators,
                    ft.Container(
                        content=table_row,
                        height=350,  # Ограничиваем высоту для вертикального скроллинга
                    ),
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,  # Вертикальный скроллинг
            )

        # Для планшета
        elif is_tab:
            table = ft.DataTable(
                columns=columns,
                rows=rows,
                # border=ft.border.all(1, ft.colors.BLACK12),
                # heading_row_color=ft.colors.BLACK12,
            )

            # Используем тот же подход с Row для горизонтального скроллинга
            table_row = ft.Row(
                [
                    ft.Container(
                        content=table,
                        padding=10,
                        bgcolor=ft.colors.WHITE,
                        border_radius=10,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=5,
                            color=ft.colors.with_opacity(0.15, ft.colors.BLACK),
                        ),
                        width=1000,  # Большая ширина для скроллинга
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )

            return ft.Column(
                [header, table_row],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
                height=500,  # Фиксированная высота для Column
            )

        # Для десктопа
        else:
            table = ft.DataTable(
                columns=columns,
                rows=rows,
                border=ft.border.all(1, ft.colors.BLACK12),
                heading_row_color=ft.colors.BLACK12,
            )

            # Даже для десктопа добавляем скроллинг для больших таблиц
            table_row = ft.Row(
                [
                    ft.Container(
                        content=table,
                        padding=10,
                        bgcolor=ft.colors.WHITE,
                        border_radius=10,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=5,
                            color=ft.colors.with_opacity(0.15, ft.colors.BLACK),
                        ),
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )

            return ft.Column(
                [header, table_row],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
                height=600,  # Больше места для десктопа
            )

    # Создание панели с метриками (оставлено с вашими изменениями)
    def metrics_panel():
        is_mob = is_mobile(page)
        is_tab = is_tablet(page)

        # Загрузка статистики из кэшированных данных
        client_count = (
            len(cached_data["clients"]) if cached_data["clients"] is not None else "..."
        )
        products_count = (
            len(cached_data["products"])
            if cached_data["products"] is not None
            else "..."
        )
        orders_count = (
            len(cached_data["orders"]) if cached_data["orders"] is not None else "..."
        )

        # Расчет прибыли, если есть данные о заказах
        total_profit = 0
        if cached_data["orders"] is not None:
            total_profit = sum(order["total_price"] for order in cached_data["orders"])

        # Элементы метрик
        metrics = [
            {
                "icon": ft.icons.PEOPLE_ALT,
                "title": "Пользователи",
                "value": str(client_count),
            },
            {
                "icon": ft.icons.INVENTORY_2,
                "title": "Товары",
                "value": str(products_count),
            },
            {
                "icon": ft.icons.SHOPPING_BAG,
                "title": "Заказы",
                "value": str(orders_count),
            },
            {
                "icon": ft.icons.TRENDING_UP,
                "title": "Прибыль",
                "value": (
                    f"₽ {total_profit:,.2f}"
                    if isinstance(total_profit, (int, float))
                    else total_profit
                ),
            },
        ]

        # Определяем размеры метрик в зависимости от устройства
        if is_mob:
            metric_width = 145  # Уже на мобильных устройствах
            padding = 10
            icon_size = 22
            title_size = 12
            value_size = 18
        elif is_tab:
            metric_width = 180  # Средний размер для планшетов
            padding = 15
            icon_size = 24
            title_size = 14
            value_size = 20
        else:
            metric_width = 240  # Широкие блоки для десктопа
            padding = 20
            icon_size = 28
            title_size = 16
            value_size = 24

        # Создаем отдельные элементы метрик с учетом размеров устройства
        metric_items = []
        for metric in metrics:
            metric_items.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(metric["icon"], size=icon_size, color=PINK_DARK),
                            ft.Text(
                                metric["title"],
                                size=title_size,
                                color=TEXT,
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Text(
                                metric["value"],
                                size=value_size,
                                color=PINK_DARK,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                    ),
                    padding=ft.padding.all(padding),
                    border_radius=ft.border_radius.all(10),
                    bgcolor=PINK_LIGHT,
                    width=metric_width,
                    height=120 if is_mob else 140,  # Фиксируем высоту для единообразия
                    expand=True,  # Это позволит контейнеру растягиваться в ряду
                )
            )

        # Разделяем метрики на две строки, по две метрики в каждой
        # Всегда используем сетку 2x2 независимо от устройства
        metrics_layout = ft.Column(
            [
                ft.Row(
                    [metric_items[0], metric_items[1]],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    [metric_items[2], metric_items[3]],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=10,
        )

        return ft.Column(
            [
                ft.Text(
                    "Статистика",
                    size=18 if is_mob else 24,
                    weight=ft.FontWeight.BOLD,
                    color=PINK_DARK,
                ),
                metrics_layout,
            ],
            spacing=15,
        )

    # Определение различных видов контента с адаптивными таблицами
    def users_content():
        # Асинхронно загружаем данные о клиентах
        executor.submit(load_data, "clients")

        # Колонки таблицы остаются прежними
        columns = [
            ft.DataColumn(ft.Text("ID", color=TEXT)),
            ft.DataColumn(ft.Text("Имя", color=TEXT)),
            ft.DataColumn(ft.Text("Email", color=TEXT)),
            ft.DataColumn(ft.Text("Телефон", color=TEXT)),
            ft.DataColumn(ft.Text("Роль", color=TEXT)),
            ft.DataColumn(ft.Text("Действия", color=TEXT)),
        ]

        rows = []

        # Если данные еще не загружены, показываем индикатор загрузки
        if cached_data["clients"] is None:
            loading_row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Загрузка данных...")),
                    ft.DataCell(ft.ProgressBar(width=100)),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                ]
            )
            rows.append(loading_row)
        else:
            # Создаем строки таблицы на основе данных из БД
            for client in cached_data["clients"]:
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(client["id"]), color=TEXT)),
                            ft.DataCell(ft.Text(client["full_name"], color=TEXT)),
                            ft.DataCell(ft.Text(client["email"] or "-", color=TEXT)),
                            ft.DataCell(ft.Text(client["phone"], color=TEXT)),
                            ft.DataCell(ft.Text(client["role"] or "USER", color=TEXT)),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        # ft.IconButton(
                                        #     icon=ft.icons.EDIT,
                                        #     icon_color=PINK_DARK,
                                        #     tooltip="Редактировать",
                                        #     data=client["id"],
                                        #     # on_click=edit_client
                                        # ),
                                        ft.IconButton(
                                            icon=ft.icons.DELETE,
                                            icon_color=PINK_DARK,
                                            tooltip="Удалить",
                                            data=client["id"],
                                            on_click=delete_client_handler,
                                        ),
                                    ]
                                )
                            ),
                        ]
                    )
                )

        return ft.Container(
            content=create_adaptive_data_view(
                "Управление пользователями",
                "Здесь вы можете просматривать и управлять аккаунтами пользователей",
                columns,
                rows,
            ),
            padding=15,
        )

    def products_content():
        # Асинхронно загружаем данные о товарах
        executor.submit(load_data, "products")

        columns = [
            ft.DataColumn(ft.Text("ID", color=TEXT)),
            ft.DataColumn(ft.Text("Название", color=TEXT)),
            ft.DataColumn(ft.Text("Категория", color=TEXT)),
            ft.DataColumn(ft.Text("Цена", color=TEXT)),
            ft.DataColumn(ft.Text("Остаток", color=TEXT)),
            ft.DataColumn(ft.Text("Действия", color=TEXT)),
        ]

        rows = []

        # Если данные еще не загружены, показываем индикатор загрузки
        if cached_data["products"] is None:
            loading_row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Загрузка данных...")),
                    ft.DataCell(ft.ProgressBar(width=100)),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                ]
            )
            rows.append(loading_row)
        else:
            # Создаем строки таблицы на основе данных из БД
            for product in cached_data["products"]:
                # Получаем название категории, если она есть
                category_name = (
                    product["category"]["name"] if product.get("category") else "-"
                )

                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(product["id"]), color=TEXT)),
                            ft.DataCell(ft.Text(product["name"], color=TEXT)),
                            ft.DataCell(ft.Text(category_name, color=TEXT)),
                            ft.DataCell(
                                ft.Text(f"₽ {product['price']:,.2f}", color=TEXT)
                            ),
                            ft.DataCell(ft.Text(str(product["quantity"]), color=TEXT)),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        # ft.IconButton(
                                        #     icon=ft.icons.EDIT,
                                        #     icon_color=PINK_DARK,
                                        #     tooltip="Редактировать",
                                        #     data=product["id"],
                                        #     # on_click=edit_product
                                        # ),
                                        ft.IconButton(
                                            icon=ft.icons.DELETE,
                                            icon_color=PINK_DARK,
                                            tooltip="Удалить",
                                            data=product["id"],
                                            on_click=delete_product_handler,
                                        ),
                                    ]
                                )
                            ),
                        ]
                    )
                )

        return ft.Container(
            content=create_adaptive_data_view(
                "Управление товарами",
                "Здесь вы можете добавлять, редактировать и удалять товары",
                columns,
                rows,
            ),
            padding=15,
        )

    def orders_content():
        # Асинхронно загружаем данные о заказах
        executor.submit(load_data, "orders")

        columns = [
            ft.DataColumn(ft.Text("ID", color=TEXT)),
            ft.DataColumn(ft.Text("Клиент", color=TEXT)),
            ft.DataColumn(ft.Text("Дата", color=TEXT)),
            ft.DataColumn(ft.Text("Сумма", color=TEXT)),
            ft.DataColumn(ft.Text("Статус", color=TEXT)),
            ft.DataColumn(ft.Text("Действия", color=TEXT)),
        ]

        rows = []

        # Если данные еще не загружены, показываем индикатор загрузки
        if cached_data["orders"] is None:
            loading_row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Загрузка данных...")),
                    ft.DataCell(ft.ProgressBar(width=100)),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                ]
            )
            rows.append(loading_row)
        else:
            # Создаем строки таблицы на основе данных из БД
            for order in cached_data["orders"]:
                # Получаем данные о клиенте
                client_name = (
                    order["client"]["full_name"] if order.get("client") else "-"
                )

                # Устанавливаем цвет и фон в зависимости от статуса заказа
                status_colors = {
                    "Доставлено": (YELLOW_LIGHT, PINK_DARK),
                    "В процессе": (TEXT, YELLOW_DARK),
                    "Отправлено": (PINK_DARK, YELLOW_DARK),
                    "Создано": (TEXT, PINK_LIGHT),
                    "Отменено": (YELLOW_LIGHT, ft.colors.RED_500),
                }

                status_text = order["status"] if order.get("status") else "Создано"
                text_color, bg_color = status_colors.get(
                    status_text, (TEXT, YELLOW_DARK)
                )

                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(order["id"]), color=TEXT)),
                            ft.DataCell(ft.Text(client_name, color=TEXT)),
                            ft.DataCell(ft.Text(order["order_date"], color=TEXT)),
                            ft.DataCell(
                                ft.Text(f"₽ {order['total_price']:,.2f}", color=TEXT)
                            ),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(status_text, color=text_color),
                                    bgcolor=bg_color,
                                    border_radius=5,
                                    padding=5,
                                )
                            ),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        # ft.IconButton(
                                        #     icon=ft.icons.RECEIPT_LONG,
                                        #     icon_color=PINK_DARK,
                                        #     tooltip="Детали заказа",
                                        #     data=order["id"],
                                        #     # on_click=view_order_details
                                        # ),
                                        ft.IconButton(
                                            icon=ft.icons.EDIT,
                                            icon_color=PINK_DARK,
                                            tooltip="Изменить статус",
                                            data=order["id"],
                                            # on_click=update_order_status
                                        ),
                                        ft.IconButton(
                                            icon=ft.icons.DELETE,
                                            icon_color=PINK_DARK,
                                            tooltip="Удалить заказ",
                                            data=order["id"],
                                            on_click=delete_order_handler,
                                        ),
                                    ]
                                )
                            ),
                        ]
                    )
                )

        return ft.Container(
            content=create_adaptive_data_view(
                "Управление заказами",
                "Здесь вы можете просматривать и обрабатывать заказы пользователей",
                columns,
                rows,
            ),
            padding=15,
        )

    # Отчеты оставлены без изменений
    def reports_content():
        metrics_container = ft.Container(
            content=metrics_panel(),
            padding=ft.padding.all(15),
            border_radius=ft.border_radius.all(10),
            border=ft.border.all(1, PINK_LIGHT),
            margin=ft.margin.only(bottom=15),
        )

        return ft.Container(
            content=ft.Column(
                [
                    metrics_container,
                    ft.Text(
                        "Отчеты и статистика",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=PINK_DARK,
                    ),
                    ft.Text(
                        "Здесь вы можете просматривать аналитические данные и отчеты",
                        color=TEXT,
                    ),
                    # Примеры элементов для отчетов
                    # ft.Row([
                    #     ft.Container(
                    #         content=ft.Column([
                    #             ft.Text("Продажи по категориям", weight=ft.FontWeight.BOLD, color=PINK_DARK),
                    #             # Здесь можно добавить график или диаграмму
                    #         ]),
                    #         padding=15,
                    #         border_radius=10,
                    #         bgcolor=PINK_LIGHT,
                    #         expand=True,
                    #         height=200,
                    #     ),
                    #     ft.Container(
                    #         content=ft.Column([
                    #             ft.Text("Динамика продаж", weight=ft.FontWeight.BOLD, color=PINK_DARK),
                    #             # Здесь можно добавить график или диаграмму
                    #         ]),
                    #         padding=15,
                    #         border_radius=10,
                    #         bgcolor=PINK_LIGHT,
                    #         expand=True,
                    #         height=200,
                    #     ),
                    # ], spacing=10),
                ],
                spacing=15,
            ),
            padding=15,
        )

    # Функция для переключения контента
    def switch_content(content_func):
        """Переключает содержимое основного контейнера"""
        if current_content.current:
            # Показываем индикатор загрузки
            current_content.current.content = ft.Container(
                content=ft.Column(
                    [
                        ft.ProgressBar(),
                        ft.Text("Загрузка данных...", text_align=ft.TextAlign.CENTER),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=20,
                alignment=ft.alignment.center,
            )
            page.update()

            # Запускаем обновление содержимого после небольшой задержки
            new_content = content_func()
            current_content.current.content = new_content.content
            page.update()

    # Обновленная адаптивная навигационная панель
    def build_navigation():
        is_mob = is_mobile(page)
        is_tab = is_tablet(page)

        # Навигационные пункты
        nav_items = [
            {
                "title": "Пользователи",
                "icon": ft.icons.PEOPLE,
                "action": lambda: switch_content(users_content),
            },
            {
                "title": "Товары",
                "icon": ft.icons.INVENTORY,
                "action": lambda: switch_content(products_content),
            },
            {
                "title": "Заказы",
                "icon": ft.icons.SHOPPING_CART,
                "action": lambda: switch_content(orders_content),
            },
            {
                "title": "Отчеты",
                "icon": ft.icons.BAR_CHART,
                "action": lambda: switch_content(reports_content),
            },
        ]

        # Для мобильной версии - компактные кнопки только с иконками
        if is_mob:
            nav_buttons = [
                ft.IconButton(
                    icon=item["icon"],
                    icon_color=PINK_DARK,
                    tooltip=item["title"],
                    on_click=lambda e, action=item["action"]: action(),
                    style=ft.ButtonStyle(
                        bgcolor={"hovered": PINK_LIGHT, "": ft.colors.TRANSPARENT},
                    ),
                )
                for item in nav_items
            ]

            # Горизонтальная прокрутка для кнопок
            return ft.Container(
                content=ft.Row(
                    nav_buttons,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=ft.padding.symmetric(vertical=5, horizontal=10),
                bgcolor=YELLOW_LIGHT,
                border=ft.border.only(bottom=ft.BorderSide(1, PINK_LIGHT)),
                height=50,
            )

        # Для планшета - кнопки с иконками и короткими подписями
        elif is_tab:
            nav_buttons = [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(item["icon"], size=20, color=PINK_DARK),
                            ft.Text(
                                item["title"],
                                size=12,
                                color=PINK_DARK,
                            ),
                        ],
                        spacing=5,
                    ),
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(5),
                    bgcolor=PINK_LIGHT,
                    margin=ft.margin.only(right=10),
                    ink=True,
                    on_click=lambda e, action=item["action"]: action(),
                )
                for item in nav_items
            ]

            # Горизонтальная прокрутка для кнопок
            return ft.Container(
                content=ft.Row(
                    nav_buttons,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=5,
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=ft.padding.all(10),
                bgcolor=YELLOW_LIGHT,
                border=ft.border.only(bottom=ft.BorderSide(1, PINK_LIGHT)),
                height=70,
            )

        # Для десктопа - полноразмерные кнопки с подписями
        else:
            nav_buttons = [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(item["icon"], size=20, color=PINK_DARK),
                            ft.Text(
                                item["title"],
                                size=14,
                                color=PINK_DARK,
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=ft.padding.all(15),
                    border_radius=ft.border_radius.all(5),
                    bgcolor=PINK_LIGHT,
                    margin=ft.margin.only(right=15),
                    ink=True,
                    on_click=lambda e, action=item["action"]: action(),
                )
                for item in nav_items
            ]

            # Для десктопа прокрутка обычно не нужна, но добавим на всякий случай
            return ft.Container(
                content=ft.Row(
                    nav_buttons,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=5,
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=ft.padding.all(10),
                bgcolor=YELLOW_LIGHT,
                border=ft.border.only(bottom=ft.BorderSide(1, PINK_LIGHT)),
                height=80,
            )

    # Заголовок панели администратора
    def admin_header():
        is_mob = is_mobile(page)

        # Выпадающее меню для мобильной версии
        menu_items = [
            ft.PopupMenuItem(text="Профиль", icon=ft.icons.PERSON),
            ft.PopupMenuItem(text="Настройки", icon=ft.icons.SETTINGS),
            ft.PopupMenuItem(
                text="Выйти", icon=ft.icons.LOGOUT, on_click=lambda e: page.go("/login")
            ),
        ]

        # Кнопка для заголовка
        header_actions = (
            ft.PopupMenuButton(
                items=menu_items,
                icon=ft.icons.MORE_VERT,
                tooltip="Меню",
            )
            if is_mob
            else ft.ElevatedButton(
                text="Выйти",
                icon=ft.icons.LOGOUT,
                style=ft.ButtonStyle(
                    bgcolor=PINK_MEDIUM,
                    color=YELLOW_LIGHT,
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                on_click=lambda e: page.go("/login"),
            )
        )

        # Адаптивная компоновка заголовка
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        ft.icons.ADMIN_PANEL_SETTINGS,
                        color=PINK_DARK,
                        size=30 if not is_mob else 24,
                    ),
                    ft.Text(
                        "Панель администратора",
                        size=24 if not is_mob else 18,
                        weight=ft.FontWeight.BOLD,
                        color=PINK_DARK,
                    ),
                    header_actions,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.all(15),
            bgcolor=YELLOW_LIGHT,
            border=ft.border.only(bottom=ft.BorderSide(1, PINK_LIGHT)),
            # Убираем нижний отступ, так как теперь за ним следует навигация
            margin=ft.margin.all(0),
        )

    # Основной макет с учетом мобильного режима
    def build_layout():
        is_mob = is_mobile(page)
        is_tab = is_tablet(page)

        # Предварительно загружаем данные о клиентах
        executor.submit(load_data, "clients")

        # Создаем контейнер для динамического содержимого
        content_container = ft.Container(
            content=users_content().content,  # По умолчанию показываем управление пользователями
            padding=0,
            expand=True,
            ref=current_content,
        )

        # Получаем заголовок и навигацию
        header = admin_header()
        navigation = build_navigation()

        # Новая структура с навигацией сверху (одинаковая для всех устройств)
        return ft.Column(
            [
                header,
                navigation,  # Теперь навигация сверху
                ft.Container(
                    content=content_container,
                    padding=ft.padding.symmetric(horizontal=10 if is_mob else 15),
                    expand=True,
                ),
            ],
            expand=True,
        )

    # Обработка изменения размера
    def page_resize(e):
        # Полностью обновляем макет при изменении размера окна
        page.controls.clear()
        page.add(
            ft.Container(
                content=build_layout(),
                expand=True,
                bgcolor=YELLOW_LIGHT,
            )
        )
        page.update()

    page.on_resize = page_resize

    # Возвращаем контейнер с адаптивным макетом
    return ft.Container(
        content=build_layout(),
        expand=True,
        bgcolor=YELLOW_LIGHT,
    )
