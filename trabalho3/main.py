import dotenv
import os
import logging
import schedule
import time
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import mysql.connector
import datetime

# configuracoes
CSV_PATH = "producao-mar-1941-1979.csv"
PASTA_SAIDA = "resultados"
LOG_FILE = os.path.join(PASTA_SAIDA, "pipeline.log")
GRAF_PIZZA = os.path.join(PASTA_SAIDA, "grafico_pizza.png")
GRAF_AREA = os.path.join(PASTA_SAIDA, "grafico_area.png")

DECADA_INICIO = 1970
DECADA_FIM    = 1979

dotenv.load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_DATABASE"),
}

os.makedirs(PASTA_SAIDA, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# leitura do csv
def obter_dados():
    try:
        df = pd.read_csv(CSV_PATH, encoding="utf-8-sig", sep=",", engine="python")
        df.columns = df.columns.str.strip()
        logging.info(f"CSV carregado: {len(df)} registros.")
        return df
    except FileNotFoundError:
        logging.error("Arquivo CSV não encontrado.")
        print("Erro: arquivo CSV não encontrado.")
        return None
    except Exception as e:
        logging.error(f"Erro ao carregar CSV: {e}")
        print("Erro ao carregar dados:", e)
        return None


# limpeza
def processar_dados(df):
    try:
        COLS_NUM = [
            "Produção de Óleo (m³)",
            "Produção de Condensado (m³)",
            "Produção de Gás Associado (Mm³)",
            "Produção de Água (m³)",
        ]
        for col in COLS_NUM:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", ".", regex=False).str.strip(),
                errors="coerce",
            )

        df = df[(df["Ano"] >= DECADA_INICIO) & (df["Ano"] <= DECADA_FIM)].copy()
        df = df.dropna(subset=["Produção de Óleo (m³)"])
        df[COLS_NUM] = df[COLS_NUM].fillna(0)
        df = df.reset_index(drop=True)

        logging.info(f"Dados filtrados ({DECADA_INICIO}–{DECADA_FIM}): {len(df)} registros.")
        return df
    except Exception as e:
        logging.error(f"Erro ao processar dados: {e}")
        print("Erro ao processar dados:", e)
        return None


