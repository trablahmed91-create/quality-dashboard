import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Tableau de bord des réclamations", layout="wide")
st.title(" Tableau de bord des réclamations - Qualité")

# Vérifier si le fichier existe
fichier = "CLAIMS.xlsx2.xlsx"
if not os.path.exists(fichier):
    st.error(f"Le fichier {fichier} est introuvable. Vérifiez qu'il est dans le dépôt.")
    st.stop()

# Lire le fichier avec l'en-tête à la ligne 6
try:
    df = pd.read_excel(fichier, sheet_name="Total Claims April-2025,", header=5)
except Exception as e:
    st.error(f"Erreur de lecture : {e}")
    st.stop()

df.columns = df.columns.str.strip()

# Vérifier les colonnes disponibles
colonnes_disponibles = df.columns.tolist()
st.write("*Colonnes disponibles :*", colonnes_disponibles)

# Colonnes souhaitées (avec ajustement possible)
mapping = {
    "Date": "Date",
    "Code": "code",
    "Customer": "Customer",
    "Statut réclamation": "Claim statue",
    "Defect": "Defect",
    "4M": "4M",
    "Statut": "Statue",
    "Resp": "Resp",
    "Code dép.": "Dep code"
}

df_final = pd.DataFrame()
for nouveau, ancien in mapping.items():
    if ancien in df.columns:
        df_final[nouveau] = df[ancien]
    else:
        df_final[nouveau] = ""

# Nettoyage
df_final["Date"] = pd.to_datetime(df_final["Date"], errors="coerce").dt.date
df_final = df_final.fillna("")
df_final = df_final.astype(str)

# KPIs
total = len(df_final)
ouvertes = len(df_final[df_final["Statut réclamation"].str.contains("Open", na=False)])

c1, c2 = st.columns(2)
c1.metric(" Total des réclamations", total)
c2.metric(" Ouvertes", ouvertes)

# Graphique 4M
st.subheader(" Répartition par catégorie 4M")
if "4M" in df_final.columns:
    data_4m = df_final["4M"][df_final["4M"] != ""]
    if not data_4m.empty:
        counts = data_4m.value_counts().reset_index()
        counts.columns = ["4M", "Nombre"]
        fig = px.bar(counts, x="4M", y="Nombre", title="Réclamations par 4M")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée 4M (colonne vide).")
else:
    st.info("Colonne 4M introuvable.")

# Tableau
st.subheader(" Détail des réclamations (toutes les lignes)")
st.dataframe(df_final)
