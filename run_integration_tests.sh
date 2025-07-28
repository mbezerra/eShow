#!/bin/bash

# Script para executar testes de integração da API eShow
# Autor: Sistema de Testes eShow
# Data: $(date)

echo "🎵 eShow - Testes de Integração da API"
echo "======================================"
echo ""

# Verificar se o ambiente virtual está ativo
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Ambiente virtual não está ativo. Ativando..."
    source venv/bin/activate
fi

# Verificar se as dependências estão instaladas
echo "📦 Verificando dependências..."
pip install -q pytest pytest-cov pytest-asyncio httpx

# Configurar variáveis de ambiente para teste
export TESTING=True
export DATABASE_URL="sqlite:///./test_integration.db"

echo ""
echo "🧪 Executando testes de integração..."
echo ""

# Executar testes de integração com cobertura
pytest tests/test_integration.py \
    tests/test_integration_coverage.py \
    -v \
    --cov=app \
    --cov=domain \
    --cov=infrastructure \
    --cov-report=html:htmlcov/integration \
    --cov-report=term-missing \
    --cov-report=xml:coverage.xml \
    --tb=short \
    --maxfail=10 \
    --durations=10

# Verificar se os testes passaram
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Todos os testes de integração passaram!"
    echo ""
    echo "📊 Relatórios de cobertura gerados:"
    echo "   - HTML: htmlcov/integration/index.html"
    echo "   - XML: coverage.xml"
    echo ""
    echo "🎯 Cobertura de código:"
    echo "   - Abra htmlcov/integration/index.html no navegador para ver detalhes"
    echo ""
else
    echo ""
    echo "❌ Alguns testes falharam. Verifique os logs acima."
    echo ""
    exit 1
fi

# Executar testes específicos de cobertura
echo "🔍 Executando testes de cobertura específicos..."
pytest tests/test_integration_coverage.py -v --tb=short

# Executar testes de fluxo completo
echo ""
echo "🔄 Executando testes de fluxo completo..."
pytest tests/test_integration.py::TestAPIIntegration::test_complete_workflow_integration -v --tb=short

echo ""
echo "🎉 Testes de integração concluídos!"
echo ""
echo "📈 Para ver a cobertura detalhada:"
echo "   open htmlcov/integration/index.html"
echo ""
echo "📋 Para executar testes específicos:"
echo "   pytest tests/test_integration.py::TestAPIIntegration::test_auth_integration_flow -v"
echo "" 