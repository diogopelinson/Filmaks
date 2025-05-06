from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from filmes import app, db
from models import Filmes, Usuarios
from helpers import recupera_imagem, deleta_arquivo
import time

#CRIACÃO DAS ROTAS

#Visual Dashboard Dos Filmes
@app.route('/')
def index():
    lista = Filmes.query.order_by(Filmes.id)
    return render_template('lista.html', titulo='Filmes', filmes=lista )

#Editar Filmes
@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        #queryString
        return redirect (url_for('login', proxima=url_for('editar')))
    filme = Filmes.query.filter_by(id=id).first()
    capa_filme = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Filme', filme=filme, capa_filme=capa_filme)

#Atualizar Filme 
@app.route('/atualizar', methods=['POST',])
def atualizar():
    filme = Filmes.query.filter_by(id=request.form['id']).first()
    filme.nome = request.form['nome']
    filme.genero = request.form['genero']
    filme.plataforma = request.form['plataforma']
    
    db.session.add(filme)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(filme.id)
    arquivo.save(f'{upload_path}/capa{filme.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


#Deletar Filme
@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect (url_for('login'))

    Filmes.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Filme deletado com sucesso!')

    return redirect(url_for('index'))


#Novo filme
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        #queryString
        return redirect (url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Filme')

#Criar Filme
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

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_filme.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

#Login
@app.route('/login')
def login():
    #complemento da queryString
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

#Autenticar 
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


#Imagem Capa Padrão
@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo )




