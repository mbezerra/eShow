#!/bin/bash

# Script para executar testes de API do eShow

echo "🧪 Iniciando testes de API do eShow..."

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado. Criando..."
    python -m venv venv
fi

# Ativar ambiente virtual
echo "📦 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências se necessário
echo "🔧 Verificando dependências..."
pip install -r requirements.txt

# Verificar se o requests está instalado
echo "📋 Verificando biblioteca requests..."
if ! python -c "import requests" 2>/dev/null; then
    echo "📦 Instalando biblioteca requests..."
    pip install requests
fi

# Verificar se o servidor está rodando
echo "🔍 Verificando se o servidor está rodando..."
if ! curl -s http://localhost:8000/docs > /dev/null; then
    echo "⚠️  Servidor não está rodando na porta 8000"
    echo "💡 Execute primeiro: ./start_server.sh"
    echo ""
    echo "Ou inicie o servidor em background:"
    echo "source venv/bin/activate && python run.py &"
    echo ""
    read -p "Deseja continuar mesmo assim? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Teste cancelado"
        exit 1
    fi
else
    echo "✅ Servidor está rodando"
fi

# Executar testes
echo ""
echo "🚀 Executando testes de API..."
echo "📊 Testando todos os endpoints..."
echo ""

python test_api_endpoints.py

echo ""
echo "✅ Testes concluídos!"
echo ""
echo "📈 Resumo:"
echo "   - Todos os endpoints foram testados"
echo "   - Verifique os resultados acima"
echo "   - Status 200 = Sucesso"
echo "   - Status 4xx/5xx = Erro"
echo ""
echo "🔧 Para executar novamente: ./test_api.sh" 