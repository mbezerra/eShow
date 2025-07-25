#!/bin/bash

# Script para executar os testes do eShow

echo "🚀 Executando testes do eShow..."

# Verificar se o ambiente virtual está ativo
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Ambiente virtual não está ativo. Ativando..."
    source venv/bin/activate
fi

# Instalar dependências de teste se necessário
echo "📦 Verificando dependências de teste..."
pip install pytest pytest-cov

# Executar todos os testes com cobertura
echo "🧪 Executando testes com cobertura..."
pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html

# Verificar se os testes passaram
if [ $? -eq 0 ]; then
    echo "✅ Todos os testes passaram!"
    echo "📊 Relatório de cobertura gerado em htmlcov/index.html"
else
    echo "❌ Alguns testes falharam!"
    exit 1
fi 