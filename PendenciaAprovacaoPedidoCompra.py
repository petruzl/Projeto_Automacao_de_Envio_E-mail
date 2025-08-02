#regras:
#se tiver linha evia email para RSANTOS - teste estou enviando no meu email



import oracledb
from sqlalchemy import create_engine
import pandas as pd
import yagmail

# Inicializa Oracle Instant Client
oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_12_2")

# Conexão com o banco Oracle
host = "10.20.1.10"
port = 1521
service_name = "piramide.subnetprivate.vcnfsj.oraclevcn.com"
dsn = oracledb.makedsn(host, port, service_name=service_name)

user = "piramide"
password = "piramide"

engine = create_engine(f"oracle+oracledb://{user}:{password}@{dsn}")

# SQL – apenas pendências com mais de 24h
query = """
SELECT CASE
         WHEN pc.empresa = '50' THEN
          '50-PJ'
         WHEN pc.empresa = '03' THEN
          '03-CN'
         ELSE
          pc.empresa
       END AS EMPRESA,
       pc.filial,
       CASE
         WHEN pc.filial = '03' THEN
          'FSF'
         WHEN pc.filial = '09' THEN
          'BEATRIZ'
         WHEN pc.filial = '10' THEN
          'FACA'
         WHEN pc.filial = '11' THEN
          'FBV'
         WHEN pc.filial = '12' THEN
          'ELVIRA'
         WHEN pc.filial = '13' THEN
          'GAZOLLA'
         WHEN pc.filial = '14' THEN
          'BRASILIA2'
         WHEN pc.filial = '50' THEN
          'FSJ'
         WHEN pc.filial = '51' THEN
          'FSM'
         WHEN pc.filial = '53' THEN
          'BRASILIA1'
         ELSE
          pc.filial
       END AS Fazenda,
       --pc.filial,
       trunc(pc.dt_pedido) AS data_af,
       trunc(P.DAT_PENDENCIA) AS DAT_PENDENCIA,
       pc.numpedc AS AF,
       --pc.fornecedor AS FORN,
       f.nome RAZAO_SOCIAL,
       to_char(pc.val_total_pedido, '9G999G999D99') AS VALOR,
       --pc.cod_usuario AS USUARIO,
       u.nom_usuario AS NOME_USUARIO,
       --p.cod_usuario AS APROVADOR,
       u2.nom_usuario
       --pc.cod_alcada AS ALCADA,
       --p.cod_tipo_id_usuario as COD_PAPEL,
       --pap.dsc_tipo_id_usuario as PAPEL,
       --pc.dat_inclusao AS INCLUSAO,
      /* CASE
         WHEN SYSDATE > P.DAT_PENDENCIA + INTERVAL '1' DAY THEN
          'PENDENTE > 24h'
         ELSE
          'Dentro do prazo'
       END AS STATUS_PENDENCIA*/
  FROM pedido_compra pc
  JOIN itens_ped_compra ipc ON (pc.filial = ipc.filial AND
                               pc.numpedc = ipc.numpedc)
  JOIN aplicacao ap ON (ipc.cod_aplicacao = ap.codaplica AND
                       ipc.filial = ap.FILIAL)
  JOIN fornec f ON (pc.fornecedor = f.codigo)
  LEFT JOIN PIR_DOCUMENTO_PROCESSO PR ON (pc.num_seq_doc_processo =
                                         PR.num_seq_doc_processo)
  JOIN PIR_PENDENCIA_PROCESSO PEND ON (PEND.NUM_SEQ_DOC_PROCESSO =
                                      PR.NUM_SEQ_DOC_PROCESSO)
  LEFT JOIN UNIDADE_COMPRADORA UC ON UC.COD_UNCOMP = PC.COD_UNCOMP
  LEFT JOIN PIR_USUARIO_PENDENCIA_PROCESSO p ON (PEND.NUM_SEQ_PENDENCIA_PROCESSO =
                                                p.num_seq_pendencia_processo)
  LEFT JOIN PIR_DELEGACAO_APROVACAO DEL ON (DEL.COD_USUARIO_OFICIAL =
                                           P.COD_USUARIO AND P.COD_TIPO_ID_USUARIO =
                                           DEL.COD_PAPEL AND
                                           AP.CCUSTO = DEL.COD_CCUSTO AND
                                           SYSDATE BETWEEN
                                           DAT_VIGENCIA_INICIAL AND
                                           DAT_VIGENCIA_FINAL)
  JOIN pir_tipo_id_usuario PAP ON (PAP.COD_TIPO_ID_USUARIO =
                                  P.COD_TIPO_ID_USUARIO)
  JOIN usuario u ON U.NOM_USUARIO_LOGIN = pc.cod_usuario
  
  JOIN usuario u2 ON U2.NOM_USUARIO_LOGIN = p.cod_usuario
 WHERE
--pc.ind_autorizacao = 'N'
 p.cod_usuario = 'RSANTOS'
--AND SYSDATE > P.DAT_PENDENCIA + INTERVAL '1' DAY
 GROUP BY pc.empresa,
          pc.filial,
          pc.filial,
          pc.dt_pedido,
          P.DAT_PENDENCIA,
          pc.numpedc,
          pc.cod_usuario,
          p.cod_usuario,
          P.COD_TIPO_ID_USUARIO,
          PAP.DSC_TIPO_ID_USUARIO,
          u.nom_usuario,
          pc.cod_alcada,
          pc.dat_inclusao,
          pc.fornecedor,
          f.nome,
          pc.val_total_pedido,
          UC.DSC_UNCOMP,
          u2.nom_usuario
 ORDER BY pc.filial, pc.numpedc, P.COD_TIPO_ID_USUARIO
"""

# Executa a consulta
df = pd.read_sql(query, con=engine)

# Corrige formatação de datas
df["data_af"] = pd.to_datetime(df["data_af"]).dt.strftime("%d/%m/%Y")
df["dat_pendencia"] = pd.to_datetime(df["dat_pendencia"]).dt.strftime("%d/%m/%Y")

# Corrige formatação de valor
df["valor"] = df["valor"].apply(lambda x: f"{float(str(x).replace('.', '').replace(',', '.')):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))


# Verifica se há pendências > 24h
if df.empty:
    print("Sem pendências AF. Nenhum e-mail enviado.")
else:
    # Salva o resultado em Excel
    arquivo = "resultado_afs_pendentes.xlsx"
    df.columns = df.columns.str.upper()  # Converte os nomes das colunas para maiúsculas
    df.to_excel(arquivo, index=False)

    # Envia o e-mail com yagmail
    yag = yagmail.SMTP(
        user='aprovacao@envio.agrosaojose.com.br',
        password='At?6KvS4y!D4',
        host='mail.agrosaojose.com.br',
        port=587,
        smtp_starttls=True,
        smtp_ssl=False
    )

    yag.send(
        to="leandro.petruz@agrosaojose.com.br",
        subject="AFs Pendentes de Autorização - Rinaldo",
        contents="Segue em anexo o relatório com as AFs pendentes. Acesse o sistema: http://10.20.2.10:90/piramide/asp/Geral/login.aspx?forceCredentials=true",
        attachments=arquivo
    )

    print("E-mail enviado com sucesso!")
