# Scripts do eShow

Este diretório contém scripts para facilitar o desenvolvimento e teste da API eShow.

## 🚀 Scripts Disponíveis

### 1. `start_server.sh` - Iniciar Servidor
Inicia o servidor FastAPI com todas as configurações necessárias.

```bash
./start_server.sh
```

**O que faz:**
- ✅ Verifica/cria ambiente virtual
- ✅ Ativa ambiente virtual
- ✅ Instala dependências
- ✅ Inicia servidor na porta 8000
- ✅ Mostra URLs de documentação

**URLs disponíveis após execução:**
- 📖 Documentação: http://localhost:8000/docs
- 🏥 Health Check: http://localhost:8000/health

### 2. `test_api.sh` - Testar API
Executa testes completos de todos os endpoints da API.

```bash
./test_api.sh
```

**O que faz:**
- ✅ Verifica/cria ambiente virtual
- ✅ Ativa ambiente virtual
- ✅ Instala dependências
- ✅ Verifica se servidor está rodando
- ✅ Executa testes de todos os endpoints
- ✅ Mostra resumo dos resultados

**Pré-requisito:** Servidor deve estar rodando (execute `./start_server.sh` primeiro)

## 🔧 Como Usar

### Cenário 1: Primeira Execução
```bash
# 1. Iniciar servidor
./start_server.sh

# 2. Em outro terminal, executar testes
./test_api.sh
```

### Cenário 2: Servidor Já Rodando
```bash
# Apenas executar testes
./test_api.sh
```

### Cenário 3: Apenas Servidor
```bash
# Apenas iniciar servidor
./start_server.sh
```

## 📊 Resultados dos Testes

O script `test_api.sh` testa **todos os 19 grupos de endpoints**:

1. **Autenticação** - Login
2. **Usuários** - CRUD completo
3. **Profiles** - CRUD completo com coordenadas geográficas
4. **Roles** - CRUD completo
5. **Artist Types** - CRUD completo
6. **Musical Styles** - CRUD completo
7. **Event Types** - CRUD completo
8. **Festival Types** - CRUD completo
9. **Space Types** - CRUD completo
10. **Spaces** - CRUD completo
11. **Artists** - CRUD completo
12. **Space Event Types** - CRUD completo
13. **Space Festival Types** - CRUD completo
14. **Bookings** - CRUD completo
15. **Reviews** - CRUD completo
16. **Interests** - CRUD completo
17. **Financials** - CRUD completo
18. **Location Search** - Busca por localização
19. **Artist Musical Styles** - Relacionamentos

## 🎯 Status Codes

- **200** = ✅ Sucesso
- **4xx** = ⚠️ Erro do cliente (parâmetros inválidos, não encontrado)
- **5xx** = ❌ Erro do servidor (problema interno)

## 🛠️ Solução de Problemas

### Erro: "Servidor não está rodando"
```bash
# Execute primeiro o servidor
./start_server.sh
```

### Erro: "Ambiente virtual não encontrado"
O script criará automaticamente o ambiente virtual.

### Erro: "Biblioteca requests não encontrada"
O script instalará automaticamente a biblioteca requests.

## 📝 Notas

- Os scripts são executáveis (`chmod +x`)
- Funcionam em sistemas Linux/macOS
- Requerem Python 3.8+
- Usam ambiente virtual para isolamento
- Verificam automaticamente dependências

## 🔄 Execução Rápida

Para desenvolvimento rápido:
```bash
# Terminal 1: Servidor
./start_server.sh

# Terminal 2: Testes
./test_api.sh
``` 