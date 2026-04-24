import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tableau de bord des réclamations", layout="wide")
st.title(" Tableau de bord des réclamations - Qualité")

# 1. Charger tout le fichier sans en‑tête
try:
    df_raw = pd.read_excel("CLAIMS.xlsx2.xlsx", sheet_name=None, header=None)
except Exception as e:
    st.error(f"Impossible de lire le fichier : {e}")
    st.stop()

# Prendre la première feuille (quel que soit son nom)
first_sheet = list(df_raw.keys())[0]
df = df_raw[first_sheet]

# 2. Trouver la ligne qui contient les mots-clés (Date, code, Customer, ...)
mots_cles = ["date", "code", "customer", "claim", "defect", "4m", "statue", "resp", "dep code"]
ligne_entete = None
for i, row in df.iterrows():
    # Convertir toute la ligne en chaîne de caractères minuscules
    row_lower = " ".join(row.astype(str).str.lower())
    if all(mot in row_lower for mot in ["date", "code", "customer"]):
        ligne_entete = i
        break

if ligne_entete is None:
    st.error("La ligne d'en-tête n'a pas été trouvée. Vérifiez que les colonnes 'Date', 'code', 'Customer' existent.")
    st.stop()

# 3. Extraire les noms de colonnes et les données
colonnes = df.iloc[ligne_entete].astype(str).str.strip().tolist()
data = df.iloc[ligne_entete+1:].reset_index(drop=True)
data.columns = colonnes

# 4. Sélectionner les 9 colonnes souhaitées (avec correspondance floue)
def trouver_colonne(noms_possibles):
    for col in colonnes:
        for nom in noms_possibles:
            if col.lower() == nom.lower() or nom.lower() in col.lower():
                return col
    return None

mapping = {
    "Date": ["Date", "date"],
    "Code": ["code", "Code", "PN", "code produit"],
    "Customer": ["Customer", "customer", "Client"],
    "Statut réclamation": ["Claim statue", "Claim status", "Statut", "Claim statue"],
    "Defect": ["Defect", "defect", "Défaut"],
    "4M": ["4M", "4M ", "AM", "4m"],
    "Statut": ["Statue", "Statut", "status", "State"],
    "Resp": ["Resp", "resp", "DEP", "Responsible"],
    "Code dép.": ["Dep code", "dep code", "Code dép.", "Dept Code"]
}

df_final = pd.DataFrame()
for colonne_fr, possibles in mapping.items():
    col_trouvee = trouver_colonne(possibles)
    if col_trouvee:
        df_final[colonne_fr] = data[col_trouvee]
    else:
        df_final[colonne_fr] = ""

# 5. Nettoyer la date et les valeurs vides
df_final["Date"] = pd.to_datetime(df_final["Date"], errors="coerce").dt.date
df_final = df_final.fillna("").astype(str)

# 6. Indicateurs
total = len(df_final)
ouvertes = len(df_final[df_final["Statut réclamation"].str.contains("Open", na=False)])

col1, col2 = st.columns(2)
col1.metric(" Total des réclamations", total)
col2.metric(" Ouvertes", ouvertes)

# 7. Afficher le tableau complet
st.subheader(" Détail des réclamations (toutes les lignes)")
st.dataframe(df_final)
