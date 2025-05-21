import sqlite3

def init_db():
    conn = sqlite3.connect("clients.db")
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, message TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS auto_reply (id INTEGER PRIMARY KEY, text TEXT)")
    c.execute("INSERT OR IGNORE INTO auto_reply (id, text) VALUES (1, 'Спасибо за сообщение! Мы скоро ответим.')")
    conn.commit()
    conn.close()

def add_client(name):
    conn = sqlite3.connect("clients.db")
    c = conn.cursor()
    c.execute("INSERT INTO clients (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def log_message(client_name, message):
    conn = sqlite3.connect("clients.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (client_name, message) VALUES (?, ?)", (client_name, message))
    conn.commit()
    conn.close()

def get_auto_reply():
    conn = sqlite3.connect("clients.db")
    c = conn.cursor()
    c.execute("SELECT text FROM auto_reply WHERE id = 1")
    result = c.fetchone()
    conn.close()
    return result[0] if result else ""

def set_auto_reply(text):
    conn = sqlite3.connect("clients.db")
    c = conn.cursor()
    c.execute("REPLACE INTO auto_reply (id, text) VALUES (1, ?)", (text,))
    conn.commit()
    conn.close()