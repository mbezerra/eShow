#!/usr/bin/env python3
"""
Script para inicializar dados de exemplo de financials
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.database.models.financial_model import FinancialModel
from infrastructure.database.models.profile_model import ProfileModel
from infrastructure.database.database import Base

def init_financials_data():
    """Inicializar dados de exemplo de financials"""
    
    # Configurar banco de dados
    database_url = os.getenv("DATABASE_URL", "sqlite:///./eShow.db")
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    with SessionLocal() as db:
        try:
            # Verificar se já existem financials
            existing_financials = db.query(FinancialModel).first()
            if existing_financials:
                print("Financials já existem no banco de dados. Pulando inicialização...")
                return
            
            # Obter profiles existentes
            profiles = db.query(ProfileModel).all()
            
            if not profiles:
                print("Nenhum profile encontrado. Execute init_profiles.py primeiro.")
                return
            
            # Dados de exemplo de financials
            financials_data = [
                {
                    "profile_id": profiles[0].id,
                    "banco": "341",  # Itaú
                    "agencia": "1234",
                    "conta": "12345-6",
                    "tipo_conta": "Corrente",
                    "cpf_cnpj": "12345678901",
                    "tipo_chave_pix": "CPF",
                    "chave_pix": "12345678901",
                    "preferencia": "PIX"
                },
                {
                    "profile_id": profiles[1].id,
                    "banco": "237",  # Bradesco
                    "agencia": "5678",
                    "conta": "67890-1",
                    "tipo_conta": "Poupança",
                    "cpf_cnpj": "98765432100",
                    "tipo_chave_pix": "E-mail",
                    "chave_pix": "usuario@example.com",
                    "preferencia": "PIX"
                },
                {
                    "profile_id": profiles[2].id,
                    "banco": "104",  # Caixa
                    "agencia": "9012",
                    "conta": "34567-8",
                    "tipo_conta": "Corrente",
                    "cpf_cnpj": "11122233344",
                    "tipo_chave_pix": "Celular",
                    "chave_pix": "11987654321",
                    "preferencia": "TED"
                }
            ]
            
            # Adicionar mais dados se houver mais profiles
            if len(profiles) > 3:
                additional_data = [
                    {
                        "profile_id": profiles[3].id,
                        "banco": "001",  # Banco do Brasil
                        "agencia": "3456",
                        "conta": "78901-2",
                        "tipo_conta": "Poupança",
                        "cpf_cnpj": "12345678000195",  # CNPJ
                        "tipo_chave_pix": "CNPJ",
                        "chave_pix": "12345678000195",
                        "preferencia": "PIX"
                    },
                    {
                        "profile_id": profiles[4].id if len(profiles) > 4 else profiles[0].id,
                        "banco": "033",  # Santander
                        "agencia": "7890",
                        "conta": "23456-7",
                        "tipo_conta": "Corrente",
                        "cpf_cnpj": "55544433322",
                        "tipo_chave_pix": "Aleatória",
                        "chave_pix": "123e4567-e89b-12d3-a456-426614174000",
                        "preferencia": "PIX"
                    },
                    {
                        "profile_id": profiles[5].id if len(profiles) > 5 else profiles[1].id,
                        "banco": "260",  # Nu Pagamentos
                        "agencia": "0001",
                        "conta": "89012-3",
                        "tipo_conta": "Corrente",
                        "cpf_cnpj": "66677788899",
                        "tipo_chave_pix": "E-mail",
                        "chave_pix": "contato@empresa.com.br",
                        "preferencia": "PIX"
                    }
                ]
                
                financials_data.extend(additional_data)
            
            # Criar financials no banco
            created_count = 0
            for financial_data in financials_data:
                financial = FinancialModel(
                    profile_id=financial_data["profile_id"],
                    banco=financial_data["banco"],
                    agencia=financial_data["agencia"],
                    conta=financial_data["conta"],
                    tipo_conta=financial_data["tipo_conta"],
                    cpf_cnpj=financial_data["cpf_cnpj"],
                    tipo_chave_pix=financial_data["tipo_chave_pix"],
                    chave_pix=financial_data["chave_pix"],
                    preferencia=financial_data["preferencia"]
                )
                
                db.add(financial)
                created_count += 1
            
            db.commit()
            print(f"✅ {created_count} registros financeiros criados com sucesso!")
            
            # Mostrar estatísticas
            total_financials = db.query(FinancialModel).count()
            print(f"📊 Total de registros financeiros no banco: {total_financials}")
            
            # Mostrar distribuição por banco
            bancos_count = {}
            all_financials = db.query(FinancialModel).all()
            for financial in all_financials:
                if financial.banco in bancos_count:
                    bancos_count[financial.banco] += 1
                else:
                    bancos_count[financial.banco] = 1
            
            print("📈 Distribuição por banco:")
            bank_names = {
                "001": "Banco do Brasil",
                "033": "Santander",
                "104": "Caixa",
                "237": "Bradesco",
                "260": "Nu Pagamentos",
                "341": "Itaú"
            }
            
            for banco, count in bancos_count.items():
                bank_name = bank_names.get(banco, f"Banco {banco}")
                print(f"   {bank_name} ({banco}): {count} registros")
            
            # Mostrar distribuição por tipo de chave PIX
            pix_types_count = {}
            for financial in all_financials:
                if financial.tipo_chave_pix in pix_types_count:
                    pix_types_count[financial.tipo_chave_pix] += 1
                else:
                    pix_types_count[financial.tipo_chave_pix] = 1
            
            print("🔑 Distribuição por tipo de chave PIX:")
            for tipo, count in pix_types_count.items():
                print(f"   {tipo}: {count} registros")
                
        except Exception as e:
            print(f"❌ Erro ao criar registros financeiros: {e}")
            db.rollback()

if __name__ == "__main__":
    print("🚀 Inicializando dados de financials...")
    init_financials_data()
    print("✨ Processo concluído!") 