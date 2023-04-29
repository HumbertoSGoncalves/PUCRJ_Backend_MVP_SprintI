from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Vinho, Nota
from logger import logger
from schemas import *
from flask_cors import CORS


info = Info(title="MVP - Backend", version="2.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# tags que serão expostas na documentação
home_tag = Tag(name="Documentacoes", description="Seleção de documentação: Swagger, Redoc ou RapiDoc (prefiro o Swagger!)")
vinho_tag = Tag(name="Vinho", description="Retire, adicione, ou encontre os seus vinhos na adega.")
nota_tag = Tag(name="Nota", description="Adicione notas sobre os vinhos da adega.")


# redirecionamento para o /openApi, permitindo a escolha de documentação desejada para averiguar funcionamento das APIs.
@app.get('/', tags=[home_tag])
def home():
    return redirect('/openapi')


# dados a serem inseridos para que um vinho seja adicionado na adega, assim como as possibibilidades de erros e suas respostas
# em caso de vinhos repetidos, somente o log informará que já é existente, não tendo impacto no frontend
@app.post('/vinho', tags=[vinho_tag],
          responses={"200": VinhoSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_vinho(form: VinhoSchema):
    """Chegou vinho novo na adega, so adicionar!
    """
    vinho = Vinho(
        vinho=form.vinho,
        uva=form.uva,
        ano=form.ano,
        categoria=form.categoria,
        fabricante=form.fabricante)
    logger.debug(f"Adicionando vinho: '{vinho.vinho}'")
    try:
        session = Session()
        session.add(vinho)
        session.commit()
        logger.debug(f"Adicionado vinho: '{vinho.vinho}'")
        return apresenta_vinho(vinho), 200
    except IntegrityError as e:
        error_msg = "Vinho ja existente na adega."
        logger.warning(f"Erro ao adicionar vinho '{vinho.vinho}', {error_msg}")
        return {"message": error_msg}, 409
    except Exception as e:
        error_msg = "Não foi possível salvar novo vinho na Adega online :/"
        logger.warning(f"Erro ao adicionar vinho '{vinho.vinho}', {error_msg}")
        return {"message": error_msg}, 400


#listar todos os vinhos existentes na adega
@app.get('/vinhos', tags=[vinho_tag],
        responses={"200": ListagemVinhosSchema, "404": ErrorSchema})
def get_vinhos():
    """Retorna todos os vinhos que estão na sua adega!
    """
    logger.debug(f"Coletando vinhos ")
    session = Session()
    vinhos = session.query(Vinho).all()
    if not vinhos:
        return {"vinhos": []}, 200
    else:
        logger.debug(f"%d vinhos encontrados" % len(vinhos))
        print(vinhos)
        return apresenta_vinhos(vinhos), 200


# retorna todas as informaçoes associadas ao vinho procurado
@app.get('/vinho', tags=[vinho_tag],
        responses={"200": VinhoViewSchema, "404": ErrorSchema})
def get_vinho(query: VinhoBuscaSchema):
    """Retorna um vinho específico com as suas referentes notas!
    """
    vinho_id = query.vinho
    logger.debug(f"Coletando dados sobre vinho #{vinho_id}")
    session = Session()
    vinho = session.query(Vinho).filter(Vinho.vinho == vinho_id).first()
    if not vinho:
        error_msg = "Vinho não encontrado na Adega :/"
        logger.warning(f"Erro ao buscar vinho '{vinho_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Vinho econtrado: '{vinho.vinho}'")
        return apresenta_vinho(vinho), 200


# deleta vinhos da adega, assim como retorna mensagens de erro em caso o vinho não seja encontrado
@app.delete('/vinho', tags=[vinho_tag],
            responses={"200": VinhoDelSchema, "404": ErrorSchema})
def del_vinho(query: VinhoBuscaSchema):
    """Retirar vinhos da sua adega!
    """
    vinho_nome = unquote(unquote(query.vinho))
    print(vinho_nome)
    logger.debug(f"Deletando dados sobre vinho #{vinho_nome}")
    session = Session()
    count = session.query(Vinho).filter(Vinho.vinho == vinho_nome).delete()
    session.commit()
    if count:
        logger.debug(f"Deletado vinho #{vinho_nome}")
        return {"message": "Vinho removido (espero que tenha sido bebido)", "id": vinho_nome}
    else:
        error_msg = "Vinho não encontrado na base (ja bebeu, talvez?)"
        logger.warning(f"Erro ao deletar vinho #'{vinho_nome}', {error_msg}")
        return {"message": error_msg}, 404


#inserção de notas referentes aos vinhos da adega, assim como mensagens de erro em caso o vinho não exista
@app.post('/nota', tags=[nota_tag],
        responses={"200": VinhoViewSchema, "404": ErrorSchema})
def add_nota(form: NotaSchema):
    """Adicione notas aos vinhos da sua adega!
    """
    vinho_id  = form.vinho_id
    logger.debug(f"Adicionando comentários ao vinho #{vinho_id}")
    session = Session()
    vinho = session.query(Vinho).filter(Vinho.id == vinho_id).first()
    if not vinho:
        error_msg = "Vinho não encontrado na adega (talvez ja tenha bebido?)."
        logger.warning(f"Erro ao adicionar comentário ao vinho '{vinho_id}', {error_msg}")
        return {"message": error_msg}, 404
    texto = form.texto
    nota = Nota(texto)
    vinho.adiciona_nota(nota)
    session.commit()
    logger.debug(f"Adicionado comentário ao vinho #{vinho_id}")
    return apresenta_vinho(vinho), 200
