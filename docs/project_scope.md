# 🧠 Real Estate Data Intelligence: Pipeline, API & Price Prediction

## 🎯 Objetivo

Transformar dados brutos de imóveis à venda em São Paulo em insights acionáveis e previsões de preços utilizando um pipeline completo que combina **engenharia de dados**, **ciência de dados** e **visualização interativa com Power BI**.

---

## 🔍 Visão Geral

O projeto realiza scraping automatizado de imóveis do site [chavesnamao.com.br](https://www.chavesnamao.com.br/apartamentos-a-venda/sp-sao-paulo/), armazena os dados em um pipeline em camadas e oferece uma API FastAPI para consulta. A nova fase estende esse pipeline com análise exploratória, modelagem preditiva e dashboards em Power BI.

---

## 🧱 Arquitetura do Pipeline

### 1. Coleta (Bronze)

* **Playwright** + **BeautifulSoup** para scraping dos dados da web.
* Salvamento dos dados crus em `.csv`.

### 2. Processamento (Silver)

* Limpeza e padronização com **pandas**.
* Conversão de tipos, tratamento de valores ausentes e normalização.

### 3. Armazenamento (Gold)

* Armazenamento final dos dados limpos em **PostgreSQL**.
* Modelagem analítica com **dbt-core** para consumo otimizado.

---

## 🧠 Camada de Ciência de Dados

### 🔎 Análise Exploratória de Dados (EDA)

* Estudo estatístico com `pandas`, `matplotlib`, `seaborn`.
* Identificação de outliers, correlações e padrões nos dados.

### 📊 Modelagem Preditiva

* Modelos de regressão para **previsão de preços de imóveis**:

  * Regressão Linear
  * Random Forest Regressor
  * XGBoost
* Avaliação com MAE, RMSE, R².
* Feature engineering para capturar variáveis relevantes (ex: localização, área, vagas, etc).

---

## 📈 Visualização com Power BI

* Dashboard conectado ao banco de dados PostgreSQL.
* Indicadores interativos: faixa de preço por bairro, média por número de quartos, tendência temporal etc.
* Atualização automática dos dados (via agendamento ou botão de refresh).

---

## 🌐 API com FastAPI

* Endpoints para consulta de imóveis com filtros.
* Exportação dos dados em JSON e CSV.
* Endpoint `/status` para checar data e status da última atualização.
* Documentação interativa em `/docs` (Swagger) e `/redoc`.

---

## ✅ Testes Automatizados

* Testes com `pytest` para scraping, ETL, API e modelos preditivos.
* Integração contínua com **GitHub Actions**.

---

## 🐳 Deploy e Infraestrutura

* **Docker** para facilitar o deploy em qualquer ambiente.
* Pipeline CI/CD com GitHub Actions.
* Deploy planejado em **AWS** (EC2, RDS, ou ECS).

---

## 🧰 Tecnologias

| Camada         | Tecnologias Principais    |
| -------------- | ------------------------- |
| Coleta         | Playwright, BeautifulSoup |
| ETL            | Python, Pandas            |
| Banco de Dados | PostgreSQL, SQLAlchemy    |
| Modelagem      | scikit-learn, XGBoost     |
| API            | FastAPI, Uvicorn          |
| Transformação  | dbt-core                  |
| Visualização   | Power BI                  |
| Infraestrutura | Docker, GitHub Actions    |

---

## 🚀 Impacto Esperado

* Tornar acessíveis dados estruturados de imóveis.
* Permitir análises automatizadas e decisões baseadas em dados.
* Implementar modelos preditivos úteis para compradores, corretores e investidores.
* Demonstrar conhecimento prático em ciência de dados aplicada ao mercado imobiliário.
