import cv2
import streamlit as st
from PIL import Image
import time
from util import get_limits  

target_color = [42, 42, 165]

st.title("Deteksi Warna Real-Time")

# Tombol untuk menghentikan stream
if 'run' not in st.session_state:
    st.session_state.run = True

def stop_stream():
    st.session_state.run = False

st.sidebar.button("Stop Stream", on_click=stop_stream)

# Placeholder untuk menampilkan frame video
frame_placeholder = st.empty()

# Inisialisasi kamera
cap = cv2.VideoCapture(0)

# Perulangan untuk membaca dan menampilkan frame secara real-time
while st.session_state.run:
    ret, frame = cap.read()
    if not ret:
        st.error("Gagal mengambil frame dari kamera.")
        break

    # Ubah frame dari BGR ke HSV
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Dapatkan batas bawah dan atas berdasarkan warna target
    lower_limit, upper_limit = get_limits(color=target_color)

    # Buat mask untuk mendeteksi warna target
    mask = cv2.inRange(hsv_image, lower_limit, upper_limit)

    # Mengubah mask ke PIL image untuk mendapatkan bounding box
    mask_pil = Image.fromarray(mask)
    bbox = mask_pil.getbbox()

    # Jika bounding box terdeteksi, gambar kotak di sekeliling objek
    if bbox is not None:
        x1, y1, x2, y2 = bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    # Konversi frame ke RGB untuk ditampilkan di Streamlit
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_placeholder.image(frame_rgb, channels="RGB")

    # Delay kecil untuk memberi waktu pembaruan frame
    time.sleep(0.03)

cap.release()
st.write("Stream video telah dihentikan.")