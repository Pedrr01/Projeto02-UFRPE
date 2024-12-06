import sqlite3
import os

# Função para recuperar as disciplinas
def get_disciplinas():
    database_path = os.path.join('database', 'disciplinas.db')
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(''' 
        SELECT * FROM disciplinas 
    ''')
    disciplinas = cursor.fetchall()

    conn.close()
    return disciplinas

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

# Função para exibir as disciplinas e suas publicações
def visualizar_disciplinas_e_publicacoes():
    disciplinas = get_disciplinas()
    
    if disciplinas:
        for disciplina in disciplinas:
            print(f"ID: {disciplina[0]}")
            print(f"Nome: {disciplina[1]}")
            print(f"Descrição: {disciplina[2]}")
            print("Publicações:")
            
            publicacoes = get_publicacoes(disciplina[0])
            if publicacoes:
                for pub in publicacoes:
                    print(f"  ID: {pub[0]}")
                    print(f"  Tipo: {pub[1]}")
                    print(f"  Título: {pub[2]}")
                    print(f"  Conteúdo: {pub[3]}")
                    if pub[4]:
                        print(f"  Arquivo: {pub[4]}")
                    print("-" * 40)
            else:
                print("  Nenhuma publicação encontrada para esta disciplina.")
            print("=" * 40)
    else:
        print("Nenhuma disciplina encontrada.")

# Exemplo de chamada para visualizar as disciplinas e publicações
if __name__ == '__main__':
    visualizar_disciplinas_e_publicacoes()
