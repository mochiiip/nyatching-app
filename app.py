import streamlit as st
import pandas as pd

# --- データ読み込み ---
cats = pd.read_csv("cats_info.csv")

st.title("🐾 Nyatching")
st.write("運命の保護猫を見つけよう")

# --- ユーザー条件 ---
st.sidebar.header("あなたの希望")

want_friendly = st.sidebar.checkbox("人慣れしてる猫がいい")
want_kids_ok = st.sidebar.checkbox("子どもOK")
want_other_cats_ok = st.sidebar.checkbox("先住猫OK")
want_alone_ok = st.sidebar.checkbox("お留守番OK")
want_fiv_negative = st.sidebar.checkbox("FIV陰性のみ")

# --- マッチスコア計算 ---
def calculate_score(cat):
    score = 0
    total = 5

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

    return score, total


scores = cats.apply(lambda row: calculate_score(row), axis=1)
cats["match_score"] = scores.apply(lambda x: x[0])
cats["match_percent"] = scores.apply(lambda x: int((x[0] / x[1]) * 100))

cats_sorted = cats.sort_values(by="match_score", ascending=False).reset_index(drop=True)

# --- セッション状態 ---
if "cat_index" not in st.session_state:
    st.session_state.cat_index = 0

if "likes" not in st.session_state:
    st.session_state.likes = []

# --- 猫表示 ---
if st.session_state.cat_index < len(cats_sorted):

    cat = cats_sorted.iloc[st.session_state.cat_index]

    st.subheader(cat["name"])

    st.image("images/" + cat["image"], width=350)

    st.write("年齢:", cat["age"])
    st.write("性別:", cat["gender"])

    st.write("マッチ度")
    st.progress(cat["match_percent"] / 100)
    st.write(f"{cat['match_percent']} %")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💚 気になる"):
            st.session_state.likes.append(cat)
            st.session_state.cat_index += 1
            st.rerun()

    with col2:
        if st.button("⏭ スキップ"):
            st.session_state.cat_index += 1
            st.rerun()

# --- 結果表示 ---
else:

    st.header("あなたが気になった猫")

    if len(st.session_state.likes) == 0:
        st.write("まだ気になる猫はありません")

    else:
        for cat in st.session_state.likes:

            st.subheader(cat["name"])

            col1, col2 = st.columns([1,2])

            with col1:
                st.image("images/" + cat["image"], width=200)

            with col2:
                st.write("年齢:", cat["age"])
                st.write("性別:", cat["gender"])

                st.write("マッチ度")
                st.progress(cat["match_percent"] / 100)
                st.write(f"{cat['match_percent']} %")

            st.divider()
