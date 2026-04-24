import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tableau de bord des réclamations", layout="wide")
st.title(" Tableau de bord des réclamations - Qualité")

# تحميل الملف مباشرة
try:
    df = pd.read_excel("CLAIMS.xlsx2.xlsx", sheet_name="Total Claims April-2025,", header=5)
except:
    st.error("لم يتم العثور على الملف. تأكد من رفع CLAIMS.xlsx2.xlsx إلى نفس المجلد")
    st.stop()

# عرض أول 10 أسطر فقط للاختبار
st.subheader("أول 10 صفوف من البيانات")
st.dataframe(df.head(10))

# عرض أسماء الأعمدة
st.write("أسماء الأعمدة:", df.columns.tolist())
