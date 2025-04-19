# 📌 Escopo do Projeto: API de Imóveis - São Paulo

## 🌟 Objetivo
Este projeto tem como objetivo construir uma API profissional utilizando **FastAPI** que fornece dados atualizados sobre **apartamentos à venda na cidade de São Paulo**, extraídos do site [chavesnamao.com.br](https://www.chavesnamao.com.br/apartamentos-a-venda/sp-sao-paulo/).

A API expõe endpoints que permitem consultar, filtrar e explorar os imóveis com base em critérios como preço, metragem, número de quartos, banheiros, vagas, entre outros.

---

## 🔍 Descrição Geral do Projeto
A aplicação realiza o **scraping automatizado** das páginas do site "Chaves na Mão", utilizando:
- **Playwright** para lidar com a renderização dinâmica do conteúdo.
- **BeautifulSoup** para fazer o parsing e extração de informações específicas de cada card de imóvel.

As informações coletadas incluem:
- Título do anúncio
- Preço
- Tamanho (m²)
- Número de dormitórios
- Número de banheiros
- Vagas de garagem
- Link para o anúncio

Esses dados passam por um pipeline profissional estruturado em camadas.

---

## 🧱 Pipeline de Dados (ETL)
A arquitetura do projeto segue uma pipeline com as seguintes camadas:
- **Bronze:** Armazenamento dos dados crus em CSV (diretório `data/csv`).
- **Silver:** Limpeza, padronização e transformação dos dados (remoção de duplicatas, conversão de tipos, extração de padrões).
- **Gold:** Dados tratados e armazenados no **PostgreSQL**, prontos para consumo via API e análises com **dbt**.

---

## 🏧 Funcionalidades da API
- Listar todos os apartamentos disponíveis.
- Filtros por faixa de preço, metragem, número de dormitórios, banheiros e vagas.
- Detalhes completos de cada imóvel.
- Paginação de resultados.
- Exportação de dados em CSV ou JSON.
- Endpoint de status de atualização do scraping.

---

## 📜 Documentação Interativa
- **Swagger UI** gerado automaticamente pelo FastAPI.
- Documentação interativa disponível em `/docs`.
- Alternativa com **Redoc** em `/redoc`.

---

## 🧪 Testes Automatizados
- Testes unitários para scraping, limpeza e transformação dos dados.
- Testes dos endpoints da API.
- Testes de integração com o banco de dados.
- Framework: **pytest** com cobertura integrada no CI.

---

## 📈 Análises e Visualização (Opcional)
- Uso de **dbt-core** para modelagem analítica e transformação SQL em camadas.
- Possibilidade de integração com **Streamlit** para criação de dashboards interativos.

---

## 🚀 Deploy e Infraestrutura
- **Docker** para containerização da aplicação e ambientes consistentes.
- **GitHub Actions** para CI/CD com etapas de lint, testes e deploy.
- Deploy planejado na **AWS** (EC2, RDS ou ECS) com escalabilidade e segurança.

---

## 🔧 Tecnologias Utilizadas
- **Python 3.11**
- **FastAPI**
- **Playwright** + **BeautifulSoup**
- **Pandas**
- **PostgreSQL**
- **SQLAlchemy**
- **dbt-core**
- **Docker**
- **GitHub Actions**
- **Streamlit** (opcional)
- **pytest**

---

## ❓ Por que este projeto é relevante?
Imóveis são um mercado em constante movimento e nem sempre os dados estão disponíveis de forma estruturada. Este projeto organiza, limpa e disponibiliza os dados de forma acessível, possibilitando:
- Estudos de mercado imobiliário.
- Visualizações e dashboards.
- Sistemas de recomendação.
- Monitoramento de preços.

---

## 📘 Como isso será documentado no README
Este escopo será incorporado na seção de introdução do `README.md` final, servindo como referência para novos desenvolvedores, recrutadores e interessados em entender a motivação, arquitetura e objetivos do projeto.

