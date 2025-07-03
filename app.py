from PIL import Image
import streamlit as st
import os

types = ["各停", "準急", "急行", "回送"]
destinations = ["涼波", "宇土", "久保井公園", "行幸", "姫谷", "北姫谷", "月光台"]

type_selected = st.selectbox("種別を選択", types)
dest_selected = st.selectbox("行き先を選択", destinations)

type_image_path = f"方向幕/種別/{type_selected}.png"
dest_image_path = f"方向幕/行き先/{dest_selected}.png"

if os.path.exists(type_image_path) and os.path.exists(dest_image_path):
    img_type = Image.open(type_image_path)
    img_dest = Image.open(dest_image_path)
    
    # 高さを合わせるためリサイズ（種別画像の高さに行き先画像を合わせる）
    base_height = img_type.height
    ratio = base_height / img_dest.height
    new_width = int(img_dest.width * ratio)
    img_dest_resized = img_dest.resize((new_width, base_height))
    
    # 横幅合計
    total_width = img_type.width + img_dest_resized.width
    
    # 新規画像作成（横長）
    new_img = Image.new("RGBA", (total_width, base_height))
    
    # 2つの画像を並べて貼る
    new_img.paste(img_type, (0, 0))
    new_img.paste(img_dest_resized, (img_type.width, 0))
    
    # Streamlitに表示
    st.image(new_img)
else:
    if not os.path.exists(type_image_path):
        st.error(f"種別画像が見つかりません: {type_image_path}")
    if not os.path.exists(dest_image_path):
        st.error(f"行き先画像が見つかりません: {dest_image_path}")
