# Estágio de build
FROM node:18.17.0-alpine AS build

WORKDIR /app

# Habilitar yarn
RUN corepack enable

# Copiar arquivos de dependências
COPY package*.json ./

# Instalar dependências
RUN npm ci --only=production

# Copiar código fonte
COPY . .

# Definir variável de ambiente para o backend
ARG REACT_APP_BACKEND_URL=http://localhost/api
ENV REACT_APP_BACKEND_URL=$REACT_APP_BACKEND_URL

# Build da aplicação
RUN npm run build

# Estágio de produção com NGINX
FROM nginx:alpine

# Copiar arquivos buildados
COPY --from=build /app/build /usr/share/nginx/html

# Copiar configuração customizada do NGINX
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Criar usuário não-root (nginx group already exists in nginx:alpine)
RUN adduser -S -D -H -u 1001 -h /var/cache/nginx -s /sbin/nologin -G nginx nginx || true

# Ajustar permissões
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d

# Expor porta
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Comando padrão
CMD ["nginx", "-g", "daemon off;"]
