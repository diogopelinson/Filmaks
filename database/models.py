from filmes import db

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