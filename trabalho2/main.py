import os
import json
import sqlite3
import warnings
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

warnings.filterwarnings("ignore")

CSV_PATH   = "producao-mar-1941-1979.csv"
DB_PATH    = "anp_producao.db"
JSON_PATH  = "dados_tratados.json"
GRAF_SERIE = "grafico_serie_temporal.png"
GRAF_EXTRA = "grafico_producao_por_estado.png"

DECADA_INICIO = 1970
DECADA_FIM    = 1979

print("ETAPA 1 — Leitura do CSV (fonte ANP)")

df_raw = pd.read_csv(CSV_PATH, encoding="utf-8-sig", sep=",", engine="python")
df_raw.columns = df_raw.columns.str.strip()

print(f"  Registros brutos  : {len(df_raw):,}")
print(f"  Colunas           : {len(df_raw.columns)}")
print(f"  Período original  : {df_raw['Ano'].min()} – {df_raw['Ano'].max()}")

print('\n')
print("ETAPA 2 — Tratamento e limpeza")

def to_float(series):
    return (
        series.astype(str)
              .str.replace(",", ".", regex=False)
              .str.strip()
              .replace({"nan": None, "": None})
              .astype(float, errors="ignore")
    )

COLS_NUM = [
    "Produção de Óleo (m³)",
    "Produção de Condensado (m³)",
    "Produção de Gás Associado (Mm³)",
    "Produção de Gás Não Associado (Mm³)",
    "Produção de Água (m³)",
]

for col in COLS_NUM:
    df_raw[col] = pd.to_numeric(
        df_raw[col].astype(str).str.replace(",", ".", regex=False).str.strip(),
        errors="coerce",
    )

df = df_raw[(df_raw["Ano"] >= DECADA_INICIO) & (df_raw["Ano"] <= DECADA_FIM)].copy()
df = df.dropna(subset=["Produção de Óleo (m³)"])
df = df.reset_index(drop=True)

print(f"  Registros após filtro ({DECADA_INICIO}–{DECADA_FIM}): {len(df):,}")
print(f"  Nulos em Óleo removidos  : OK")
print(f"  Estados presentes        : {sorted(df['Estado'].dropna().unique())}")

print('\n')
print("ETAPA 3 — Conversão para JSON")

records = df[
    ["Ano", "Mês/Ano", "Estado", "Bacia", "Campo", "Poço",
     "Produção de Óleo (m³)", "Produção de Condensado (m³)",
     "Produção de Gás Associado (Mm³)", "Produção de Água (m³)"]
].copy()

records["Produção de Óleo (m³)"] = records["Produção de Óleo (m³)"].fillna(0)

json_data = {
    "fonte": "ANP — Agência Nacional do Petróleo, Gás Natural e Biocombustíveis",
    "dataset": "Produção Marítima de Petróleo e Gás",
    "periodo_filtrado": f"{DECADA_INICIO}–{DECADA_FIM}",
    "total_registros": len(records),
    "registros": records.to_dict(orient="records"),
}

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2, default=str)

print(f"  Arquivo gerado: {JSON_PATH}  ({os.path.getsize(JSON_PATH)/1024:.1f} KB)")

print('\n')
print("ETAPA 4 — Estatísticas descritivas")

anual = (
    df.groupby("Ano")["Produção de Óleo (m³)"]
      .sum()
      .reset_index(name="oleo_total_m3")
)

media = anual["oleo_total_m3"].mean()
maximo = anual["oleo_total_m3"].max()
minimo = anual["oleo_total_m3"].min()
ano_max = anual.loc[anual["oleo_total_m3"].idxmax(), "Ano"]
ano_min = anual.loc[anual["oleo_total_m3"].idxmin(), "Ano"]

print(f"  Produção anual de Óleo — Período {DECADA_INICIO}–{DECADA_FIM}")
print(f"  {'Média':10s}: {media:>15,.1f} m³/ano")
print(f"  {'Máximo':10s}: {maximo:>15,.1f} m³  (ano {ano_max})")
print(f"  {'Mínimo':10s}: {minimo:>15,.1f} m³  (ano {ano_min})")

por_estado = (
    df.groupby("Estado")["Produção de Óleo (m³)"]
      .agg(["sum", "mean", "max", "min"])
      .rename(columns={"sum": "Total (m³)", "mean": "Média (m³)",
                       "max": "Máximo (m³)", "min": "Mínimo (m³)"})
      .sort_values("Total (m³)", ascending=False)
)
print("\n  Produção por Estado:")
print(por_estado.to_string())

stats_json = {
    "media_anual_m3": round(media, 2),
    "maximo_m3": round(maximo, 2),
    "ano_maximo": int(ano_max),
    "minimo_m3": round(minimo, 2),
    "ano_minimo": int(ano_min),
    "por_estado": por_estado.reset_index().to_dict(orient="records"),
}

print('\n')
print("ETAPA 5 — Armazenamento em SQLite")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS producao_maritima")
cur.execute("""
CREATE TABLE producao_maritima (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    ano              INTEGER,
    mes_ano          TEXT,
    estado           TEXT,
    bacia            TEXT,
    campo            TEXT,
    poco             TEXT,
    oleo_m3          REAL,
    condensado_m3    REAL,
    gas_assoc_mm3    REAL,
    agua_m3          REAL
)
""")

