
import sqlite3

def criar_tabela():
    conn = sqlite3.connect('agendamentos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_procedimento TEXT NOT NULL,
            data TEXT NOT NULL,
            horario TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def inserir_agendamento(tipo_procedimento, data, horario):
    conn = sqlite3.connect('agendamentos.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO agendamentos (tipo_procedimento, data, horario) VALUES (?, ?, ?)",
                   (tipo_procedimento, data, horario))
    conn.commit()
    conn.close()

def buscar_agendamentos():
    conn = sqlite3.connect('agendamentos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agendamentos")
    agendamentos = cursor.fetchall()
    conn.close()
    return agendamentos

def agendamento_existe(data, horario):
    conn = sqlite3.connect('agendamentos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM agendamentos WHERE data = ? AND horario = ?", (data, horario))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] > 0
