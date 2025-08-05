# Фінансовий Менеджер (REST API)
Цей проєкт є backend-системою для управління персональними фінансами користувача. Користувачі можуть створювати гаманці, додавати транзакції, генерувати звіти та відслідковувати витрати за категоріями.

## 🔧 Використані технології

- **Python 3.11**
- **Django**
- **Django REST Framework (DRF)**
- **JWT (аутентифікація)**
- **Swagger (документація API)**

---

## 🛠️ Як запустити проєкт локально

1. **Клонувати репозиторій**
   ```bash
   git clone https://github.com/DorogaSmerti/MoneyTracke.git
   cd MoneyTracker
2. Створити та активувати віртуальне середовище
   ```
   python -m venv venv
   source venv/bin/activate  # або venv\Scripts\activate для Windows
3. Встановити залежності
   ```
   pip install -r requirements.txt
5. Застосувати міграції
   ```
   python manage.py migrate
7. Запустити сервер
   ```
   python manage.py runserver
