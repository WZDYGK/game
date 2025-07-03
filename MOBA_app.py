import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import random

st.set_page_config(page_title="2D 单人枪战游戏", layout="centered")
st.title("2D 单人枪战游戏 Demo")

# 游戏参数
game_width = 600
game_height = 400
player_size = 30
enemy_size = 30
bullet_size = 8
player_speed = 20
enemy_speed = 8
bullet_speed = 30

# 辅助函数：画圆
def cv2_circle(img, center, radius, color):
    cx, cy = center
    for x in range(cx-radius, cx+radius+1):
        for y in range(cy-radius, cy+radius+1):
            if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
                if (x-cx)**2 + (y-cy)**2 <= radius**2:
                    img[y, x] = color
    return img

# 初始化session_state
def init_state():
    if "player_pos" not in st.session_state:
        st.session_state.player_pos = [game_width // 2, game_height - 50]
    if "enemy_pos" not in st.session_state:
        st.session_state.enemy_pos = [random.randint(50, game_width-50), 50]
    if "bullets" not in st.session_state:
        st.session_state.bullets = []  # [(x, y)]
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "game_over" not in st.session_state:
        st.session_state.game_over = False

init_state()

# 玩家移动按钮
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("⬅️ 左移"):
        st.session_state.player_pos[0] = max(player_size//2, st.session_state.player_pos[0] - player_speed)
with col2:
    if st.button("⬆️ 上移"):
        st.session_state.player_pos[1] = max(player_size//2, st.session_state.player_pos[1] - player_speed)
with col3:
    if st.button("➡️ 右移"):
        st.session_state.player_pos[0] = min(game_width-player_size//2, st.session_state.player_pos[0] + player_speed)
col4, col5, col6 = st.columns([1,1,1])
with col5:
    if st.button("⬇️ 下移"):
        st.session_state.player_pos[1] = min(game_height-player_size//2, st.session_state.player_pos[1] + player_speed)

# 射击
st.write("点击下方画布射击！")

# 画布
canvas_result = st_canvas(
    fill_color="#00000000",
    stroke_width=1,
    background_color="#222",
    update_streamlit=True,
    height=game_height,
    width=game_width,
    drawing_mode="point",
    key="canvas",
)

# 处理射击
if canvas_result.json_data is not None and len(canvas_result.json_data["objects"]) > 0:
    last_obj = canvas_result.json_data["objects"][-1]
    if last_obj["type"] == "circle":
        # 新子弹
        bx, by = int(last_obj["left"]), int(last_obj["top"])
        px, py = st.session_state.player_pos
        dx, dy = bx - px, by - py
        norm = np.hypot(dx, dy)
        if norm == 0:
            norm = 1
        dx, dy = dx / norm, dy / norm
        st.session_state.bullets.append({
            "pos": [px, py],
            "dir": [dx, dy]
        })
    # 清空画布
    canvas_result.json_data["objects"].clear()

# 更新子弹位置
new_bullets = []
for bullet in st.session_state.bullets:
    bx, by = bullet["pos"]
    dx, dy = bullet["dir"]
    bx += int(dx * bullet_speed)
    by += int(dy * bullet_speed)
    # 子弹出界
    if 0 < bx < game_width and 0 < by < game_height:
        bullet["pos"] = [bx, by]
        new_bullets.append(bullet)
st.session_state.bullets = new_bullets

# 敌人AI：简单追踪玩家
ex, ey = st.session_state.enemy_pos
px, py = st.session_state.player_pos
dx, dy = px - ex, py - ey
norm = np.hypot(dx, dy)
if norm != 0:
    dx, dy = dx / norm, dy / norm
    ex += int(dx * enemy_speed)
    ey += int(dy * enemy_speed)
st.session_state.enemy_pos = [ex, ey]

# 检查碰撞（子弹打中敌人）
new_bullets = []
enemy_hit = False
for bullet in st.session_state.bullets:
    bx, by = bullet["pos"]
    if abs(bx - ex) < (enemy_size//2) and abs(by - ey) < (enemy_size//2):
        st.session_state.score += 1
        enemy_hit = True
    else:
        new_bullets.append(bullet)
st.session_state.bullets = new_bullets
if enemy_hit:
    # 敌人重生
    st.session_state.enemy_pos = [random.randint(50, game_width-50), 50]

# 检查玩家被敌人碰到
if abs(px - ex) < (player_size//2 + enemy_size//2) and abs(py - ey) < (player_size//2 + enemy_size//2):
    st.session_state.game_over = True

# 绘制所有元素
canvas_data = np.zeros((game_height, game_width, 3), dtype=np.uint8)
# 玩家
cv_px, cv_py = st.session_state.player_pos
canvas_data = cv2_circle(canvas_data, (cv_px, cv_py), player_size//2, (0,255,0))
# 敌人
cv_ex, cv_ey = st.session_state.enemy_pos
canvas_data = cv2_circle(canvas_data, (cv_ex, cv_ey), enemy_size//2, (255,0,0))
# 子弹
for bullet in st.session_state.bullets:
    bx, by = bullet["pos"]
    canvas_data = cv2_circle(canvas_data, (bx, by), bullet_size//2, (255,255,0))

st.image(canvas_data, channels="RGB")

# 分数和游戏结束
st.markdown(f"**分数：{st.session_state.score}**")
if st.session_state.game_over:
    st.error("游戏结束！你被敌人抓住了。点击下方按钮重新开始。")
    if st.button("重新开始"):
        for key in ["player_pos", "enemy_pos", "bullets", "score", "game_over"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun() 