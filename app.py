import streamlit as st 
from PIL import Image 
from utils.face_processor import process_face_image
from utils.ai_analyzer import analizer_report


st.set_page_config(
    page_title="AI Face Analyzer",
    page_icon="📷",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* مخفی کردن منوی پیش‌فرض استریم‌لیت و فوتر */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* استایل کلی پس‌زمینه */
    .main {
        background-color: #f8f9fa;
    }
    
    /* سفارشی‌سازی دکمه‌ها */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        background-color: #2563eb;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    </style>
    """, unsafe_allow_html=True
)
with st.sidebar:
    st.markdown("### ℹ️ درباره پروژه")
    st.info(
        "این اپلیکیشن یک نسخه اولیه (MVP) هوشمند برای پردازش تصویر، تشخیص چهره و ارائه گزارش‌های مراقبتی با استفاده از هوش مصنوعی است."
    )
    st.markdown("---")
    st.markdown("🛠️ **تکنولوژی‌ها:**")
    st.markdown("- Python & Streamlit\n- OpenCV & NumPy\n- Groq API (LLM)")
    st.markdown("---")
    st.markdown("👨‍💻 **وضعیت:** نسخه ۱.۰ (MVP)")

# هدر اصلی زیبا با تراز وسط
st.markdown("<h1 style='text-align: center; color: #0f172a;'>🔍 تحلیل‌گر هوشمند چهره</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 1.1rem;'>سیستم هوشمند پردازش تصویر، تشخیص چهره و تولید گزارش تخصصی پوست و ظاهر</p>", unsafe_allow_html=True)
st.markdown("---")

# کادر آپلود تصویر داخل یک کارت شیک
with st.container(border=True):
    st.markdown("### 📸 بارگذاری تصویر")
    uploaded_file = st.file_uploader(
        "یک تصویر واضح از صورت خود انتخاب کنید (فرمت‌های JPG، PNG)", 
        type=["jpg", "jpeg", "png"]
    )

if uploaded_file is not None:
    image_bytes = uploaded_file.getvalue()
    
    # استفاده از دو ستون برای نمایش عکس اصلی و نتیجه پردازش کنار هم
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("#### تصویر آپلود شده")
            st.image(uploaded_file, use_container_width=True)
    
    with st.spinner("⏳ در حال پردازش تصویر و تشخیص چهره..."):
        success, message, processed_img = process_face_image(image_bytes)
        
    if success:
        with col2:
            with st.container(border=True):
                st.markdown("#### نتیجه پردازش (Face Mesh/Box)")
                st.image(processed_img, use_container_width=True)
        
        st.success(message)
        
        # بخش گزارش هوش مصنوعی در یک کارت جذاب
        with st.spinner("🤖 در حال آماده‌سازی گزارش تخصصی هوش مصنوعی..."):
            ai_success, ai_report = analizer_report()
            
        if ai_success:
            st.markdown("---")
            with st.container(border=True):
                st.markdown("### 📋 گزارش تحلیل هوشمند چهره")
                st.markdown(ai_report)
        else:
            st.error(ai_report)
    else:
        st.error(message)