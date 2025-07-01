#!/bin/bash

echo "🚀 Iniciando Guess Game em modo produção..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose não está disponível. Verifique a instalação do Docker."
    exit 1
fi

echo "🛑 Parando containers existentes..."
docker compose down

echo "🔨 Construindo e iniciando containers..."
docker compose up --build -d

echo "⏳ Aguardando containers ficarem prontos..."
sleep 15

echo "📊 Status dos containers:"
docker compose ps

RUNNING_CONTAINERS=$(docker compose ps --services --filter "status=running" | wc -l)
TOTAL_SERVICES=5

if [ "$RUNNING_CONTAINERS" -lt "$TOTAL_SERVICES" ]; then
    echo "❌ Alguns containers não estão rodando. Verificando logs..."
    echo ""
    echo "🔍 Logs dos serviços:"
    docker compose logs --tail=20
    exit 1
fi

echo "✅ Aplicação iniciada com sucesso!"
echo "🌐 Frontend disponível em: http://localhost"
echo "🔧 API disponível em: http://localhost/api"
echo "📊 Status do NGINX: http://localhost/nginx_status"

echo ""
echo "📝 Comandos úteis:"
echo "  - Ver logs: docker compose logs -f"
echo "  - Parar aplicação: docker compose down"
echo "  - Reiniciar: docker compose restart"
echo "  - Ver status: docker compose ps"
