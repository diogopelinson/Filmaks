from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'cassics'

# CONEXÃO COM O BANCO DE DADOS (MYSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'admin',
        servidor = 'localhost',
        database = 'filmaks'
    )

db = SQLAlchemy(app)

#CRIACÃO DAS CLASSES DO DB
class Filmes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    genero = db.Column(db.String(40), nullable=False)
    plataforma = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<name %r>' % self.name
    

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<name %r>' % self.name
    

#CRIACÃO DAS ROTAS
@app.route('/')
def index():
    lista = Filmes.query.order_by(Filmes.id)
    return render_template('lista.html', titulo='Filmes', filmes=lista )

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        #queryString
        return redirect (url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Filme')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    genero = request.form['genero']
    plataforma = request.form['plataforma']

    filme = Filmes.query.filter_by(nome=nome).first()
    
    if filme:
        flash('Filme já existente!')
        return redirect(url_for('index'))
    
    novo_filme = Filmes(nome=nome, genero=genero, plataforma=plataforma)
    db.session.add(novo_filme)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/login')
def login():
    #complemento da queryString
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

#Login 
@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado!')
        return redirect(url_for('login'))
    
    
#Logout
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))
    
app.run(debug=True) 
