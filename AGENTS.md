# AGENTS.md — Binho Gourmet (Single-Tenant SaaS)

Este repositório é um SaaS **single-tenant** (apenas um negócio: **Binho Gourmet**).  
Objetivo: controle financeiro, estoque de insumos, precificação por receita (gramas/ml/un), PDV e impostos (MEI).

## Regras de ouro (NÃO QUEBRAR)
1. **NÃO usar Vite**
2. **NÃO usar Tailwind**
3. Frontend deve permanecer em **Create React App (CRA) + TypeScript + CSS Modules**
4. Manter UI dark premium já existente (não reestilizar “do zero”)
5. **Single-tenant**: nada de `tenant_id`, nada de multiempresa
6. Sem signup público: apenas login (seed cria admin)

## Resultado esperado (Definition of Done)
- `docker-compose up --build` sobe:
  - Postgres
  - Backend FastAPI (porta 8000)
  - Frontend CRA (porta 3000)
- Frontend deixa de usar mocks e consome API real.
- README.md em PT-BR **para iniciante absoluto**, com:
  - Rodar com Docker (recomendado)
  - Rodar sem Docker (alternativa)
  - Primeiro login (admin)
  - Troubleshooting (CORS, portas, deps)
  - Checklist do que testar

---

# Stack e estrutura obrigatória

## Backend (criar pasta `/backend`)
- FastAPI
- SQLAlchemy 2.x
- Pydantic
- JWT Auth (OAuth2 password flow)
- Password hashing (passlib/bcrypt)
- CORS liberado para `http://localhost:3000`
- Banco: **PostgreSQL via docker-compose**
- Modo iniciante sem Docker: **SQLite fallback** se `DATABASE_URL` não existir

### Estrutura sugerida
/backend/app
- main.py
- /core (config.py, security.py)
- /db (session.py)
- /models (models.py)
- /schemas (auth.py, inventory.py, finance.py, recipes.py, pos.py, taxes.py)
- /routers (auth.py, inventory.py, finance.py, recipes.py, pos.py, taxes.py)
- /seed (seed.py)

Também criar:
- /backend/requirements.txt
- /backend/Dockerfile

## Frontend (já existe)
- CRA + TS + CSS Modules
- React Router v6
- Recharts
- Axios
- Token JWT guardado em localStorage
- `src/services/api.ts` (Axios com interceptor Bearer token)
- Trocar mocks por chamadas ao backend, sem quebrar o layout atual

---

# Domínio e regras de negócio

## Unidades e precificação por receita (core)
- Estoque (ingredients) pode estar em: `kg`, `g`, `L`, `ml`, `un`
- Receita deve aceitar qty em:
  - `g` para itens em kg/g
  - `ml` para itens em L/ml
  - `un` para unidade

Conversões:
- `kg -> g` (x1000)
- `L -> ml` (x1000)

Custo unitário pequeno:
- `R$/g = (R$/kg) / 1000`
- `R$/ml = (R$/L) / 1000`

Custo total por unidade:
- ingredientes_por_unidade = (Σ custo dos ingredientes do lote) / rendimento
- mão_de_obra_por_unidade = ((tempo_lote_min/60) * custo_hora) / rendimento
- custo_total_unid = ingredientes_por_unidade + mão_de_obra_por_unidade + embalagem_unid + outros_unid

Preço final:
- preço_unid = custo_total_unid * multiplicador (x2 / x3 etc)
- margem = (preço_unid - custo_total_unid) / preço_unid

Alertas:
- se qty da receita > estoque disponível convertido (g/ml/un) => erro/alerta claro

## PDV / Ordem
Ao finalizar venda:
- criar `order` + `order_items`
- criar `transaction` de entrada (venda)
- baixar estoque automaticamente conforme recipe * qty
- se faltar ingrediente: bloquear e retornar erro claro (nome do ingrediente, precisa X, tem Y)

## Impostos (MEI)
- Página no front já calcula; backend deve ao menos persistir configurações:
  - GET/PUT `/taxes/settings`

---

# Endpoints mínimos (REST)

## Auth
- POST `/auth/login` -> `{access_token, token_type}`
- GET `/me` -> usuário logado

## Ingredients (estoque)
- GET `/ingredients`
- POST `/ingredients`
- PUT `/ingredients/{id}`
- DELETE `/ingredients/{id}`

## Recipes
- GET `/recipes`
- POST `/recipes`
- PUT `/recipes/{id}`
- DELETE `/recipes/{id}`
Opcional:
- GET `/recipes/{id}/pricing`

## Finance (transactions)
- GET `/transactions` (+ filtros de data)
- POST `/transactions`

## POS (orders)
- POST `/orders` (finaliza venda e dá baixa)

## Taxes settings
- GET `/taxes/settings`
- PUT `/taxes/settings`

## Seed
- Criar admin:
  - email: `admin@binhogourmet.local`
  - senha: `admin123`
- Criar contas e categorias padrão
- Criar alguns ingredientes de exemplo

---

# Convenções
- Mensagens de erro devem ser claras (PT-BR é ok)
- Validar inputs (valores > 0, datas, ids existentes)
- Não adicionar dependências desnecessárias
- Preferir código simples e legível
- Tudo pronto para commit

---

# Arquivos adicionais obrigatórios
- `docker-compose.yml` na raiz
- `.env.example` na raiz (com explicação)
- `/backend/.env.example`
- README.md “iniciante absoluto”