# 1. Imagem Base
FROM python:3.10-slim-bullseye

# 2. Variáveis de Ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Define o diretório de trabalho ANTES de qualquer outra coisa
WORKDIR /app

# 4. Copia e instala as dependências primeiro.
# Isso aproveita o cache do Docker: se o requirements.txt não mudar,
# este passo não será executado novamente em builds futuros.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia o script de entrypoint e dá permissão de execução DENTRO do build.
# Certifique-se que o nome 'persistir_migration.sh' está correto.
COPY ./persistir_migration.sh .
RUN chmod +x ./persistir_migration.sh

# 6. Finalmente, copia o restante do código do projeto.
COPY . .

# 7. Define o entrypoint.
ENTRYPOINT ["/app/persistir_migration.sh"]