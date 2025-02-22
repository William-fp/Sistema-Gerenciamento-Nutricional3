from fastapi import APIRouter, HTTPException
from odmantic import ObjectId
from models import Refeicao, Usuario, Alimento
from database import engine
import re

router = APIRouter(
    prefix="/refeicoes",
    tags=["Refeicoes"],
)

@router.get("/", response_model=list[Refeicao])
async def get_all_refeicoes() -> list[Refeicao]:
    refeicoes = await engine.find(Refeicao)
    return refeicoes

@router.get("/{refeicao_id}", response_model=Refeicao)
async def get_refeicao(refeicao_id: str):
    refeicao = await engine.find_one(Refeicao, Refeicao.id == ObjectId(refeicao_id))
    if not refeicao:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")
    return refeicao

@router.post("/", response_model=Refeicao)
async def create_refeicao(refeicao: Refeicao) -> Refeicao:
    """
    Cria uma refeição e adiciona vários alimentos pelo nome.
    """
    usuario = await engine.find_one(Usuario, Usuario.id == ObjectId(refeicao.usuario.id))
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    alimentos_nomes = [alimento.nome for alimento in refeicao.alimentos]
    alimentos = []
    for nome in alimentos_nomes:
        alimento = await engine.find_one(Alimento, Alimento.nome == nome)
        if not alimento:
            raise HTTPException(status_code=404, detail=f"Alimento '{nome}' não encontrado")
        alimentos.append(alimento)

    nova_refeicao = Refeicao(
        tipo=refeicao.tipo,
        data=refeicao.data,
        usuario=usuario,
        alimentos=alimentos
    )

    await engine.save(nova_refeicao)
    return