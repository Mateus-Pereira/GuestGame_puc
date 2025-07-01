#!/bin/bash

echo "🔍 Monitoramento do Guess Game"
echo "================================"

check_service() {
    local service=$1
    local url=$2
    
    echo -n "🔍 $service: "
    
    if curl -s --max-time 5 "$url" > /dev/null 2>&1; then
        echo "✅ OK"
        return 0
    else
        echo "❌ FALHA"
        return 1
    fi
}

check_containers() {
    echo ""
    echo "📊 Status dos Containers:"
    echo "========================"
    
    docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
}

check_error_logs() {
    echo ""
    echo "🚨 Últimos Erros (últimos 10 minutos):"
    echo "======================================"
    
    # Verificar logs de erro dos últimos 10 minutos
    docker compose logs --since=10m 2>&1 | grep -i "error\|exception\|failed\|critical" | tail -10
    
    if [ $? -ne 0 ]; then
        echo "✅ Nenhum erro encontrado nos últimos 10 minutos"
    fi
}

check_resources() {
    echo ""
    echo "💾 Uso de Recursos:"
    echo "=================="
    
    echo "🐳 Docker:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}" | head -6
    
    echo ""
    echo "💽 Espaço em Disco:"
    df -h | grep -E "(Filesystem|/dev/)"
}

check_connectivity() {
    echo ""
    echo "🌐 Verificação de Conectividade:"
    echo "==============================="
    
    check_service "Frontend" "http://localhost"
    check_service "API Health" "http://localhost/api/health"
    check_service "NGINX Status" "http://localhost/nginx_status"
    
    echo -n "🔍 PostgreSQL: "
    if docker compose exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
        echo "✅ OK"
    else
        echo "❌ FALHA"
    fi
}

check_performance() {
    echo ""
    echo "⚡ Métricas de Performance:"
    echo "=========================="
    
    echo -n "🔍 Tempo de resposta da API: "
    response_time=$(curl -o /dev/null -s -w "%{time_total}" http://localhost/api/health)
    echo "${response_time}s"
    
    echo -n "🔍 Conexões ativas (NGINX): "
    curl -s http://localhost/nginx_status | grep "Active connections" | awk '{print $3}'
    
    echo -n "🔍 Workers Backend: "
    docker compose exec backend1 ps aux | grep gunicorn | grep -v grep | wc -l
}

main() {
    if ! docker compose version > /dev/null 2>&1; then
        echo "❌ Docker Compose não está disponível"
        exit 1
    fi
    
    check_containers
    check_connectivity
    check_performance
    check_resources
    check_error_logs
    
    echo ""
    echo "✅ Monitoramento concluído!"
    echo ""
    echo "📝 Comandos úteis:"
    echo "  - Ver logs em tempo real: docker compose logs -f"
    echo "  - Reiniciar serviços: docker compose restart"
    echo "  - Ver status detalhado: docker compose ps"
}

main "$@"
