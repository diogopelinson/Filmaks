import os
from filmes import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField

class FormularioFilme(FlaskForm):
    nome = StringField('Nome do Filme:', [validators.DataRequired(), validators.Length(min=1, max=50)])
    genero = StringField('Gênero:', [validators.DataRequired(), validators.Length(min=1, max=40)])
    plataforma = StringField('Plataforma:', [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname:', [validators.DataRequired(), validators.Length(min=1, max=8)] )
    senha = PasswordField('Senha:', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')

def recupera_imagem(id):
    upload_path = app.config['UPLOAD_PATH']
    for nome_arquivo in os.listdir(upload_path):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo
    return 'capa_padrao.jpg'


def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        arquivo_path = os.path.join(app.config['UPLOAD_PATH'], arquivo)
        if os.path.exists(arquivo_path):
            os.remove(arquivo_path)