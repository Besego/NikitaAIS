import flet as ft

from pages.login_page import login_view
from pages.registration_page import registration_view
from pages.user_page import user_view
from pages.admin_page import admin_view
from pages.create_component_page import create_component_view


def main(page: ft.Page):
    page.title = "KS AIS"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    static_views = {
        "/login": login_view(page),
        "/registration": registration_view(page),
        "/admin": admin_view(page),
    }

    def route_change(route):
        page.views.clear()
        view_to_append = None
        current_route = page.route

        if current_route.startswith("/user/"):
            parts = current_route.split("/")
            if len(parts) == 3:
                user_id = parts[2]
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
        elif current_route == "/admin":
            view_to_append = admin_view(page)

        elif (
            current_route == "/create_component"
        ):
            view_to_append = create_component_view(
                page
            )  # create_component_view возвращает ft.View
        else:
            view_content = static_views.get(current_route)
            if view_content is None:
                view_content = static_views["/login"]
                current_route = "/login"

            if view_to_append is None and view_content is not None:
                view_to_append = ft.View(
                    route=current_route,
                    controls=[view_content],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    padding=0,
                )
            elif view_to_append is None and view_content is None:
                view_to_append = ft.View(
                    route="/login",
                    controls=[ft.Text("Ошибка: страница входа не найдена.")],
                )

        # Добавляем подготовленное представление
        if view_to_append:
            page.views.append(view_to_append)
        else:
            print(f"Error: No view could be determined for route {current_route}")
            page.views.append(
                ft.View(route="/login", controls=[ft.Text("Ошибка маршрутизации.")])
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Начальный маршрут
    if page.session.contains_key("user_id"):
        user_id = page.session.get("user_id")
        page.go(f"/user/{user_id}")
    else:
        page.go("/login")


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
