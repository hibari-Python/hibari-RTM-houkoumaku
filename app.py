from PIL import Image
import streamlit as st
import os

types = ["各停", "準急", "急行", "回送"]
destinations = ["涼波", "宇土", "久保井公園", "行幸", "姫谷", "北姫谷", "月光台", "nothing"]

type_selected = st.selectbox("種別を選択", types)
dest_selected = st.selectbox("行き先を選択", destinations)

if type_selected == "回送":
    type_image_path = "方向幕/種別/nothing.png"
    dest_image_path = "方向幕/行き先/nothing.png"
else:
    type_image_path = f"方向幕/種別/{type_selected}.png"
    if dest_selected == "nothing":
        dest_image_path = "方向幕/行き先/nothing.png"
    else:
        dest_image_path = f"方向幕/行き先/{dest_selected}.png"

if os.path.exists(type_image_path) and os.path.exists(dest_image_path):
    img_type = Image.open(type_image_path)
    img_dest = Image.open(dest_image_path)
    
    base_height = img_type.height
    ratio = base_height / img_dest.height
    new_width = int(img_dest.width * ratio)
    img_dest_resized = img_dest.resize((new_width, base_height))

    total_width = img_type.width + img_dest_resized.width
    new_img = Image.new("RGBA", (total_width, base_height))

    new_img.paste(img_type, (0, 0))
    new_img.paste(img_dest_resized, (img_type.width, 0))

    st.image(new_img)
else:
    if not os.path.exists(type_image_path):
        st.error(f"種別画像が見つかりません: {type_image_path}")
    if not os.path.exists(dest_image_path):
        st.error(f"行き先画像が見つかりません: {dest_image_path}")
