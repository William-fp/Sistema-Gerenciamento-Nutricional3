from fastapi import APIRouter, HTTPException, Depends, Query
from odmantic import ObjectId
from models import Usuario
from database import engine
from odmantic.query import desc
from datetime import datetime

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
)

@router.post("/", response_model=Usuario)
async def create_usuario(usuario: Usuario):
    """
    Cria um novo usuário.
    """
    await engine.save(usuario)
    return usuario

@router.get("/usuarios", response_model=list[Usuario])
async def get_all_usuarios(
    skip: int = 0,
    limit: int = Query(default=10, le=100),
    sort_by: str = Query(default="nome"),
    order: str = Query(default="asc")
):
    # Acessa dinamicamente o atributo do modelo pelo nome
    campo = getattr(Usuario, sort_by, None)
    if campo is None:
        raise HTTPException(status_code=400, detail="Parâmetro sort_by inválido")
    if order not in ("asc", "desc"):
        raise HTTPException(status_code=400, detail="Parâmetro order inválido")
    
    sort_expression = campo if order == "asc" else desc(campo)
    usuarios = await engine.find(Usuario, sort=sort_expression, skip=skip, limit=limit)
    return usuarios

@router.get("/usuarios/entre_datas/", response_model=list[Usuario])
async def get_usuarios_entre_datas(
    data_inicial: datetime = Query(...),
    data_final: datetime = Query(...)
):
    data_inicial = data_inicial.replace(hour=0, minute=0, second=0, microsecond=0)
    data_final = data_final.replace(hour=23, minute=59, second=59, microsecond=999999)
    eventos = await engine.find(Usuario, Usuario.data >= data_inicial, Usuario.data <= data_final)
    return eventos


@router.get("/{usuario_id}", response_model=Usuario)
async def get_usuario(usuario_id: str):
    """
    Obtém um usuário pelo ID.
    """
    usuario = await engine.find_one(Usuario, Usuario.id == ObjectId(usuario_id))
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.put("/{usuario_id}", response_model=Usuario)
async def update_usuario(usuario_id: str, usuario_data: dict):
    """
    Atualiza um usuário pelo ID.
    """
    usuario = await engine.find_one(Usuario, Usuario.id == ObjectId(usuario_id))
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    for key, value in usuario_data.items():
        setattr(usuario, key, value)
    await engine.save(usuario)
    return usuario

@router.delete("/{usuario_id}")
async def delete_usuario(usuario_id: str):
    """
    Deleta um usuário pelo ID.
    """
    usuario = await engine.find_one(Usuario, Usuario.id == ObjectId(usuario_id))
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    await engine.delete(usuario)
    return {"message": "Usuário deletado com sucesso"}

@router.get("/buscar/", response_model=list[Usuario])
async def search_usuarios(query: str):
    """
    Busca usuários por nome (case insensitive).
    """
    collection = engine.get_collection(Usuario)
    pipeline = [
        {
            "$match": {
                "nome": {
                    "$regex": query,
                    "$options": "i"
                }
            }
        }
    ]
    usuarios = await collection.aggregate(pipeline).to_list(length=None)
    return usuarios

@router.get("/status/contar")
async def count_usuarios():
    """
    Conta o numero de usuarios

    Returns:
        Objeto: Retorna um objeto com o total de usuario
    """ 
    count = await engine.count(Usuario)
    return {"total_usuarios": count}