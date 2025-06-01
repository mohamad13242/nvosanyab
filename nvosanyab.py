
import streamlit as st
import pandas as pd
import datetime

# تنظیمات صفحه
st.set_page_config(
    page_title="نوسان‌یاب",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ظاهر تیره
primaryColor = "#0F1B2B"
backgroundColor = "#0A0F1A"
secondaryBackgroundColor = "#1E2C3A"
textColor = "#FAFAFA"
font = "sans serif"

# تیتر اپلیکیشن
st.markdown(f"""
    <style>
        .reportview-container {{
            background-color: {backgroundColor};
            color: {textColor};
        }}
        .sidebar .sidebar-content {{
            background-color: {secondaryBackgroundColor};
        }}
        .css-1d391kg, .css-1v3fvcr {{ color: {textColor} !important; }}
    </style>
    <h1 style='text-align: right; color: {textColor}; font-family: {font};'>
        📈 نوسان‌یاب – شناسایی سهم‌های مستعد رشد
    </h1>
""", unsafe_allow_html=True)

# بارگذاری فایل داده‌ها
uploaded_file = st.file_uploader("📥 فایل CSV معاملات روزانه را بارگذاری کنید", type=["csv"])
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()
        st.success("✅ فایل با موفقیت بارگذاری شد.")

        # پردازش داده‌ها: مثال ساده فیلتر حجم مشکوک
        df['change'] = df['close'] - df['open']
        suspicious_volume = df[(df['volume'] > 2 * df['avg_volume']) & (df['change'] > 0)]

        st.markdown("### 📊 سهم‌های مشکوک به ورود پول هوشمند:")
        st.dataframe(suspicious_volume[['symbol', 'name', 'close', 'volume', 'avg_volume', 'change']])

        # نمودار برای یک سهم خاص
        st.markdown("### 📌 نمودار قیمت یک سهم خاص")
        symbol = st.selectbox("🔍 انتخاب نماد:", df['symbol'].unique())
        symbol_data = df[df['symbol'] == symbol].sort_values(by='date')
        st.line_chart(symbol_data[['close']].reset_index(drop=True))

    except Exception as e:
        st.error(f"❌ خطا در پردازش فایل: {e}")
else:
    st.info("برای شروع، لطفاً فایل CSV روزانه بازار را بارگذاری کنید.")
