Automacao de Notificacao para Aprovacao de solicitacao ou pedido de compra

Descrição
Rotina Python que consulta o banco de dados em busca de autorizações de pedido de compra pendentes e envia notificações por e-mail aos gestores para agilizar a aprovação.

Funcionalidades
- Consulta automática de pendências no banco de dados
- Envio automático de e-mail para os gestores responsáveis
- Registro de operações e status para controle/auditoria

Tecnologias
- Python (conexão com banco de dados e SMTP para e-mails)
- SQL
- Task Scheduler do Windows

Benefícios
- Agilidade no fluxo de aprovações
- Redução de acompanhamento manual
- Processo seguro e auditável

Uso
1. Configure o acesso ao banco e credenciais de e-mail no arquivo de configuração.
2. Execute `main.py` manualmente ou agende via Task Scheduler.