insert_rows = [
    (
        row["Ano"],
        row["Mês/Ano"],
        row["Estado"],
        row["Bacia"],
        row["Campo"],
        row["Poço"],
        row["Produção de Óleo (m³)"],
        row["Produção de Condensado (m³)"],
        row["Produção de Gás Associado (Mm³)"],
        row["Produção de Água (m³)"],
    )
    for _, row in df.iterrows()
]
cur.executemany(
    "INSERT INTO producao_maritima (ano,mes_ano,estado,bacia,campo,poco,oleo_m3,"
    "condensado_m3,gas_assoc_mm3,agua_m3) VALUES (?,?,?,?,?,?,?,?,?,?)",
    insert_rows,
)

cur.execute("DROP TABLE IF EXISTS estatisticas")
cur.execute("""
CREATE TABLE estatisticas (
    periodo      TEXT,
    media_anual  REAL,
    maximo       REAL,
    ano_maximo   INTEGER,
    minimo       REAL,
    ano_minimo   INTEGER
)
""")
cur.execute(
    "INSERT INTO estatisticas VALUES (?,?,?,?,?,?)",
    (f"{DECADA_INICIO}-{DECADA_FIM}", round(media, 2),
     round(maximo, 2), int(ano_max), round(minimo, 2), int(ano_min)),
)

conn.commit()
conn.close()

count_db = sqlite3.connect(DB_PATH).execute(
    "SELECT COUNT(*) FROM producao_maritima"
).fetchone()[0]
print(f"  Banco de dados  : {DB_PATH}")
print(f"  Registros salvos: {count_db:,}")

print('\n')
print("ETAPA 6 — Geração de gráficos")

VERDE   = "#2ecc71"
AZUL    = "#2980b9"
LARANJA = "#e67e22"
CINZA   = "#ecf0f1"
ESCURO  = "#2c3e50"

fig1, ax1 = plt.subplots(figsize=(11, 5))
fig1.patch.set_facecolor(CINZA)
ax1.set_facecolor(CINZA)

ax1.fill_between(anual["Ano"], anual["oleo_total_m3"] / 1e6,
                 alpha=0.3, color=AZUL)
ax1.plot(anual["Ano"], anual["oleo_total_m3"] / 1e6,
         color=AZUL, linewidth=2.5, marker="o", markersize=7,
         markerfacecolor="white", markeredgewidth=2, label="Produção de Óleo")

ax1.axhline(media / 1e6, color=LARANJA, linestyle="--",
            linewidth=1.5, label=f"Média: {media/1e6:.2f} Mm³/ano")

ax1.set_title("Produção Marítima de Óleo — Última Década (1970–1979)",
              fontsize=14, fontweight="bold", color=ESCURO, pad=12)
ax1.set_xlabel("Ano", fontsize=11, color=ESCURO)
ax1.set_ylabel("Produção (Mm³)", fontsize=11, color=ESCURO)
ax1.set_xticks(anual["Ano"])
ax1.tick_params(colors=ESCURO)
ax1.spines[["top", "right"]].set_visible(False)
ax1.legend(fontsize=10)
ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f"))

ax1.annotate(
    f"Máx: {maximo/1e6:.1f} Mm³\n({ano_max})",
    xy=(ano_max, maximo / 1e6),
    xytext=(ano_max - 1.2, maximo / 1e6 + 0.05 * maximo / 1e6),
    fontsize=9, color=ESCURO,
    arrowprops=dict(arrowstyle="->", color=ESCURO, lw=1.2),
)

plt.tight_layout()
fig1.savefig(GRAF_SERIE, dpi=150, bbox_inches="tight")
plt.close(fig1)
print(f"  Gráfico 1 salvo: {GRAF_SERIE}")

por_estado_total = (
    df.groupby("Estado")["Produção de Óleo (m³)"]
      .sum()
      .sort_values(ascending=True)
)

fig2, ax2 = plt.subplots(figsize=(9, 5))
fig2.patch.set_facecolor(CINZA)
ax2.set_facecolor(CINZA)

cores = [VERDE if v == por_estado_total.max() else AZUL
         for v in por_estado_total.values]

bars = ax2.barh(por_estado_total.index,
                por_estado_total.values / 1e6,
                color=cores, edgecolor="white", height=0.55)

for bar, val in zip(bars, por_estado_total.values / 1e6):
    ax2.text(val + 0.02, bar.get_y() + bar.get_height() / 2,
             f"{val:.1f} Mm³", va="center", fontsize=9.5, color=ESCURO)

ax2.set_title("Produção Acumulada de Óleo por Estado (1970–1979)",
              fontsize=13, fontweight="bold", color=ESCURO, pad=12)
ax2.set_xlabel("Produção Total (Mm³)", fontsize=11, color=ESCURO)
ax2.tick_params(colors=ESCURO)
ax2.spines[["top", "right"]].set_visible(False)
ax2.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f"))

plt.tight_layout()
fig2.savefig(GRAF_EXTRA, dpi=150, bbox_inches="tight")
plt.close(fig2)
print(f"  Gráfico 2 salvo: {GRAF_EXTRA}")

print('\n')
print("Pipeline concluído:")
print(f"  {'CSV lido':<35}: {CSV_PATH}")
print(f"  {'JSON gerado':<35}: {JSON_PATH}")
print(f"  {'Banco SQLite':<35}: {DB_PATH}")
print(f"  {'Gráfico série temporal':<35}: {GRAF_SERIE}")
print(f"  {'Gráfico por estado':<35}: {GRAF_EXTRA}")
print(f"  {'Registros processados':<35}: {len(df):,}")
print(f"  {'Período analisado':<35}: {DECADA_INICIO}–{DECADA_FIM}")