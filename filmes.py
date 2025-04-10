from flask import Flask, render_template, request, redirect, session, flash

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

app = Flask(__name__)
app.secret_key = 'cassics'

@app.route('/')
def index():
    return render_template('lista.html', titulo='Filmes', filmes=lista )

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Filme')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    genero = request.form['genero']
    plataforma = request.form['plataforma']
    filme = Filme(nome, genero, plataforma)
    lista.append(filme)
    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if 'cassics' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash(session['usuario_logado'] + ' logado com sucesso!')
        return redirect('/')
    else:
        flash('Usuário não logado!')
        return redirect('/login')
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect('/')
    
app.run(debug=True) 
