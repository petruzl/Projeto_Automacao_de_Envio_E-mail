# 🤖 Automação de Processo com Python (RPA)

Este projeto implementa uma automação de processo utilizando **Python, SQLAlchemy, Pandas e Yagmail**.  
O objetivo é **reduzir atividades manuais** e garantir **mais agilidade e padronização** no envio de relatórios diários.

## 🚀 Funcionalidades
- Geração de **logs estruturados** para acompanhamento da execução.
- Conexão com banco de dados (Oracle ou outro compatível via SQLAlchemy).
- Execução de **consulta SQL** para identificar pendências.
- Tratamento e formatação dos dados com **Pandas**.
- Geração de relatório em **Excel**.
- Envio automático do relatório por **e-mail**.

## 🛠️ Tecnologias e Bibliotecas
- [Python 3.10+](https://www.python.org/)
- [logging](https://docs.python.org/3/library/logging.html) → monitoramento e logs.
- [pandas](https://pandas.pydata.org/) → manipulação de dados.
- [sqlalchemy](https://www.sqlalchemy.org/) → conexão e execução de queries.
- [oracledb](https://oracle.github.io/python-oracledb/) → driver Oracle (pode ser substituído por outro, ex: psycopg2 para PostgreSQL).
- [yagmail](https://github.com/kootenpv/yagmail) → envio simplificado de e-mails.

## Benefícios
- Agilidade no fluxo de aprovações
- Redução de acompanhamento manual
- Processo seguro e auditável

## Uso
1. Configure o acesso ao banco e credenciais de e-mail no arquivo de configuração.
2. Execute `main.py` manualmente ou agende via Task Scheduler.
3. Sempre que precisar instalar todas as dependências em outro ambiente, use:
     pip install -r requirements.txt

## 📂 Estrutura do Projeto

automacao-rpa-python/
│
├── automacao_RPA_com_Python_mascara.py   # Script principal
├── requirements.txt                      # Lista de bibliotecas necessárias
├── README.md                             # Documentação do projeto
