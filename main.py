from fastapi import FastAPI
from rotas import home, usuarios
#from rotas import home, usuarios, refeicoes, alimentos

app = FastAPI()

app.include_router(home.router)
app.include_router(usuarios.router)
#app.include_router(refeicoes.router)
#app.include_router(alimentos.router)