#!/bin/bash


echo "🔍 Verificando instalação do Docker..."
echo "====================================="
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado."
    echo "📖 Instale o Docker seguindo: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✅ Docker encontrado: $(docker --version)"

if docker compose version &> /dev/null; then
    echo "✅ Docker Compose (v2) encontrado: $(docker compose version)"
    echo "export DOCKER_COMPOSE_CMD='docker compose'" > ~/.docker_compose_env
    echo "🎯 Usando: docker compose"
    exit 0
fi

if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose (v1) encontrado: $(docker-compose --version)"
    echo "export DOCKER_COMPOSE_CMD='docker-compose'" > ~/.docker_compose_env
    echo "🎯 Usando: docker-compose"
    exit 0
fi

echo "❌ Docker Compose não encontrado."
echo ""
echo "📖 Soluções:"
echo "1. Se você usa Docker Desktop:"
echo "   - Abra Docker Desktop → Settings → Resources → WSL Integration"
echo "   - Ative a integração para sua distribuição WSL"
echo "   - Clique em 'Apply & Restart'"
echo ""
echo "2. Ou instale Docker Compose manualmente:"
echo "   sudo curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose"
echo "   sudo chmod +x /usr/local/bin/docker-compose"
echo ""
exit 1
