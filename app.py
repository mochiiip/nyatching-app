import streamlit as st
import pandas as pd

cats = pd.read_csv("cats_info.csv")

st.title("🐾 Nyatching")
st.write("運命の保護猫を見つけよう")

# --- 性別日本語変換 ---
def gender_jp(g):
    if g == "female":
        return "女の子"
    elif g == "male":
        return "男の子"
    return g


# --- セッション ---
if "step" not in st.session_state:
    st.session_state.step = "diagnosis"

if "cat_index" not in st.session_state:
    st.session_state.cat_index = 0

if "likes" not in st.session_state:
    st.session_state.likes = []


# =====================
# 診断画面
# =====================

if st.session_state.step == "diagnosis":

    st.header("あなたの希望を教えてください")

    want_friendly = st.checkbox("人慣れしている猫がいい")
    want_kids_ok = st.checkbox("子どもOK")
    want_other_cats_ok = st.checkbox("先住猫OK")
    want_alone_ok = st.checkbox("お留守番OK")
    want_fiv_negative = st.checkbox("FIV陰性のみ")

    if st.button("おすすめの猫を見る"):

        st.session_state.prefs = {
            "friendly": want_friendly,
            "kids_ok": want_kids_ok,
            "other_cats_ok": want_other_cats_ok,
            "alone_ok": want_alone_ok,
            "fiv_negative": want_fiv_negative
        }

        st.session_state.step = "matching"
        st.rerun()


# =====================
# マッチング処理
# =====================

if st.session_state.step == "matching":

    prefs = st.session_state.prefs

    def calculate_score(cat):

        score = 0
        total = 5

        if prefs["friendly"] and cat["friendly"] == "yes":
            score += 1

        if prefs["kids_ok"] and cat["kids_ok"] == "yes":
            score += 1

        if prefs["other_cats_ok"] and cat["other_cats_ok"] == "yes":
            score += 1

        if prefs["alone_ok"] and cat["alone_ok"] == "yes":
            score += 1

        if prefs["fiv_negative"] and cat["is_fiv_positive"] == False:
            score += 1

        return score, total


    scores = cats.apply(lambda row: calculate_score(row), axis=1)

    cats["match_score"] = scores.apply(lambda x: x[0])
    cats["match_percent"] = scores.apply(lambda x: int((x[0] / x[1]) * 100))

    cats_sorted = cats.sort_values(by="match_score", ascending=False).reset_index(drop=True)


    # =====================
    # 猫表示
    # =====================

    if st.session_state.cat_index < len(cats_sorted):

        cat = cats_sorted.iloc[st.session_state.cat_index]

        st.subheader(cat["name"])

        st.image("images/" + cat["image"], use_container_width=True)

        st.write("年齢:", cat["age"])
        st.write("性別:", gender_jp(cat["gender"]))

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

    # =====================
    # 結果
    # =====================

    else:

        st.header("気になった猫")

        if len(st.session_state.likes) == 0:
            st.write("まだ気になる猫はいません")

        else:

            for cat in st.session_state.likes:

                st.subheader(cat["name"])

                st.image("images/" + cat["image"], width=250)

                st.write("年齢:", cat["age"])
                st.write("性別:", gender_jp(cat["gender"]))

                st.progress(cat["match_percent"] / 100)
                st.write(f"マッチ度 {cat['match_percent']} %")

                st.divider()
