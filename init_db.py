import sqlite3

#nome do banco de dados
DATABASE_NAME = 'biblioteca.db'

# instruções para o .bd
DROP_LIVROS_TABLE = "DROP TABLE IF EXISTS livros;"

CREATE_LIVROS_TABLE = """
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    ano_publicacao INTEGER,
    disponivel BOOLEAN,
    capa TEXT
);
"""

def init_db():
    """
    Função para inicializar a conexão e criar a tabela livros.
    """
    conn = None
    try:
        # conecta ao banco de dados com o cursor
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute(DROP_LIVROS_TABLE)
        cursor.execute(CREATE_LIVROS_TABLE)
        
        dados_iniciais = [
            ('O Guia do Mochileiro das Galáxias', 'Douglas Adams', 1979, 1, None),
            ('Clean Code', 'Robert C. Martin', 2008, 1, None),
        ]
        
        # uso de executemany para inserir todos os dados de uma vez (melhor performance)
        cursor.executemany(
            "INSERT INTO livros (titulo, autor, ano_publicacao, disponivel, capa) VALUES (?, ?, ?, ?, ?)",
            dados_iniciais
        )
        
        # 6. salva as mudanças
        conn.commit()

        print(f"✅ Banco de dados '{DATABASE_NAME}' inicializado com sucesso e tabela 'livros' criada.")

    except sqlite3.Error as e:
        print(f"❌ Ocorreu um erro ao inicializar o banco de dados: {e}")
    finally:
        # fecha a conexão
        if conn:
            conn.close()

if __name__ == '__main__':
    init_db()