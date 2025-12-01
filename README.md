# FocoTotal API

API simples para gerenciar sessões de estudo, matérias e recursos, construída com FastAPI.

## 1. Pré-requisitos

* **Python 3.8+**
* **PostgreSQL:** Um servidor de banco de dados PostgreSQL em execução.
* **Git**

## 2. Configuração do Ambiente

Siga os passos abaixo para configurar o ambiente de desenvolvimento local.

### a. Clone o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd foco_total
```

### b. Crie e Ative o Ambiente Virtual

É uma boa prática usar um ambiente virtual para isolar as dependências do projeto.

**No Windows:**

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
.\venv\Scripts\activate
```

**No macOS/Linux:**

```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate
```

### c. Instale as Dependências

Com o ambiente virtual ativado, instale os pacotes necessários que estão listados no arquivo `requirements.txt`.

```bash
pip install -r FocoTotal/requirements.txt
```

### d. Configure o Banco de Dados SQLite

Você não precisa criar o banco de dados nem as tabelas manualmente.

O arquivo `focototal.db` será criado automaticamente na raiz do projeto (`foco_total/`) na primeira vez que a API iniciar, e as tabelas necessárias (`materias`, `recursos`, `sessoes_estudo`) serão criadas automaticamente pelo sistema no startup.

## 3. Executando a Aplicação

Com tudo configurado, você pode iniciar o servidor da API.

1. Navegue até o diretório raiz do projeto (`foco_total`).
2. Execute o seguinte comando no terminal (com o ambiente virtual ativado):

    ```bash
    uvicorn FocoTotal.main:app --reload
    ```

    * `FocoTotal.main:app`: informa ao Uvicorn onde encontrar a instância do FastAPI.
    * `--reload`: faz com que o servidor reinicie automaticamente após qualquer alteração no código.

3. Abra seu navegador e acesse [http://127.0.0.1:8000](http://127.0.0.1:8000). Você verá a mensagem `{"status":"online","projeto":"FocoTotal API"}`.

## 4. Documentação da API (Swagger)

O FastAPI gera automaticamente uma documentação interativa da API. Para acessá-la, visite:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Nesta página, você pode visualizar todos os endpoints e testá-los diretamente do navegador.
