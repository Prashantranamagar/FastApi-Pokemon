from sqlalchemy.future import select
from sqlalchemy.orm import Session
from .models import Pokemon
from .schemas import PokemonCreate

async def get_pokemon(db: Session, pokemon_id: int):
    return await db.get(Pokemon, pokemon_id)

async def get_pokemons(db: Session, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Pokemon).offset(skip).limit(limit))
    return result.scalars().all()

async def create_pokemon(db: Session, pokemon: PokemonCreate):
    db_pokemon = Pokemon(**pokemon.dict())
    db.add(db_pokemon)
    await db.commit()
    await db.refresh(db_pokemon)
    return db_pokemon

async def get_pokemons_by_name_and_type(db: Session, name: str = None, ptype: str = None):
    query = select(Pokemon)
    if name:
        query = query.where(Pokemon.name.ilike(f"%{name}%"))
    if ptype:
        query = query.where(Pokemon.types.any(ptype))
    result = await db.execute(query)
    return result.scalars().all()
