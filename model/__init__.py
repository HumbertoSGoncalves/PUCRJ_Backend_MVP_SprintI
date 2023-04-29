from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from model.base import Base
from model.nota import Nota
from model.vinho import Vinho

# Verificação e criação de diretório.
db_path = "database/"
if not os.path.exists(db_path):
   os.makedirs(db_path)


# url de acesso ao banco sqlite local
db_url = 'sqlite:///%s/db.sqlite3' % db_path


# conexão com o banco
engine = create_engine(db_url, echo=False)


# seção com o banco
Session = sessionmaker(bind=engine)


# criação do banco, em caso não exista
if not database_exists(engine.url):
    create_database(engine.url) 


# criação das tabelas do banco
Base.metadata.create_all(engine)
