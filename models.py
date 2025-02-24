from odmantic import Model, Reference, Field
from datetime import datetime


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
    data: datetime

class Refeicao(Model):
    tipo: str  
    usuario: Usuario = Reference()  
    alimentos: list[Alimento] = Field(default_factory=list)