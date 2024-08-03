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


# Tags that will be shown in the documentation
home_tag = Tag(name="Documentacoes", description="Seleção de documentação: Swagger, Redoc ou RapiDoc (prefiro o Swagger!)")
vinho_tag = Tag(name="Vinho", description="Retire, adicione, ou encontre os seus vinhos na adega.")
nota_tag = Tag(name="Nota", description="Adicione notas sobre os vinhos da adega.")


# Redirect to /openApi, allowing the selection of the desired documentation to verify the functionality of the APIs.
@app.get('/', tags=[home_tag])
def home():
    return redirect('/openapi')


# Data to be entered for a wine to be added to the cellar, as well as possible errors and their responses.
# In case of duplicate wines, only the log will indicate that it already exists, having no impact on the frontend.
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


# List all existing wines in the cellar.
@app.get('/vinhos', tags=[vinho_tag],
        responses={"200": ListagemVinhosSchema, "404": ErrorSchema})
def get_vinhos():
    """Returns all the wines that are in your cellar.
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


# Returns all the information associated with the requested wine.
@app.get('/vinho', tags=[vinho_tag],
        responses={"200": VinhoViewSchema, "404": ErrorSchema})
def get_vinho(query: VinhoBuscaSchema):
    """Returns a specific wine along with its associated notes.
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


# Deletes wines from the cellar and returns error messages if the wine is not found.
@app.delete('/vinho', tags=[vinho_tag],
            responses={"200": VinhoDelSchema, "404": ErrorSchema})
def del_vinho(query: VinhoBuscaSchema):
    """Removes wines from the cellar.
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


# Inserts notes related to the wines in the cellar and returns error messages if the wine does not exist.
@app.post('/nota', tags=[nota_tag],
        responses={"200": VinhoViewSchema, "404": ErrorSchema})
def add_nota(form: NotaSchema):
    """Add notes to the wines in your cellar.
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
