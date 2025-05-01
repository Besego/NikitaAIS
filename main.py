import flet as ft

# Импортируем представления страниц
from pages.login_page import login_view
from pages.registration_page import registration_view

from pages.user_page import user_view
from pages.admin_page import admin_view

# from pages.cart_page import cart_view
# from pages.orders_page import orders_view


def main(page: ft.Page):
    page.title = "KS AIS"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Словарь для хранения представлений по маршрутам (статичные маршруты)
    static_views = {
        "/login": login_view(page),
        "/registration": registration_view(page),
        "/admin": admin_view(page),
    }

    def route_change(route):
        page.views.clear()
        view_to_append = None  # Переименовали переменную для ясности
        current_route = page.route

        # Проверяем динамические маршруты
        if current_route.startswith("/user/"):
            parts = current_route.split("/")
            if len(parts) == 3:
                user_id = parts[2]
                # user_view уже возвращает ft.View
                view_to_append = user_view(page, user_id)
            else:
                # Если ID пользователя не указан, перенаправляем на логин
                view_content = static_views["/login"]
                current_route = "/login"
                view_to_append = ft.View(
                    route=current_route,
                    controls=[view_content],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    padding=0,
                )
        # elif current_route.startswith("/cart/"): # Добавьте обработку других динамических маршрутов, если они возвращают View
        #     parts = current_route.split("/")
        #     if len(parts) == 3:
        #         user_id = parts[2]
        #         view_to_append = cart_view(page, user_id) # Предполагая, что cart_view возвращает View
        #     else:
        #         view_content = static_views["/login"]
        #         current_route = "/login"
        #         view_to_append = ft.View(
        #             route=current_route,
        #             controls=[view_content],
        #             vertical_alignment=ft.MainAxisAlignment.CENTER,
        #             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        #             padding=0,
        #         )
        # elif current_route.startswith("/orders/"): # Добавьте обработку других динамических маршрутов, если они возвращают View
        #     parts = current_route.split("/")
        #     if len(parts) == 3:
        #         user_id = parts[2]
        #         view_to_append = orders_view(page, user_id) # Предполагая, что orders_view возвращает View
        #     else:
        #         view_content = static_views["/login"]
        #         current_route = "/login"
        #         view_to_append = ft.View(
        #             route=current_route,
        #             controls=[view_content],
        #             vertical_alignment=ft.MainAxisAlignment.CENTER,
        #             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        #             padding=0,
        #         )
        else:
            # Обрабатываем статичные маршруты или случаи, когда динамический маршрут не вернул View
            view_content = static_views.get(current_route)
            if view_content is None:
                view_content = static_views["/login"]
                current_route = "/login"

            # Для статичных маршрутов создаем View здесь
            view_to_append = ft.View(
                route=current_route,
                controls=[view_content],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                padding=0,
            )

        # Добавляем подготовленное представление
        if view_to_append:
            page.views.append(view_to_append)
        else:
            # Обработка случая, если view_to_append не был создан (маловероятно с текущей логикой, но для безопасности)
            print(f"Error: No view could be determined for route {current_route}")
            # Можно перенаправить на страницу логина по умолчанию
            login_view_content = static_views["/login"]
            page.views.append(
                ft.View(
                    route="/login",
                    controls=[login_view_content],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    padding=0,
                )
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Устанавливаем начальный маршрут
    page.go("/login")


# Запуск приложения
ft.app(target=main)
