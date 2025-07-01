#!/bin/bash

echo "🚀 Iniciando Guess Game em modo desenvolvimento..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose não está disponível. Verifique a instalação do Docker."
    exit 1
fi

echo "🛑 Parando containers existentes..."
docker compose -f docker-compose.dev.yml down

echo "🔨 Construindo e iniciando containers..."
docker compose -f docker-compose.dev.yml up --build -d

echo "⏳ Aguardando containers ficarem prontos..."
sleep 15

echo "📊 Status dos containers:"
docker compose -f docker-compose.dev.yml ps

echo "✅ Aplicação iniciada com sucesso em modo desenvolvimento!"
echo "🔧 API disponível em: http://localhost:5000"
echo "🗄️ PostgreSQL disponível em: localhost:5432"

echo ""
echo "📝 Comandos úteis:"
echo "  - Ver logs: docker compose -f docker-compose.dev.yml logs -f"
echo "  - Parar aplicação: docker compose -f docker-compose.dev.yml down"
echo "  - Reiniciar: docker compose -f docker-compose.dev.yml restart"
echo "  - Ver status: docker compose -f docker-compose.dev.yml ps"

echo ""
echo "🔧 Para desenvolvimento do frontend:"
echo "  cd frontend && npm install && npm start"
