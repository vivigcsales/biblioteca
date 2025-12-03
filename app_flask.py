import sqlite3
from flask import Flask, render_template, request, redirect, url_for

import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
DATABASE_NAME = 'biblioteca.db'
UPLOAD_FOLDER = 'static/assets'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#função para obter a conexão
def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    # retorna colunas como dicionário, podendo acessar colunas por nome
    conn.row_factory = sqlite3.Row 
    return conn

#rota (GET para listar/) (POST para adicionar) livros
@app.route('/', methods=['GET'])
def list_books():
    """Render the list of books (GET only)."""
    conn = get_db_connection()
    livros = conn.execute('SELECT * FROM livros ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', livros=livros)


@app.route('/add', methods=['GET', 'POST'])
def add_book():
    """Show the form to add a book (GET) and handle submission (POST)."""
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        try:
            ano_publicacao = int(request.form['ano_publicacao'])
        except ValueError:
            ano_publicacao = None
        disponivel = 1 if 'disponivel' in request.form else 0
        
        # Handle file upload
        capa_filename = None
        if 'capa' in request.files:
            file = request.files['capa']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                capa_filename = filename

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO livros (titulo, autor, ano_publicacao, disponivel, capa) VALUES (?, ?, ?, ?, ?)',
            (titulo, autor, ano_publicacao, disponivel, capa_filename)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('list_books'))
    return render_template('add_book.html')

@app.route('/book/<int:id>', methods=['GET'])
def get_book(id):
    """Return book details as JSON (for Modal)."""
    conn = get_db_connection()
    livro = conn.execute('SELECT * FROM livros WHERE id = ?', (id,)).fetchone()
    conn.close()
    if livro is None:
        return {'error': 'Book not found'}, 404
    return dict(livro)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    """Edit an existing book."""
    conn = get_db_connection()
    livro = conn.execute('SELECT * FROM livros WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        try:
            ano_publicacao = int(request.form['ano_publicacao'])
        except ValueError:
            ano_publicacao = None
        disponivel = 1 if 'disponivel' in request.form else 0
        
        # Handle file upload (optional update)
        capa_filename = livro['capa'] # Keep existing by default
        if 'capa' in request.files:
            file = request.files['capa']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                capa_filename = filename

        conn.execute(
            'UPDATE livros SET titulo = ?, autor = ?, ano_publicacao = ?, disponivel = ?, capa = ? WHERE id = ?',
            (titulo, autor, ano_publicacao, disponivel, capa_filename, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('list_books'))

    conn.close()
    return render_template('edit_book.html', livro=livro)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    """Delete a book."""
    conn = get_db_connection()
    conn.execute('DELETE FROM livros WHERE id = ?', (id,)).fetchone()
    conn.commit()
    conn.close()
    return redirect(url_for('list_books'))

# Keep the original route name for backward compatibility (optional)
@app.route('/', methods=['GET'])
def index():
    return list_books()


if __name__ == '__main__':
    app.run(port=5000, debug=True)