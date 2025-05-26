# Robby Azwan Saputra 
# 140810230008
# Website Color Picker Using Streamlit
import streamlit as st
from PIL import Image
from PIL import ImageDraw
import numpy as np
import json
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import io
from io import BytesIO

# Buat gambar palet horizontal
def generate_palette_image(hex_colors):
    block_size = 100
    img_width = block_size * len(hex_colors)
    img_height = 100
    img = Image.new("RGB", (img_width, img_height), color="white")
    draw = ImageDraw.Draw(img)

    for i, hex_color in enumerate(hex_colors):
        rgb = tuple(int(hex_color[j:j+2], 16) for j in (1, 3, 5))
        draw.rectangle(
            [i * block_size, 0, (i + 1) * block_size, img_height],
            fill=rgb
        )
    return img

st.set_page_config(page_title="Palette Color Picker", page_icon="❤️",layout="wide")

st.markdown(
    "<h1 style='text-align: center;'>Color Picker Website</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>Upload gambar Anda dan dapatkan 5 warna paling dominan dalam bentuk palet warna yang estetik.</p>",
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Silahkan upload file photo Anda di sini:", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    # Resize image untuk proses lebih cepat
    img = image.resize((150, 150))
    img_np = np.array(img)
    img_np = img_np.reshape((-1, 3))  # 2D array (pixel, warna)

    # KMeans untuk cari warna dominan
    kmeans = KMeans(n_clusters=5, random_state=42)
    kmeans.fit(img_np)
    colors = np.round(kmeans.cluster_centers_).astype(int)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## Photo yang Diupload")
    
        # Konversi gambar ke base64
        import base64
        from io import BytesIO

        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode()

        st.markdown(f"""
        <div style="width:100%; height:670px; overflow:hidden; border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,0.2);">
            <img src="data:image/png;base64,{img_b64}" style="width:100%; height:100%; object-fit:cover;"/>
        </div>
        """, unsafe_allow_html=True)


    with col2:
        st.markdown("## Representasi Pie Chart")
        labels = [f"Warna {i+1}" for i in range(5)]
        counts = np.bincount(kmeans.labels_)

        fig, ax = plt.subplots()
        ax.pie(
            counts,
            labels=labels,
            colors=[f'#{r:02x}{g:02x}{b:02x}' for r, g, b in colors],
            startangle=90,
            autopct='%1.1f%%'
        )
        ax.axis('equal')
        st.pyplot(fig)
    
    st.markdown(
    "<h1 style='text-align: center;'>5 Warna Paling Dominan</h1>",
    unsafe_allow_html=True
)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        hex_color = '#%02x%02x%02x' % tuple(colors[i])
        col.markdown(
        f"<div style='background-color:{hex_color}; height:120px; border-radius:10px;'></div><br><center><code>{hex_color}</code></center>",
        unsafe_allow_html=True
        )
    
    # Data palet dalam format HEX
    hex_colors = [f'#{r:02x}{g:02x}{b:02x}' for r, g, b in colors]

    # TXT content
    palette_txt = "\n".join([f"Warna {i+1}: {hex}" for i, hex in enumerate(hex_colors)])

    # JSON content
    palette_json = json.dumps({"palette": hex_colors}, indent=2)

    palette_img = generate_palette_image(hex_colors)
    
    img_bytes = BytesIO()
    palette_img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    st.markdown(
    "<h1 style='text-align: center; margin-top: 10px;'>Download Palet Anda</h1>",
    unsafe_allow_html=True
)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            label="⬇️ Download .TXT",
            data=palette_txt,
            file_name="palet_warna.txt",
            mime="text/plain"
        )

    with col2:
        st.download_button(
            label="⬇️ Download .JSON",
            data=palette_json,
            file_name="palet_warna.json",
            mime="application/json"
        )

    with col3:
        st.download_button(
            label="⬇️ Download Gambar",
            data=img_bytes,
            file_name="palet_warna.png",
            mime="image/png"
        )

else:
    st.info("Silakan upload foto Anda terlebih dahulu untuk memulai proses.")

st.markdown(
    """
    <hr style="margin-top: 50px; border: 1px solid #eee;" />
    <div style="text-align: center; font-size: 14px; color: gray; padding: 10px 0;">
        Made by <strong>Robby - 230008</strong> | &copy; All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)