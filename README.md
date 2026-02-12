# Binho Gourmet — SaaS Single-Tenant (Financeiro + Estoque + Receitas + PDV)

Este projeto é um sistema para **um único negócio**: **Binho Gourmet**.

- Frontend: **Create React App (CRA) + TypeScript + CSS Modules**
- Backend: **FastAPI + SQLAlchemy + JWT**
- Banco recomendado: **PostgreSQL (Docker Compose)**
- Modo iniciante sem Docker: **SQLite fallback no backend**

---

## 1) Pré-requisitos (bem simples)

### Windows (PowerShell)
1. Instale Node.js LTS: https://nodejs.org/
2. Instale Python 3.11+: https://www.python.org/downloads/
3. (Opcional, recomendado) Instale Docker Desktop: https://www.docker.com/products/docker-desktop/

### Linux/Mac
1. Node.js LTS
2. Python 3.11+
3. Docker + Docker Compose plugin (opcional, recomendado)

---

## 2) Rodar com Docker (recomendado para iniciantes)

> Esse modo sobe frontend + backend + postgres com **um comando**.

### Passo a passo
1. Abra terminal na raiz do projeto.
2. (Opcional) copie `.env.example` para `.env` e ajuste segredo JWT.
3. Rode:

```bash
docker compose up --build
```

4. Aguarde os containers ficarem ativos.
5. Acesse:
   - Frontend: http://localhost:3000
   - Backend docs: http://localhost:8000/docs

### Primeiro login
- Email: `admin@binhogourmet.local`
- Senha: `admin123`

---

## 3) Rodar sem Docker (alternativa didática)

## 3.1 Backend (FastAPI)

### Windows (PowerShell)
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Linux/Mac
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

> Se `DATABASE_URL` estiver vazio, o backend usa `sqlite:///./dev.db` automaticamente.

## 3.2 Frontend (CRA)

### Windows / Linux / Mac
```bash
cd frontend
npm install
npm start
```

Acesse: http://localhost:3000

---

## 4) Estrutura principal

```text
backend/
  app/
    core/ config.py, security.py
    db/ session.py
    models/ models.py
    schemas/ ...
    routers/ auth, inventory, finance, recipes, pos, taxes
    seed/ seed.py
frontend/
  src/
    pages/
    services/api.ts
docker-compose.yml
```

---

## 5) API disponível

- `POST /auth/login`
- `GET /me`
- `GET/POST/PUT/DELETE /ingredients`
- `GET/POST/PUT/DELETE /recipes`
- `GET /recipes/{id}/pricing`
- `GET/POST /transactions`
- `GET /categories`
- `GET /accounts`
- `POST /orders`
- `GET/PUT /taxes/settings`

Docs interativa: http://localhost:8000/docs

---

## 6) Troubleshooting (problemas comuns)

### Porta 3000 ou 8000 ocupada
- Feche app/processo que está usando a porta.
- Ou altere mapeamento no `docker-compose.yml`.

### Erro de CORS
- Verifique `BACKEND_CORS_ORIGINS` no backend.
- Deve incluir `http://localhost:3000`.

### Backend não conecta no banco
- No Docker, confirme se serviço `postgres` subiu.
- Sem Docker, remova `DATABASE_URL` para usar SQLite local.

### Login falhando
- Confira se seed executou no startup.
- Credenciais padrão: `admin@binhogourmet.local` / `admin123`.

---

## 7) Checklist de validação (faça nesta ordem)

1. [ ] Login com admin funciona.
2. [ ] Criar ingrediente em Estoque funciona.
3. [ ] Criar receita com linha de ingrediente funciona.
4. [ ] Finalizar venda no PDV cria pedido e baixa estoque.
5. [ ] Venda gera transação de entrada no financeiro.
6. [ ] Dashboard exibe entradas dos últimos 30 dias.

---

## 8) Dica extra: rodar front+back sem Docker em 1 comando (opcional)

Na raiz do projeto:
```bash
npm install
npm run dev
```

Esse comando usa `concurrently` e inicia backend + frontend juntos.
