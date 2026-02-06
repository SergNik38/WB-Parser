# Руководство по развертыванию (Deployment Guide)

Чтобы запустить парсер на сервере и сделать его доступным через интернет, выполните следующие шаги.

## 1. Аренда сервера (VPS)
Вам понадобится виртуальный сервер (VPS).
- **ОС**: Ubuntu 22.04 LTS (рекомендуется)
- **Характеристики**: Минимальные (1 CPU, 1-2 GB RAM, 10-20 GB SSD) достаточно.
- **Провайдеры**: Timeweb, Reg.ru, Aeza, DigitalOcean, Hetzner и др.

## 2. Подготовка сервера
Подключитесь к серверу по SSH:
```bash
ssh root@your_server_ip
```

### Установите Docker и Docker Compose
Выполните команды:
```bash
apt update && apt install -y curl
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

## 3. Загрузка проекта на сервер
Самый простой способ — скопировать файлы с вашего компьютера на сервер.

**Вариант А: Если вы используете Git (рекомендуется)**
1. Залейте проект на GitHub/GitLab.
2. На сервере:
   ```bash
   git clone https://github.com/your-username/wb-parser.git
   cd wb-parser
   ```

**Вариант Б: Копирование через SCP (если нет Git)**
С вашего локального компьютера выполните:
```bash
# Находясь в папке проекта
scp -r . root@your_server_ip:/root/wb-parser
```

## 4. Запуск приложения
Зайдите в папку проекта на сервере:
```bash
cd /root/wb-parser
```
Запустите контейнер:
```bash
docker compose up -d --build
```

Приложение запустится и будет работать в фоне.
Оно будет доступно по адресу: `http://your_server_ip:8000`

## 5. Важное: Прокси (Proxy)
Wildberries блокирует IP-адреса хостинг-провайдеров. **Без прокси парсер на сервере работать не будет (будет ошибка 429).**

1. Купите **Резидентные (Residential)** или **Мобильные** прокси (IPv4).
2. Отредактируйте файл `scraper.py` на сервере:
   ```bash
   nano scraper.py
   ```
   Найдите строку создания клиента и добавьте прокси:
   ```python
   # Пример
   async with httpx.AsyncClient(headers=self.headers, proxies="http://login:pass@ip:port", http2=True) as client:
   ```
3. Перезапустите приложение:
   ```bash
   docker compose restart
   ```

## 6. (Дополнительно) Домен и HTTPS
Если вы хотите красивый домен (например, `wbparser.com`) и HTTPS:
1. Купите домен и направьте A-запись на IP сервера.
2. Установите Nginx и Certbot.
   *Это более сложный шаг, для MVP можно использовать прямой доступ по IP.*
