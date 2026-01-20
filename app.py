import streamlit as st
import math

# 設定網頁標題
st.set_page_config(page_title="IPF GL 計算器", page_icon="🏋️‍♂️")

st.title("🏋️‍♂️ IPF GL 係數計算器")
st.write("輸入你的體重與成績，自動計算 IPF GL 分數")

# --- 1. 定義係數資料 (Python 字典格式) ---
COEFFICIENTS = {
    "Female": {
        "Raw": {"A": 610.32796, "B": 1045.59282, "C": 0.0304889},
        "Equipped": {"A": 758.63878, "B": 949.31382, "C": 0.0243547}
    },
    "Male": {
        "Raw": {"A": 1199.72839, "B": 1030.90069, "C": 0.0092155},
        "Equipped": {"A": 1236.61249, "B": 990.26461, "C": 0.0118756}
    }
}

# --- 2. 建立輸入介面 ---
col1, col2 = st.columns(2)
with col1:
    gender = st.radio("性別", ["Female", "Male"], index=0, format_func=lambda x: "女生" if x == "Female" else "男生")
with col2:
    equipment = st.radio("裝備", ["Raw", "Equipped"], index=0, format_func=lambda x: "無裝備 (Raw)" if x == "Raw" else "有裝備")

unit = st.radio("單位", ["kg", "lbs"], horizontal=True)

bodyweight = st.number_input("體重 (Bodyweight)", min_value=0.0, step=0.1, format="%.1f")

st.subheader("三項成績 (輸入 0 代表沒測)")
c1, c2, c3 = st.columns(3)
with c1:
    squat = st.number_input("深蹲 (Squat)", min_value=0.0, step=0.5)
with c2:
    bench = st.number_input("臥推 (Bench)", min_value=0.0, step=0.5)
with c3:
    deadlift = st.number_input("硬舉 (Deadlift)", min_value=0.0, step=0.5)

# --- 3. 計算邏輯函數 ---
def calculate_score(weight, bw, coeffs):
    if weight <= 0 or bw <= 0:
        return 0
    denominator = coeffs["A"] - coeffs["B"] * math.exp(-coeffs["C"] * bw)
    if denominator == 0: return 0
    return (weight * 100) / denominator

# --- 4. 執行計算與顯示結果 ---
if st.button("開始計算", type="primary"):
    if bodyweight <= 0:
        st.error("❌ 請輸入有效的體重！")
    else:
        # 單位轉換：如果是 lbs，轉成 kg 運算
        factor = 0.45359237 if unit == "lbs" else 1.0
        bw_kg = bodyweight * factor
        s_kg = squat * factor
        b_kg = bench * factor
        d_kg = deadlift * factor
        total_kg = s_kg + b_kg + d_kg

        # 取得對應係數
        coeffs = COEFFICIENTS[gender][equipment]

        # 計算各項分數
        s_score = calculate_score(s_kg, bw_kg, coeffs)
        b_score = calculate_score(b_kg, bw_kg, coeffs)
        d_score = calculate_score(d_kg, bw_kg, coeffs)
        total_score = calculate_score(total_kg, bw_kg, coeffs)

        st.divider()
        st.subheader("📊 計算結果 (IPF GL Points)")
        
        # 顯示總分大數據
        st.metric(label="🏆 總分 (Total GL)", value=f"{total_score:.2f}", delta=f"總和重量: {total_kg:.1f} kg")

        # 顯示單項細節
        c_res1, c_res2, c_res3 = st.columns(3)
        c_res1.info(f"**深蹲**: {s_score:.2f} 分")
        c_res2.info(f"**臥推**: {b_score:.2f} 分")
        c_res3.info(f"**硬舉**: {d_score:.2f} 分")
