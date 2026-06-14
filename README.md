# AISSI

AI-Assisted Swing Trading Infrastructure for IDX (Indonesia Stock Exchange)

AISSI is an institutional-style AI trading infrastructure built for Indonesian stock market analysis, monitoring, screening, portfolio analytics, and automated alerting.

---

# FEATURES

## Market Intelligence

- Market Regime Detection
- Sector Rotation Analysis
- AI Signal Engine
- Adaptive Screener
- Technical Indicator Engine

## Trading Infrastructure

- Backtesting Engine
- Forward Testing Engine
- Portfolio Risk Management
- Position Sizing
- Risk Reward Calculation

## Monitoring

- Real-time Monitoring Engine
- Telegram AI Alerts
- Scheduled Automation
- Snapshot Persistence

## Dashboard

- Next.js Institutional Dashboard
- FastAPI REST API
- Supabase Authentication
- Portfolio Tracking

---

# TECH STACK

## Backend

- Python
- FastAPI
- Pandas
- TA
- APScheduler
- Loguru
- Supabase
- Telegram Bot API

## Frontend

- Next.js
- TypeScript
- TailwindCSS
- Axios

## Database / Cloud

- Supabase
- Vercel
- Railway / Render

---

# PROJECT STRUCTURE

```txt
AISSI/
│
├── backend/
│   ├── app/
│   ├── engines/
│   ├── runners/
│   ├── jobs/
│   ├── data/
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── services/
│   └── hooks/
│
├── README.md
└── .gitignore
```

````

---

# INSTALLATION

## 1. Clone Repository

```bash
git clone YOUR_REPOSITORY_URL
```

---

# BACKEND SETUP

## 1. Create Virtual Environment

```bash
python -m venv venv
```

---

## 2. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create:

```txt
backend/.env
```

Example:

```env
SUPABASE_URL=
SUPABASE_KEY=

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

ENVIRONMENT=development
```

---

## 5. Run Backend

```bash
uvicorn main:app --reload
```

Backend API:

```txt
http://127.0.0.1:8000
```

Swagger Docs:

```txt
http://127.0.0.1:8000/docs
```

---

# FRONTEND SETUP

## 1. Install Dependencies

```bash
npm install
```

---

## 2. Configure Environment Variables

Create:

```txt
frontend/.env.local
```

Example:

```env
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
```

---

## 3. Run Frontend

```bash
npm run dev
```

Frontend:

```txt
http://localhost:3000
```

---

# RUNNERS

## Download Market Data

```bash
python -m runners.run_downloader
```

---

## Generate Indicators

```bash
python -m runners.run_indicators
```

---

## Run Screener

```bash
python -m runners.run_screener
```

---

## Run AI Signals

```bash
python -m runners.run_ai_signal
```

---

## Run Monitoring

```bash
python -m runners.run_monitoring
```

---

## Test Full Pipeline

```bash
python -m runners.test_pipeline
```

---

# DEPLOYMENT

## Frontend

- Vercel

## Backend

- Railway / Render

## Database

- Supabase

---

# SECURITY NOTES

- Never commit `.env`
- Never expose API keys
- Use `.gitignore`
- Rotate credentials if leaked

---

# LICENSE

Personal / Educational Project

```
````
