#!/bin/bash

# Script para iniciar o servidor eShow com ambiente virtual ativo

echo "🚀 Iniciando servidor eShow..."

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

# Iniciar servidor
echo "🌐 Iniciando servidor na porta 8000..."
echo "📖 Documentação disponível em: http://localhost:8000/docs"
echo "🏥 Health check: http://localhost:8000/health"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo ""

python run.py 