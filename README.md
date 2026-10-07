# Pokédex Battle API

API em Python com FastAPI para cadastrar, atualizar, excluir e combater Pokémons. A aplicação usa PostgreSQL para persistir os dados e calcula o resultado da batalha com base no nível e na força de cada Pokémon.

## Objetivo

A API permite:

- Listar os Pokémons cadastrados.
- Inserir novos Pokémons.
- Editar campos existentes.
- Excluir um Pokémon.
- Calcular uma batalha entre dois Pokémons.

O score de batalha é calculado por:

$$
\text{score} = \text{nível} \times \text{força}
$$

O Pokémon com o maior score vence. Quando os scores forem iguais, o resultado é `draw`.

## Arquitetura

O projeto está organizado em camadas:

- `api` — aplicação FastAPI, rotas e schemas.
- `database` — conexão com o PostgreSQL.
- `domain` — regras de negócio, incluindo o cálculo da batalha.
- `migrations` — schema do banco e script do usuário de aplicação.
- `tests` — testes da regra de batalha.

O Swagger e o ReDoc são gerados automaticamente pelo FastAPI.

## Banco de dados

O banco é PostgreSQL 16. A tabela `pokedex` contém:

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `nome_pokemon` | `VARCHAR(100)` | Nome do Pokémon. |
| `tipo_pokemon` | `VARCHAR(50)` | Tipo do Pokémon. |
| `nivel_pokemon` | `INTEGER` | Nível do Pokémon. |
| `forca_pokemon` | `INTEGER` | Força do Pokémon. |

A migração também insere os primeiros registros:

- Pikachu — elétrico, nível 1, força 10.
- Charmander — fogo, nível 2, força 10.
- Bulbassaur — planta, nível 1, força 8.
- Squirtle — água, nível 1, força 9.

## Configuração

Copie o exemplo de ambiente:

```bash
cp .env.example .env
```

O arquivo `.env` aceita as variáveis seguintes:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=arthur@123
DB_HOST=postgres
DB_PORT=5432
DB_NAME=pokemon
DB_USER=pokemon_app
DB_PASSWORD=arthur_app@123
```

- `POSTGRES_USER` e `POSTGRES_PASSWORD` configuram o usuário administrativo do PostgreSQL.
- `DB_HOST` é o hostname do banco dentro da rede do Docker.
- `DB_PORT` é a porta do PostgreSQL.
- `DB_NAME` é o banco de dados.
- `DB_USER` e `DB_PASSWORD` configuram o usuário da API.

> Não substitua os valores por credenciais reais antes de utilizar o projeto em um ambiente compartilh. O arquivo `.env` deve permanecer local e não ser versionado.

## Executar com Docker Compose

Execute o projeto a partir da raiz do projeto:

```bash
docker compose up --build -d
```

Os serviços criados são:

- `postgres` — PostgreSQL 16.
- `migrations` — cria e configura o usuário da aplicação.
- `api` — backend FastAPI.

A API fica disponível em:

```text
http://localhost:8000
```

O banco fica disponível em:

```text
localhost:5432
```

Para verificar o estado:

```bash
docker compose ps
```

Para interromper os serviços:

```bash
docker compose down
```

Para remover também o banco e os dados:

```bash
docker compose down -v
```

## Executar localmente

Instale as dependências:

```bash
python3 -m pip install -r requirements.txt
```

Configure o ambiente com `.env` e execute o backend:

```bash
python3 -m uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

Quando executado localmente, o valor de `DB_HOST` deve apontar para uma instância PostgreSQL disponível, por exemplo `localhost`.

## Documentação da API

A documentação automatizada está disponível em:

- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### Listar Pokémons

```http
GET /pokemon
```

Resposta JSON com todos os registros da tabela.

### Inserir Pokémon

```http
POST /insert
```

Corpo JSON:

```json
{
  "nome": "charmeleon",
  "tipo": "fogo",
  "nivel": 3,
  "forca": 12
}
```

### Editar Pokémon

```http
PUT /edit/pikachu
```

O corpo pode conter qualquer combinação de campos:

```json
{
  "forca": 11
}
```

### Excluir Pokémon

```http
DELETE /delete/pikachu
```

### Batalha

```http
POST /battle
```

Corpo JSON:

```json
{
  "primeiro": "pikachu",
  "segundo": "charmander"
}
```

Resposta semelhante a:

```json
{
  "primeiro": "pikachu",
  "segundo": "charmander",
  "winner": "first",
  "first_score": 10,
  "second_score": 20
}
```

O valor de `winner` pode ser:

- `first` — primeiro Pokémon vence.
- `second` — segundo Pokémon vence.
- `draw` — empate.

## Exemplos com PowerShell

Listar Pokémons:

```powershell
Invoke-WebRequest http://localhost:8000/pokemon
```

Executar uma batalha:

```powershell
$body = @{
    primeiro = "pikachu"
    segundo = "charmander"
} | ConvertTo-Json

Invoke-WebRequest `
    -Uri http://localhost:8000/battle `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

## Testes

A lógica de batalha pode ser testada com:

```bash
python3 -m unittest discover -s tests -v
```

## Migrações

- [migrations/schema/00_create_pokedex.sql](migrations/schema/00_create_pokedex.sql) cria a tabela e os dados iniciais.
- [migrations/scripts/create_user.sh](migrations/scripts/create_user.sh) cria ou atualiza o usuário da aplicação.

O script de usuário é executado como uma etapa do Compose depois que o PostgreSQL está saudável.
