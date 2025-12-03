import sqlite3

# 1. Nome do arquivo do banco de dados (biblioteca.db)
DATABASE_NAME = 'biblioteca.db'

# 2. Instrução SQL para criar a tabela 'livros' 
#  sintaxe adaptada para SQLite
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
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute(DROP_LIVROS_TABLE)
        cursor.execute(CREATE_LIVROS_TABLE)
        
        #  Conecta ao banco de dados. Se o arquivo não existir, ele será criado. Executa a instrução para criar a tabela
        # Opcional: Insere alguns dados iniciais para teste (se desejar)

        cursor.execute("INSERT INTO livros (titulo, autor, ano_publicacao, disponivel) VALUES ('O Guia do Mochileiro das Galáxias', 'Douglas Adams', 1979, 1)")
        cursor.execute("INSERT INTO livros (titulo, autor, ano_publicacao, disponivel) VALUES ('Clean Code', 'Robert C. Martin', 2008, 1)")
        
        # 5. Salva (commita) as mudanças
        conn.commit()

        print(f"✅ Banco de dados '{DATABASE_NAME}' inicializado com sucesso e tabela 'livros' criada.")

    except sqlite3.Error as e:
        print(f"❌ Ocorreu um erro ao inicializar o banco de dados: {e}")
    finally:
        if conn:
                conn.close()

if __name__ == '__main__':
    init_db()