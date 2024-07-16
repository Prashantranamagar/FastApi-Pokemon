from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import SessionLocal, init_db

router = APIRouter()

# Dependency
async def get_db():
    async with SessionLocal() as db:
        yield db

@router.on_event("startup")
async def startup():
    await init_db()

@router.get("/pokemons/", response_model=List[schemas.Pokemon])
async def read_pokemons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pokemons = await crud.get_pokemons(db, skip=skip, limit=limit)
    return pokemons

@router.get("/pokemons/filter", response_model=List[schemas.Pokemon])
async def filter_pokemons(name: str = None, ptype: str = None, db: Session = Depends(get_db)):
    pokemons = await crud.get_pokemons_by_name_and_type(db, name=name, ptype=ptype)
    return pokemons
