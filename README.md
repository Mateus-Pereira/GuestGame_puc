# 🎮 Guess Game - Jogo de Adivinhação Otimizado

Um jogo de adivinhação moderno e escalável desenvolvido com arquitetura de microsserviços, utilizando Flask (backend), React (frontend), PostgreSQL (banco de dados) e NGINX (proxy reverso), totalmente containerizado com Docker Compose.

## 📖 Sobre o Projeto

O Guess Game é uma aplicação web interativa onde usuários podem criar jogos de adivinhação personalizados e desafiar outros jogadores. O projeto foi desenvolvido com foco em **escalabilidade**, **segurança** e **experiência do usuário**, implementando as melhores práticas de desenvolvimento moderno.

## 🏗️ Decisões de Design e Arquitetura

### Arquitetura de Microsserviços

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│                 │    │                  │    │                 │
│   NGINX Proxy   │◄───┤   Load Balancer  ├───►│   Frontend      │
│   (Port 80/443) │    │   + Rate Limit   │    │   (React SPA)   │
│                 │    │                  │    │                 │
└─────────┬───────┘    └──────────────────┘    └─────────────────┘
          │
          ▼
┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │
│   Backend 1     │    │   Backend 2     │
│   (Gunicorn)    │    │   (Gunicorn)    │
│                 │    │                 │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          └──────────┬───────────┘
                     ▼
          ┌─────────────────┐
          │                 │
          │   PostgreSQL    │
          │   (Database)    │
          │                 │
          └─────────────────┘
```

### Justificativas das Escolhas Tecnológicas

#### 1. **NGINX como Proxy Reverso**
- **Por que**: Melhor performance para servir arquivos estáticos e balanceamento de carga
- **Benefícios**: 
  - Rate limiting nativo
  - Compressão gzip automática
  - SSL termination
  - Cache de arquivos estáticos
- **Alternativas consideradas**: Apache HTTP Server (descartado por maior consumo de recursos)

#### 2. **Gunicorn em vez do Flask Dev Server**
- **Por que**: Flask dev server não é adequado para produção
- **Benefícios**:
  - Suporte a múltiplos workers
  - Melhor gestão de memória
  - Maior estabilidade sob carga
  - Logs estruturados
- **Configuração**: 2 workers por instância para otimizar uso de CPU

#### 3. **PostgreSQL como Banco de Dados**
- **Por que**: Necessidade de ACID compliance e relacionamentos complexos
- **Benefícios**:
  - Transações robustas
  - Suporte a JSON nativo
  - Excelente performance para consultas complexas
  - Extensibilidade
- **Alternativas consideradas**: MongoDB (descartado por não precisarmos de flexibilidade de schema)

#### 4. **React para Frontend**
- **Por que**: Necessidade de interface dinâmica e responsiva
- **Benefícios**:
  - Component-based architecture
  - Virtual DOM para performance
  - Ecossistema maduro
  - Hot reload para desenvolvimento
- **Alternativas consideradas**: Vue.js (descartado por menor familiaridade da equipe)

#### 5. **Docker Compose para Orquestração**
- **Por que**: Simplicidade de deployment e consistência entre ambientes
- **Benefícios**:
  - Isolamento de dependências
  - Facilidade de scaling horizontal
  - Configuração declarativa
  - Networking automático entre serviços
- **Alternativas consideradas**: Kubernetes (descartado por complexidade desnecessária para o escopo atual)

### Padrões de Design Implementados

#### 1. **Separation of Concerns**
- Frontend focado apenas na apresentação
- Backend focado na lógica de negócio
- Banco de dados focado na persistência
- NGINX focado no roteamento e cache

#### 2. **Stateless Architecture**
- Autenticação via JWT (sem sessões no servidor)
- Cada request é independente
- Facilita scaling horizontal

#### 3. **Health Checks e Monitoring**
- Endpoints de saúde em todos os serviços
- Logs estruturados para debugging
- Métricas de performance

#### 4. **Security by Design**
- Rate limiting para prevenir ataques
- Headers de segurança no NGINX
- Validação rigorosa de entrada
- Usuários não-root nos containers

### Otimizações de Performance

#### 1. **Caching Strategy**
```nginx
# Arquivos estáticos com cache longo
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

#### 2. **Compressão**
```nginx
# Compressão gzip para reduzir bandwidth
gzip on;
gzip_types text/plain application/json application/javascript text/css;
```

#### 3. **Connection Pooling**
- PostgreSQL configurado com connection pooling
- Reutilização de conexões HTTP no NGINX