# criar o banco
def criar_banco():
    try:
        cnx = mysql.connector.connect(
            host = DB_CONFIG['host'],
            user = DB_CONFIG["user"],
            password = DB_CONFIG["password"],
        )
        cursor = cnx.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS producao_maritima (
                id            INT AUTO_INCREMENT PRIMARY KEY,
                ano           SMALLINT,
                mes_ano       VARCHAR(10),
                estado        VARCHAR(50),
                bacia         VARCHAR(100),
                campo         VARCHAR(100),
                oleo_m3       DOUBLE DEFAULT 0,
                condensado_m3 DOUBLE DEFAULT 0,
                gas_assoc_mm3 DOUBLE DEFAULT 0,
                agua_m3       DOUBLE DEFAULT 0
            )
        """)
        cnx.commit()
        logging.info("Estrutura do banco criada/verificada com sucesso.")
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro: usuário ou senha incorretos.")
            logging.error("Erro de autenticação MySQL.")
        else:
            print("Erro MySQL:", err)
            logging.error(f"Erro ao criar estrutura: {err}")
    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()


# salvar no banco
def salvar_no_banco(df):
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()

        # Remove registros anteriores do período para garantir idempotência
        cursor.execute(
            "DELETE FROM producao_maritima WHERE ano BETWEEN %s AND %s",
            (DECADA_INICIO, DECADA_FIM)
        )

        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO producao_maritima
                    (ano, mes_ano, estado, bacia, campo,
                     oleo_m3, condensado_m3, gas_assoc_mm3, agua_m3)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                int(row["Ano"]),
                str(row["Mês/Ano"]),
                str(row["Estado"])  if pd.notna(row["Estado"]) else None,
                str(row["Bacia"])   if pd.notna(row["Bacia"])  else None,
                str(row["Campo"])   if pd.notna(row["Campo"])  else None,
                float(row["Produção de Óleo (m³)"]),
                float(row["Produção de Condensado (m³)"]),
                float(row["Produção de Gás Associado (Mm³)"]),
                float(row["Produção de Água (m³)"]),
            ))

        cnx.commit()
        logging.info(f"{len(df)} registros salvos no MySQL.")
    except mysql.connector.Error as err:
        if cnx:
            cnx.rollback()
        print("Erro MySQL:", err)
        logging.error(f"Erro ao salvar no MySQL: {err}")
    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()


# consulta do banco
def consultar_dados():
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        df = pd.read_sql("SELECT * FROM producao_maritima", cnx)
        logging.info("Consulta ao banco executada com sucesso.")
        return df
    except mysql.connector.Error as err:
        print("Erro MySQL:", err)
        logging.error(f"Erro ao consultar dados: {err}")
        return None
    finally:
        if cnx and cnx.is_connected():
            cnx.close()


# estatisticas
def calcular_estatisticas(df):
    try:
        stats = df["oleo_m3"].describe()

        print("\nESTATÍSTICAS — Produção de Óleo (m³):")
        print(stats)

        caminho = os.path.join(PASTA_SAIDA, "estatisticas.txt")
        with open(caminho, "w", encoding="utf-8") as f:
            f.write("ESTATÍSTICAS — Produção de Óleo (m³)\n")
            f.write(str(stats))

        logging.info("Estatísticas calculadas e salvas.")
    except Exception as e:
        logging.error(f"Erro ao calcular estatísticas: {e}")
        print("Erro ao calcular estatísticas:", e)


# graficos
def grafico_pizza_estados(df):
    try:
        por_estado = (
            df.groupby("estado")["oleo_m3"]
            .sum()
            .sort_values(ascending=False)
        )

        labels  = por_estado.index.tolist()
        valores = por_estado.values.tolist()
        CORES   = ["#e94560", "#2e86ab", "#f18f01", "#533483",
                   "#2ecc71", "#c73e1d", "#a23b72", "#16213e"]

        fig, ax = plt.subplots(figsize=(9, 7))
        fig.patch.set_facecolor("#1a1a2e")
        ax.set_facecolor("#1a1a2e")

        wedges, texts, autotexts = ax.pie(
            valores,
            labels=None,
            autopct="%1.1f%%",
            startangle=140,
            colors=CORES[:len(labels)],
            explode=[0] * len(labels),
            pctdistance=0.75,
            wedgeprops=dict(linewidth=2, edgecolor="#1a1a2e"),
        )
        for at in autotexts:
            at.set_color("#e0e0e0")
            at.set_fontsize(10)
            at.set_fontweight("bold")

        patches = [
            plt.Rectangle(
                (0, 0), 1, 1,
                fc=CORES[i],
                label=f"{labels[i]}  —  {valores[i]/1e6:,.2f} Mm³"
            )
            for i in range(len(labels))
        ]
        ax.legend(
            handles=patches,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.14),
            ncol=2,
            fontsize=9.5,
            framealpha=0.1,
            labelcolor="#e0e0e0",
        )

        ax.set_title(
            "Participação por Estado — Produção Acumulada de Óleo (1970–1979)",
            fontsize=13, fontweight="bold", color="#e0e0e0", pad=18,
        )

        plt.tight_layout()
        plt.savefig(GRAF_PIZZA, dpi=150, bbox_inches="tight", facecolor="#1a1a2e")
        plt.close()
        logging.info(f"Gráfico de pizza (estados) salvo: {GRAF_PIZZA}")

    except Exception as e:
        logging.error(f"Erro ao gerar gráfico de pizza: {e}")
        print("Erro ao gerar gráfico de pizza:", e)


def grafico_area_empilhada_campos(df):
    try:
        import numpy as np

        top_campos = (
            df.groupby("campo")["oleo_m3"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .index.tolist()
        )

        df2 = df.copy()
        df2["campo_grupo"] = df2["campo"].apply(
            lambda c: c if c in top_campos else "Outros"
        )

        pivot = (
            df2.groupby(["ano", "campo_grupo"])["oleo_m3"]
            .sum()
            .unstack(fill_value=0)
            / 1e6
        )

        cols = [c for c in pivot.columns if c != "Outros"]
        if "Outros" in pivot.columns:
            cols = cols + ["Outros"]
        pivot = pivot[cols]

        CORES = ["#e94560", "#2e86ab", "#f18f01", "#533483",
                 "#2ecc71", "#778ca3"]

        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor("#1a1a2e")
        ax.set_facecolor("#1a1a2e")

        ax.stackplot(
            pivot.index,
            [pivot[col].values for col in pivot.columns],
            labels=pivot.columns.tolist(),
            colors=CORES[:len(pivot.columns)],
            alpha=0.85,
        )

        ax.set_title(
            "Evolução Anual da Produção de Óleo — Top 5 Campos + Outros (1970–1979)",
            fontsize=13, fontweight="bold", color="#e0e0e0", pad=14,
        )
        ax.set_xlabel("Ano", fontsize=11, color="#e0e0e0")
        ax.set_ylabel("Produção (Mm³)", fontsize=11, color="#e0e0e0")
        ax.set_xticks(pivot.index)
        ax.tick_params(colors="#e0e0e0")
        ax.spines[["top", "right", "left", "bottom"]].set_color("#333355")
        ax.yaxis.grid(True, linestyle="--", alpha=0.25, color="#e0e0e0")
        ax.set_axisbelow(True)

        legend = ax.legend(
            loc="upper left",
            fontsize=9,
            framealpha=0.15,
            labelcolor="#e0e0e0",
            title="Campo",
            title_fontsize=9,
        )
        legend.get_title().set_color("#e0e0e0")

        plt.tight_layout()
        plt.savefig(GRAF_AREA, dpi=150, bbox_inches="tight", facecolor="#1a1a2e")
        plt.close()
        logging.info(f"Gráfico de área empilhada (campos) salvo: {GRAF_AREA}")

    except Exception as e:
        logging.error(f"Erro ao gerar gráfico de área empilhada: {e}")
        print("Erro ao gerar gráfico de área empilhada:", e)


# pipeline
def executar_pipeline():
    logging.info(f"{'='*75}")
    logging.info(f"Pipeline iniciado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    df = obter_dados()

    df = processar_dados(df)
    if df is None or df.empty:
        print("Erro: nenhum dado válido após processamento.")
        logging.warning("DataFrame vazio após processamento.")
        return

    criar_banco()
    salvar_no_banco(df)

    df_db = consultar_dados()
    if df_db is None or df_db.empty:
        print("Erro: não foi possível consultar dados do banco.")
        logging.warning("Consulta retornou vazia.")
        return

    calcular_estatisticas(df_db)
    grafico_pizza_estados(df_db)
    grafico_area_empilhada_campos(df_db)

    logging.info("Pipeline executado com sucesso.")
    print("Pipeline executado com sucesso.")
    print(f"Resultados salvos em: {PASTA_SAIDA}")


if __name__ == "__main__":
    executar_pipeline()

    schedule.every().day.at("20:34").do(executar_pipeline)
    print("Agendamento ativo — execução diária às 20:34.")

    while True:
        schedule.run_pending()
        time.sleep(60)