from fastapi import APIRouter, HTTPException,  Query
from odmantic import ObjectId
from typing import List, Optional
from models import Refeicao, Usuario, Alimento
from database import engine
from odmantic.query import desc

router = APIRouter(
    prefix="/refeicoes",
    tags=["Refeicoes"],
)

@router.post("/", response_model=Refeicao, operation_id="create_refeicao")
async def criar_refeicao(
    tipo: str = Query(..., description="Tipo da refeição (ex: café da manhã, almoço)"),
    usuario_id: str = Query(..., description="ID do usuário associado"),
    alimentos_nomes: List[str] = Query(..., description="Lista de nomes dos alimentos")
):
    """
    Cria uma nova refeição com os alimentos especificados.
    """
    # Verificar se o usuário existe
    usuario = await engine.find_one(Usuario, Usuario.id == ObjectId(usuario_id))
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Buscar alimentos
    alimentos = []
    for nome in alimentos_nomes:
        alimento = await engine.find_one(Alimento, Alimento.nome == nome)
        if not alimento:
            raise HTTPException(status_code=404, detail=f"Alimento com nome '{nome}' não encontrado")
        alimentos.append(alimento)

    # Criar refeição
    nova_refeicao = Refeicao(
        tipo=tipo,
        usuario=usuario,
        alimentos=alimentos
    )
    
    await engine.save(nova_refeicao)
    return nova_refeicao

@router.get("/", response_model=list[Refeicao])
async def get_all_refeicoes(
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "tipo",
    order: str = "asc"
):
    
    campo = getattr(Refeicao, sort_by, None)
    if campo is None:
        raise HTTPException(status_code=400, detail="Parâmetro sort_by inválido")

    if order not in ("asc", "desc"):
        raise HTTPException(status_code=400, detail="Parâmetro order inválido")

    sort_expression = campo if order == "asc" else desc(campo)

    refeicoes = await engine.find(Refeicao, sort=sort_expression, skip=skip, limit=limit)
    return refeicoes


@router.get("/{refeicao_id}", response_model=Refeicao, operation_id="obter_refeicao")
async def obter_refeicao(refeicao_id: str):
    """
    Obtém uma refeição pelo ID.
    """
    refeicao = await engine.find_one(Refeicao, Refeicao.id == ObjectId(refeicao_id))
    if not refeicao:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")
    return refeicao


@router.get("/{refeicao_id}/calorias", response_model=dict, operation_id="obter_calorias_refeicao")
async def obter_refeicao_calorias(refeicao_id: str):
    """
    Obtém a quantidade total de calorias de uma refeição pelo ID.
    """
    refeicao = await engine.find_one(Refeicao, Refeicao.id == ObjectId(refeicao_id))
    if not refeicao:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")

    total_calorias = sum(alimento.calorias for alimento in refeicao.alimentos)

    return {
        "refeicao_id": str(refeicao.id),
        "tipo": refeicao.tipo,
        "usuario_id": str(refeicao.usuario.id),
        "total_calorias": total_calorias,
    }

@router.put("/{refeicao_id}", response_model=Refeicao, operation_id="atualizar_refeicao")
async def atualizar_refeicao(
    refeicao_id: str,
    tipo: Optional[str] = Query(None),
    usuario_id: Optional[str] = Query(None),
    alimentos_nomes: Optional[List[str]] = Query(None)
):
    """
    Atualiza uma refeição existente.
    """
    refeicao = await engine.find_one(Refeicao, Refeicao.id == ObjectId(refeicao_id))
    if not refeicao:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")

    # Atualizar campos
    if tipo:
        refeicao.tipo = tipo
    if usuario_id:
        usuario = await engine.find_one(Usuario, Usuario.id == ObjectId(usuario_id))
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        refeicao.usuario = usuario
    if alimentos_nomes:
        novos_alimentos = []
        for nome in alimentos_nomes:
            alimento = await engine.find_one(Alimento, Alimento.nome == nome)
            if not alimento:
                raise HTTPException(status_code=404, detail=f"Alimento com nome '{nome}' não encontrado")
            novos_alimentos.append(alimento)
        refeicao.alimentos = novos_alimentos

    await engine.save(refeicao)
    return refeicao

@router.delete("/{refeicao_id}", operation_id="deletar_refeicao")
async def deletar_refeicao(refeicao_id: str):
    """
    Deleta uma refeição pelo ID.
    """
    refeicao = await engine.find_one(Refeicao, Refeicao.id == ObjectId(refeicao_id))
    if not refeicao:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")
    await engine.delete(refeicao)
    return {"message": "Refeição deletada com sucesso"}