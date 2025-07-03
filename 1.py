import streamlit as st
import random

# 词库示例
word_pairs = [
    ("苹果", "apple"),
    ("香蕉", "banana"),
    ("橙子", "orange"),
    ("猫", "cat"),
    ("狗", "dog"),
    ("书", "book"),
    ("桌子", "table"),
    ("椅子", "chair"),
]

# 初始化 session_state
if 'remaining_pairs' not in st.session_state:
    st.session_state.remaining_pairs = word_pairs.copy()
    st.session_state.selected_cn = None
    st.session_state.selected_en = None
    st.session_state.matched = []
    # 打乱顺序
    st.session_state.cn_list = [cn for cn, en in word_pairs]
    st.session_state.en_list = [en for cn, en in word_pairs]
    random.shuffle(st.session_state.cn_list)
    random.shuffle(st.session_state.en_list)

st.title("英语单词消消乐：中英文配对")
st.write("点击一个中文，再点击一个英文，配对成功即可消除！")

# 选中提示
selected_cn = st.session_state.selected_cn
selected_en = st.session_state.selected_en

# 选择中文
st.subheader("选择中文：")
cols_cn = st.columns(4)
for i, cn in enumerate(st.session_state.cn_list):
    if cn not in [pair[0] for pair in st.session_state.matched]:
        button_style = (
            "background-color:#ffd700; color:black; font-weight:bold;" if selected_cn == cn else ""
        )
        if cols_cn[i % 4].button(cn, key=f"cn_{cn}", help="点击选择中文单词"):
            st.session_state.selected_cn = cn
        # 高亮选中
        if selected_cn == cn:
            cols_cn[i % 4].markdown(f"<div style='text-align:center; color:#ffd700;'>已选中</div>", unsafe_allow_html=True)

# 选择英文
st.subheader("选择英文：")
cols_en = st.columns(4)
for i, en in enumerate(st.session_state.en_list):
    if en not in [pair[1] for pair in st.session_state.matched]:
        button_style = (
            "background-color:#87ceeb; color:black; font-weight:bold;" if selected_en == en else ""
        )
        if cols_en[i % 4].button(en, key=f"en_{en}", help="点击选择英文单词"):
            st.session_state.selected_en = en
        # 高亮选中
        if selected_en == en:
            cols_en[i % 4].markdown(f"<div style='text-align:center; color:#87ceeb;'>已选中</div>", unsafe_allow_html=True)

# 判断配对
if st.session_state.selected_cn and st.session_state.selected_en:
    pair = (st.session_state.selected_cn, st.session_state.selected_en)
    if pair in word_pairs:
        st.success(f"配对成功：{pair[0]} - {pair[1]}")
        st.session_state.matched.append(pair)
        # 重置选择
        st.session_state.selected_cn = None
        st.session_state.selected_en = None
    else:
        st.error("配对错误，请重新选择！")
        st.session_state.selected_cn = None
        st.session_state.selected_en = None

# 游戏结束
if len(st.session_state.matched) == len(word_pairs):
    st.balloons()
    st.success("恭喜你，全部配对成功！")
    if st.button("再来一局"):
        st.session_state.clear()
        st.rerun() 