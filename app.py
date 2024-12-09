from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
app = Flask(__name__)
app.secret_key = '1110'


def get_db_connection():
    conn = sqlite3.connect(os.path.join('database', 'users.db'))
    conn.row_factory = sqlite3.Row
    return conn
def get_disciplina_db_connection():
    conn = sqlite3.connect(os.path.join('database', 'disciplinas.db'))
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        faculdade = request.form['faculdade']
        curso = request.form['curso']
        periodo = request.form['periodo']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        if user:
            return render_template('forms.html', error="Usuário já cadastrado", name=name, email=email, faculdade=faculdade, curso=curso, periodo=periodo)
        if password != confirm_password:
            return render_template('forms.html', error="Senhas não coincidem", name=name, email=email, faculdade=faculdade, curso=curso, periodo=periodo)
        if not email.endswith('@ufrpe.br'):
            return render_template('forms.html', error="O e-mail deve ser do domínio @ufrpe.br", name=name, email=email, faculdade=faculdade, curso=curso, periodo=periodo)


        cursor.execute('INSERT INTO users (name, email, password, faculdade, curso, periodo) VALUES (?, ?, ?, ?, ?, ?)',
                       (name, email, password, faculdade, curso, periodo))
        conn.commit()
        conn.close()
        return redirect(url_for('success'))
    return render_template('forms.html')


@app.route('/success')
def success():
    return render_template('success.html')
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        session['user_id'] = user['id']
       
        if email == 'adm@ufrpe.br':
            return redirect(url_for('admin'))  
        return redirect(url_for('feed'))  
    else:
        return render_template('index.html', error="Conta não cadastrada")


@app.route('/feed', methods=['GET', 'POST'])
def feed():
    if 'user_id' not in session:
        return redirect(url_for('index'))




    user_id = session['user_id']
    conn = get_disciplina_db_connection()
    cursor = conn.cursor()








    if request.method == 'POST':
        nome = request.form.get('disciplina_name')
        descricao = request.form.get('disciplina_desc')








        if nome:
            cursor.execute('INSERT INTO disciplinas (nome, descricao) VALUES (?, ?)', (nome, descricao))
            conn.commit()








    cursor.execute('SELECT * FROM disciplinas')
    disciplinas = cursor.fetchall()
    conn.close()
    return render_template('feed.html', user=user_id, disciplinas=disciplinas)
@app.route('/dashboard/<int:user_id>', methods=['GET', 'POST'])
def dashboard(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        if 'edit' in request.form:
            return redirect(url_for('edit', user_id=user_id))
        elif 'delete' in request.form:
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))


    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return render_template('dashboard.html', user=user)


@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cursor.execute('UPDATE users SET name = ?, email = ?, password = ? WHERE id = ?',
                       (name, email, password, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard', user_id=user_id))


    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return render_template('editar.html', user=user)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user_id' not in session:
        return redirect(url_for('index'))


    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()


    if user['email'] != 'adm@ufrpe.br':
        conn.close()
        return redirect(url_for('feed'))


    if request.method == 'POST':
        if 'delete' in request.form:
            user_id_to_delete = request.form['delete']
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id_to_delete,))
            conn.commit()
   
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()


    return render_template('admin.html', users=users)


@app.route('/admin_login', methods=['POST'])
def admin_login():
    email = request.form['email']
    password = request.form['password']


    if email == 'adm@ufrpe.br' and password == 'adm':
        session['user_id'] = 1  # ID do admin
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('index', error="Credenciais inválidas"))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/disciplina', methods=['GET', 'POST'])
def disciplina():
    conn = get_disciplina_db_connection()
    cursor = conn.cursor()

    erro = None  # Variável para armazenar mensagens de erro
    sucesso = None  # Variável para mensagens de sucesso

    if request.method == 'POST':
        tipo = request.form.get('tipo')  # Tipo de publicação (link, comentário, arquivo)
        titulo = request.form.get('titulo')  # Título da publicação
        conteudo = request.form.get('conteudo')  # Conteúdo ou link
        arquivo = request.files.get('arquivo')  # Arquivo enviado (opcional)

        # Validações de formulário
        if not tipo:
            erro = "Por favor, selecione o tipo de publicação."
        elif not (conteudo or (arquivo and arquivo.filename)):
            erro = "Por favor, preencha o conteúdo ou envie um arquivo."
        else:
            try:
                if tipo == "link":
                    conteudo = request.form.get('conteudo_link')
                    if not conteudo:
                        erro = "Por favor, insira a URL do link."
                    else:
                        cursor.execute(
                            'INSERT INTO publicacoes (tipo, titulo, conteudo) VALUES (?, ?, ?)',
                            (tipo, titulo or "Sem título", conteudo)
                        )
                elif tipo == "comentario":
                    conteudo = request.form.get('conteudo_comentario')
                    if not conteudo:
                        erro = "Por favor, insira o conteúdo do comentário."
                    else:
                        cursor.execute(
                            'INSERT INTO publicacoes (tipo, titulo, conteudo) VALUES (?, ?, ?)',
                            (tipo, titulo or "Sem título", conteudo)
                        )
                elif tipo == "arquivo":
                    if arquivo and arquivo.filename:
                        uploads_dir = os.path.join('static', 'uploads')
                        os.makedirs(uploads_dir, exist_ok=True)

                        # Salva o arquivo
                        caminho_arquivo = os.path.join(uploads_dir, arquivo.filename)
                        arquivo.save(caminho_arquivo)

                        cursor.execute(
                            'INSERT INTO publicacoes (tipo, titulo, conteudo, arquivo) VALUES (?, ?, ?, ?)',
                            (tipo, titulo or "Sem título", conteudo, caminho_arquivo)
                        )
                    else:
                        erro = "Por favor, envie um arquivo válido."
                else:
                    erro = "Tipo de publicação inválido."

                if erro is None:
                    conn.commit()
                    sucesso = "Publicação feita com sucesso!"
            except sqlite3.Error as e:
                erro = f"Erro no banco de dados: {str(e)}"
            except Exception as e:
                erro = f"Erro ao processar a publicação: {str(e)}"

    # Busca todas as publicações para exibição
    cursor.execute('SELECT * FROM publicacoes')
    publicacoes = cursor.fetchall()
    conn.close()

    return render_template('disciplina.html', publicacoes=publicacoes, erro=erro, sucesso=sucesso)

@app.route('/disciplinas')
def disciplinas():
    return render_template('disciplina.html')

# Rota para a página de Publicações
@app.route('/publicacoes')
def publicacoes():
    return render_template('publicacoes.html')

if __name__ == '__main__':
    app.run(debug=True)


