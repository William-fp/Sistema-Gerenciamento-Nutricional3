from fastapi import APIRouter, HTTPException, Depends, Query
from database import DBConnection

router = APIRouter(
    prefix="/alimentos",
    tags=["Alimentos"],
)

conn_handle = DBConnection()
conn = conn_handle.get_db_connection()

