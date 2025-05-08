from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from filmes import app, db
from database.models import Filmes
from helpers.helpers import recupera_imagem, deleta_arquivo, FormularioFilme
from helpers.config_img import UPLOAD_PATH
import time
import os

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
    form = FormularioFilme()
    form.nome.data = filme.nome
    form.genero.data = filme.genero
    form.plataforma.data = filme.plataforma
    capa_filme = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Filme', id=id, capa_filme=capa_filme, form=form)

#Atualizar Filme 
@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioFilme(request.form)

    if form.validate_on_submit():
        filme = Filmes.query.filter_by(id=request.form['id']).first()
        filme.nome = form.nome.data
        filme.genero = form.genero.data
        filme.plataforma = form.plataforma.data
        
        db.session.add(filme)
        db.session.commit()

    arquivo = request.files['arquivo']
    if arquivo:
        timestamp = time.time()
        deleta_arquivo(filme.id)
        nome_arquivo = f'capa{filme.id}-{timestamp}.jpg'
        caminho_arquivo = os.path.join(UPLOAD_PATH, nome_arquivo)
        arquivo.save(caminho_arquivo)

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
        return redirect (url_for('login', proxima=url_for('novo')))
    form = FormularioFilme()
    return render_template('novo.html', titulo='Novo Filme', form=form)


# Criar Filme
@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioFilme(request.form)

    if not form.validate_on_submit():
        flash('Erro na validação do formulário.')
        return redirect(url_for('novo'))

    flash('Formulário enviado corretamente!')
    nome = form.nome.data
    genero = form.genero.data
    plataforma = form.plataforma.data

  
    filme = Filmes.query.filter_by(nome=nome).first()

    if filme:
        flash('Filme já existente!')
        return redirect(url_for('index'))

   
    novo_filme = Filmes(nome=nome, genero=genero, plataforma=plataforma)
    db.session.add(novo_filme)
    db.session.commit()


    if 'arquivo' in request.files:
        arquivo = request.files['arquivo']
        timestamp = time.time()

        nome_arquivo = f'capa{novo_filme.id}-{timestamp}.jpg'

        arquivo.save(os.path.join(UPLOAD_PATH, nome_arquivo))

    return redirect(url_for('index'))



#Imagem Capa Padrão
@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo )




