"# 🌉 Multi-Platform Bridge (Telegram ↔ Matrix ↔ MS Teams)

Профессиональный двусторонний бридж для синхронизации сообщений и медиафайлов между тремя популярными платформами коммуникации.

## 🚀 Основные возможности
- **Двусторонняя синхронизация**: Сообщения из одного мессенджера мгновенно появляются в двух других.
- **Поддержка медиа**: Пересылка файлов и документов между платформами.
- **HTTP API**: Возможность отправлять сообщения в любую из подключенных сетей через внешний REST API.
- **Защита от циклов**: Интеллектуальный State Manager предотвращает бесконечную пересылку одного и того же сообщения (эхо).
- **Модульная архитектура**: Легкое добавление новых адаптеров (например, Slack, Discord).

## 🛠 Установка и сборка

### 1. Требования
- Python 3.10 или выше
- Доступ к API Telegram (BotFather)
- Аккаунт/бот в Matrix Synapse
- Регистрация приложения в Microsoft Azure (для MS Teams)

### 2. Развертывание
```bash
# Клонирование репозитория
git clone https://github.com/kernelpanic700/multi-platform-bridge.git
cd multi-platform-bridge

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
# venv\\Scripts\\activate # Для Windows

# Установка зависимостей
pip install -r requirements.txt
```

### 3. Настройка конфигурации
Создайте файл `.env` в корне проекта на основе примера:

```env
# --- Telegram ---
TG_TOKEN=your_bot_token
TG_CHAT_ID=123456789

# --- Matrix ---
MATRIX_HOMESERVER=https://matrix.org
MATRIX_USER=@bridge_bot:matrix.org
MATRIX_PASSWORD=your_password
MATRIX_ROOM_ID=!roomid:matrix.org

# --- MS Teams ---
TEAMS_TENANT_ID=your_tenant_id
TEAMS_CLIENT_ID=your_client_id
TEAMS_CLIENT_SECRET=your_client_secret
TEAMS_CHANNEL_ID=your_channel_id

# --- HTTP API ---
API_PORT=8000
API_TOKEN=your_secure_api_token
```

### 4. Запуск
```bash
python src/main.py
```

## 🔌 Использование HTTP API

Бридж предоставляет API для интеграции с внешними системами.

**Эндпоинт**: `POST /send`

**Заголовки**:
- `X-Token`: Ваш `API_TOKEN` из файла `.env`
- `Content-Type`: `application/json`

**Тело запроса**:
```json
{
  \"text\": \"Привет из внешней системы!\",
  \"sender_id\": \"ExternalSystem\",
  \"file_path\": \"/path/to/file\", 
  \"file_name\": \"document.pdf\"
}
```

**Пример запроса через curl**:
```bash
curl -X POST \"http://localhost:8000/send\" \\
     -H \"X-Token: your_secure_api_token\" \\
     -H \"Content-Type: application/json\" \\
     -d '{\"text\": \"Привет всем через API!\", \"sender_id\": \"Admin\"}'
```

## 📐 Архитектура
Проект построен по паттерну «Адаптер»:
- `BridgeEngine`: Центральный узел, который маршрутизирует сообщения.
- `BaseAdapter`: Интерфейс, который должен реализовать каждый новый мессенджер.
- `StateManager`: Хранит историю сообщений для предотвращения зацикливания.
- `MediaUtils`: Унифицированный интерфейс для работы с файлами.
"