import sqlite3 as sql

def instantiate_db():
    create_table_usersdonjons()
    create_table_usersmetier()
    create_table_quetes()
    create_table_usersquetes()

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

def create_table_quetes():  
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS quetes (
            quete TEXT NOT NULL
        )
        ''')
    conn.commit()
    conn.close()

def create_table_usersquetes():
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS usersquetes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudo TEXT NOT NULL,
            quete TEXT NOT NULL,
            UNIQUE(pseudo, quete)
        )
        ''')
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

def insert_quete(quete):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO quetes (quete) VALUES (?)', (quete,))
    conn.commit()
    conn.close()

def save_donjons_for_user(pseudo, donjons):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    for donjon in donjons:
        cur.execute('INSERT OR IGNORE INTO usersdonjons (pseudo, donjon) VALUES (?, ?)', (pseudo, donjon))
    conn.commit()
    conn.close()

def save_quetes_for_user(pseudo, quetes):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    for quete in quetes:
        cur.execute('INSERT OR IGNORE INTO usersquetes (pseudo, quete) VALUES (?, ?)', (pseudo, quete))
    conn.commit()
    conn.close()

def delete_donjons_for_user(pseudo, donjons):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    for donjon in donjons:
        cur.execute('DELETE FROM usersdonjons WHERE pseudo = ? AND donjon = ?', (pseudo, donjon))
    conn.commit()
    conn.close()

def delete_quetes_for_user(pseudo, quetes):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    for quete in quetes:
        cur.execute('DELETE FROM usersquetes WHERE pseudo = ? AND quete = ?', (pseudo, quete))
    conn.commit()
    conn.close()

def delete_quete_existante(quete):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    print("-----------------------------------------------------")
    print(quete)
    cur.execute('DELETE FROM quetes WHERE quete = ?', (quete,))
    cur.execute('DELETE FROM usersquetes WHERE quete = ?', (quete,))
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

def get_users_for_quete(quete):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT pseudo FROM usersquetes WHERE quete = ?', (quete,))
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

def get_quetes_existantes():
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT quete FROM quetes')
    data = cur.fetchall()
    conn.close()
    return [row[0] for row in data]

def get_quetes_from_user(pseudo):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT quete FROM usersquetes WHERE pseudo = ?', (pseudo,))
    data = cur.fetchall()
    conn.close()
    return [row[0] for row in data]