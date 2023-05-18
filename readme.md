# Home work 10

Агрегатор валют з багатьох провайдерів

## Розгортаня проекту (команди для Windows)

1. Ініціалізувати GIT, склонувати репозиторій
    ```bash
    git init
    git clone https://github.com/AtamanAA/hillel_py_pro_lesson12.git    
    ```
2. Встановити venv та активувати його
    ```bash
    python -m venv venv
   .\venv\Scripts\activate    
    ```
3. Інсталювати сторонні пакети у venv
    ```bash
    python -m pip install -r requirements.txt    
    ```

4. Для запуску процессу [RabbitMQ](https://www.rabbitmq.com) в окремому терміналі виконати команду (переконатися що [Docker Desktop](https://www.docker.com/products/docker-desktop/) запущений )
    ```bash
    docker run -d -p 5672:5672 rabbitmq    
    ```
5. У окремому терміналі перейти до деректорії проекту та запустити процесс [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)
    ```bash
    .\venv\Scripts\activate
    celery -A exchange_rates worker -l info -P gevent   
    ```
6. 5. У окремому терміналі перейти до деректорії проекту та запустити процесс [Celery Beat](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html)
    ```bash
    .\venv\Scripts\activate
    celery -A exchange_rates beat -l INFO   
    ```
7. Повернутися до першого терміналу (де активоване venv) та виконати запуск основного web-серверу
    ```bash
    python manage.py runserver   
    ```
7. В браузері перейти на головну сторінку
    http://127.0.0.1:8000/
