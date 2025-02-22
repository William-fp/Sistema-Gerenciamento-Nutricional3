from odmantic import Model, Reference, Field
from typing import List
from datetime import date

class Alimento(Model):
    nome: str
    calorias: float
    proteinas: float
    carboidratos: float
    gorduras: float
    sodio: float
    acucar: float

class Usuario(Model):
    nome: str
    idade: int
    peso: float

class Refeicao(Model):
    tipo: str  
    data: date
    usuario: Usuario = Reference()  
    alimentos: List[Alimento] = Field(default_factory=list)