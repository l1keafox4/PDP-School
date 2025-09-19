#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime
import logging
import mysql.connector
import requests
import json
import traceback
from typing import Dict, List, Optional, Tuple, Union

# Настройка логирования
logging.basicConfig(
    filename='/var/www/html/bans/PLUGIN_DEVELOPING/ban_system.log',
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("ban_system")

# Добавляем вывод в консоль для отладки
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Настройки базы данных
DB_CONFIG = {
    'host': '37.27.96.155',
    'port': 3306,
    'user': 'litebans',
    'password': 'limon1232',
    'database': 'litebans'
}

# Настройки Telegram API
TELEGRAM_BOT_TOKEN = '7665890197:AAE89GCrTvoL1C_F0HLNJpItW--crlrt91A'
TELEGRAM_CHAT_ID = '1400003638'

# Настройки Pterodactyl API
PTERO_API_KEY = 'ptlc_NsSejdgFgkg20Z8cLPkbMIV6ltsS4DV0KZi56g5CoiV'
PTERO_API_URL = 'https://panel.mchost.uz/api/client/servers/2ea62c18/command'

# Время ожидания для публикации пруфа (в секундах)
# 7200 секунд = 2 часа
PROOF_TIMEOUT = 7200  # Для производства: 2 часа 
# PROOF_TIMEOUT = 60  # Для тестирования: 1 минута

# Файлы для хранения времени последней проверки
LAST_CHECK_FILE = '/var/www/html/bans/PLUGIN_DEVELOPING/last_ban_check.txt'
LAST_UNBAN_CHECK_FILE = '/var/www/html/bans/PLUGIN_DEVELOPING/last_unban_check.txt'

def log_message(message: str, level: str = "info") -> None:
    """Записывает сообщение в лог с указанным уровнем"""
    if level.lower() == "info":
        logger.info(message)
    elif level.lower() == "error":
        logger.error(message)
    elif level.lower() == "warning":
        logger.warning(message)
    elif level.lower() == "debug":
        logger.debug(message)
    else:
        logger.info(message)

def get_db_connection():
    """Создает соединение с базой данных"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        log_message(f"Ошибка подключения к базе данных: {err}", "error")
        return None

def close_db_connection(conn):
    """Закрывает соединение с базой данных"""
    if conn and conn.is_connected():
        conn.close()

def send_telegram_message(message: str) -> bool:
    """Отправляет сообщение в Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            log_message(f"Сообщение в Telegram отправлено успешно")
            return True
        else:
            log_message(f"Ошибка отправки сообщения в Telegram: {response.text}", "error")
            return False
    except Exception as e:
        log_message(f"Исключение при отправке сообщения в Telegram: {e}", "error")
        return False

def execute_pterodactyl_command(command: str) -> bool:
    """Выполняет команду на сервере через Pterodactyl API"""
    try:
        headers = {
            "Authorization": f"Bearer {PTERO_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        data = {
            "command": command
        }
        
        response = requests.post(PTERO_API_URL, headers=headers, json=data)
        
        if response.status_code == 204:
            log_message(f"Команда '{command}' успешно выполнена на сервере")
            return True
        else:
            log_message(f"Ошибка выполнения команды '{command}': {response.text}", "error")
            return False
    except Exception as e:
        log_message(f"Исключение при выполнении команды '{command}': {e}", "error")
        return False

def get_last_check_timestamp(check_type: str = "ban") -> int:
    """Получает время последней проверки из файла"""
    file_path = LAST_CHECK_FILE if check_type == "ban" else LAST_UNBAN_CHECK_FILE
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                timestamp = int(f.read().strip())
                return timestamp
        else:
            # Если файл не существует, используем текущее время - 1 минуту
            # чтобы не получать слишком старые баны при первом запуске
            current_time = int(time.time())
            with open(file_path, 'w') as f:
                f.write(str(current_time - 60))
            return current_time - 60
    except Exception as e:
        log_message(f"Ошибка при чтении времени последней проверки: {e}", "error")
        # В случае ошибки возвращаем текущее время - 1 день
        return int(time.time()) - 86400

def update_last_check_timestamp(timestamp: int, check_type: str = "ban") -> None:
    """Обновляет время последней проверки в файле"""
    file_path = LAST_CHECK_FILE if check_type == "ban" else LAST_UNBAN_CHECK_FILE
    
    try:
        with open(file_path, 'w') as f:
            f.write(str(timestamp))
        log_message(f"Время последней проверки ({check_type}) обновлено: {timestamp}")
    except Exception as e:
        log_message(f"Ошибка при обновлении времени последней проверки: {e}", "error")

def get_helpers_list(conn) -> List[str]:
    """Получает список хелперов из базы данных"""
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT username FROM litebans_users WHERE role = 'helper'"
        cursor.execute(query)
        helpers = [row['username'] for row in cursor.fetchall()]
        
        if not helpers:
            log_message("Внимание: список хелперов пуст", "warning")
            return []
        
        log_message(f"Получен список хелперов: {', '.join(helpers)}")
        return helpers
    except Exception as e:
        log_message(f"Ошибка при получении списка хелперов: {e}", "error")
        return []
    finally:
        cursor.close()

def get_last_ban_id():
    """Возвращает последний известный ID бана"""
    last_ban_id_file = '/var/www/html/bans/PLUGIN_DEVELOPING/last_ban_id.txt'
    
    if os.path.exists(last_ban_id_file):
        try:
            with open(last_ban_id_file, 'r') as f:
                return int(f.read().strip())
        except (ValueError, IOError) as e:
            log_message(f"Ошибка при чтении последнего ID бана: {e}", "error")
            return 0
    return 0

def update_last_ban_id(ban_id):
    """Обновляет последний известный ID бана"""
    last_ban_id_file = '/var/www/html/bans/PLUGIN_DEVELOPING/last_ban_id.txt'
    
    try:
        with open(last_ban_id_file, 'w') as f:
            f.write(str(ban_id))
        log_message(f"Обновлен последний ID бана: {ban_id}")
        return True
    except IOError as e:
        log_message(f"Ошибка при обновлении последнего ID бана: {e}", "error")
        return False

def check_new_bans(conn):
    """Проверяет новые баны от хелперов и отправляет уведомления"""
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Проверяем, инициализирована ли система
        system_init_flag = '/var/www/html/bans/PLUGIN_DEVELOPING/system_initialized.flag'
        if not os.path.exists(system_init_flag):
            log_message("Система не инициализирована, запуск процесса инициализации")
            reset_system_state()
            return
        
        helpers = get_helpers_list(conn)
        if not helpers:
            log_message("Невозможно проверить новые баны: список хелперов пуст", "warning")
            return
        
        # Получаем последний известный ID бана
        last_ban_id = get_last_ban_id()
        
        # Подготовка списка хелперов для SQL-запроса
        helpers_placeholders = ', '.join(['%s'] * len(helpers))
        
        # Запрос на основе ID бана, а не времени
        # Также проверяем, был ли бан уже обработан (используем специальную таблицу)
        query = f"""
            SELECT b.id, b.uuid, h.name AS player_name,
                   b.banned_by_name, b.reason, b.time, b.until
            FROM litebans_bans b
            LEFT JOIN litebans_history h ON b.uuid = h.uuid
            LEFT JOIN (
                SELECT DISTINCT ban_id, 1 as processed FROM litebans_processed_bans
            ) p ON b.id = p.ban_id
            WHERE b.active = 1
                AND b.banned_by_name IN ({helpers_placeholders})
                AND b.id > %s
                AND p.processed IS NULL  -- Исключаем уже обработанные баны
            GROUP BY b.id
            ORDER BY b.id DESC
            LIMIT 5
        """
        
        params = helpers + [last_ban_id]
        cursor.execute(query, params)
        bans = cursor.fetchall()
        
        # Записываем в лог информацию о поиске
        log_message(f"Поиск новых банов с ID > {last_ban_id}. Найдено: {len(bans)}")
        
        # Запоминаем максимальный ID бана из текущей выборки
        max_id_from_batch = last_ban_id
        if bans:
            max_id_from_batch = max(ban['id'] for ban in bans)
        
        for ban in bans:
            ban_id = ban['id']
            player_name = ban['player_name'] if ban['player_name'] else 'Unknown'
            helper_name = ban['banned_by_name']
            ban_reason = ban['reason']
            
            # Проверяем, есть ли уже пруф для этого бана перед отправкой уведомления
            proof_check_query = "SELECT COUNT(*) as count FROM litebans_ban_proofs WHERE ban_id = %s"
            proof_cursor = conn.cursor(dictionary=True)
            proof_cursor.execute(proof_check_query, (ban_id,))
            proof_result = proof_cursor.fetchone()
            has_proof = proof_result['count'] > 0
            proof_cursor.close()
            
            if has_proof:
                log_message(f"СКИП: Для бана ID: {ban_id} от хелпера {helper_name} уже есть пруф. Пропускаем.")
                # Отмечаем бан как обработанный
                mark_ban_as_processed(conn, ban_id, "proof_exists")
                continue
            
            # Обработка даты с учетом возможных типов данных
            try:
                # Проверяем, что ban['time'] не None и может быть преобразован в число
                if ban['time'] is None:
                    raise ValueError("Timestamp is None")
                    
                # Если это строка, пытаемся преобразовать
                if isinstance(ban['time'], str) and ban['time'].isdigit():
                    ban_timestamp = int(ban['time'])
                else:
                    ban_timestamp = int(float(ban['time']))
                    
                # Проверяем, что временная метка в разумном диапазоне (2020-2030 годы)
                # Это помогает избежать ошибок с очень большими или маленькими значениями
                if 1577836800 <= ban_timestamp <= 1893456000:  # между 2020-01-01 и 2030-01-01
                    # Форматируем даты для отображения
                    ban_time = datetime.datetime.fromtimestamp(ban_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                    proof_deadline = datetime.datetime.fromtimestamp(ban_timestamp + PROOF_TIMEOUT).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    log_message(f"Невалидный timestamp для бана ID {ban_id}: {ban_timestamp}", "warning")
                    ban_time = 'Некорректная дата'
                    proof_deadline = datetime.datetime.fromtimestamp(time.time() + PROOF_TIMEOUT).strftime('%Y-%m-%d %H:%M:%S')
            except Exception as e:
                log_message(f"Ошибка обработки временной метки для бана ID: {ban_id}: {e}", "error")
                # Даже если дата некорректная, устанавливаем дедлайн от текущего времени
                ban_time = 'Некорректная дата'
                proof_deadline = datetime.datetime.fromtimestamp(time.time() + PROOF_TIMEOUT).strftime('%Y-%m-%d %H:%M:%S')
            
            log_message(f"Обнаружен новый бан ID: {ban_id}, Игрок: {player_name}, Хелпер: {helper_name}")
            
            # Отправляем уведомление в Telegram
            deadline_hours = PROOF_TIMEOUT / 3600  # конвертируем секунды в часы
            message = f"<b>🔵 НОВЫЙ БАН ОТ ХЕЛПЕРА</b>\n\nХелпер <b>{helper_name}</b> забанил игрока <b>{player_name}</b>.\n\nПричина: <b>{ban_reason}</b>\n\nПруф должен быть опубликован до: <b>{proof_deadline}</b>"
            
            # Отправляем сообщение и отмечаем бан как обработанный
            if send_telegram_message(message):
                # Отмечаем бан как обработанный в базе данных, чтобы избежать дублирования
                mark_ban_as_processed(conn, ban_id, "notification_sent")
                log_message(f"Новый бан от хелпера: ID {ban_id}, Игрок {player_name}, Хелпер {helper_name}, Время {ban_time}, Дедлайн {proof_deadline}")
            else:
                log_message(f"Ошибка при отправке уведомления о бане ID {ban_id}", "error")
        
        # Обновляем последний ID бана, если нашли новые баны
        if max_id_from_batch > last_ban_id:
            update_last_ban_id(max_id_from_batch)
            log_message(f"Обновлен последний ID бана с {last_ban_id} на {max_id_from_batch}")
        
        # Для совместимости обновляем также временную метку
        current_timestamp = int(time.time())
        update_last_check_timestamp(current_timestamp, "ban")
        
    except Exception as e:
        log_message(f"Ошибка при проверке новых банов: {e}", "error")
        log_message(traceback.format_exc(), "error")
    finally:
        cursor.close()

def register_helper_violation(conn, helper_name: str, ban_id: int, player_name: str) -> int:
    """Регистрирует нарушение хелпера и возвращает количество нарушений"""
    cursor = conn.cursor(dictionary=True)
    
    try:
        # ПЕРВАЯ ПРОВЕРКА: проверяем наличие пруфа
        proof_query = "SELECT COUNT(*) as count FROM litebans_ban_proofs WHERE ban_id = %s"
        cursor.execute(proof_query, (ban_id,))
        has_proof = cursor.fetchone()['count'] > 0
        
        if has_proof:
            log_message(f"ЗАЩИТА ОТ ОШИБОК: Для бана ID: {ban_id} уже добавлен пруф. Нарушение НЕ БУДЕТ зарегистрировано!")
            return 0
        
        # Создаем таблицу для отслеживания нарушений, если её нет
        create_table_query = """
            CREATE TABLE IF NOT EXISTS litebans_helper_violations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                helper_name VARCHAR(255) NOT NULL,
                ban_id INT NOT NULL,
                player_name VARCHAR(255) NOT NULL,
                violation_time INT NOT NULL,
                processed TINYINT(1) DEFAULT 0
            )
        """
        cursor.execute(create_table_query)
        conn.commit()
        
        # Проверяем, было ли уже зарегистрировано нарушение для этого бана
        check_query = "SELECT COUNT(*) as count FROM litebans_helper_violations WHERE ban_id = %s"
        cursor.execute(check_query, (ban_id,))
        exists = cursor.fetchone()['count'] > 0
        
        if exists:
            log_message(f"Нарушение для бана ID: {ban_id} уже было зарегистрировано ранее.")
            
            # Получаем количество нарушений хелпера
            violations_query = "SELECT COUNT(*) as count FROM litebans_helper_violations WHERE helper_name = %s"
            cursor.execute(violations_query, (helper_name,))
            return cursor.fetchone()['count']
        
        # ПОСЛЕДНЯЯ ПРОВЕРКА: еще раз проверяем наличие пруфа перед добавлением нарушения
        cursor.execute(proof_query, (ban_id,))
        has_proof = cursor.fetchone()['count'] > 0
        
        if has_proof:
            log_message(f"ПОСЛЕДНЯЯ ЗАЩИТА: Для бана ID: {ban_id} был добавлен пруф. Нарушение не будет зарегистрировано.")
            return 0
        
        # Добавляем запись о нарушении
        current_time = int(time.time())
        insert_query = """
            INSERT INTO litebans_helper_violations 
            (helper_name, ban_id, player_name, violation_time) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (helper_name, ban_id, player_name, current_time))
        conn.commit()
        
        # Получаем обновленное количество нарушений
        violations_query = "SELECT COUNT(*) as count FROM litebans_helper_violations WHERE helper_name = %s"
        cursor.execute(violations_query, (helper_name,))
        violations_count = cursor.fetchone()['count']
        
        log_message(f"Зарегистрировано нарушение для хелпера {helper_name}. Всего нарушений: {violations_count}")
        
        return violations_count
    except Exception as e:
        log_message(f"Ошибка при регистрации нарушения: {e}", "error")
        log_message(traceback.format_exc(), "error")
        return 0
    finally:
        cursor.close()

def punish_helper(conn, helper_name: str) -> bool:
    """Отправляет предупреждение хелперу после 5 нарушений (без бана)"""
    cursor = conn.cursor()
    
    try:
        log_message(f"Отправка предупреждения хелперу {helper_name} после 5 нарушений")
        
        # НЕ удаляем права и НЕ баним хелпера, только отправляем предупреждение
        
        # Сбрасываем счетчик нарушений
        delete_violations = "DELETE FROM litebans_helper_violations WHERE helper_name = %s"
        cursor.execute(delete_violations, (helper_name,))
        conn.commit()
        
        log_message(f"Счетчик нарушений для хелпера {helper_name} сброшен")
        
        # Отправка предупреждения в Telegram
        message = f"<b>⚠️ ПРЕДУПРЕЖДЕНИЕ ХЕЛПЕРУ</b>\n\nХелпер <b>{helper_name}</b> получил максимальное количество предупреждений (5/5) за нарушение правил предоставления пруфов. Пожалуйста, соблюдайте правила предоставления пруфов в будущем."
        send_telegram_message(message)
        
        log_message(f"Хелперу {helper_name} отправлено предупреждение о достижении 5/5 нарушений")
        return True
    except Exception as e:
        log_message(f"Ошибка при удалении хелпера: {e}", "error")
        log_message(traceback.format_exc(), "error")
        return False
    finally:
        cursor.close()

def check_bans_without_proofs(conn):
    """Проверяет баны без пруфов и разбанивает игроков, если пруф не предоставлен"""
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Проверяем, инициализирована ли система
        system_init_flag = '/var/www/html/bans/PLUGIN_DEVELOPING/system_initialized.flag'
        if not os.path.exists(system_init_flag):
            log_message("Система не инициализирована, пропускаем проверку банов без пруфов")
            return
        
        # Получаем последний известный ID бана
        last_ban_id = get_last_ban_id()
        log_message(f"Последний известный ID бана: {last_ban_id}")
        
        # Получаем список хелперов
        helpers = get_helpers_list(conn)
        if not helpers:
            log_message("Невозможно проверить баны без пруфов: список хелперов пуст", "warning")
            return
        
        # Текущее время
        current_timestamp = int(time.time())
        
        # Вычисляем временной лимит для проверки (текущее время - время ожидания пруфа)
        time_limit = current_timestamp - PROOF_TIMEOUT
        
        # Работаем ТОЛЬКО с новыми банами - теми, которые появились после инициализации системы
        new_bans_only = int(os.path.getmtime(system_init_flag)) # Время инициализации системы
        
        # Подготовка списка хелперов для SQL-запроса
        helpers_placeholders = ', '.join(['%s'] * len(helpers))
        
        # Получаем все баны и проверяем, какие из них без пруфов
        log_message("Используем новый режим работы: предварительный анализ без разбана")
        
        # Сначала получим все пруфы из базы данных
        proofs_query = "SELECT ban_id FROM litebans_ban_proofs"
        cursor.execute(proofs_query)
        proof_results = cursor.fetchall()
        proofs_ban_ids = [r['ban_id'] for r in proof_results] if proof_results else []
        
        # Записываем, сколько пруфов найдено в базе данных
        log_message(f"Найдено {len(proofs_ban_ids)} пруфов в базе данных")
        
        # Теперь получим все активные баны от хелперов
        query = f"""
            SELECT b.id, b.uuid, 
                   h.name AS player_name,
                   b.banned_by_name, 
                   b.reason, 
                   b.time,
                   b.until
            FROM litebans_bans b
            LEFT JOIN litebans_history h ON b.uuid = h.uuid
            WHERE 
                b.active = 1
                AND b.banned_by_name IN ({helpers_placeholders})
                AND b.time > %s      -- Только баны после инициализации системы
                AND b.time < %s      -- Только баны, для которых истекло время предоставления пруфа
                AND b.id > %s        -- Только новые баны по ID
            GROUP BY b.id
            ORDER BY b.time DESC
            LIMIT 10
        """
        
        params = helpers + [new_bans_only, time_limit, last_ban_id]
        cursor.execute(query, params)
        bans = cursor.fetchall()
        
        # Фильтруем баны без пруфов
        bans_without_proofs = []
        for ban in bans:
            ban_id = ban['id']
            if ban_id not in proofs_ban_ids:
                bans_without_proofs.append(ban)
        
        log_message(f"Найдено {len(bans_without_proofs)} банов без пруфов из {len(bans)} активных банов")
        
        # Отправляем запрос в Телеграм по каждому бану без пруфа
        for ban in bans_without_proofs:
            ban_id = ban['id']
            player_name = ban['player_name'] if ban['player_name'] else 'Unknown'
            helper_name = ban['banned_by_name']
            
            try:
                ban_time = datetime.datetime.fromtimestamp(ban['time']).strftime('%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError, OverflowError):
                ban_time = 'Некорректная дата'
            
            # Дополнительная проверка наличия пруфа
            proof_check_query = "SELECT COUNT(*) as count FROM litebans_ban_proofs WHERE ban_id = %s"
            proof_cursor = conn.cursor(dictionary=True)
            proof_cursor.execute(proof_check_query, (ban_id,))
            proof_result = proof_cursor.fetchone()
            has_proof = proof_result['count'] > 0
            proof_cursor.close()
            
            if has_proof:
                log_message(f"ДОПОЛНИТЕЛЬНАЯ ПРОВЕРКА: Для бана ID: {ban_id} всё же найден пруф, пропускаем")
                mark_ban_as_processed(conn, ban_id, "has_proof_skip")
                continue
            
            # Формируем сообщение для Телеграм
            unban_question = f"<b>🔴 ТРЕБУЕТСЯ ПОДТВЕРЖДЕНИЕ РАЗБАНА</b>\n\nИгрок <b>{player_name}</b> может быть разбанен, так как хелпер <b>{helper_name}</b> не предоставил пруф.\n\nБан ID: <b>{ban_id}</b>\nВремя бана: <b>{ban_time}</b>\n\nРазрешить разбан? Система находится в режиме тестирования."
            
            # Отправляем сообщение в Телеграм
            if send_telegram_message(unban_question):
                log_message(f"Отправлен запрос на разбан игрока {player_name} (ID бана: {ban_id})")
                mark_ban_as_processed(conn, ban_id, "question_sent")
            else:
                log_message(f"Ошибка при отправке запроса на разбан игрока {player_name}", "error")
        
        # Обновляем время последней проверки разбанов
        update_last_check_timestamp(current_timestamp, "unban")
        
        # Формируем SQL запрос для поиска банов без пруфов
        helpers_placeholders = ", ".join(["%s"] * len(helpers))
        query = f"""
            SELECT b.id, b.uuid, 
                   h.name AS player_name,
                   b.banned_by_name, 
                   b.reason, 
                   b.time,
                   b.until
            FROM litebans_bans b
            LEFT JOIN litebans_history h ON b.uuid = h.uuid
            WHERE 
                b.active = 1
                AND b.banned_by_name IN ({helpers_placeholders})
                AND b.time > %s      -- Только баны после инициализации системы
                AND b.time < %s      -- Только баны, для которых истекло время предоставления пруфа
                AND b.id > %s        -- Только новые баны по ID
            GROUP BY b.id
            ORDER BY b.time DESC
        """
        
        params = helpers + [new_bans_only, time_limit, last_ban_id]
        cursor.execute(query, params)
        bans_without_proofs = cursor.fetchall()

        # Логируем информацию о найденных банах
        count = len(bans_without_proofs)
        log_message(f"Найдено {count} банов без пруфов для проверки")

        if count == 0:
            log_message("Нет банов, требующих обработки")
            return

        # Запоминаем максимальный ID бана из выборки
        max_id_from_batch = max(ban['id'] for ban in bans_without_proofs) if bans_without_proofs else last_ban_id
        log_message(f"Максимальный ID бана в текущей выборке: {max_id_from_batch}")

        # Дополнительная фильтрация банов для исключения тех, у которых есть пруфы
        log_message("Проверка пруфов для найденных банов...")
        
        # Создадим новый список только с банами без пруфов
        bans_actually_without_proofs = []
        for ban in bans_without_proofs:
            ban_id = ban['id']
            # Проверка пруфа для каждого бана
            proof_check_query = "SELECT COUNT(*) as count FROM litebans_ban_proofs WHERE ban_id = %s"
            proof_cursor = conn.cursor(dictionary=True)
            proof_cursor.execute(proof_check_query, (ban_id,))
            proof_result = proof_cursor.fetchone()
            has_proof = proof_result and proof_result['count'] > 0
            proof_cursor.close()
            
            if has_proof:
                log_message(f"Бан ID {ban_id} имеет пруф - пропускаем")
                # Отмечаем бан как обработанный, чтобы больше не проверять его
                mark_ban_as_processed(conn, ban_id, "has_proof_skip")
                continue
            
            # Если пруфа нет, добавляем в список банов без пруфов
            bans_actually_without_proofs.append(ban)
            log_message(f"Бан ID {ban_id} не имеет пруфа - добавлен в очередь на обработку")
        
        # Обновляем список банов без пруфов
        bans_without_proofs = bans_actually_without_proofs
        count = len(bans_without_proofs)
        log_message(f"После дополнительной проверки осталось {count} банов без пруфов")
        
        if count == 0:
            log_message("Нет банов, требующих обработки")
            return

        # Запоминаем максимальный ID бана из выборки
        max_id_from_batch = max(ban['id'] for ban in bans_without_proofs) if bans_without_proofs else last_ban_id
        log_message(f"Максимальный ID бана в текущей выборке: {max_id_from_batch}")

        # Обрабатываем каждый бан без пруфа
        for ban in bans_without_proofs:
            try:
                ban_id = ban['id']
                player_name = ban['player_name'] if ban['player_name'] else 'Unknown'
                helper_name = ban['banned_by_name']

                # Безопасное форматирование времени
                try:
                    ban_time = datetime.datetime.fromtimestamp(ban['time']).strftime('%Y-%m-%d %H:%M:%S')
                except (ValueError, TypeError, OverflowError):
                    ban_time = 'Некорректная дата'

                log_message(f"Обработка бана ID: {ban_id}, Игрок: {player_name}, Забанен хелпером: {helper_name}, Время бана: {ban_time}")

                # Дополнительная проверка наличия пруфа - более тщательная
                # Проверяем несколькими способами
                has_proof = False
                
                # Проверка 1: Стандартная проверка в таблице litebans_ban_proofs
                proof_check_query = "SELECT COUNT(*) as count FROM litebans_ban_proofs WHERE ban_id = %s"
                proof_cursor = conn.cursor(dictionary=True)
                proof_cursor.execute(proof_check_query, (ban_id,))
                proof_result = proof_cursor.fetchone()
                if proof_result and proof_result['count'] > 0:
                    has_proof = True
                    log_message(f"Проверка 1: Для бана ID: {ban_id} найден пруф в таблице litebans_ban_proofs")
                
                # Проверка 2: Проверка в таблице с прикрепленными файлами
                if not has_proof:
                    attachment_query = "SELECT COUNT(*) as count FROM litebans_attachments WHERE ban_id = %s"
                    proof_cursor.execute(attachment_query, (ban_id,))
                    attachment_result = proof_cursor.fetchone()
                    if attachment_result and attachment_result['count'] > 0:
                        has_proof = True
                        log_message(f"Проверка 2: Для бана ID: {ban_id} найдены файлы в таблице litebans_attachments")
                    
                # Проверка 3: Поиск записей в логах действий с упоминанием пруфа
                if not has_proof:
                    log_query = "SELECT COUNT(*) as count FROM litebans_actions_log WHERE action_text LIKE %s AND related_id = %s"
                    proof_cursor.execute(log_query, (f"%proof%", ban_id))
                    log_result = proof_cursor.fetchone()
                    if log_result and log_result['count'] > 0:
                        has_proof = True
                        log_message(f"Проверка 3: Для бана ID: {ban_id} найдены записи в логах о добавлении пруфа")
                
                proof_cursor.close()
                
                if has_proof:
                    log_message(f"ЗАЩИТА: Для бана ID: {ban_id} обнаружен опубликованный пруф. Отмена обработки нарушения.")
                    mark_ban_as_processed(conn, ban_id, "proof_found")
                    continue  # Пропускаем этот бан и переходим к следующему

                # Проверка, что бан еще активен
                active_check_query = "SELECT active FROM litebans_bans WHERE id = %s"
                active_cursor = conn.cursor(dictionary=True)
                active_cursor.execute(active_check_query, (ban_id,))
                active_result = active_cursor.fetchone()
                is_active = active_result and active_result['active'] == 1
                active_cursor.close()

                if not is_active:
                    log_message(f"ЗАЩИТА: Бан ID: {ban_id} уже неактивен. Пропускаем обработку.")
                    mark_ban_as_processed(conn, ban_id, "already_inactive")
                    continue  # Пропускаем неактивные баны

                # Проверка, является ли хелпер действующим
                helper_check_query = "SELECT COUNT(*) as count FROM litebans_users WHERE username = %s AND role = 'helper'"
                helper_cursor = conn.cursor(dictionary=True)
                helper_cursor.execute(helper_check_query, (helper_name,))
                helper_result = helper_cursor.fetchone()
                is_helper = helper_result and helper_result['count'] > 0
                helper_cursor.close()

                if not is_helper:
                    log_message(f"ЗАЩИТА: {helper_name} больше не является хелпером. Пропускаем обработку.")
                    mark_ban_as_processed(conn, ban_id, "not_helper_anymore")
                    continue  # Пропускаем баны от бывших хелперов
            except Exception as e:
                log_message(f"Ошибка при проверке бана ID {ban_id}: {e}", "error")
                continue  # Пропускаем проблемный бан

            # Если все проверки пройдены, только тогда регистрируем нарушение
            log_message(f"Все проверки пройдены, регистрируем нарушение для хелпера {helper_name}")

            # Регистрируем нарушение хелпера и получаем количество нарушений
            violation_count = register_helper_violation(conn, helper_name, ban_id, player_name)

            # Проверяем, было ли зарегистрировано нарушение
            if violation_count > 0:
                # Еще раз проверяем наличие пруфа
                proof_cursor = conn.cursor(dictionary=True)
                proof_cursor.execute(proof_check_query, (ban_id,))
                proof_result = proof_cursor.fetchone()
                has_proof = proof_result['count'] > 0
                proof_cursor.close()
                
                if has_proof:
                    log_message(f"Для бана ID: {ban_id} обнаружен опубликованный пруф. Отмена обработки нарушения.")
                    continue
                
                # Дополнительная проверка наличия пруфа перед отправкой уведомления
                # Ещё одна проверка, чтобы убедиться, что мы не отправляем ложные уведомления
                
                # Получаем информацию о бане из основной таблицы, чтобы уточнить причину
                ban_info_query = "SELECT reason FROM litebans_bans WHERE id = %s"
                ban_info_cursor = conn.cursor(dictionary=True)
                ban_info_cursor.execute(ban_info_query, (ban_id,))
                ban_info = ban_info_cursor.fetchone()
                ban_info_cursor.close()
                
                # Проверяем, есть ли в причине бана указание на пруф
                reason_has_proof_reference = False
                if ban_info and ban_info['reason']:
                    reason = ban_info['reason'].lower()
                    proof_keywords = ['proof', 'пруф', 'screen', 'скрин', 'video', 'видео']
                    for keyword in proof_keywords:
                        if keyword in reason:
                            reason_has_proof_reference = True
                            log_message(f"В причине бана ID: {ban_id} найдена ссылка на пруф: '{keyword}'")
                            break
                
                # Если в причине бана есть указание на пруф, пропускаем этот бан
                if reason_has_proof_reference:
                    log_message(f"ЗАЩИТА: В причине бана ID: {ban_id} содержится указание на пруф. Пропускаем.")
                    mark_ban_as_processed(conn, ban_id, "reason_has_proof_reference")
                    continue
                
                # Отправляем уведомление в Telegram админу о необходимости проверки
                admin_message = f"<b>🔵 ИНФОРМАЦИЯ</b>\n\nТребуется проверка наличия пруфа для бана:\n\nИгрок: <b>{player_name}</b>\nХелпер: <b>{helper_name}</b>\nВремя бана: <b>{ban_time}</b>\nБан ID: <b>{ban_id}</b>\n\nПожалуйста, проверьте наличие пруфа и примите решение."
                send_telegram_message(admin_message)
                
                # Отмечаем бан как обработанный
                mark_ban_as_processed(conn, ban_id, "admin_notified")
                continue
            else:
                log_message(f"Нарушение не было зарегистрировано для бана ID: {ban_id} (возможно, пруф уже был добавлен)")
                # Отмечаем бан как обработанный, чтобы больше не проверять его
                mark_ban_as_processed(conn, ban_id, "no_violation")
                continue
            
            # Отправляем команду на разбан с причиной "Proof yo'q"
            unban_command = f"unban {player_name} Proof yo'q"
            
            if execute_pterodactyl_command(unban_command):
                log_message(f"Игрок {player_name} успешно разбанен из-за отсутствия пруфа")
                
                # Обновляем статус бана в базе данных
                unban_reason = "Proof yo'q"  # Добавляем переменную с точным значением
                update_query = "UPDATE litebans_bans SET active = 0, removed_by_name = 'System', removed_by_uuid = 'auto-unban', removed_by_date = %s, removed_by_reason = %s WHERE id = %s"
                cursor.execute(update_query, (current_timestamp, unban_reason, ban_id))  # Используем причину разбана "Proof yo'q"
                conn.commit()
                
                # Отправляем уведомление в Telegram о разбане
                unban_message = f"<b>🟢 АВТОМАТИЧЕСКИЙ РАЗБАН</b>\n\nИгрок <b>{player_name}</b> был автоматически разбанен из-за отсутствия пруфа от хелпера <b>{helper_name}</b>."
                send_telegram_message(unban_message)
                # Отмечаем бан как полностью обработанный (игрок разбанен)
                mark_ban_as_processed(conn, ban_id, "player_unbanned")
            else:
                log_message(f"Ошибка при разбане игрока {player_name}", "error")
        
        # Обновляем время последней проверки разбанов
        update_last_check_timestamp(current_timestamp, "unban")
        
    except Exception as e:
        log_message(f"Ошибка при проверке банов без пруфов: {e}", "error")
        log_message(traceback.format_exc(), "error")
    finally:
        cursor.close()

def mark_ban_as_processed(conn, ban_id, process_type="notification"):
    """Отмечает бан как обработанный в специальной таблице"""
    cursor = conn.cursor()
    current_time = int(time.time())
    
    try:
        # Добавляем запись в таблицу обработанных банов
        query = "INSERT INTO litebans_processed_bans (ban_id, process_time, process_type) VALUES (%s, %s, %s)"
        cursor.execute(query, (ban_id, current_time, process_type))
        conn.commit()
        log_message(f"Бан ID: {ban_id} отмечен как обработанный (тип: {process_type})")
        return True
    except Exception as e:
        log_message(f"Ошибка при отметке бана {ban_id} как обработанного: {e}", "error")
        return False
    finally:
        cursor.close()

def get_max_ban_id(conn):
    """Получает максимальный ID бана в базе данных"""
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT MAX(id) as max_id FROM litebans_bans"
        cursor.execute(query)
        result = cursor.fetchone()
        max_id = result['max_id'] if result and result['max_id'] is not None else 0
        return max_id
    except Exception as e:
        log_message(f"Ошибка при получении максимального ID бана: {e}", "error")
        return 0
    finally:
        cursor.close()

def initialize_system():
    """Инициализирует систему и создает флаг инициализации"""
    log_message("Инициализация системы")
    
    # Путь к флагу инициализации
    system_init_flag = '/var/www/html/bans/PLUGIN_DEVELOPING/system_initialized.flag'
    
    # Проверяем, существует ли флаг
    if os.path.exists(system_init_flag):
        log_message("Система уже инициализирована")
        return
    
    # Получаем последний ID бана из базы данных
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT MAX(id) as max_id FROM litebans_bans")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        # Если нашли максимальный ID, устанавливаем его как последний известный
        if result and result['max_id']:
            max_id = result['max_id']
            # Устанавливаем последний известный ID бана
            update_last_ban_id(max_id)
            log_message(f"Установлен последний известный ID бана: {max_id}")
        else:
            # Устанавливаем значение по умолчанию
            update_last_ban_id(0)
            log_message("Не удалось получить последний ID бана, установлено значение 0")
    except Exception as e:
        log_message(f"Ошибка при инициализации системы: {e}", "error")
        update_last_ban_id(0)  # Устанавливаем значение по умолчанию в случае ошибки
    
    # Устанавливаем текущее время для других таймстемпов
    current_time = int(time.time())
    with open(check_file, 'w') as f:
        f.write(str(current_time))
    with open(unban_file, 'w') as f:
        f.write(str(current_time))
    
    # Создаем флаг инициализации
    with open(system_init_flag, 'w') as f:
        f.write(str(current_time))
    
    log_message("Система успешно инициализирована")


def reset_system_state():
    """Сбрасывает состояние системы, удаляя файлы с сохраненными таймстемпами"""
    log_message("Сброс состояния системы")
    
    # Удаляем файлы с таймстемпами
    timestamp_files = [check_file, unban_file, last_ban_id_file]
    for file in timestamp_files:
        if os.path.exists(file):
            os.remove(file)
            log_message(f"Файл {file} удален")
    
    # Удаляем флаг инициализации
    system_init_flag = '/var/www/html/bans/PLUGIN_DEVELOPING/system_initialized.flag'
    if os.path.exists(system_init_flag):
        os.remove(system_init_flag)
        log_message(f"Флаг инициализации удален")
    
    # Запускаем инициализацию системы заново
    initialize_system()
    
    # Дополнительных действий не требуется, система уже инициализирована
    
    log_message("Система полностью сброшена и готова к мониторингу только новых банов")
    return True

def main():
    """Основная функция для запуска процесса мониторинга банов"""
    try:
        log_message("=" * 50)
        log_message("Запуск системы мониторинга банов v1.0 (Без отображения старых банов)")
        log_message("=" * 50)
        
        # Инициализируем систему при каждом запуске
        # Функция сама проверит, существует ли флаг инициализации
        # и создаст его только при необходимости
        initialize_system()
        
        # Проверяем, была ли инициализация
        system_init_flag = '/var/www/html/bans/PLUGIN_DEVELOPING/system_initialized.flag'
        first_run = not os.path.exists(system_init_flag) or os.path.getmtime(system_init_flag) > time.time() - 5
        
        if first_run:
            log_message("[ВАЖНО] Система инициализирована, теперь будут отслеживаться только НОВЫЕ баны!")
            # Запускаем одноразовую очистку нарушений хелперов
            try:
                conn = get_db_connection()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM litebans_helper_violations")
                    conn.commit()
                    cursor.close()
                    log_message("[ВАЖНО] Таблица нарушений хелперов очищена")
                    close_db_connection(conn)
            except Exception as e:
                log_message(f"Ошибка при очистке нарушений хелперов: {e}", "error")
        
        log_message("Система в рабочем режиме, ожидает новых банов...")
        
        # Основной цикл работы
        while True:
            conn = get_db_connection()
            if conn:
                try:
                    # Проверяем новые баны
                    check_new_bans(conn)
                    
                    # Проверяем баны без пруфов
                    check_bans_without_proofs(conn)
                finally:
                    close_db_connection(conn)
            
            # Пауза между проверками
            time.sleep(10)  # Проверяем каждые 10 секунд
            
    except KeyboardInterrupt:
        log_message("Система мониторинга банов остановлена пользователем", "warning")
    except Exception as e:
        log_message(f"Критическая ошибка в работе системы: {e}", "error")
        log_message(traceback.format_exc(), "error")

if __name__ == "__main__":
    main()
