import streamlit as st
import cv2
import numpy as np

# Бет баптаулары
st.set_page_config(page_title="Ақылды өсімдік мониторингі", page_icon="🌱", layout="centered")

st.title("🌱 Ақылды ауыл шаруашылығы")
st.caption("Өсімдік ауруларын суреттен танитын мониторинг жүйесі")

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
    
    # Түстік маскалар
    green_mask = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))
    yellow_mask = cv2.inRange(hsv, np.array([15, 40, 40]), np.array([35, 255, 255]))
    brown_mask = cv2.inRange(hsv, np.array([10, 40, 20]), np.array([20, 255, 200]))
    
    # Пикселдерді есептеу
    total_pixels = image.shape[0] * image.shape[1]
    green_pixels = cv2.countNonZero(green_mask)
    yellow_pixels = cv2.countNonZero(yellow_mask)
    brown_pixels = cv2.countNonZero(brown_mask)
    
    green_pct = (green_pixels / total_pixels) * 100
    yellow_pct = (yellow_pixels / total_pixels) * 100
    brown_pct = (brown_pixels / total_pixels) * 100
    other_pct = 100 - (green_pct + yellow_pct + brown_pct)
    
    # Суретті көрсету
    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Түпнұсқа сурет", use_container_width=True)
    
    # 1. ЖАЛПЫ КӨРСЕТКІШТЕР КЕСТЕСІ
    st.header("📊 Жалпы көрсеткіштер")
    st.table({
        "Көрсеткіш": ["Сау өсімдік (Жасыл)", "Ауру/Сарғайған (Сары)", "Құрғап қалған (Қоңыр)", "Қабырға/қоршаған орта"],
        "Мәні": [f"{green_pct:.2f}%", f"{yellow_pct:.2f}% ⚠️", f"{brown_pct:.2f}%", f"{other_pct:.2f}%"]
    })
    
    # 2. ДИАГНОСТИКА НӘТИЖЕСІ
    st.header("🔬 ТАМЫР ЭЛЕМЕНТТЕРІНІҢ ТАЛДАУЫ")
    
    st.subheader("1. ⚠️ АЗОТ (N) ЖЕТІСПЕУШІЛІГІ")
    st.table({
        "Параметр": ["Белгісі", "Себебі", "Шешімі"],
        "Ақпарат": [
            "Жапырақтары сарғыштап, төменнен жоғары қарай сарғыштау",
            "Азот — хлорофилл құрамына кіреді, жетіспегенде жапырақтар сарғыштап, өсуі баяулайды",
            "Аммиак селитрасы (аммоний нитраты), мочевина, құс пометы"
        ]
    })
    
    st.subheader("2. ⚠️ ТЕМІР (Fe) ЖЕТІСПЕУШІЛІГІ")
    st.table({
        "Параметр": ["Белгісі", "Себебі", "Шешімі"],
        "Ақпарат": [
            "Жас жапырақтар сарғыштап, тамырлары жасыл қалады",
            "Темір — хлорофилл синтезіне қатысады, жетіспегенде хлороз пайда болады",
            "Темір хелаты, темір сульфаты (жапыраққа шашырау)"
        ]
    })
    
    # ҚОРЫТЫНДЫ СТАТУС
    st.subheader("📝 Қорытынды")
    if yellow_pct > 10 or brown_pct > 5:
        st.error(f"🚨 **Статус: НАЗАР АУДАРЫҢЫЗ!**\nСарғыш/қуарған аймақтар **{yellow_pct + brown_pct:.2f}%** құрайды — бұл 10% шегінен асып кеткен. Өсімдікте негізгі элементтердің жетіспеушілігі анықталды.")
    else:
        st.success("✅ **Статус: ӨСІМДІК ЖАҒДАЙЫ ЖАҚСЫ.**")
        
    # 3. ҰСЫНЫСТАР КЕСТЕСІ
    st.header("💡 Ұсыныстар")
    st.table({
        "Қадам": ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"],
        "Әрекет": [
            "Азотты тыңайтқыш беріңіз — аммиак селитрасы немесе мочевина (1-2 г/л су)",
            "Темір хелатын шашырыңыз — жапыраққа 0,1% ерітінді (2 аптада 1 рет)",
            "Ылғалдылықты арттырыңыз — 60-80% ылғалдылықты қажет етеді",
            "Жапырақтарына шашыратыңыз — күніне 1-2 рет су шашырау",
            "Топырақты ауыстырыңыз — жаңа ылғал сақтайтын, қышқыл топырақ (pH 5.5-6.5)",
            "Құрғап қалған жапырақтарды кесіңіз — жаңа өсуге мүмкіндік беріңіз"
        ]
    })
