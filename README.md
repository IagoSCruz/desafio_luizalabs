# Documentação da API: Processador de Arquivos de Sistema Legado

Este projeto consiste em uma API desenvolvida para processar, validar e armazenar dados de um sistema legado contidos em arquivos de texto (`.txt`) com formato de largura fixa.

**URL Base da API:** `http://127.0.0.1:8000/api/`

---

## Tecnologias e Conceitos Aplicados

-   **Backend:** Python 3.10, Django 5.2, Django REST Framework
-   **Banco de Dados:** SQLite (padrão do Django para desenvolvimento)
-   **Containerização:** Docker & Docker Compose
-   **Arquitetura:** API RESTful
-   **Versionamento:** Git

---

## Como Executar o Projeto

**Pré-requisitos:**
* [Git](https://git-scm.com/)
* [Docker](https://www.docker.com/products/docker-desktop/)
* [Docker Compose](https://docs.docker.com/compose/install/)

**Passos para Execução:**

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/desktop/desktop/issues/18661](https://github.com/desktop/desktop/issues/18661)
    cd [nome-da-pasta-do-projeto]
    ```

2.  **Construa e inicie os contêineres:**
    O Docker Compose cuidará de tudo: construir a imagem, instalar as dependências e aplicar as migrações do banco de dados.
    ```bash
    docker-compose up --build
    ```
    *A aplicação estará rodando e acessível em `http://localhost:8000`.*

3.  **(Não obrigatório) Crie um superusuário para acessar o Admin:**
    Abra um novo terminal e execute:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
    *A interface admin do Django ficará disponível em `http://localhost:8000/admin/`.*

---

## Endpoints da API

### 1. Processar e Salvar Arquivo de Dados

Este endpoint é usado para enviar um arquivo de texto. O sistema irá processar, validar e armazenar esses dados em um banco de dados.

-   **Endpoint:** `/processar-arquivo/`
-   **Método:** `POST`
-   **Descrição:** Recebe um arquivo `.txt` formatado, processa cada linha e salva as informações de usuários, pedidos e produtos no banco. A operação é idempotente: dados existentes (baseados em `user_id` e `order_id`) serão atualizados; novos dados serão criados.

#### Corpo da Requisição (Payload)

A requisição deve ser do tipo `multipart/form-data`.

| Chave (Key) | Tipo | Obrigatório | Descrição                                        |
| :---------- | :--- | :---------- | :----------------------------------------------- |
| `file`      | File | **Sim** | O arquivo `.txt` contendo os dados dos pedidos. |

#### Resposta de Sucesso (`200 OK`)

Indica que o arquivo foi recebido e os dados foram salvos com sucesso.

`json
    {
    "status": "Arquivo processado e dados salvos com sucesso."
    }`


### 2. Listas todos os Usuarios

Esse endpoint retorna uma lista de todos os usuários que foram salvos no bano de dados, junto com seus respectivos pedidos e produtos cadastrados do sistema legado.

-  **Endpoint:** `/users/`
-  **Metodo:** `GET`
-  **Descrição:** Retorna uma lista completa de todos os usuarios cadastrados, ordenando-os pelo `user_id`

#### Resposta de Sucesso (`200 OK`)


### 3. Buscar um usuario especifico

Este endpoint dados completos de um único usuário, identificado pelo seu ID.

-   **Endpoint:** `/users/<user_id>/`
-   **Método:** `GET`
-   **Descrição:** Retorna os detalhes de um usuário específico, incluindo todos os seus pedidos e produtos.

#### Resposta de Sucesso (`200 OK`)

#### Resposta de Erro (`400 OK`)

Ocorre erro caso o user_id não exista no banco de dados da aplicação.


---

### Executando o teste via Postman

- Persistindo os dados no sistema de processamento.
![image](https://github.com/user-attachments/assets/d3552e57-5f9b-4410-b09b-634d5beee9e2)


- Buscando os usuários, listando os produtos e histórico de compra.

![image](https://github.com/user-attachments/assets/df577644-f73b-4509-921f-566b6da33dc9)

