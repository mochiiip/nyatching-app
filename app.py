import streamlit as st
import pandas as pd

st.title("ニャッチング診断")

cats = pd.read_csv("cats_info.csv")

for _, cat in cats.iterrows():
    st.subheader(cat["name"])

    st.image("images/" + cat["image"], width=300)

    st.write("年齢:", cat["age"])
    st.write("性別:", cat["gender"])
    st.write("人慣れ:", cat["friendly"])
    st.write("お留守番OK:", cat["alone_ok"])
    st.write("子どもOK:", cat["kids_ok"])
    st.write("他の猫OK:", cat["other_cats_ok"])
    st.write("猫エイズ:", cat["is_fiv_positive"])

    st.divider()

import streamlit as st
import pandas as pd

# データ読み込み
cats = pd.read_csv("cats_info.csv")

st.title("🐾 Nyatching")
st.write("運命の保護猫を見つけよう")

# --- ユーザー条件入力 ---
st.sidebar.header("あなたの希望")

want_friendly = st.sidebar.checkbox("人慣れしてる子がいい")
want_kids_ok = st.sidebar.checkbox("子どもOK")
want_other_cats_ok = st.sidebar.checkbox("先住猫OK")
want_alone_ok = st.sidebar.checkbox("お留守番OK")
want_fiv_negative = st.sidebar.checkbox("FIV陰性のみ")

# --- マッチスコア関数 ---
def calculate_score(cat):

    score = 0

    if want_friendly and cat["friendly"] == "yes":
        score += 1

    if want_kids_ok and cat["kids_ok"] == "yes":
        score += 1

    if want_other_cats_ok and cat["other_cats_ok"] == "yes":
        score += 1

    if want_alone_ok and cat["alone_ok"] == "yes":
        score += 1

    if want_fiv_negative and cat["is_fiv_positive"] == False:
        score += 1

    return score


# --- スコア計算 ---
cats["match_score"] = cats.apply(calculate_score, axis=1)

# --- スコア順並び替え ---
cats_sorted = cats.sort_values(by="match_score", ascending=False)

st.header("あなたに合う猫")

# --- 猫表示 ---
for _, cat in cats_sorted.iterrows():

    st.subheader(cat["name"])

    col1, col2 = st.columns([1,2])

    with col1:
        st.image("images/" + cat["image"], width=250)

    with col2:
        st.write("年齢:", cat["age"])
        st.write("性別:", cat["gender"])
        st.write("マッチ度:", cat["match_score"])

        if st.button(f"{cat['name']} をお気に入り"):
            st.success("お気に入りに追加しました")

    st.divider()
