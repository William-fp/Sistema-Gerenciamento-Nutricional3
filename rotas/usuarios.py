from fastapi import APIRouter, HTTPException
from odmantic import ObjectId
from models import Usuario
from database import engine


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
)

@router.post("/", response_model=Usuario)
async def create_usuario(usuario: Usuario):
    
    await engine.save(usuario)
    return usuario


@router.get("/", response_model=list[Usuario])
async def get_all_usuarios() -> list[Usuario]:
   
    usuarios = await engine.find(Usuario)
    return usuarios


@router.get("/{usuario_id}", response_model=Usuario)
async def get_usuario(usuario_id: str):
   
    usuario = await engine.find_one(Usuario, Usuario.id == ObjectId(usuario_id))
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.put("/{usuario_id}", response_model=Usuario)
async def update_usuario(usuario_id: str, usuario_data: dict):
    
    usuario = await engine.find_one(Usuario, Usuario.id == ObjectId(usuario_id))
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    for key, value in usuario_data.items():
        setattr(usuario, key, value)
    await engine.save(usuario)
    return usuario

@router.delete("/{usuario_id}")
async def delete_usuario(usuario_id: str):

    usuario = await engine.find_one(Usuario, Usuario.id == ObjectId(usuario_id))
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    await engine.delete(usuario)
    return {"message": "Usuário excluído com sucesso"}

@router.get("/buscar/", response_model=list[Usuario])
async def search_usuarios(query: str):
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


