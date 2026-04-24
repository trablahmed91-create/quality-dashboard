[19:53, 24/04/2026] Ahmed: import streamlit as st
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
[19:56, 24/04/2026] Ahmed: import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tableau de bord des réclamations", layout="wide")
st.title(" Tableau de bord des réclamations - Qualité")

# قراءة الملف (بدون تحديد header)
df_raw = pd.read_excel("CLAIMS.xlsx2.xlsx", sheet_name=None, header=None)

# نأخذ أول ورقة (بغض النظر عن اسمها)
first_sheet_name = list(df_raw.keys())[0]
df = df_raw[first_sheet_name]

# البحث عن الصف الذي يحتوي على "Date" و "code" و "Customer" إلخ
header_row = None
for i, row in df.iterrows():
    row_text = " ".join(row.astype(str).str.lower())
    if "date" in row_text and "code" in row_text and "customer" in row_text:
        header_row = i
        break

if header_row is None:
    st.error("لم نعثر على الصف المناسب. تأكد من وجود أعمدة مثل Date, code, Customer...")
    st.stop()

# تعيين العناوين والبيانات
columns = df.iloc[header_row].astype(str).str.strip().tolist()
data = df.iloc[header_row+1:].reset_index(drop=True)
data.columns = columns

# الأعمدة التي نريدها (بأسمائها الحقيقية)
needed = ["Date", "code", "Customer", "Claim statue", "Defect", "4M", "Statue", "Resp", "Dep code"]
for col in needed:
    if col not in data.columns:
        data[col] = ""

df_final = data[needed]

# تنظيف
df_final["Date"] = pd.to_datetime(df_final["Date"], errors="coerce").dt.date
df_final = df_final.fillna("").astype(str)

# مؤشرات
total = len(df_final)
ouvertes = len(df_final[df_final["Claim statue"].str.contains("Open", na=False)])

c1, c2 = st.columns(2)
c1.metric(" Total des réclamations", total)
c2.metric(" Ouvertes", ouvertes)

# جدول كامل
st.subheader("📄 Toutes les réclamations")
st.dataframe(df_final)
