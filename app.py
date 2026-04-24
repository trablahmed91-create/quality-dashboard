import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tableau de bord des réclamations", layout="wide")
st.title(" Tableau de bord des réclamations - Qualité")

# Chargement brut
df_raw = pd.read_excel("CLAIMS.xlsx2.xlsx", sheet_name="Total Claims April-2025,", header=None)

# Trouver ligne contenant "Date"
header_row = None
for i, row in df_raw.iterrows():
    row_str = row.astype(str).str.lower().tolist()
    if any("date" in str(cell).lower() for cell in row_str if pd.notna(cell)):
        header_row = i
        break

if header_row is None:
    st.error("Ligne d'en-tête non trouvée")
    st.stop()

columns = df_raw.iloc[header_row].astype(str).str.strip().tolist()
data = df_raw.iloc[header_row+1:].reset_index(drop=True)
data.columns = columns

# Colonnes voulues
cols = ["Date", "code", "Customer", "Claim statue", "Defect", "4M", "Statue", "Resp", "Dep code"]
for col in cols:
    if col not in data.columns:
        data[col] = ""

df = data[cols]

# Renommage
df.rename(columns={
    "code": "Code",
    "Claim statue": "Statut réclamation",
    "Statue": "Statut",
    "Dep code": "Code dép."
}, inplace=True)

# Date
df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
df = df.fillna("")
df = df.astype(str)

# Indicateurs
total = len(df)
ouvertes = len(df[df["Statut réclamation"].str.contains("Open", na=False)])

col1, col2 = st.columns(2)
col1.metric(" Total des réclamations", total)
col2.metric(" Ouvertes", ouvertes)

# Graphique 4M
st.subheader(" Répartition par catégorie 4M")
if "4M" in df.columns:
    data_4m = df["4M"][df["4M"] != ""]
    if not data_4m.empty:
        counts = data_4m.value_counts().reset_index()
        counts.columns = ["4M", "Nombre"]
        fig = px.bar(counts, x="4M", y="Nombre", title="Réclamations par 4M")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée 4M trouvée.")
else:
    st.info("Colonne 4M manquante.")

st.subheader(" Détail des réclamations (toutes les lignes)")
st.dataframe(df)
