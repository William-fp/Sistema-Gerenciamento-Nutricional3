from fastapi import APIRouter, HTTPException
from odmantic import ObjectId
from models import Alimento
from database import engine
from odmantic.query import desc


router = APIRouter(
    prefix="/alimentos",
    tags=["Alimentos"],
)

@router.post("/", response_model=Alimento)
async def create_alimento(alimento: Alimento):
    await engine.save(alimento)
    return alimento

@router.get("/", response_model=list[Alimento])
async def get_all_alimentos(
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "nome",
    order: str = "asc"
):
    # Tenta acessar dinamicamente o atributo de Alimento com o nome passado em sort_by
    campo = getattr(Alimento, sort_by, None)
    if campo is None:
        raise HTTPException(status_code=400, detail="Parâmetro sort_by inválido")
    
    if order not in ("asc", "desc"):
        raise HTTPException(status_code=400, detail="Parâmetro order inválido")
    
    sort_expression = campo if order == "asc" else desc(campo)
    
    alimentos = await engine.find(Alimento, sort=sort_expression, skip=skip, limit=limit)
    return alimentos

@router.get("/{alimento_id}", response_model=Alimento)
async def get_alimento(alimento_id: str):
   
    alimento = await engine.find_one(Alimento, Alimento.id == ObjectId(alimento_id))
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento não encontrado")
    return alimento

@router.put("/{alimento_id}", response_model=Alimento)
async def update_alimento(alimento_id: str, alimento_data: dict):
    
    alimento = await engine.find_one(Alimento, Alimento.id == ObjectId(alimento_id))
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento não encontrado")
    for key, value in alimento_data.items():
        setattr(alimento, key, value)
    await engine.save(alimento)
    return alimento

@router.delete("/{alimento_id}")
async def delete_alimento(alimento_id: str):
 
    alimento = await engine.find_one(Alimento, Alimento.id == ObjectId(alimento_id))
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento não encontrado")
    await engine.delete(alimento)
    return {"message": "Alimento deletado com sucesso"}


@router.get("/buscar/", response_model=list[Alimento])
async def search_alimentos(query: str):
    collection = engine.get_collection(Alimento)
    
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
    
    alimentos = await collection.aggregate(pipeline).to_list(length=None)
    
    return alimentos