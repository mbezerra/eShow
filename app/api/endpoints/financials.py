from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from infrastructure.database.database import get_database_session
from app.core.auth import get_current_active_user
from app.application.services.financial_service import FinancialService
from app.schemas.financial import (
    FinancialCreate, FinancialUpdate, FinancialResponse, FinancialWithRelations,
    FinancialListResponse, FinancialListWithRelations, TipoContaEnum, 
    TipoChavePixEnum, PreferenciaTransferenciaEnum
)
from app.schemas.user import UserResponse

router = APIRouter()

def get_financial_service(db: Session = Depends(get_database_session)) -> FinancialService:
    return FinancialService(db)

@router.post("/", response_model=FinancialResponse, status_code=201)
async def create_financial(
    financial_data: FinancialCreate,
    current_user: UserResponse = Depends(get_current_active_user),
    service: FinancialService = Depends(get_financial_service)
):
    """Criar um novo registro financeiro"""
    try:
        # Validar regras de negócio
        errors = service.validate_business_rules(financial_data)
        if errors:
            raise HTTPException(status_code=400, detail={"errors": errors})
        
        financial = service.create_financial(financial_data)
        return financial
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/{financial_id}", response_model=Union[FinancialResponse, FinancialWithRelations])
async def get_financial(
    financial_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    current_user: UserResponse = Depends(get_current_active_user),
    service: FinancialService = Depends(get_financial_service)
):
    """Obter um registro financeiro por ID"""
    try:
        financial = service.get_financial_by_id(financial_id, include_relations)
        if not financial:
            raise HTTPException(status_code=404, detail="Registro financeiro não encontrado")
        return financial
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/", response_model=Union[FinancialListResponse, FinancialListWithRelations])
async def get_all_financials(
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    current_user: UserResponse = Depends(get_current_active_user),
    service: FinancialService = Depends(get_financial_service)
):
    """Obter todos os registros financeiros"""
    try:
        financials = service.get_all_financials(include_relations)
        return {"items": financials}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/profile/{profile_id}", response_model=Union[FinancialListResponse, FinancialListWithRelations])
async def get_financials_by_profile(
    profile_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    current_user: UserResponse = Depends(get_current_active_user),
    service: FinancialService = Depends(get_financial_service)
):
    """Obter todos os registros financeiros de um profile"""
    try:
        financials = service.get_financials_by_profile_id(profile_id, include_relations)
        return {"items": financials}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/banco/{banco}", response_model=Union[FinancialListResponse, FinancialListWithRelations])
async def get_financials_by_banco(
    banco: str,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    current_user: UserResponse = Depends(get_current_active_user),
    service: FinancialService = Depends(get_financial_service)
):
    """Obter todos os registros financeiros de um banco específico"""
    try:
        # Validar formato do código do banco
        if not banco.isdigit() or len(banco) != 3:
            raise HTTPException(status_code=400, detail="Código do banco deve ser uma string com 3 dígitos (001-999)")
        
        banco_num = int(banco)
        if banco_num < 1 or banco_num > 999:
            raise HTTPException(status_code=400, detail="Código do banco deve estar entre 001 e 999")
        
        financials = service.get_financials_by_banco(banco, include_relations)
        return {"items": financials}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/tipo-conta/{tipo_conta}", response_model=Union[FinancialListResponse, FinancialListWithRelations])
async def get_financials_by_tipo_conta(
    tipo_conta: TipoContaEnum,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    current_user: UserResponse = Depends(get_current_active_user),
    service: FinancialService = Depends(get_financial_service)
):
    """Obter registros financeiros por tipo de conta"""
    try:
        financials = service.get_financials_by_tipo_conta(tipo_conta, include_relations)
        return {"items": financials}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/tipo-chave-pix/{tipo_chave_pix}", response_model=Union[FinancialListResponse, FinancialListWithRelations])
