# Разработка распределённых программных систем
---
Данный репозиторий содержит в себе практические работы по курсу "Разработка распределённых программных систем".

**Работу выполнял:** студент 4 курса НИУ ВШЭ, Кирьянов Сергей, группы ПИ-21-3

---

### Структура репозитория
    DDSS/
    ├─ Labs/ - материалы по практическим работам
    ├─ src/ - исходный код программы

---

### Запуск 

1. Клонируйте репозиторий:
    ```
    git clone <URL>
    cd <DDSS>
    ```

2. Создайте виртуальное окружение:
    ```
    python -m venv venv
    ```

3. Активируйте виртуальное окружение:
    На Windows:
    ```
    venv\Scripts\activate
    ```
    На macOS/Linux:
    ```
    source venv/bin/activate
    ```

4. Установите зависимости:
    ```
    pip install -r requirements.txt
    ```

5. Проверка кода линтером:
    ```
    flake8 src
    ```

6. Запустите приложение:
    ```
    uvicorn src.main:app --reload
    ```
    Приложение будет запущено по адресу ```http://127.0.0.1:8000```
