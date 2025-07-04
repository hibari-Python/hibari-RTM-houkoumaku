from PIL import Image
import streamlit as st
import os
import time

base_dir = os.path.dirname(os.path.abspath(__file__))

types = ["各停", "準急", "急行", "回送", "nothing"]
destinations = ["涼波", "宇土", "久保井公園", "行幸", "姫谷", "北姫谷", "月光台", "nothing"]
houmen = ["なし", "行幸方面"]  # 方面は2つだけ

type_selected = st.selectbox("種別を選択", types)
houmen_selected = st.selectbox("方面を選択", houmen)

# 回送のときは行き先は nothing に固定、方面はなしに固定
if type_selected == "回送":
    dest_selected = "nothing"
    houmen_selected = "なし"
else:
    dest_selected = st.selectbox("行き先を選択", destinations)

switch_interval = st.number_input("切り替え秒数（秒）", min_value=1, max_value=10, value=3)

image_area = st.empty()

def load_and_combine_images(type_img_name, dest_img_name):
    type_image_path = os.path.join(base_dir, "方向幕", "種別", f"{type_img_name}.png")
    dest_image_path = os.path.join(base_dir, "方向幕", "行き先", f"{dest_img_name}.png")
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
        return new_img
    else:
        missing = []
        if not os.path.exists(type_image_path):
            missing.append(f"種別画像が見つかりません: {type_image_path}")
        if not os.path.exists(dest_image_path):
            missing.append(f"行き先画像が見つかりません: {dest_image_path}")
        for msg in missing:
            st.error(msg)
        return None

if houmen_selected == "なし":
    # 方面なしなら固定表示
    combined_img = load_and_combine_images(type_selected, dest_selected)
    if combined_img:
        image_area.image(combined_img)
else:
    # 方面ありは交互表示
    while True:
        # 種別＋行き先表示
        combined_img = load_and_combine_images(type_selected, dest_selected)
        if combined_img:
            image_area.image(combined_img)
        time.sleep(switch_interval)

        # nothing（種別）＋ 方面表示
        combined_img = load_and_combine_images("nothing", houmen_selected)
        if combined_img:
            image_area.image(combined_img)
        time.sleep(switch_interval)
