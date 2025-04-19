Pipeline de CI/CD (GitHub Actions)
testes com pyhton
dbt-core
machine learning
deploy
disponibilizar em uma api com FastAPI com endpoint
Adicionar autenticação na API (token JWT)
conteineirizar a aplicação com o docker
Validação dos dados no banco?
Agendamento da pipeline?
Crie um arquivo chamado Makefile na raiz do projeto:
Controlar o numero de paginas disponíveis para fazer o scraping

Configure ECS Cluster + Fargate para rodar o container (AWS Free Tier, mais complexo, mas ideal pra portfólio)
⚠️ Exige mais configuração, mas é excelente para currículos de Data Engineer.



real_estate_pipeline/
├── data/
│   ├── raw/                    # Dados brutos (ex: HTML, JSON)
│   ├── cleaned/                # Dados limpos (ex: CSVs)
│   └── db/                     # Migrations ou backups do banco
├── pipeline/
│   ├── __init__.py
│   ├── scraper.py              # Código com Playwright para scraping
│   ├── cleaner.py              # Código de limpeza e transformação
│   ├── postgres_writer.py      # Inserção dos dados no PostgreSQL
│   └── utils.py                # Funções auxiliares (ex: logging, parsing)
├── api/
│   ├── __init__.py
│   └── main.py                 # FastAPI para servir os dados
├── dbt/
│   └── ...                     # (Mais tarde) Modelos e configs dbt
├── .env                        # Variáveis de ambiente
├── requirements.txt
├── Makefile
├── Dockerfile
└── README.md
