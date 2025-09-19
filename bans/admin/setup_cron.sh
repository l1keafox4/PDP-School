#!/bin/bash

# Скрипт для настройки cron задачи для проверки банов без пруфов
# Запускать от пользователя, под которым работает веб-сервер (обычно www-data)

# Добавить задачу в crontab для запуска каждые 10 минут
CRON_JOB="*/10 * * * * php /var/www/html/bans/admin/auto_unban_checker.php > /var/www/html/bans/PLUGIN_DEVELOPING/cron_output.log 2>&1"

# Путь к текущему скрипту
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

# Убедиться, что лог-директория существует
mkdir -p "${SCRIPT_DIR}/../PLUGIN_DEVELOPING"

echo "Настройка cron задачи для автоматической проверки банов без пруфов..."

# Проверяем, существует ли уже такая задача
EXISTING_CRON=$(crontab -l 2>/dev/null | grep "auto_unban_checker.php")

if [ -n "$EXISTING_CRON" ]; then
    echo "Задача уже существует в crontab:"
    echo "$EXISTING_CRON"
else
    # Добавляем новую задачу
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Задача добавлена в crontab. Проверка будет выполняться каждые 10 минут."
fi

echo "Настройка завершена. Проверьте работу скрипта через некоторое время."
echo "Логи будут записываться в: ${SCRIPT_DIR}/../PLUGIN_DEVELOPING/auto_unban_log.txt"
