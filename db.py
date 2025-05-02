from datetime import datetime
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload
from dotenv import load_dotenv
from sqlalchemy import func
from models.models import Base
import bcrypt

# from cart import cart_manager
from models.models import User, UserRoleEnum, Component, Sale


load_dotenv()


class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.Session = None
        self.connect()

    # def connect(self):
    #     """Метод для подключения к базе данных."""
    #     try:
    #         db_name = os.getenv("DB_NAME")
    #         db_user = os.getenv("DB_USER")
    #         db_password = os.getenv("DB_PASSWORD")
    #         db_host = os.getenv("DB_HOST")
    #         db_port = os.getenv("DB_PORT")

    #         if not all([db_name, db_user, db_password, db_host, db_port]):
    #             print(
    #                 "Ошибка: Не все переменные окружения для подключения к БД установлены."
    #             )
    #             return

    #         db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    #         self.engine = create_engine(db_url)
    #         self.Session = sessionmaker(bind=self.engine)
    #         print("Успешное подключение к базе данных.")
    #     except Exception as e:
    #         print(f"Ошибка подключения к базе данных: {e}")
    
    def connect(self):
        """Метод для подключения к базе данных."""
        try:
            db_url = f"sqlite:///nikitos.db"
            self.engine = create_engine(
                db_url, connect_args={"check_same_thread": False}
            )
            self.Session = sessionmaker(bind=self.engine)

            Base.metadata.create_all(self.engine)
            
            print("Успешное подключение к базе данных.")
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
    
    def create_tables(self):
        """Создание таблиц в базе данных."""
        try:
            # Создание всех таблиц по моделям
            Base.metadata.create_all(self.engine)
            print("Таблицы успешно созданы.")
        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}")
    
    def inset_data(self):
        """Метод для вставки начальных данных в базу данных."""
        try:
            session = self.Session()
            users_data = [
                {'username': 'john_doe', 'password': '$2b$12$ksgIxYJLSqvj9XU4FvH6B.tCUnvGdnljH5fxlEu7gPti.0TbfAotW', 'email': 'john@example.com', 'role': 'SUPPLIER'},
                {'username': 'admin_user', 'password': '$2b$12$ksgIxYJLSqvj9XU4FvH6B.tCUnvGdnljH5fxlEu7gPti.0TbfAotW', 'email': 'admin@example.com', 'role': 'ADMIN'},
                {'username': 'mary_smith', 'password': '$2b$12$ksgIxYJLSqvj9XU4FvH6B.tCUnvGdnljH5fxlEu7gPti.0TbfAotW', 'email': 'mary@example.com', 'role': 'SUPPLIER'},
                {'username': 'test_supplier', 'password': '$2b$12$ksgIxYJLSqvj9XU4FvH6B.tCUnvGdnljH5fxlEu7gPti.0TbfAotW', 'email': 'test@example.com', 'role': 'SUPPLIER'},
                {'username': 'alice_jones', 'password': '$2b$12$ksgIxYJLSqvj9XU4FvH6B.tCUnvGdnljH5fxlEu7gPti.0TbfAotW', 'email': 'alice@example.com', 'role': 'SUPPLIER'},
                {'username': 'bob_brown', 'password': '$2b$12$ksgIxYJLSqvj9XU4FvH6B.tCUnvGdnljH5fxlEu7gPti.0TbfAotW', 'email': 'bob@example.com', 'role': 'SUPPLIER'},
                {'username': 'clara_wilson', 'password': '$2b$12$ksgIxYJLSqvj9XU4FvH6B.tCUnvGdnljH5fxlEu7gPti.0TbfAotW', 'email': 'clara@example.com', 'role': 'SUPPLIER'},
                {'username': 'david_lee', 'password': '$2b$12$ksgIxYJLSqvj9XU4FvH6B.tCUnvGdnljH5fxlEu7gPti.0TbfAotW', 'email': 'david@example.com', 'role': 'SUPPLIER'},
                {'username': 'emma_taylor', 'password': '$2b$12$ksgIxYJLSqvj9XU4FvH6B.tCUnvGdnljH5fxlEu7gPti.0TbfAotW', 'email': 'emma@example.com', 'role': 'SUPPLIER'},
                {'username': 'admin_two', 'password': '$2b$12$ksgIxYJLSqvj9XU4FvH6B.tCUnvGdnljH5fxlEu7gPti.0TbfAotW', 'email': 'admin2@example.com', 'role': 'ADMIN'},
                {'username': 'test@test.com', 'password': '$2b$12$ksgIxYJLSqvj9XU4FvH6B.tCUnvGdnljH5fxlEu7gPti.0TbfAotW', 'email': 'test@test.com', 'role': 'SUPPLIER'},
                {'username': 'admin@admin.com', 'password': '$2b$12$Nd0GfmUFkIgPGz84IVGkBu8Q6CBk/ccR2IypacyoswCHLdgGm6XDS', 'email': 'admin@admin.com', 'role': 'ADMIN'},
                
            ]

            # Mock data for components
            components_data = [
                {'user_id': 1, 'name': 'Resistor 1k', 'description': '1k Ohm resistor', 'quantity': 1000, 'price': 0.50},
                {'user_id': 1, 'name': 'Capacitor 10uF', 'description': '10uF ceramic capacitor', 'quantity': 500, 'price': 1.20},
                {'user_id': 3, 'name': 'LED Red', 'description': 'Red LED 5mm', 'quantity': 2000, 'price': 0.30},
                {'user_id': 3, 'name': 'Arduino Uno', 'description': 'Arduino Uno microcontroller', 'quantity': 50, 'price': 25.00},
                {'user_id': 4, 'name': 'Transistor 2N3904', 'description': 'NPN transistor', 'quantity': 800, 'price': 0.75},
                {'user_id': 5, 'name': 'Diode 1N4148', 'description': 'Signal diode', 'quantity': 1500, 'price': 0.20},
                {'user_id': 6, 'name': 'Resistor 10k', 'description': '10k Ohm resistor', 'quantity': 1200, 'price': 0.60},
                {'user_id': 7, 'name': 'LED Blue', 'description': 'Blue LED 5mm', 'quantity': 1800, 'price': 0.35},
                {'user_id': 8, 'name': 'Capacitor 100uF', 'description': '100uF electrolytic capacitor', 'quantity': 300, 'price': 1.50},
                {'user_id': 9, 'name': 'Raspberry Pi 4', 'description': 'Raspberry Pi 4 Model B', 'quantity': 20, 'price': 55.00},
            ]

            # Mock data for sales
            sales_data = [
                {'component_id': 1, 'user_id': 1, 'quantity': 100, 'total_price': 50.00, 'sale_date': datetime(2025, 4, 1, 10, 30)},
                {'component_id': 2, 'user_id': 1, 'quantity': 50, 'total_price': 60.00, 'sale_date': datetime(2025, 4, 2, 14, 15)},
                {'component_id': 3, 'user_id': 3, 'quantity': 200, 'total_price': 60.00, 'sale_date': datetime(2025, 4, 3, 9, 0)},
                {'component_id': 4, 'user_id': 3, 'quantity': 5, 'total_price': 125.00, 'sale_date': datetime(2025, 4, 4, 16, 20)},
                {'component_id': 5, 'user_id': 4, 'quantity': 100, 'total_price': 75.00, 'sale_date': datetime(2025, 4, 5, 11, 45)},
                {'component_id': 6, 'user_id': 5, 'quantity': 300, 'total_price': 60.00, 'sale_date': datetime(2025, 4, 6, 13, 0)},
                {'component_id': 7, 'user_id': 6, 'quantity': 150, 'total_price': 90.00, 'sale_date': datetime(2025, 4, 7, 15, 30)},
                {'component_id': 8, 'user_id': 7, 'quantity': 200, 'total_price': 70.00, 'sale_date': datetime(2025, 4, 8, 8, 45)},
                {'component_id': 9, 'user_id': 8, 'quantity': 50, 'total_price': 75.00, 'sale_date': datetime(2025, 4, 9, 17, 0)},
                {'component_id': 10, 'user_id': 9, 'quantity': 2, 'total_price': 110.00, 'sale_date': datetime(2025, 4, 10, 12, 0)},
            ]

            # Insert users
            for user_data in users_data:
                user = User(**user_data)
                session.add(user)
            
            # Commit users to ensure user_id is generated
            session.commit()

            # Insert components
            for component_data in components_data:
                component = Component(**component_data)
                session.add(component)
            
            # Commit components to ensure component_id is generated
            session.commit()

            # Insert sales
            for sale_data in sales_data:
                sale = Sale(**sale_data)
                session.add(sale)
            
            # Commit all changes
            session.commit()
            session.close()
        except Exception as e:
            session.rollback()
            print(f"Ошибка при вставке начальных данных: {e}")
            session.close()
            return False


    # def connect(self):
    #     """Подключается к файлу SQLite"""
    #     try:
    #         # Файл БД можно задать через переменную окружения DB_FILE
    #         db_file = os.getenv("DB_FILE", "harukoshop.db")
    #         db_url = f"sqlite:///{db_file}"

    #         # check_same_thread=False позволяет использовать один движок в нескольких потоках UI-приложения
    #         self.engine = create_engine(
    #             db_url, connect_args={"check_same_thread": False}
    #         )
    #         self.Session = sessionmaker(bind=self.engine)

    #         # Если таблиц ещё нет – создаём их по моделям
    #         from models.models import Base  # импорт внутри, чтобы избежать циклических

    #         Base.metadata.create_all(self.engine)

    #         print(f"Успешное подключение к SQLite: {db_file}")
    #     except Exception as e:
    #         print(f"Ошибка подключения к базе данных: {e}")

    def register_user(self, username, email, password, role=UserRoleEnum.SUPPLIER):
        """Метод для регистрации нового пользователя."""
        if not self.Session:
            print("Ошибка: Сессия базы данных не инициализирована.")
            return False, "Ошибка подключения к базе данных."

        session = self.Session()
        try:
            # Проверка, существует ли пользователь с таким email
            existing_user = session.query(User).filter_by(email=email).first()
            if existing_user:
                return False, "Пользователь с таким email уже существует."

            # Хеширование пароля
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            # Создание нового пользователя
            new_user = User(
                username=username,
                email=email,
                password=hashed_password.decode("utf-8"),  # Сохраняем хеш как строку
                role=role,
            )
            session.add(new_user)
            session.commit()
            print(f"Пользователь {email} успешно зарегистрирован.")
            return True, "Регистрация прошла успешно!"
        except Exception as e:
            session.rollback()
            print(f"Ошибка при регистрации пользователя: {e}")
            return False, f"Ошибка при регистрации: {e}"
        finally:
            session.close()

    def verify_user(self, email, password):
        """
        Проверяет учетные данные пользователя.
        """
        if not self.Session:
            return False, None

        session = self.Session()
        try:
            # Находим пользователя по email
            user = session.query(User).filter(User.email == email).first()

            if not user:
                return False, None

            # Проверяем пароль
            if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                # Возвращаем данные о пользователе
                user_data = {
                    "id": user.user_id,
                    "name": user.username,
                    "role": user.role,
                    "email": user.email,
                }
                print(user_data)
                return True, user_data
            else:
                return False, None
        except Exception as e:
            print(f"Ошибка при проверке пользователя: {e}")
            return False, None
        finally:
            session.close()

    def get_components_by_user(self, user_id: int):
        """Загрузка всех комплектующих определенного пользователя."""
        session = self.Session()
        try:
            components = session.query(Component).filter(Component.user_id == user_id).all()
            return components
        finally:
            session.close()

    def get_all_components(self):
        """Загрузка всех комплектующих всех пользователей."""
        session = self.Session()
        try:
            components = session.query(Component).all()
            return components
        finally:
            session.close()

    def get_users_by_sales_count(self):
        """Отображение списка пользователей по количеству проданных комплектующих."""
        session = self.Session()
        try:
            users = session.query(
                User,
                func.count(Sale.sale_id).label('sales_count')
            ).outerjoin(Sale, User.user_id == Sale.user_id).group_by(User.user_id).order_by(func.count(Sale.sale_id).desc()).all()
            return users
        finally:
            session.close()

    def get_sales_by_user(self, user_id: int):
        """Отображение списка всех продаж определенного пользователя."""
        session = self.Session()
        try:
            sales = session.query(Sale).filter(Sale.user_id == user_id).all()
            return sales
        finally:
            session.close()

    def create_component(self, user_id: int, name: str, description: str, quantity: int, price: float):
        """Создание нового комплектующего."""
        session = self.Session()
        try:
            new_component = Component(
                user_id=user_id,
                name=name,
                description=description,
                quantity=quantity,
                price=price
            )
            session.add(new_component)
            session.commit()
            return new_component
        except Exception as e:
            session.rollback()
            print(f"Ошибка при создании комплектующего: {e}")
            return None
        finally:
            session.close()

    # def get_all_sales(self):
    #     """Отображение списка всех продаж всех пользователей."""
    #     session = self.Session()
    #     try:
    #         sales = session.query(Sale).all()
    #         return sales
    #     finally:
    #         session.close()
    
    def get_all_sales(self):
        """Отображение списка всех продаж всех пользователей с предзагрузкой связанных данных."""
        session = self.Session()
        try:
            sales = session.query(Sale).options(
                joinedload(Sale.component),
                joinedload(Sale.user)
            ).all()
            return sales
        finally:
            session.close()
            
    def get_all_components(self):
        """Загрузка всех комплектующих всех пользователей."""
        session = self.Session()
        try:
            components = session.query(Component).all()
            return components
        finally:
            session.close()

    def get_all_users(self):
        """Получение всех пользователей."""
        session = self.Session()
        try:
            users = session.query(User).all()
            return users
        finally:
            session.close()        

    # def delete_user(self, user_id: int):
    #     """Удаление пользователя."""
    #     session = self.Session()
    #     try:
    #         user = session.query(User).filter(User.user_id == user_id).first()
    #         if user:
    #             session.delete(user)
    #             session.commit()
    #             return True
    #         return False
    #     except Exception as e:
    #         session.rollback()
    #         print(f"Ошибка при удалении пользователя: {e}")
    #         return False
    #     finally:
    #         session.close()

    # def delete_component(self, component_id: int):
    #     """Удаление комплектующего."""
    #     session = self.Session()
    #     try:
    #         component = session.query(Component).filter(Component.component_id == component_id).first()
    #         if component:
    #             session.delete(component)
    #             session.commit()
    #             return True
    #         return False
    #     except Exception as e:
    #         session.rollback()
    #         print(f"Ошибка при удалении комплектующего: {e}")
    #         return False
    #     finally:
    #         session.close()
    
    def delete_user(self, user_id: int):
        """Удаление пользователя и всех связанных данных."""
        session = self.Session()
        try:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                # Удаляем все продажи, связанные с комплектующими пользователя
                components = session.query(Component).filter(Component.user_id == user_id).all()
                for component in components:
                    session.query(Sale).filter(Sale.component_id == component.component_id).delete()
                # Удаляем все комплектующие пользователя
                session.query(Component).filter(Component.user_id == user_id).delete()
                # Удаляем самого пользователя
                session.delete(user)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Ошибка при удалении пользователя: {e}")
            return False
        finally:
            session.close()

    def delete_component(self, component_id: int):
        """Удаление комплектующего и всех связанных продаж."""
        session = self.Session()
        try:
            component = session.query(Component).filter(Component.component_id == component_id).first()
            if component:
                # Удаляем все продажи, связанные с этим комплектующим
                session.query(Sale).filter(Sale.component_id == component_id).delete()
                # Удаляем само комплектующее
                session.delete(component)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Ошибка при удалении комплектующего: {e}")
            return False
        finally:
            session.close()

    def delete_sale(self, sale_id: int):
        """Удаление продажи."""
        session = self.Session()
        try:
            sale = session.query(Sale).filter(Sale.sale_id == sale_id).first()
            if sale:
                session.delete(sale)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Ошибка при удалении продажи: {e}")
            return False
        finally:
            session.close()

    def create_sale(self, component_id: int, user_id: int, quantity: int):
        """Создание новой продажи."""
        session = self.Session()
        try:
            # Получаем комплектующее по component_id
            component = session.query(Component).filter(Component.component_id == component_id).first()
            if not component:
                print("Ошибка: Комплектующее не найдено.")
                return None
            if component.quantity < quantity:
                print("Ошибка: Недостаточно комплектующих для продажи.")
                return None
            
            # Рассчитываем общую стоимость
            total_price = component.price * quantity
            
            # Создаем новую продажу
            new_sale = Sale(
                component_id=component_id,
                user_id=user_id,
                quantity=quantity,
                total_price=total_price
            )
            
            # Уменьшаем количество комплектующих
            component.quantity -= quantity
            
            # Добавляем продажу и коммитим изменения
            session.add(new_sale)
            session.commit()
            return new_sale
        except Exception as e:
            # В случае ошибки откатываем транзакцию
            session.rollback()
            print(f"Ошибка при создании продажи: {e}")
            return None
        finally:
            session.close()        


db_manager = DatabaseManager()
db_manager.create_tables()
db_manager.inset_data()
