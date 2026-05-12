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

#### Локальная разработка
```bash
# Установка зависимостей
pip install -r requirements.txt

# Создать .env из примера и заполнить секреты
cp .env.example .env

# Запуск
python src/main.py
```

#### Docker
```bash
# Собрать образ
docker build -t bridge-bot .

# Запустить через docker-compose
docker-compose up -d
```

## 📚 API

Бридж предоставляет HTTP API для внешней интеграции.

### POST /send
Отправить текстовое сообщение во все подключенные сети.

```bash
curl -X POST http://localhost:8000/send \
  -H "Content-Type: application/json" \
  -H "x-token: secret-bridge-token" \
  -d '{"sender_id":"System","text":"Hello from API"}'
```

### POST /webhooks/teams
Принимает вебхуки от Microsoft Teams. Требуется настройка в Azure.

## 🧪 Тестирование

```bash
python -m pytest tests/ -v
```

## 🧹 Вспомогательные команды

```bash
make help   # показать все команды
make lint   # запустить линтеры
make clean  # очистить кеш и временные файлы
```

## ⚙️ Структура конфигурации

- `config/bridge_config.yaml` — список синхронизируемых чатов
- `.env` — секреты и параметры подключения

## 🔄 Как это работает

1. Адаптеры (Telegram, Matrix, Teams) получают входящие сообщения через polling/вебхуки.
2. Сообщение приводится к унифицированному формату `BridgeMessage`.
3. Ядро (`BridgeEngine`) проверяет на дубликаты через `StateManager`.
4. Сообщение рассылается во все остальные сети, исключая исходную.
5. Временные файлы автоматически удаляются после обработки.

## 📂 Структура проекта

```
.
├── config/
│   ├── bridge_config.yaml
│   └── settings.py
├── src/
│   ├── adapters/
│   │   ├── base.py
│   │   ├── telegram_adapter.py
│   │   ├── matrix_adapter.py
│   │   └── teams_adapter.py
│   ├── core/
│   │   ├── engine.py
│   │   └── state.py
│   ├── api/
│   │   └── server.py
│   ├── utils/
│   │   └── media.py
│   └── main.py
├── tests/
├── .github/workflows/ci.yml
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── requirements.txt
└── README.md
```

## 🔧 Устранение неполадок

- **Telegram не подключается**: Проверьте `TG_TOKEN` в `.env` и доступность серверов Telegram.
- **Matrix возвращает ошибки**: Убедитесь, что `MATRIX_USER` и `MATRIX_PASSWORD` верны, и пользователь состоит в указанных комнатах.
- **Teams не отправляет сообщения**: Проверьте настройки Azure AD и валидность токена OAuth2."