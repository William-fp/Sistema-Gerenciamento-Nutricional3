from fastapi import APIRouter, Depends, HTTPException, Query
from database import DBConnection

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
)

conn_handle = DBConnection()
conn = conn_handle.get_db_connection()

@router.post("/", response_model=Usuario)
def create_usuario(usuario: Usuario, session: Session = Depends(get_session)):
    """
    Cria um usuario
    Args:
        usuario (Usuario): Objeto usuario a ser criado
        session (Session): Sessao do banco de dados

    Returns:
        usuario: Usuario criado
    """ 
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario
# nao mexi ainda
