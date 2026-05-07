"# 🌉 Multi-Platform Bridge (Telegram ↔ Matrix ↔ MS Teams)

Профессиональный двусторонний бридж для синхронизации сообщений и медиафайлов между несколькими чатами и комнатами на разных коммуникационных платформах.

## 🚀 Основные возможности
- **Многоканальная синхронизация**: Возможность подключения нескольких чатов/комнат от каждой платформы. Все сообщения из любого подключенного канала рассылаются во все остальные.
- **Двусторонняя синхронизация медиа**: Полноценная пересылка файлов и документов между Telegram и Matrix (включая автоматическое временное хранение).
- **Интеллектуальная защита от циклов**: Обновленный `StateManager` с использованием LRU-кэша предотвращает «эхо»-эффект и утечки памяти, используя уникальные ID сообщений.
- **Интеграция с MS Teams**: Полноценная поддержка через Microsoft Graph API с использованием OAuth2 (Client Credentials flow) и вебхуками.
- **HTTP API**: Возможность отправлять текстовые сообщения и файлы в любую из сетей через внешний REST API.
- **Безопасная конфигурация**: Разделение секретов (в `.env`) и структуры сети (в `config/bridge_config.yaml`).

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

# Установка зависимостей
pip install -r requirements.txt
```

### 3. Настройка конфигурации

#### А. Секреты (`.env`)
Создайте файл `.env` в корне проекта:
```env
# --- Telegram ---
TG_TOKEN=your_bot_token

# --- Matrix ---
MATRIX_HOMESERVER=https://matrix.org
MATRIX_USER=@bridge_bot:matrix.org
MATRIX_PASSWORD=your_password

# --- MS Teams ---
TEAMS_TENANT_ID=your_tenant_id
TEAMS_CLIENT_ID=your_client_id
TEAMS_CLIENT_SECRET=your_client_secret

# --- HTTP API ---
API_PORT=8000
API_TOKEN=your_secure_api_token
```

#### Б. Структура сети (`config/bridge_config.yaml`)
В этом файле укажите ID всех чатов, которые должны быть связаны:
```yaml
telegram:
  chats: 
    - \"123456789\"
    - \"987654321\"

matrix:
  rooms: 
    - \"!room_id_1:matrix.org\"
    - \"!room_id_2:matrix.org\"

teams:
  channels: 
    - \"channel_id_1\"
```

### 4. Запуск
```bash
python src/main.py
```

## 🔌 Использование HTTP API

**Эндпоинт**: `POST /send`
**Заголовки**: `X-Token: your_secure_api_token`

**Тело запроса**:
```json
{
  \"text\": \"Привет всем!\",
  \"sender_id\": \"Admin\",
  \"file_path\": \"/path/to/file\", 
  \"file_name\": \"document.pdf\"
}
```

## 📐 Архитектура
- `BridgeEngine`: Центральный узел маршрутизации.
- `StateManager`: LRU-кэш для предотвращения зацикливания сообщений.
- `MediaUtils`: Система управления временными файлами для кросс-платформенной пересылки.
- `Adapters`: Модульные реализации для каждой платформы, поддерживающие списки каналов."