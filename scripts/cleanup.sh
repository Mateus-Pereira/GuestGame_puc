#!/bin/bash


echo "🧹 Limpeza do Guess Game"
echo "======================="

show_help() {
    echo "Uso: $0 [OPÇÃO]"
    echo ""
    echo "Opções:"
    echo "  containers  - Parar e remover containers"
    echo "  images      - Remover imagens não utilizadas"
    echo "  volumes     - Remover volumes órfãos (CUIDADO: remove dados!)"
    echo "  logs        - Limpar logs do NGINX"
    echo "  all         - Limpeza completa (CUIDADO: remove tudo!)"
    echo "  --help      - Mostrar esta ajuda"
    echo ""
}

if [ $# -eq 0 ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    show_help
    exit 0
fi

OPTION=$1

cleanup_containers() {
    echo "🛑 Parando e removendo containers..."
    docker compose down --remove-orphans
    echo "✅ Containers removidos!"
}

cleanup_images() {
    echo "🗑️ Removendo imagens não utilizadas..."
    docker image prune -f
    docker system prune -f
    echo "✅ Imagens limpas!"
}

cleanup_volumes() {
    echo "⚠️  ATENÇÃO: Isso removerá TODOS os dados do banco!"
    read -p "Tem certeza? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker volume prune -f
        echo "✅ Volumes removidos!"
    else
        echo "❌ Operação cancelada."
    fi
}

cleanup_logs() {
    echo "📝 Limpando logs do NGINX..."
    if [ -f "./nginx/logs/access.log" ]; then
        > ./nginx/logs/access.log
        echo "✅ Log de acesso limpo!"
    fi
    if [ -f "./nginx/logs/error.log" ]; then
        > ./nginx/logs/error.log
        echo "✅ Log de erro limpo!"
    fi
}

cleanup_all() {
    echo "⚠️  LIMPEZA COMPLETA - Isso removerá TUDO!"
    read -p "Tem certeza? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cleanup_containers
        cleanup_images
        cleanup_volumes
        cleanup_logs
        echo "✅ Limpeza completa realizada!"
    else
        echo "❌ Operação cancelada."
    fi
}

case $OPTION in
    "containers")
        cleanup_containers
        ;;
    "images")
        cleanup_images
        ;;
    "volumes")
        cleanup_volumes
        ;;
    "logs")
        cleanup_logs
        ;;
    "all")
        cleanup_all
        ;;
    *)
        echo "❌ Opção '$OPTION' não reconhecida."
        show_help
        exit 1
        ;;
esac

echo ""
echo "🎯 Limpeza concluída!"
