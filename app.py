import streamlit as st
import pandas as pd

st.title("ニャッチング診断")

cats = pd.read_csv("cats_info.csv")

for _, cat in cats.iterrows():
    st.subheader(cat["name"])

    st.image("images/" + cat["image"], width=300)

    st.write("年齢:", cat["age"])
    st.write("性別:", cat["sex"])
    st.write("性格:", cat["personality"])
    st.write("人慣れ:", cat["friendly"])
    st.write("お留守番OK:", cat["alone_ok"])
    st.write("子どもOK:", cat["kids_ok"])
    st.write("他の猫OK:", cat["other_cats_ok"])
    st.write("猫エイズ:", cat["is_fiv_positive"])

    st.divider()
