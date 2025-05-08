import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='admin'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `filmaks`;")
cursor.execute("CREATE DATABASE `filmaks`;")
cursor.execute("USE `filmaks`;")

# criando tabelas
TABLES = {}
TABLES['Filmes'] = ('''
    CREATE TABLE `filmes` (
                    
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `nome` varchar(50) NOT NULL,
    `genero` varchar(40) NOT NULL,
    `plataforma` varchar(20) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
    CREATE TABLE `usuarios` (
    `nome` varchar(20) NOT NULL,
    `nickname` varchar(8) NOT NULL,
    `senha` varchar(100) NOT NULL,
    PRIMARY KEY (`nickname`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print('Criando tabela {}:'.format(tabela_nome), end=' ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe')
        else:
            print(err.msg)
    else:
        print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
    ('Diogo Pelinson', 'Dxygo', 'lydon'),
    ('Mariana Soliguetti', 'Marisoli', 'riva'),
    ('Adriana Duarte', 'Dridu', 'python')
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from filmaks.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo filmes
filmes_sql = 'INSERT INTO filmes (nome, genero, plataforma) VALUES (%s, %s, %s)'
filmes = [
    ('Titanic', 'Romance', 'Disney+'),
    ('Interestelar', 'Ficção científica', 'Max'),
    ('Ilha do medo', 'Suspense', 'Prime Video'),
    ('Hop - Rebelde sem Páscoa', 'Infantil/Comédia', 'Prime Video'),
    ('Kingsman: Serviço Secreto', 'Ação', 'Disney+'),
    ('Covil de Ladrões 2', 'Ação/Crime', 'Prime Video')
]
cursor.executemany(filmes_sql, filmes)

cursor.execute('select * from filmaks.filmes')
print(' -------------  Filmes:  -------------')
for filme in cursor.fetchall():
    print(filme[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
