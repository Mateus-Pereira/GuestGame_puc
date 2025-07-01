#!/bin/bash

echo "🔄 Script de Atualização do Guess Game"
echo ""

show_help() {
    echo "Uso: $0 [COMPONENTE] [VERSÃO]"
    echo ""
    echo "Componentes disponíveis:"
    echo "  backend    - Atualizar apenas o backend"
    echo "  frontend   - Atualizar apenas o frontend"
    echo "  nginx      - Atualizar apenas o NGINX"
    echo "  postgres   - Atualizar apenas o PostgreSQL"
    echo "  all        - Atualizar todos os componentes"
    echo ""
    echo "Exemplos:"
    echo "  $0 backend latest"
    echo "  $0 postgres 15-alpine"
    echo "  $0 all"
    echo ""
}

if [ $# -eq 0 ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    show_help
    exit 0
fi

COMPONENT=$1
VERSION=${2:-"latest"}

update_backend() {
    echo "🔄 Atualizando backend..."
    docker compose build --no-cache backend1 backend2
    docker compose up -d backend1 backend2
    echo "✅ Backend atualizado!"
}

update_frontend() {
    echo "🔄 Atualizando frontend..."
    docker compose build --no-cache frontend
    docker compose up -d frontend
    echo "✅ Frontend atualizado!"
}

update_nginx() {
    echo "🔄 Atualizando NGINX..."
    docker compose build --no-cache nginx
    docker compose up -d nginx
    echo "✅ NGINX atualizado!"
}

update_postgres() {
    echo "🔄 Atualizando PostgreSQL..."
    echo "⚠️  ATENÇÃO: Isso pode afetar os dados existentes!"
    read -p "Deseja continuar? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker compose stop postgres
        docker compose pull postgres
        docker compose up -d postgres
        echo "✅ PostgreSQL atualizado!"
    else
        echo "❌ Atualização cancelada."
    fi
}

update_all() {
    echo "🔄 Atualizando todos os componentes..."
    docker compose build --no-cache
    docker compose up -d
    echo "✅ Todos os componentes atualizados!"
}

case $COMPONENT in
    "backend")
        update_backend
        ;;
    "frontend")
        update_frontend
        ;;
    "nginx")
        update_nginx
        ;;
    "postgres")
        update_postgres
        ;;
    "all")
        update_all
        ;;
    *)
        echo "❌ Componente '$COMPONENT' não reconhecido."
        show_help
        exit 1
        ;;
esac

echo ""
echo "📊 Status atual dos containers:"
docker compose ps
