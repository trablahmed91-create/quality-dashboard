import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tableau de bord des réclamations", layout="wide")
st.title(" Tableau de bord des réclamations - Qualité")

# Lire le fichier CSV
df = pd.read_csv("data.csv", encoding="utf-8")

# Nettoyer les noms de colonnes
df.columns = df.columns.str.strip()

# Renommer pour l'affichage (adapter au besoin)
df.rename(columns={
    "code": "Code",
    "Claim statue": "Statut réclamation",
    "Statue": "Statut",
    "Dep code": "Code dép."
}, inplace=True)

# Colonnes à afficher
colonnes = ["Date", "Code", "Customer", "Statut réclamation", "Defect", "4M", "Statut", "Resp", "Code dép."]
for col in colonnes:
    if col not in df.columns:
        df[col] = ""

df = df[colonnes]

# Date sans heure
df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
df = df.fillna("")
df = df.astype(str)

# Indicateurs
total = len(df)
ouvertes = len(df[df["Statut réclamation"].str.contains("Open", na=False)])

col1, col2 = st.columns(2)
col1.metric(" Total des réclamations", total)
col2.metric(" Ouvertes", ouvertes)

# Tableau complet
st.subheader(" Détail des réclamations (toutes les lignes)")
st.dataframe(df)
