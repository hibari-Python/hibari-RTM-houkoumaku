from PIL import Image
import streamlit as st
import os
import time

base_dir = os.path.dirname(os.path.abspath(__file__))

types = ["各停", "準急", "急行", "回送", "nothing"]
destinations = ["涼波", "宇土", "久保井公園", "行幸", "姫谷", "北姫谷", "月光台", "nothing"]
houmen = ["なし", "行幸方面"]  # 方面は2つだけ

type_selected = st.selectbox("種別を選択", types)
dest_selected = st.selectbox("行き先を選択", destinations)
houmen_selected = st.selectbox("方面を選択", houmen)
switch_interval = st.number_input("切り替え秒数（秒）", min_value=1, max_value=10, value=3)

image_area = st.empty()

if houmen_selected == "なし":
    # 方面なしなら固定表示
    type_image_path = os.path.join(base_dir, "方向幕", "種別", f"{type_selected}.png")
    dest_image_path = os.path.join(base_dir, "方向幕", "行き先", f"{dest_selected}.png")

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
        image_area.image(new_img)
    else:
        st.error("画像が見つかりません。")
else:
    # 行幸方面選択時は交互表示
    while True:
        # ① 種別＋行き先表示
        type_image_path = os.path.join(base_dir, "方向幕", "種別", f"{type_selected}.png")
        dest_image_path = os.path.join(base_dir, "方向幕", "行き先", f"{dest_selected}.png")
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
            image_area.image(new_img)
        time.sleep(switch_interval)

        # ② nothing（種別）＋ 行幸方面（方面）
        type_image_path = os.path.join(base_dir, "方向幕", "種別", "nothing.png")
        houmen_image_path = os.path.join(base_dir, "方向幕", "行き先", "行幸方面.png")
        if os.path.exists(type_image_path) and os.path.exists(houmen_image_path):
            img_type = Image.open(type_image_path)
            img_dest = Image.open(houmen_image_path)
            base_height = img_type.height
            ratio = base_height / img_dest.height
            new_width = int(img_dest.width * ratio)
            img_dest_resized = img_dest.resize((new_width, base_height))
            total_width = img_type.width + img_dest_resized.width
            new_img = Image.new("RGBA", (total_width, base_height))
            new_img.paste(img_type, (0, 0))
            new_img.paste(img_dest_resized, (img_type.width, 0))
            image_area.image(new_img)
        time.sleep(switch_interval)
