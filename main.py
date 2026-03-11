import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Tải cấu hình từ .env
load_dotenv()

# Thiết lập cấu hình trang
st.set_page_config(page_title="FPT AI Text-to-Speech", page_icon="🎙️")

st.title("🎙️ Chuyển đổi Văn bản thành Giọng nói")
st.markdown("Chào Việt, hãy nhập nội dung bạn muốn chuyển đổi bên dưới.")

# Khởi tạo OpenAI Client
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    st.error("Thiếu API_KEY! Việt vui lòng kiểm tra lại file .env.")
    st.stop()

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# --- Giao diện bên trái (Sidebar) ---
with st.sidebar:
    st.header("Cấu hình giọng đọc")
    
    VOICE_OPTIONS = {
        "std_leminh": "Le Minh (Male / North)",
        "std_kimngan": "Kim Ngan (Female / South)",
        "std_banmai": "Ban Mai (Female / North)",
        "std_hatieumai": "Ha Tieu Mai (Female / South)",
        "std_ngoclam": "Ngoc Lam (Female / Center)",
        "std_thuminh": "Thu Minh (Female / North)",
        "std_giahuy": "Gia Huy (Male / South)",
        "std_huyphong": "Huy Phong (Male / North)",
        "std_minhquan": "Minh Quan (Male / North)",
    }
    
    # Chọn giọng đọc dựa trên tên hiển thị
    voice_label = st.selectbox("Chọn giọng đọc:", options=list(VOICE_OPTIONS.values()))
    voice_id = [k for k, v in VOICE_OPTIONS.items() if v == voice_label][0]
    
    # Chọn tốc độ
    speech_speed = st.slider("Tốc độ nói:", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

# --- Giao diện chính ---
input_text = st.text_area("Nhập văn bản tiếng Việt:", placeholder="Xin chào Việt, bạn muốn tôi nói gì hôm nay?", height=200)

if st.button("Tạo giọng nói"):
    if not input_text.strip():
        st.warning("Việt ơi, bạn chưa nhập văn bản kìa!")
    else:
        with st.spinner("Đang xử lý âm thanh..."):
            try:
                # Gọi API
                response = client.audio.speech.create(
                    model="FPT.AI-VITs",
                    input=input_text,
                    response_format='wav',
                    voice=voice_id,
                    speed=str(speech_speed),
                )
                
                # Lưu file tạm để phát lại
                output_path = "output_speech.wav"
                response.write_to_file(output_path)
                
                # Hiển thị trình phát nhạc và nút tải về
                st.success("Đã tạo xong!")
                st.audio(output_path, format="audio/wav")
                
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="Tải file .wav về máy",
                        data=file,
                        file_name="speech_fpt.wav",
                        mime="audio/wav"
                    )
            except Exception as e:
                st.error(f"Có lỗi xảy ra rồi: {e}")

st.divider()
st.caption("Ứng dụng chạy trên nền tảng Windows - Hệ điều hành yêu thích (hoặc hay bị đổ lỗi) của Việt.")