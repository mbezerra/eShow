#!/bin/bash

# Script para executar testes de performance da API eShow
# Autor: Sistema de Testes eShow
# Data: $(date)

echo "🚀 eShow - Testes de Performance da API"
echo "======================================="
echo ""

# Verificar se o ambiente virtual está ativo
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Ambiente virtual não está ativo. Ativando..."
    source venv/bin/activate
fi

# Verificar se as dependências estão instaladas
echo "📦 Verificando dependências..."
pip install -q pytest pytest-cov pytest-asyncio httpx psutil

# Configurar variáveis de ambiente para teste
export TESTING=True
export DATABASE_URL="sqlite:///./test_performance.db"

echo ""
echo "⚡ Executando testes de performance..."
echo ""

# Executar testes de performance
pytest tests/test_performance.py \
    -v \
    --tb=short \
    --maxfail=5 \
    --durations=10 \
    -m "not slow" \
    --html=reports/performance_report.html \
    --self-contained-html

# Verificar se os testes passaram
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Todos os testes de performance passaram!"
    echo ""
    echo "📊 Relatório gerado:"
    echo "   - HTML: reports/performance_report.html"
    echo ""
else
    echo ""
    echo "❌ Alguns testes de performance falharam. Verifique os logs acima."
    echo ""
    exit 1
fi

# Executar testes específicos de performance
echo "🔍 Executando testes específicos de performance..."

# Teste de tempo de resposta
echo "⏱️  Testando tempo de resposta dos endpoints..."
pytest tests/test_performance.py::TestAPIPerformance::test_endpoint_response_time -v

# Teste de throughput
echo "📈 Testando throughput da API..."
pytest tests/test_performance.py::TestAPIPerformance::test_api_throughput_performance -v

# Teste de operações em lote
echo "📦 Testando operações em lote..."
pytest tests/test_performance.py::TestAPIPerformance::test_bulk_operations_performance -v

# Teste de fluxo complexo
echo "🔄 Testando fluxo complexo..."
pytest tests/test_performance.py::TestAPIPerformance::test_complex_workflow_performance -v

echo ""
echo "🎉 Testes de performance concluídos!"
echo ""
echo "📈 Para ver o relatório detalhado:"
echo "   open reports/performance_report.html"
echo ""
echo "📋 Para executar testes específicos:"
echo "   pytest tests/test_performance.py::TestAPIPerformance::test_endpoint_response_time -v"
echo ""
echo "⚡ Métricas de Performance:"
echo "   - Tempo de resposta máximo: 1.0s por endpoint"
echo "   - Throughput mínimo: 50 req/s"
echo "   - Operações em lote: < 0.5s por operação"
echo "   - Fluxo complexo: < 3.0s total"
echo "" 