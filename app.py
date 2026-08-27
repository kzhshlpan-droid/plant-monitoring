import streamlit as st
import cv2
import numpy as np

# Бет баптаулары
st.set_page_config(page_title="Ақылды өсімдік мониторингі", page_icon="🌱", layout="centered")

st.title("🌱 Ақылды ауыл шаруашылығы")
st.subtitle("Өсімдік ауруларын суреттен танитын мониторинг жүйесі")

uploaded_file = st.file_uploader("Өсімдік жапырағының суретін жүктеңіз...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Суретті оқу
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    
    # Өлшемін 600px өзгерту
    height, width, _ = image.shape
    aspect_ratio = width / height
    new_width = 600
    new_height = int(new_width / aspect_ratio)
    image = cv2.resize(image, (new_width, new_height))
    
    # HSV түс моделіне өту
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Маскалар (Жасыл - сау, Сары - ауру)
    green_mask = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))
    yellow_mask = cv2.inRange(hsv, np.array([15, 40, 40]), np.array([35, 255, 255]))
    
    # Пикселдерді есептеу
    total_pixels = image.shape[0] * image.shape[1]
    green_pixels = cv2.countNonZero(green_mask)
    yellow_pixels = cv2.countNonZero(yellow_mask)
    
    green_pct = (green_pixels / total_pixels) * 100
    yellow_pct = (yellow_pixels / total_pixels) * 100
    
    # Түпнұсқа суретті шығару
    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Түпнұсқа сурет", use_column_width=True)
    
    # Көрсеткіштер
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Сау аймақ (Жасыл)", value=f"{green_pct:.2f}%")
    with col2:
        st.metric(label="Ауру аймақ (Сары)", value=f"{yellow_pct:.2f}%")
    
    # Статус беру
    if yellow_pct > 10:
        st.error("🚨 **Статус:** НАЗАР АУДАРЫҢЫЗ! Ауру немесе ылғал жетіспеушілігі бар.")
    else:
        st.success("✅ **Статус:** ӨСІМДІК ЖАҒДАЙЫ ЖАҚСЫ.")

# 2. Server-ге қажетті кітапханалар тізімін сақтау
%%writefile requirements.txt
streamlit
opencv-python-headless
numpy
