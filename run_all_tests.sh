#!/bin/bash

# Script principal para executar todos os testes da API eShow (Versão Corrigida)
# Autor: Sistema de Testes eShow
# Data: $(date)

echo "🎵 eShow - Suite Completa de Testes (Versão Corrigida)"
echo "====================================================="
echo ""

# Verificar se o ambiente virtual está ativo
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Ambiente virtual não está ativo. Ativando..."
    source venv/bin/activate
fi

# Verificar se as dependências estão instaladas
echo "📦 Verificando dependências..."
pip install -q pytest pytest-cov pytest-asyncio httpx psutil pytest-html

# Configurar variáveis de ambiente para teste
export TESTING=True
export DATABASE_URL="sqlite:///./test_all.db"

# Criar diretório de relatórios se não existir
REPORT_DIR="test_reports"
mkdir -p "$REPORT_DIR"

# Limpar o banco de dados de teste antes de cada execução completa
echo "🧹 Limpando banco de dados de teste..."
rm -f ./test_all.db

# Inicializar roles no banco de dados de teste
echo "⚙️ Inicializando roles no banco de dados de teste..."
python init_roles.py

# Definir grupos de testes para execução sequencial
# Grupo 1: Testes básicos que não dependem de autenticação complexa ou perfis
TEST_GROUP_1="tests/test_event_types.py tests/test_festival_types.py tests/test_musical_styles.py tests/test_artist_types.py"

# Grupo 2: Testes de autenticação e usuários
TEST_GROUP_2="tests/test_users.py tests/test_auth.py"

# Grupo 3: Testes de perfis e artistas (que dependem de usuários e roles)
TEST_GROUP_3="tests/test_profiles.py tests/test_artists.py tests/test_artist_musical_styles.py"

# Grupo 4: Testes de espaços e bookings (que dependem de perfis)
TEST_GROUP_4="tests/test_spaces.py tests/test_bookings.py"

# Grupo 5: Testes de interesses (que dependem de múltiplos perfis)
TEST_GROUP_5="tests/test_interests.py"

# Grupo 6: Testes financeiros (que dependem de perfis)
TEST_GROUP_6="tests/test_financials.py"

# Grupo 7: Testes de integração (gerais)
TEST_GROUP_7="tests/test_integration.py"

# Grupo 8: Testes de performance (se houver)
TEST_GROUP_8="tests/test_performance.py"

# Executar testes em grupos sequenciais com isolamento
echo "🚀 Executando Testes Básicos..."
pytest $TEST_GROUP_1 -v --html="$REPORT_DIR/report_basic.html" --self-contained-html || { echo "❌ Testes Básicos falharam!"; exit 1; }

echo "🧹 Limpando banco de dados para próximo grupo..."
rm -f ./test_all.db
python init_roles.py

echo "🚀 Executando Testes de Autenticação e Usuários..."
pytest $TEST_GROUP_2 -v --html="$REPORT_DIR/report_auth_users.html" --self-contained-html || { echo "❌ Testes de Autenticação e Usuários falharam!"; exit 1; }

echo "🧹 Limpando banco de dados para próximo grupo..."
rm -f ./test_all.db
python init_roles.py

echo "🚀 Executando Testes de Perfis e Artistas..."
pytest $TEST_GROUP_3 -v --html="$REPORT_DIR/report_profiles_artists.html" --self-contained-html || { echo "❌ Testes de Perfis e Artistas falharam!"; exit 1; }

echo "🧹 Limpando banco de dados para próximo grupo..."
rm -f ./test_all.db
python init_roles.py

echo "🚀 Executando Testes de Espaços e Bookings..."
pytest $TEST_GROUP_4 -v --html="$REPORT_DIR/report_spaces_bookings.html" --self-contained-html || { echo "❌ Testes de Espaços e Bookings falharam!"; exit 1; }

echo "🧹 Limpando banco de dados para próximo grupo..."
rm -f ./test_all.db
python init_roles.py

echo "🚀 Executando Testes de Interesses..."
pytest $TEST_GROUP_5 -v --html="$REPORT_DIR/report_interests.html" --self-contained-html || { echo "❌ Testes de Interesses falharam!"; exit 1; }

echo "🧹 Limpando banco de dados para próximo grupo..."
rm -f ./test_all.db
python init_roles.py

echo "🚀 Executando Testes Financeiros..."
pytest $TEST_GROUP_6 -v --html="$REPORT_DIR/report_financials.html" --self-contained-html || { echo "❌ Testes Financeiros falharam!"; exit 1; }

echo "🧹 Limpando banco de dados para próximo grupo..."
rm -f ./test_all.db
python init_roles.py

echo "🚀 Executando Testes de Integração..."
pytest $TEST_GROUP_7 -v --html="$REPORT_DIR/report_integration.html" --self-contained-html || { echo "❌ Testes de Integração falharam!"; exit 1; }

echo "🧹 Limpando banco de dados para próximo grupo..."
rm -f ./test_all.db
python init_roles.py

echo "🚀 Executando Testes de Performance..."
pytest $TEST_GROUP_8 -v --html="$REPORT_DIR/report_performance.html" --self-contained-html || { echo "❌ Testes de Performance falharam!"; exit 1; }

echo "🚀 Gerando Relatório de Cobertura de Código..."
# Gerar relatório de cobertura usando todos os testes que funcionam
pytest $TEST_GROUP_1 $TEST_GROUP_2 $TEST_GROUP_3 $TEST_GROUP_4 $TEST_GROUP_5 $TEST_GROUP_6 $TEST_GROUP_7 $TEST_GROUP_8 --cov=app --cov-report=html:"$REPORT_DIR/htmlcov" --cov-report=xml:"$REPORT_DIR/coverage.xml" --cov-report=term-missing

echo ""
echo "✅ Suite de Testes Concluída!"
echo "Relatórios HTML gerados em: $REPORT_DIR"
echo "Relatório de Cobertura HTML em: $REPORT_DIR/htmlcov/index.html"
echo "=====================================================" 