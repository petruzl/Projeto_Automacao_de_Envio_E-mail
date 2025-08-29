import logging
import datetime
import pandas as pd
import yagmail
import sqlalchemy as sa

logging.basicConfig(
    filename='execucao.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def obter_saudacao():
    """Retorna uma saudação de acordo com o horário atual"""
    hora_atual = datetime.datetime.now().hour
    if 5 <= hora_atual < 12:
        return "Bom dia"
    elif 12 <= hora_atual < 18:
        return "Boa tarde"
    else:
        return "Boa noite"

try:
    logging.info('=== Script iniciado ===')

    dsn = "oracle+oracledb://usuario:senha@host:porta/servico"
    engine = sa.create_engine(dsn)

    query = """
    SELECT
        id_pedido,
        cliente,
        valor_total,
        data_pedido,
        status
    FROM pedidos
    WHERE status = 'PENDENTE'
      AND data_pedido < SYSDATE - 1
    ORDER BY data_pedido
    """

    df = pd.read_sql(query, con=engine)

    if df.empty:
        msg = "Sem pendências encontradas. Nenhum e-mail enviado."
        logging.info(msg)
        print(msg)
    else:
        df["data_pedido"] = pd.to_datetime(df["data_pedido"]).dt.strftime("%d/%m/%Y")
        df["valor_total"] = pd.to_numeric(df["valor_total"], errors="coerce").fillna(0)
        df["valor_total"] = df["valor_total"].apply(
            lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )

        arquivo = "relatorio_pedidos_pendentes.xlsx"
        df.to_excel(arquivo, index=False)
        logging.info(f"Arquivo gerado: {arquivo}")

        saudacao = obter_saudacao()
        conteudo_email = f"""
        {saudacao},

        Segue em anexo o relatório com os pedidos pendentes de aprovação.
        """
        yag = yagmail.SMTP(
            user="usuario@email.com",
            password="sua_senha",
            host="smtp.seuprovedor.com",
            port=587,
            smtp_starttls=True,
            smtp_ssl=False
        )
        yag.send(
            to="destinatario@email.com",
            subject="Pedidos Pendentes de Aprovação",
            contents=conteudo_email,
            attachments=arquivo
        )

        msg = "E-mail enviado com sucesso!"
        logging.info(msg)
        print(msg)

except Exception as e:
    error_msg = f"Erro no script principal: {str(e)}"
    logging.error(error_msg)
    print(error_msg)

finally:
    logging.info('=== Script concluído ===')
