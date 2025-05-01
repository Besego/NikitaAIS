import flet as ft
import re  # Для проверки формата email
import time  # Для небольшой задержки и отладки

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
from models.models import UserRoleEnum


def login_view(page: ft.Page):
    """Создает представление страницы авторизации."""

    # Состояние загрузки
    is_logging_in = False
    
    # Тексты с ошибками
    email_error_text = ft.Text("", color=ft.colors.RED_500, size=12)
    password_error_text = ft.Text("", color=ft.colors.RED_500, size=12)
    
    # Функция для валидации email
    def is_valid_email(email):
        # Простая проверка наличия @ и точки после @
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None
    
    # Обработчики навигации
    def go_to_registration(e):
        page.go("/registration")

    # Обработчик изменения в поле email
    def email_changed(e):
        # Сбрасываем ошибку при редактировании поля
        email_error_text.value = ""
        email_field.border_color = PINK_MEDIUM
        page.update()
    
    # Обработчик изменения в поле пароля
    def password_changed(e):
        # Сбрасываем ошибку при редактировании поля
        password_error_text.value = ""
        password_field.border_color = PINK_MEDIUM
        page.update()

    # Поля ввода
    email_field = ft.TextField(
        label="Почта",
        width=300,
        keyboard_type=ft.KeyboardType.EMAIL,
        border_color=PINK_MEDIUM,
        focused_border_color=YELLOW_DARK,
        color=TEXT,
        on_change=email_changed,
    )
    
    password_field = ft.TextField(
        label="Пароль",
        width=300,
        password=True,
        can_reveal_password=True,
        border_color=PINK_MEDIUM,
        focused_border_color=YELLOW_DARK,
        color=TEXT,
        on_change=password_changed,
    )

    # Создаем кнопку как отдельный объект
    login_button = ft.ElevatedButton(
        text="Войти",
        width=300,
        bgcolor=PINK_MEDIUM,
        color=YELLOW_LIGHT,
    )
    
    # Индикатор загрузки
    login_progress = ft.Row(
        [
            ft.ProgressRing(color=PINK_MEDIUM, width=20, height=20),
            ft.Text("Вход...", color=TEXT),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    
    # Контейнер для переключения между кнопкой и индикатором
    login_button_container = ft.Container(
        content=login_button,
        width=300,
        alignment=ft.alignment.center,
    )

    # Отладочное сообщение
    debug_text = ft.Text("", color=TEXT, size=10)

    # Обработчик нажатия кнопки входа
    def login_click(e):
        nonlocal is_logging_in
        
        # Если уже идет процесс входа, не обрабатываем повторные нажатия
        if is_logging_in:
            return
            
        # Валидация полей
        has_errors = False
        
        # Проверка email
        if not email_field.value:
            email_error_text.value = "Введите email"
            email_field.border_color = ft.colors.RED_500
            has_errors = True
        elif not is_valid_email(email_field.value):
            email_error_text.value = "Некорректный формат email"
            email_field.border_color = ft.colors.RED_500
            has_errors = True
        else:
            email_error_text.value = ""
            email_field.border_color = PINK_MEDIUM
        
        # Проверка пароля
        if not password_field.value:
            password_error_text.value = "Введите пароль"
            password_field.border_color = ft.colors.RED_500
            has_errors = True
        else:
            password_error_text.value = ""
            password_field.border_color = PINK_MEDIUM
        
        page.update()
        
        if has_errors:
            return
        
        # Показываем индикатор загрузки
        is_logging_in = True
        debug_text.value = "Начинаем авторизацию..."
        login_button_container.content = login_progress
        page.update()
        
        # Задержка для отображения индикатора загрузки
        time.sleep(0.5)

        try:
            debug_text.value = "Проверка учетных данных..."
            page.update()
            
            # Проверяем учетные данные пользователя
            success, user_data = db_manager.verify_user(
                email_field.value, password_field.value
            )

            debug_text.value = f"Результат авторизации: {success}, {user_data}"
            page.update()
            
            if success and user_data:
                debug_text.value = "Авторизация успешна, сохраняем сессию..."
                page.update()
                
                # Сохраняем ID пользователя в сессии
                try:
                    page.session.set("user_id", user_data["id"])
                    page.session.set("user_name", user_data["name"])
                    # Преобразуем Enum в строку перед сохранением
                    user_role = (
                        str(user_data["role"].value)
                        if isinstance(user_data["role"], UserRoleEnum)
                        else user_data["role"]
                    )
                    page.session.set("user_role", user_role)
                    
                    debug_text.value = f"Сессия: user_id={page.session.get('user_id')}, name={page.session.get('user_name')}, role={page.session.get('user_role')}"
                    page.update()
                    
                    # Показываем успешное сообщение
                    page.snack_bar = ft.SnackBar(
                        ft.Text(f"Добро пожаловать, {user_data['name']}!"), 
                        bgcolor=PINK_DARK,
                        open=True
                    )
                    page.update()
                    
                    # Очистка полей
                    email_field.value = ""
                    password_field.value = ""
                    
                    # Небольшая задержка перед перенаправлением
                    time.sleep(0.5)
                    
                    # Перенаправление в зависимости от роли
                    user_id = user_data["id"]
                    debug_text.value = f"Перенаправление... Роль: {user_role}"
                    page.update()
                    
                    if user_role == UserRoleEnum.ADMIN.value:
                        debug_text.value = "Переход на страницу админа..."
                        page.update()
                        page.go("/admin")
                    else:
                        debug_text.value = f"Переход на страницу пользователя {user_id}..."
                        page.update()
                        page.go(f"/user/{user_id}")
                        
                except Exception as e:
                    debug_text.value = f"Ошибка сессии: {str(e)}"
                    page.update()
                    page.snack_bar = ft.SnackBar(
                        ft.Text(f"Ошибка при сохранении данных сессии: {str(e)}"), 
                        bgcolor=ft.colors.RED_500,
                        open=True
                    )
                    
                    # Возвращаем кнопку в исходное состояние
                    is_logging_in = False
                    login_button_container.content = login_button
                    page.update()
                    
            else:
                debug_text.value = "Неверные учетные данные"
                page.update()
                # Показываем ошибку
                page.snack_bar = ft.SnackBar(
                    ft.Text("Неверная почта или пароль."), 
                    bgcolor=ft.colors.RED_500,
                    open=True
                )
                
                # Возвращаем кнопку в исходное состояние
                is_logging_in = False
                login_button_container.content = login_button
                page.update()
                
        except Exception as e:
            debug_text.value = f"Исключение: {str(e)}"
            page.update()
            # Показываем ошибку
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Ошибка авторизации: {str(e)}"), 
                bgcolor=ft.colors.RED_500,
                open=True
            )
            
            # Возвращаем кнопку в исходное состояние
            is_logging_in = False
            login_button_container.content = login_button
            page.update()
        finally:
            # Возвращаем кнопку в исходное состояние
            is_logging_in = False
            login_button_container.content = login_button
            page.update()

    # Устанавливаем обработчик для кнопки
    login_button.on_click = login_click

    # Текст-ссылка для перехода на регистрацию
    register_link = ft.TextButton(
        content=ft.Text("Нет аккаунта? Зарегистрироваться", color=PINK_DARK, size=14),
        on_click=go_to_registration,
    )

    # Контейнер для формы
    form_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Авторизация",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=PINK_DARK,
                ),
                email_field,
                email_error_text,  # Текст с ошибкой для email
                password_field,
                password_error_text,  # Текст с ошибкой для пароля
                ft.Container(height=10),  # Небольшой отступ
                login_button_container,  # Контейнер с кнопкой/индикатором
                debug_text,  # Отладочный текст
                ft.Container(height=5),  # Небольшой отступ
                register_link,  # Добавляем ссылку
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
        ),
        padding=ft.padding.all(20),
        border_radius=ft.border_radius.all(10),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[PINK_LIGHT, YELLOW_LIGHT],
        ),
        alignment=ft.alignment.center,
        expand=True,
    )

    return form_container
