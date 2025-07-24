from typing import List, Union
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from infrastructure.database.database import get_database_session
from infrastructure.database.models.profile_model import ProfileModel
from app.core.auth import get_current_active_user
from app.application.services.review_service import ReviewService
from app.schemas.review import (
    ReviewCreate, ReviewUpdate, ReviewResponse, ReviewWithRelations,
    ReviewListResponse, ReviewListWithRelations, ProfileAverageRating
)
from app.schemas.user import UserResponse

router = APIRouter()

def get_review_service(db: Session = Depends(get_database_session)) -> ReviewService:
    return ReviewService(db)

@router.post("/", response_model=ReviewResponse, status_code=201)
async def create_review(
    review_data: ReviewCreate,
    current_user: UserResponse = Depends(get_current_active_user),
    service: ReviewService = Depends(get_review_service),
    db: Session = Depends(get_database_session)
):
    """Criar uma nova avaliação"""
    try:
        # Obter o profile_id do usuário logado
        profile = db.query(ProfileModel).filter(ProfileModel.user_id == current_user.id).first()
        
        # Se não tem profile, provavelmente é ADMIN
        if not profile:
            raise HTTPException(status_code=400, detail="Usuários ADMIN não podem fazer avaliações. Seu papel é apenas administrativo.")
        
        # Teste simples - retornar erro se for ADMIN
        if profile.role_id == 1:
            raise HTTPException(status_code=400, detail="Usuários com role ADMIN (role_id = 1) não podem fazer avaliações. Seu papel é apenas administrativo.")
        
        # Criar review com o profile_id do usuário logado
        review = service.create_review_with_profile(review_data, profile.id)
        return review
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/{review_id}", response_model=ReviewWithRelations)
async def get_review(
    review_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    current_user: UserResponse = Depends(get_current_active_user),
    service: ReviewService = Depends(get_review_service)
):
    """Obter uma avaliação por ID"""
    try:
        review = service.get_review_by_id(review_id, include_relations)
        if not review:
            raise HTTPException(status_code=404, detail="Avaliação não encontrada")
        return review
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/", response_model=ReviewListWithRelations)
async def get_all_reviews(
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    current_user: UserResponse = Depends(get_current_active_user),
    service: ReviewService = Depends(get_review_service)
):
    """Obter todas as avaliações"""
    try:
        reviews = service.get_all_reviews(include_relations)
        return {"items": reviews}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/profile/{profile_id}", response_model=ReviewListWithRelations)
async def get_reviews_by_profile(
    profile_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    current_user: UserResponse = Depends(get_current_active_user),
    service: ReviewService = Depends(get_review_service)
):
    """Obter todas as avaliações de um profile"""
    try:
        reviews = service.get_reviews_by_profile_id(profile_id, include_relations)
        return {"items": reviews}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/profile/{profile_id}/average", response_model=ProfileAverageRating)
async def get_profile_average_rating(
    profile_id: int,
    current_user: UserResponse = Depends(get_current_active_user),
    service: ReviewService = Depends(get_review_service)
):
    """Obter a média de avaliações de um profile"""
    try:
        rating_data = service.get_average_rating_by_profile(profile_id)
        return rating_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/space-event-type/{space_event_type_id}", response_model=ReviewListWithRelations)
async def get_reviews_by_space_event_type(
    space_event_type_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    current_user: UserResponse = Depends(get_current_active_user),
    service: ReviewService = Depends(get_review_service)
):
    """Obter todas as avaliações de um space-event type"""
    try:
        reviews = service.get_reviews_by_space_event_type_id(space_event_type_id, include_relations)
        return {"items": reviews}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/space-festival-type/{space_festival_type_id}", response_model=ReviewListWithRelations)
async def get_reviews_by_space_festival_type(
    space_festival_type_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    current_user: UserResponse = Depends(get_current_active_user),
    service: ReviewService = Depends(get_review_service)
):
    """Obter todas as avaliações de um space-festival type"""
    try:
        reviews = service.get_reviews_by_space_festival_type_id(space_festival_type_id, include_relations)
        return {"items": reviews}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/rating/{nota}", response_model=ReviewListWithRelations)
async def get_reviews_by_rating(
    nota: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    current_user: UserResponse = Depends(get_current_active_user),
    service: ReviewService = Depends(get_review_service)
):
    """Obter todas as avaliações com uma nota específica"""
    try:
        if nota < 1 or nota > 5:
            raise HTTPException(status_code=400, detail="Nota deve estar entre 1 e 5")
        
        reviews = service.get_reviews_by_nota(nota, include_relations)
        return {"items": reviews}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/date-range/", response_model=ReviewListWithRelations)
async def get_reviews_by_date_range(
    data_inicio: datetime = Query(..., description="Data de início (YYYY-MM-DD HH:MM:SS)"),
    data_fim: datetime = Query(..., description="Data de fim (YYYY-MM-DD HH:MM:SS)"),
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    current_user: UserResponse = Depends(get_current_active_user),
    service: ReviewService = Depends(get_review_service)
):
    """Obter avaliações em um período"""
    try:
        if data_inicio >= data_fim:
            raise HTTPException(status_code=400, detail="Data de início deve ser anterior à data de fim")
        
        reviews = service.get_reviews_by_date_range(data_inicio, data_fim, include_relations)
        return {"items": reviews}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: int,
    review_data: ReviewUpdate,
    current_user: UserResponse = Depends(get_current_active_user),
    service: ReviewService = Depends(get_review_service)
):
    """Atualizar uma avaliação"""
    try:
        # Verificar se a avaliação existe
        existing_review = service.get_review_by_id(review_id)
        if not existing_review:
            raise HTTPException(status_code=404, detail="Avaliação não encontrada")
        
        # Validar regras de negócio se os relacionamentos foram alterados
        if review_data.space_event_type_id is not None or review_data.space_festival_type_id is not None:
            # Criar dados temporários para validação
            temp_data = ReviewCreate(
                profile_id=existing_review.profile_id,
                space_event_type_id=review_data.space_event_type_id if review_data.space_event_type_id is not None else existing_review.space_event_type_id,
                space_festival_type_id=review_data.space_festival_type_id if review_data.space_festival_type_id is not None else existing_review.space_festival_type_id,
                data_hora=existing_review.data_hora,
                nota=existing_review.nota,
                depoimento=existing_review.depoimento
            )
            
            errors = service.validate_business_rules(temp_data)
            if errors:
                raise HTTPException(status_code=400, detail={"errors": errors})
        
        updated_review = service.update_review(review_id, review_data)
        return updated_review
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.delete("/{review_id}", status_code=200)
async def delete_review(
    review_id: int,
    current_user: UserResponse = Depends(get_current_active_user),
    service: ReviewService = Depends(get_review_service)
):
    """Deletar uma avaliação"""
    try:
        success = service.delete_review(review_id)
        if not success:
            raise HTTPException(status_code=404, detail="Avaliação não encontrada")
        
        return {"message": f"Avaliação com ID {review_id} foi deletada com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}") 