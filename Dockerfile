FROM python:3.12-slim

# Evita criação de arquivos .pyc e ativa logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=10000

WORKDIR /app

# Instala dependências primeiro para aproveitar cache de camadas do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Cria usuário não-root e garante permissão de escrita para o banco SQLite
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 10000

# Inicializa o servidor WSGI Gunicorn usando a variável PORT injetada pelo Render
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-10000} --workers 1 --threads 8 --timeout 120 app:app"]