#### 4. **Resource Limits**
```yaml
# Limites de recursos por container
deploy:
  resources:
    limits:
      memory: 256M
    reservations:
      memory: 128M
```

## ✨ Funcionalidades

### 🎯 Principais
- **Autenticação JWT** com redirecionamento automático
- **Limite de tentativas** configurável (1-50)
- **Feedback detalhado** sobre tentativas
- **Histórico de jogos** por usuário
- **Balanceamento de carga** automático
- **Rate limiting** para proteção contra spam

### 🚀 Otimizações Implementadas
- **Gunicorn** para produção (substituiu Flask dev server)
- **Rate limiting** no NGINX
- **Compressão gzip** para arquivos estáticos
- **Health checks** otimizados
- **Limites de recursos** por container
- **Cache de arquivos estáticos**
- **Logs estruturados**

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de ter os seguintes requisitos instalados:

- **Docker** 20.10+ ([Guia de instalação](https://docs.docker.com/get-docker/))
- **Docker Compose** 2.0+ ([Guia de instalação](https://docs.docker.com/compose/install/))
- **Sistema Operacional**: Linux, macOS ou Windows com WSL2
- **Recursos mínimos**:
  - 2GB RAM disponível
  - 5GB espaço em disco
  - Portas 80 e 5432 livres

### Verificação dos Pré-requisitos

Execute o script de verificação para confirmar se seu ambiente está pronto:

```bash
./scripts/docker-check.sh
```

## 🛠️ Instalação Passo a Passo

### Método 1: Instalação Rápida (Recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/Mateus-Pereira/GuestGame_puc.git
cd guess_game-main

# 2. Torne os scripts executáveis
chmod +x scripts/*.sh

# 3. Inicie a aplicação
./scripts/start.sh

# 4. Aguarde a inicialização (pode levar alguns minutos na primeira vez)
# A aplicação estará disponível em: http://localhost
```

### Método 2: Instalação Manual

```bash
# 1. Clone e acesse o diretório
git clone https://github.com/Mateus-Pereira/GuestGame_puc.git
cd guess_game-main

# 2. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# 3. Construa e inicie os containers
docker compose build
docker compose up -d

# 4. Verifique o status
docker compose ps
```

### Método 3: Desenvolvimento

Para desenvolvimento com hot-reload:

```bash
# 1. Inicie apenas backend e banco de dados
./scripts/start-dev.sh

# 2. Em outro terminal, inicie o frontend em modo desenvolvimento
cd frontend
npm install
npm start

# Frontend estará em: http://localhost:3000
# Backend estará em: http://localhost:5000
```

## 🎮 Guia de Uso Completo

### Primeiro Acesso

1. **Acesse a aplicação**: http://localhost
2. **Registre-se**: Clique em "Registrar" e crie sua conta
3. **Faça login**: Use suas credenciais para entrar
4. **Redirecionamento**: Você será automaticamente direcionado para o dashboard

### Criando um Jogo

1. **Acesse o Dashboard**: Após login, clique em "Criar Jogo"
2. **Configure o Jogo**:
   - **Palavra/Frase Secreta**: Digite o que os jogadores devem adivinhar
   - **Número de Tentativas**: Escolha entre 1-50 tentativas
   - **Dificuldade**: Considere o comprimento e complexidade
3. **Compartilhe**: Copie o ID gerado e compartilhe com outros jogadores

### Jogando

1. **Acesse um Jogo**: Clique em "Jogar" no menu principal
2. **Digite o ID**: Insira o ID do jogo fornecido pelo criador
3. **Faça Tentativas**: Digite suas tentativas na caixa de texto
4. **Receba Feedback**: O sistema fornecerá dicas sobre sua tentativa:
   - ✅ **Correto**: Parabéns, você acertou!
   - ❌ **Incorreto**: Tente novamente
   - 📊 **Dicas**: Informações sobre proximidade (se configurado)

### Histórico de Jogos

- **Seus Jogos**: Veja todos os jogos que você criou
- **Jogos Jogados**: Histórico dos jogos em que participou
- **Estatísticas**: Taxa de acerto e performance geral

## 🔧 Gerenciamento

### Scripts Disponíveis

```bash
# Iniciar aplicação
./scripts/start.sh

# Modo desenvolvimento
./scripts/start-dev.sh

# Monitoramento completo
./scripts/monitor.sh

# Atualizações seletivas
./scripts/update.sh [backend|frontend|nginx|all]

# Limpeza do sistema
./scripts/cleanup.sh [containers|images|volumes|logs|all]

# Verificar Docker
./scripts/docker-check.sh
```

### Comandos Docker

```bash
# Ver status
docker compose ps

# Ver logs
docker compose logs -f

# Parar aplicação
docker compose down

# Reiniciar serviços
docker compose restart
```

## 📊 Monitoramento

### Endpoints de Status
- **Frontend**: http://localhost
- **API Health**: http://localhost/api/health
- **NGINX Status**: http://localhost/nginx_status (restrito)

### Logs
```bash
# Logs em tempo real
docker compose logs -f

# Logs específicos
docker compose logs -f backend1
docker compose logs -f nginx
```

## 🔒 Segurança

### Implementadas
- **Autenticação JWT** com tokens seguros
- **Rate limiting** (10 req/s API, 5 req/s auth)
- **Headers de segurança** no NGINX
- **Usuários não-root** nos containers
- **Validação de entrada** rigorosa
- **Limites de recursos** por container

### Para Produção
1. Altere as senhas em `.env`
2. Configure HTTPS com certificados válidos
3. Configure firewall adequado
4. Monitore logs regularmente

## ⚡ Performance

### Otimizações
- **Gunicorn** com 2 workers por backend
- **Compressão gzip** automática
- **Cache de arquivos estáticos** (1 ano)
- **Conexões keepalive** otimizadas
- **Limites de memória** por container
- **Balanceamento least_conn**

### Recursos por Container
- **PostgreSQL**: 512MB (limite) / 256MB (reserva)
- **Backend**: 256MB (limite) / 128MB (reserva)
- **Frontend**: 128MB (limite) / 64MB (reserva)
- **NGINX**: 128MB (limite) / 64MB (reserva)

## 🧪 Testes

```bash
# Testes do backend
docker compose exec backend1 python -m pytest

# Testes do frontend (se disponível)
cd frontend && npm test
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente
Copie `.env.example` para `.env` e ajuste:

```env
# JWT
JWT_SECRET_KEY=sua-chave-super-secreta

# PostgreSQL
POSTGRES_PASSWORD=sua-senha-segura

# Frontend
REACT_APP_BACKEND_URL=http://localhost/api
```

### HTTPS (Produção)
1. Adicione certificados em `nginx/ssl/`
2. Descomente configurações SSL no `nginx.conf`
3. Atualize portas no `docker-compose.yml`

## 🐛 Troubleshooting

### Problemas Comuns

1. **Containers não iniciam**
   ```bash
   ./scripts/monitor.sh
   docker compose logs [serviço]
   ```

2. **Erro 502 Bad Gateway**
   ```bash
   # Verificar backends
   docker compose ps
   docker compose logs backend1 backend2
   ```

3. **Rate limit atingido**
   - Aguarde alguns segundos
   - Verifique logs do NGINX

4. **Limpeza completa**
   ```bash
   ./scripts/cleanup.sh all
   ```

## 📈 Melhorias Implementadas

### ✅ Otimizações de Performance
- **Gunicorn Production Server**: Substituído Flask dev server por Gunicorn com 2 workers
- **Rate Limiting Inteligente**: Implementado no NGINX (10 req/s API, 5 req/s auth)
- **Cache Estratégico**: Arquivos estáticos com cache de 1 ano
- **Compressão Automática**: Gzip para reduzir bandwidth em 60-80%
- **Connection Pooling**: Reutilização de conexões para melhor performance
- **Resource Limits**: Limites de memória otimizados por container

### ✅ Melhorias de Segurança
- **Headers de Segurança**: X-Frame-Options, X-Content-Type-Options, CSP
- **Rate Limiting**: Proteção contra ataques de força bruta e DDoS
- **Non-Root Users**: Todos containers executam com usuários não-privilegiados
- **Input Validation**: Validação rigorosa de todas as entradas do usuário
- **JWT Security**: Tokens seguros com expiração configurável

### ✅ Experiência do Usuário
- **Redirecionamento Inteligente**: Automático após login/registro
- **Interface Responsiva**: Design moderno que funciona em todos dispositivos
- **Feedback Visual**: Indicadores claros de status e progresso
- **Navegação Intuitiva**: Menu simplificado e fluxo de usuário otimizado
- **Error Handling**: Mensagens de erro claras e acionáveis

### ✅ Operacional e DevOps
- **Scripts de Automação**: Gerenciamento completo via scripts bash
- **Monitoramento Integrado**: Health checks e logs estruturados
- **Sistema de Limpeza**: Remoção automática de recursos não utilizados
- **Hot Reload**: Desenvolvimento com recarregamento automático
- **Multi-Environment**: Suporte para desenvolvimento, teste e produção

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

**🚀 Versão Otimizada - Desenvolvida com foco em performance, segurança e experiência do usuário.**

