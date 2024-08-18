import sqlite3 as sql

def instantiate_db():
    create_table_usersdonjons()
    create_table_usersmetier()

def create_table_usersdonjons():
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS usersdonjons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudo TEXT NOT NULL,
            donjon TEXT NOT NULL,
            UNIQUE(pseudo, donjon)
        )
        ''')
    conn.commit()
    conn.close()

def create_table_usersmetier():
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS usersmetier (pseudo TEXT, metier TEXT, niveau INTEGER)')
    conn.commit()
    conn.close()

def insert_data(pseudo, metier, niveau):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM usersmetier WHERE pseudo = ? AND metier = ?', (pseudo, metier))
    exists = cur.fetchone()[0]
    if exists:
        cur.execute('UPDATE usersmetier SET niveau = ? WHERE pseudo = ? AND metier = ?', (niveau, pseudo, metier))
    else:
        cur.execute('INSERT INTO usersmetier (pseudo, metier, niveau) VALUES (?, ?, ?)', (pseudo, metier, niveau))
    conn.commit()
    conn.close()

def save_donjons_for_user(pseudo, donjons):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    for donjon in donjons:
        cur.execute('INSERT OR IGNORE INTO usersdonjons (pseudo, donjon) VALUES (?, ?)', (pseudo, donjon))
    conn.commit()
    conn.close()

def delete_donjons_for_user(pseudo, donjons):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    for donjon in donjons:
        cur.execute('DELETE FROM usersdonjons WHERE pseudo = ? AND donjon = ?', (pseudo, donjon))
    conn.commit()
    conn.close()

def get_data_from_user(pseudo):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM usersmetier where pseudo = ?', (pseudo,))
    data = cur.fetchall()
    conn.close()
    return [(row[1], row[2]) for row in data]

def get_metier_par_niveau(metier, niveau):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT pseudo FROM usersmetier WHERE metier = ? AND niveau >= ?', (metier, niveau))
    data = cur.fetchall()
    conn.close()
    return [row[0] for row in data]

def get_users_for_donjon(donjon):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT pseudo FROM usersdonjons WHERE donjon = ?', (donjon,))
    data = cur.fetchall()
    conn.close()
    return [row[0] for row in data]

def get_donjons_from_user(pseudo): 
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT donjon FROM usersdonjons WHERE pseudo = ?', (pseudo,))
    data = cur.fetchall()
    conn.close()
    return [row[0] for row in data]