import sqlite3
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()(title="API da Biblioteca", version="1.0.0")
DATABASE_NAME = 'biblioteca.db'
# conexão com o banco de dados

# Define a estrutura de dados que a API vai receber/retornar
class LivroBase(BaseModel):
    titulo: str
    autor: str
    ano_publicacao: int
    disponivel: bool

class Livro(LivroBase):
    id: int

# cria e retonra uma conexão com o banco de dados 
def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn
# faz com que os resultados sejam acessíveis por nome de coluna tipo dicionário 

# --- Endpoints da API REST ---

# adiciona novo livro (CREATE
@app.post("/livros", status_code=status.HTTP_201_CREATED, response_model=Livro)
def add_livro(livro: LivroBase): # Pydantic valida a entrada 'livro'
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO livros (titulo, autor, ano_publicacao, disponivel) VALUES (?, ?, ?, ?)",
            (livro.titulo, livro.autor, livro.ano_publicacao, livro.disponivel)
        )
        conn.commit()
        return {"message": "Livro adicionado com sucesso", "id": cursor.lastrowid} #retorna o novo id do novo livro
        return {**livro.dict(), "id": novo_id}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro ao inserir: {e}")
    finally:
        conn.close()

# lista todos os livros (READ
@app.get("/livros/", response_model=list[Livro])
def list_livros():
    conn = get_db_connection()
    livros_db = conn.execute('SELECT * FROM livros').fetchall()
    conn.close()

    livros = [dict(livro) for livro in livros_db]
    return livros 
#faz tipo um dicionários com os livros, pq converte os objetos em uma lista

#lista um livro específico - READ SINGLE
@app.get("/livros/{id}", response_model=Livro)
def get_livro(id: int):
    conn = get_db_connection()
    # Usa WHERE para buscar pelo ID
    livro_db = conn.execute('SELECT * FROM livros WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if livro_db is None:
        # 404 Not Found se o livro não for encontrado
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
    
    # Retorna o livro como um dicionário
    return dict(livro_db)

# atualiza um livro existente - UPDATE
@app.put("/livros/{id}", response_model=Livro)
def update_livro(id: int, livro: LivroBase):
    conn = get_db_connection()
    cursor = conn.cursor()
  
    cursor.execute(
            "UPDATE livros SET titulo = ?, autor = ?, ano_publicacao = ?, disponivel = ? WHERE id = ?",
            (livro.titulo, livro.autor, livro.ano_publicacao, livro.disponivel, id)
        )
    conn.commit()
        
    #aqui ele vai verificar se alguma liha foi afetada, se o id existe 
    if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
    
    livro_atualizado = conn.execute('SELECT * FROM livros WHERE id = ?', (id,)).fetchone()
    conn.close()
    return dict(livro_atualizado)

#aqui ele busca o livro e retorna atualizado, retorna 200 e o objeto atualizado

# deleta um livro (DELETE
@app.delete("/livros/{id}", status_code=status.HTTP_200_OK)
def delete_livro(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM livros WHERE id = ?", (id,))
    conn.commit()
    
    #aqui ele verifica se alguma linha foi afetada, se o id existe
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado para exclusão")
    
    conn.close()
    return {"message": "Livro deletado com sucesso"}