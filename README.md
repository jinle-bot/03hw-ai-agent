# HW03 – LangChain agent with multiple MCP servers

Úkol demonstruje AI agenta postaveného na frameworku **LangChain**, který používá nástroje poskytované přes **Model Context Protocol (MCP)**.

Agent se připojuje ke dvěma MCP serverům:

1. **vlastní školní MCP server** běžící v samostatném Docker kontejneru přes Streamable HTTP – poskytuje stejné nástroje jako AI agent z HW01,
2. **Sequential Thinking MCP server** spouštěný agentem přes `stdio` pomocí `npx`.

---


## Architektura

Vlastní MCP server a agent jsou samostatné Python aplikace a běží v oddělených Docker kontejnerech.

Docker Compose mezi kontejnery automaticky vytváří interní síť. Agent se proto k vlastnímu MCP serveru připojuje přes adresu:

```text
http://mcp-server:8000/mcp
```

---


## Struktura projektu

```text
hw03/
├── .env
├── .gitignore
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
│
├── mcp_server/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── src/
│       └── mcp_server/
│           ├── __init__.py
│           ├── main.py
│           ├── mcp_app.py
│           ├── starlette_app.py
│           └── tool/
│               ├── __init__.py
│               ├── data.py
│               ├── get_grade.py
│               └── get_mean.py
│
└── agent/
    ├── Dockerfile
    ├── pyproject.toml
    └── src/
        └── agent/
            ├── __init__.py
            ├── main.py
            ├── agent.py
            ├── config.py
            ├── mcp.py
            └── model.py
```

Root projektu je současně `uv workspace`:

```toml
[tool.uv.workspace]
members = [
    "mcp_server",
    "agent",
]
```

Obě aplikace mají vlastní `pyproject.toml`, ale při lokálním vývoji mohou používat společné virtuální prostředí `.venv` v rootu workspace.

---


## MCP server

Vlastní MCP server je implementovaný pomocí `FastMCP`.

Server běží přes Streamable HTTP a poskytuje školní nástroje.

## `get_grade`

Vrátí známku pro zadaný předmět.

Příklad:

```text
Jakou mám známku z matematiky?
```

Agent by měl použít nástroj ze školního MCP serveru místo toho, aby si údaj vymyslel.

## `get_mean`

Vrátí aritmetický průměr známek ze všech evidovaných předmětů.

Příklad:

```text
Jaký mám průměr ze všech předmětů?
```

---


## Sequential Thinking MCP server

Druhým MCP serverem je Sequential Thinking MCP server z referenčních MCP serverů:

```text
@modelcontextprotocol/server-sequential-thinking
```

Je spouštěn přímo z kontejneru agenta:

```bash
npx -y @modelcontextprotocol/server-sequential-thinking
```

Používá transport `stdio`, takže není potřeba vytvářet další Docker service ani otevírat síťový port.

Server poskytuje nástroj:

```text
sequentialthinking
```

který je vhodný zejména pro složitější problémy vyžadující:

- rozklad problému na části,
- plánování,
- porovnávání variant,
- postupnou revizi řešení,
- strukturované uvažování.

---

## Konfigurace

### `.env`

V rootu projektu vytvořte soubor:

```text
.env
```

s OpenAI API klíčem:

```env
OPENAI_API_KEY=sk-...
```

---


## Požadavky

- Docker
- Docker Compose
- OpenAI API key
- připojení k internetu


## Spuštění

### 1. Build a spuštění MCP serveru na pozadí

```bash
docker compose up -d --build mcp-server
```

### 2. Build a spuštění interaktivního agenta

```bash
docker compose run --build --rm agent
```

Tento způsob je vhodnější než běžné:

```bash
docker compose up
```

protože logy MCP serveru se nemíchají do interaktivního terminálového chatu.

Po spuštění se zobrazí:

```text
Agent is ready.
Type 'exit' or 'quit' to terminate.

You:
```

---

## Komunikace s agentem

Agent běží v jednoduché terminálové smyčce.

Uživatel zadá:

```text
You: Jakou mám známku z matematiky?
```

agent může zavolat školní MCP tool a následně vypíše odpověď:

```text
Agent: Z matematiky máš známku 2.
```

Po zobrazení odpovědi čeká na další dotaz.

Ukončení:

```text
exit
```

nebo:

```text
quit
```

---

## Příklady dotazů

### Školní MCP tools

```text
Jakou mám známku z matematiky?
```

```text
Jakou mám známku z fyziky?
```

```text
Jakou mám známku z dějepisu?
```

Poslední dotaz je vhodný také pro kontrolu chování při neexistujícím předmětu.

```text
Jaký mám průměr ze všech zapsaných předmětů?
```

```text
Zjisti mou známku z chemie a potom můj celkový průměr.
```

---

### Sequential Thinking MCP tool

Pro kontrolu druhého MCP serveru jsou vhodné složitější úlohy:

```text
Navrhni plán migrace databáze z PostgreSQL 14 na PostgreSQL 17.
Rozděl problém na kroky, zvaž rizika a použij dostupný nástroj pro
strukturované řešení.
```

```text
Porovnej tři možné architektury systému pro synchronizaci souborů
a systematicky vyhodnoť jejich výhody, nevýhody a rizika.
```

```text
Mám aplikaci složenou z REST API, databáze a několika workerů.
Navrhni postup migrace do Docker Compose a rozděl řešení do logických kroků.
```

---

## Lokální vývoj pomocí uv

Projekt je `uv workspace`.

Synchronizace dependencies:

```bash
uv sync
```

Virtuální prostředí workspace je:

```text
hw03/.venv/
```

V PyCharmu je vhodné použít interpreter:

```text
hw03/.venv/bin/python
```

Jednotlivé podprojekty nepotřebují vlastní `.venv`.

---
