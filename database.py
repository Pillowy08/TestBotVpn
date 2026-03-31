import sqlite3
from datetime import datetime
from config import DATABASE_PATH


def get_connection():
    """Получить соединение с базой данных"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Инициализация базы данных"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Таблица пользователей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            referrer_id INTEGER,
            balance REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (referrer_id) REFERENCES users(telegram_id)
        )
    """)
    
    # Таблица покупок
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tariff TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(telegram_id)
        )
    """)
    
    # Таблица промокодов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS promo_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            discount REAL NOT NULL,
            max_uses INTEGER DEFAULT 1,
            current_uses INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Таблица активированных промокодов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_promo_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            promo_code_id INTEGER NOT NULL,
            activated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(telegram_id),
            FOREIGN KEY (promo_code_id) REFERENCES promo_codes(id),
            UNIQUE(user_id, promo_code_id)
        )
    """)
    
    # Таблица рефералов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_id INTEGER NOT NULL,
            referred_id INTEGER NOT NULL,
            bonus_earned REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (referrer_id) REFERENCES users(telegram_id),
            FOREIGN KEY (referred_id) REFERENCES users(telegram_id)
        )
    """)
    
    conn.commit()
    conn.close()


def add_user(telegram_id: int, username: str = None, first_name: str = None,
             last_name: str = None, referrer_id: int = None) -> bool:
    """Добавить нового пользователя"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (telegram_id, username, first_name, last_name, referrer_id)
            VALUES (?, ?, ?, ?, ?)
        """, (telegram_id, username, first_name, last_name, referrer_id))

        # Если есть реферер, создаем запись о реферале и начисляем бонус
        if referrer_id:
            cursor.execute("""
                INSERT INTO referrals (referrer_id, referred_id, bonus_earned)
                VALUES (?, ?, 10)
            """, (referrer_id, telegram_id))
            
            # Начисляем 10₽ рефереру
            cursor.execute("""
                UPDATE users SET balance = balance + 10 WHERE telegram_id = ?
            """, (referrer_id,))

        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user(telegram_id: int) -> dict:
    """Получить пользователя по ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None


def update_balance(telegram_id: int, amount: float) -> bool:
    """Обновить баланс пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE users SET balance = balance + ? WHERE telegram_id = ?
    """, (amount, telegram_id))
    
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    
    return affected > 0


def add_purchase(user_id: int, tariff: str, amount: float, status: str = 'pending') -> int:
    """Добавить покупку"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO purchases (user_id, tariff, amount, status)
        VALUES (?, ?, ?, ?)
    """, (user_id, tariff, amount, status))
    
    purchase_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return purchase_id


def add_promo_code(code: str, discount: float, max_uses: int = 1) -> bool:
    """Добавить промокод"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO promo_codes (code, discount, max_uses)
            VALUES (?, ?, ?)
        """, (code, discount, max_uses))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_promo_code(code: str) -> dict:
    """Получить промокод по коду"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM promo_codes 
        WHERE code = ? AND is_active = 1 AND current_uses < max_uses
    """, (code,))
    
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None


def activate_promo_code(user_id: int, promo_code_id: int) -> bool:
    """Активировать промокод для пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Проверяем, не активировал ли уже пользователь этот промокод
        cursor.execute("""
            SELECT * FROM user_promo_codes 
            WHERE user_id = ? AND promo_code_id = ?
        """, (user_id, promo_code_id))
        
        if cursor.fetchone():
            return False
        
        # Добавляем запись об активации
        cursor.execute("""
            INSERT INTO user_promo_codes (user_id, promo_code_id)
            VALUES (?, ?)
        """, (user_id, promo_code_id))
        
        # Увеличиваем счетчик использований
        cursor.execute("""
            UPDATE promo_codes SET current_uses = current_uses + 1
            WHERE id = ?
        """, (promo_code_id,))
        
        conn.commit()
        return True
    finally:
        conn.close()


def get_referrers_stats(referrer_id: int) -> dict:
    """Получить статистику реферера"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            COUNT(*) as total_referrals,
            COALESCE(SUM(bonus_earned), 0) as total_earned
        FROM referrals
        WHERE referrer_id = ?
    """, (referrer_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else {"total_referrals": 0, "total_earned": 0}


def get_all_users() -> list:
    """Получить всех пользователей"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


# Инициализируем БД при импорте
init_db()
