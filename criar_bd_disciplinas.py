import sqlite3
import os

# Função para criar o banco de dados de disciplinas e usuários
def create_database():
    os.makedirs('database', exist_ok=True)  # Garantir que o diretório exista

    # Criar banco de dados de disciplinas
    database_path = os.path.join('database', 'disciplinas.db')
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS disciplinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT
        )
    ''')

    # Criar banco de dados de usuários
    users_db_path = os.path.join('database', 'users.db')
    conn = sqlite3.connect(users_db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            faculdade TEXT,
            curso TEXT,
            periodo TEXT
        )
    ''')

    # Criar tabela de publicações (com relação à disciplina)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS publicacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        titulo TEXT,
        conteudo TEXT,
        arquivo TEXT,
        disciplina_id INTEGER,
        FOREIGN KEY (disciplina_id) REFERENCES disciplinas (id));
    ''')

    conn.commit()
    conn.close()
    print('Banco de dados e tabelas criados com sucesso.')

# Função para inserir publicações (link, comentário ou arquivo)
def insert_publicacao(disciplina_id, tipo, titulo, conteudo, arquivo=None):
    database_path = os.path.join('database', 'disciplinas.db')
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO publicacoes (tipo, titulo, conteudo, arquivo, disciplina_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (tipo, titulo, conteudo, arquivo, disciplina_id))

    conn.commit()
    conn.close()
    print('Publicação inserida com sucesso.')

# Função para recuperar publicações de uma disciplina específica
def get_publicacoes(disciplina_id):
    database_path = os.path.join('database', 'disciplinas.db')
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM publicacoes WHERE disciplina_id = ?
    ''', (disciplina_id,))
    publicacoes = cursor.fetchall()

    conn.close()
    return publicacoes

# Chama a função para criar o banco de dados e as tabelas
if __name__ == '__main__':
    create_database()
