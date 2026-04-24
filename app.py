import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tableau de bord des réclamations", layout="wide")
st.title(" Tableau de bord des réclamations - Qualité")

# Charger le fichier avec l'en-tête à la ligne 6 (index 5)
df = pd.read_excel("CLAIMS.xlsx2.xlsx", sheet_name="Total Claims April-2025,", header=5)
df.columns = df.columns.str.strip()

# Sélectionner les colonnes demandées avec leurs noms EXACTS
colonnes_voulues = {
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

# Construire le DataFrame final
df_final = pd.DataFrame()
for nouveau, ancien in colonnes_voulues.items():
    if ancien in df.columns:
        df_final[nouveau] = df[ancien]
    else:
        df_final[nouveau] = ""

# Nettoyer la date (enlever l'heure)
df_final["Date"] = pd.to_datetime(df_final["Date"], errors="coerce").dt.date

# Remplacer les NaN par des chaînes vides
df_final = df_final.fillna("")
df_final = df_final.astype(str)

# Indicateurs
total = len(df_final)
ouvertes = len(df_final[df_final["Statut réclamation"].str.contains("Open", na=False)])

col1, col2 = st.columns(2)
col1.metric(" Total des réclamations", total)
col2.metric(" Ouvertes", ouvertes)

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
        st.info("Aucune donnée 4M trouvée dans le fichier.")
else:
    st.info("Colonne 4M absente.")

# Tableau des données
st.subheader(" Détail des réclamations (toutes les lignes)")
st.dataframe(df_final)