async def get_financials_by_tipo_chave_pix(
    tipo_chave_pix: TipoChavePixEnum,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    current_user: UserResponse = Depends(get_current_active_user),
    service: FinancialService = Depends(get_financial_service)
):
    """Obter registros financeiros por tipo de chave PIX"""
    try:
        financials = service.get_financials_by_tipo_chave_pix(tipo_chave_pix, include_relations)
        return {"items": financials}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/chave-pix/{chave_pix}", response_model=Union[FinancialResponse, FinancialWithRelations])
async def get_financial_by_chave_pix(
    chave_pix: str,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    current_user: UserResponse = Depends(get_current_active_user),
    service: FinancialService = Depends(get_financial_service)
):
    """Obter registro financeiro por chave PIX"""
    try:
        financial = service.get_financial_by_chave_pix(chave_pix, include_relations)
        if not financial:
            raise HTTPException(status_code=404, detail="Registro financeiro não encontrado para esta chave PIX")
        return financial
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/preferencia/{preferencia}", response_model=Union[FinancialListResponse, FinancialListWithRelations])
async def get_financials_by_preferencia(
    preferencia: PreferenciaTransferenciaEnum,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    current_user: UserResponse = Depends(get_current_active_user),
    service: FinancialService = Depends(get_financial_service)
):
    """Obter registros financeiros por preferência de transferência"""
    try:
        financials = service.get_financials_by_preferencia(preferencia, include_relations)
        return {"items": financials}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/cpf-cnpj/{cpf_cnpj}", response_model=Union[FinancialListResponse, FinancialListWithRelations])
async def get_financials_by_cpf_cnpj(
    cpf_cnpj: str,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    current_user: UserResponse = Depends(get_current_active_user),
    service: FinancialService = Depends(get_financial_service)
):
    """Obter registros financeiros por CPF/CNPJ"""
    try:
        financials = service.get_financials_by_cpf_cnpj(cpf_cnpj, include_relations)
        return {"items": financials}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/check-chave-pix/{chave_pix}")
async def check_chave_pix_availability(
    chave_pix: str,
    exclude_id: int = Query(None, description="ID a ser excluído da verificação"),
    current_user: UserResponse = Depends(get_current_active_user),
    service: FinancialService = Depends(get_financial_service)
):
    """Verificar se uma chave PIX está disponível"""
    try:
        is_available = service.check_chave_pix_available(chave_pix, exclude_id)
        return {
            "chave_pix": chave_pix,
            "available": is_available,
            "message": "Chave PIX disponível" if is_available else "Chave PIX já está em uso"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/statistics/banks")
async def get_banks_statistics(
    current_user: UserResponse = Depends(get_current_active_user),
    service: FinancialService = Depends(get_financial_service)
):
    """Obter estatísticas de registros por banco"""
    try:
        banks_summary = service.get_banks_summary()
        return {
            "total_banks": len(banks_summary),
            "banks": banks_summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/statistics/pix-types")
async def get_pix_types_statistics(
    current_user: UserResponse = Depends(get_current_active_user),
    service: FinancialService = Depends(get_financial_service)
):
    """Obter estatísticas de tipos de chave PIX"""
    try:
        pix_types_summary = service.get_pix_types_summary()
        return {
            "total_types": len(pix_types_summary),
            "pix_types": pix_types_summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.put("/{financial_id}", response_model=FinancialResponse)
async def update_financial(
    financial_id: int,
    financial_data: FinancialUpdate,
    current_user: UserResponse = Depends(get_current_active_user),
    service: FinancialService = Depends(get_financial_service)
):
    """Atualizar um registro financeiro"""
    try:
        # Verificar se o registro existe
        existing_financial = service.get_financial_by_id(financial_id)
        if not existing_financial:
            raise HTTPException(status_code=404, detail="Registro financeiro não encontrado")
        
        updated_financial = service.update_financial(financial_id, financial_data)
        return updated_financial
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.delete("/{financial_id}", status_code=204)
async def delete_financial(
    financial_id: int,
    current_user: UserResponse = Depends(get_current_active_user),
    service: FinancialService = Depends(get_financial_service)
):
    """Deletar um registro financeiro"""
    try:
        success = service.delete_financial(financial_id)
        if not success:
            raise HTTPException(status_code=404, detail="Registro financeiro não encontrado")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}") 