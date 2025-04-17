from flask import Flask, render_template, request, redirect, session, flash, url_for

class Filme:
    def __init__(self, nome, genero, plataforma):
        self.nome = nome
        self.genero = genero
        self.plataforma = plataforma

#Lista de Filmes
filme1 = Filme('Titanic', 'Romance', 'Disney+') 
filme2 = Filme('Interestelar', 'Ficção científica', 'Max')
filme3 = Filme('Ilha do medo', 'Suspense', 'Prime Video')
lista = [filme1, filme2, filme3]

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('Diogo Pelinson', 'Dxygo', 'lydon')
usuario2 = Usuario('Mariana Soliguetti', 'Marisoli', 'riva')
usuario3 = Usuario('Adriana Duarte', 'Dridu', 'python')

#Dicionario dos usuarios
usuarios = { 
    usuario1.nickname : usuario1,
    usuario2.nickname : usuario2,
    usuario3.nickname : usuario3,
}

app = Flask(__name__)
app.secret_key = 'cassics'

@app.route('/')
def index():
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
    filme = Filme(nome, genero, plataforma)
    lista.append(filme)
    #função que instancia a pagina principal
    return redirect(url_for('index'))

@app.route('/login')
def login():
    #complemento da queryString
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

#Login 
@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
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
