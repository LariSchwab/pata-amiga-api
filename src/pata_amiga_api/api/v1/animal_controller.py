from fastapi import HTTPException
from fastapi.params import Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.pata_amiga_api.app import router
from src.pata_amiga_api.dependencias import get_db
from src.pata_amiga_api.database.modelos import AnimalEntidade
from src.pata_amiga_api.schemas.animal_schemas import Animal, AnimalCadastro, AnimalEditar

@router.get("/api/animais", tags=["animal"])
def listas_todos_animais(filtro: str = Query(default="", alias="filtro"), db: Session = Depends(get_db)):
    pesquisa = f"%{filtro}%"
    animais = db.query(AnimalEntidade).filter(
        or_(
            AnimalEntidade.nome.ilike(pesquisa),
            AnimalEntidade.especie.ilike(pesquisa),
            AnimalEntidade.raca.ilike(pesquisa),
            AnimalEntidade.ong.ilike(pesquisa),
        )
    ).all()
    animais_response = [Animal(
        id=animal.id,
        nome=animal.nome,
        especie=animal.especie,
        raca=animal.raca,
        sexo=animal.sexo,
        porte=animal.porte,
        idade=animal.idade,
        peso=animal.peso,
        ong=animal.ong,
    ) for animal in animais]
    return animais_response

@router.get("/api/animais/{id}", tags=["animal"], response_model=Animal)
def obter_por_id_animais(id: int, db: Session = Depends(get_db)):
    animal = db.query(AnimalEntidade).filter(AnimalEntidade.id == id).first()
    if animal:
        return Animal(
            id=animal.id,
            nome=animal.nome,
            especie=animal.especie,
            raca=animal.raca,
            sexo=animal.sexo,
            porte=animal.porte,
            idade=animal.idade,
            peso=animal.peso,
            ong=animal.ong,
        )
    raise HTTPException(status_code=404, detail=f"Animal não encontrado com id: {id}")

@router.post("/api/animais", tags=["animal"])
def cadastrar_animais(form: AnimalCadastro, db: Session = Depends(get_db)):
    animal = AnimalEntidade(
        nome=form.nome,
        especie=form.especie,
        raca=form.raca,
        sexo=form.sexo,
        porte=form.porte,
        idade=form.idade,
        peso=form.peso,
        ong=form.ong)

    db.add(animal)
    db.commit()
    db.refresh(animal)

    return animal

@router.delete("/api/animais/{id}", status_code=204, tags=["animal"])
def apagar_animais(id: int, db: Session = Depends(get_db)):
    animal = db.query(AnimalEntidade).filter(AnimalEntidade.id == id).first()
    if animal:
        db.delete(animal)
        db.commit()
        return
    raise HTTPException(status_code=404, detail=f"Animal não encontrado com id: {id}")

@router.put("/api/animais/{id}", tags=["animal"])
def editar_animais(id: int, form: AnimalEditar, db: Session = Depends(get_db)):
    animal = db.query(AnimalEntidade).filter(AnimalEntidade.id == id).first()
    if animal:
        animal.nome = form.nome
        animal.especie = form.especie
        animal.raca = form.raca
        animal.sexo = form.sexo
        animal.porte = form.porte
        animal.idade = form.idade
        animal.peso = form.peso
        animal.ong = form.ong
        db.commit()
        db.refresh(animal)
        return animal
    raise HTTPException(status_code=404, detail=f"Animal não encontrado com id: {id}")