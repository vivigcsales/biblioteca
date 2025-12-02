import sqlite3
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
DATABASE_NAME = 'biblioteca.db'

#função para obter a conexão
def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    # retorna colunas como dicionário, podendo acessar colunas por nome
    conn.row_factory = sqlite3.Row 
    return conn

#rota (GET para listar/) (POST para adicionar) livros
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano_publicacao = request.form['ano_publicacao']
        disponivel = 1 if 'disponivel' in request.form else 0
        
        conn = get_db_connection()
        conn.execute('INSERT INTO livros (titulo, autor, ano_publicacao, disponivel) VALUES (?, ?, ?, ?)',
                     (titulo, autor, ano_publicacao, disponivel))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

    # Listar livros
    conn = get_db_connection()
    livros = conn.execute('SELECT * FROM livros').fetchall()
    conn.close()
    
    # Renderiza o template HTML 
    return render_template('index.html', livros=livros) 

if __name__ == '__main__':
    app.run(port=5000, debug=True)