from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter(
    prefix="/refeicoes",
    tags=["Refeicoes"],
)