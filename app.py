import streamlit as st
import sqlite3
from datetime import date

# DB接続
conn = sqlite3.connect("scouting.db")
cur = conn.cursor()

# テーブル作成
cur.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_date TEXT,
    category TEXT,
    scout_name TEXT,
    player_name TEXT,
    club TEXT,
    under_club TEXT,
    info_date TEXT,
    agent TEXT,
    contract_term TEXT,
    salary TEXT,
    details TEXT,
    height INTEGER,
    weight INTEGER,
    position1 TEXT,
    position2 TEXT,
    position_number TEXT,
    foot TEXT,
    birthdate TEXT,
    nationality TEXT,
    tech INTEGER,
    tactics INTEGER,
    physical INTEGER,
    mental INTEGER,
    potential INTEGER,
    average REAL,
    summary TEXT,
    comment_good TEXT,
    comment_bad TEXT,
    comment_other TEXT,
    player_info TEXT,
    highlight1 TEXT,
    highlight2 TEXT,
    note TEXT
)
""")

# タイトル
st.title("🔍 スカウティング登録フォーム")

with st.form("scout_form"):
    st.subheader("📝 基本情報")
    col1, col2 = st.columns(2)
    with col1:
        entry_date = st.date_input("入力日", value=date.today())
        scout_name = st.text_input("入力者")
        player_name = st.text_input("氏名")
        category = st.selectbox("ジャンル分け", ["外国人（現役）", "日本人（現役）", "新卒", "レンタル視察", "OB視察"])
        info_date = st.date_input("情報提供日")
        
    with col2:
        club = st.text_input("所属クラブ（レンタル元は（）で）")
        under_club = st.text_input("前所属クラブ（U-18含む）")
        agent = st.text_input("エージェント（連絡先）")
        contract_term = st.text_input("契約期間")
        salary = st.text_input("報酬")

    details = st.text_area("その他詳細")

    st.subheader("📏 身体・ポジション情報")
    col3, col4 = st.columns(2)
    with col3:
        height = st.number_input("身長（cm）", 150, 250)
        position1 = st.selectbox("ポジション1", ["GK", "CB", "SB/WB", "VO/AC","SH/WG", "IH/OMF", "ST", "CF"])
        position_number = st.text_input("ポジション番号")
        foot = st.selectbox("利き足", ["右", "左", "両足"])
    with col4:
        weight = st.number_input("体重（kg）", 50, 150)
        position2 = st.selectbox("ポジション2", ["-", "GK", "CB", "SB/WB", "VO/AC","SH/WG", "IH/OMF", "ST", "CF"])
        birthdate = st.date_input("生年月日")
        nationality = st.text_input("国籍")

    st.subheader("📊 評価")
    col5, col6, col7 = st.columns(3)
    with col5:
        tech = st.slider("技術", 1, 10)
        tactics = st.slider("戦術", 1, 10)
    with col6:
        physical = st.slider("フィジカル", 1, 10)
        mental = st.slider("メンタル", 1, 10)
    with col7:
        potential = st.slider("将来性", 1, 10)
        average = round((tech + tactics + physical + mental + potential) / 5, 2)
        summary = st.selectbox("総評", ["A", "B", "C", "D","E"])
        st.markdown(f"📈 **平均評価: {average}**")

    st.subheader("💬 コメント")
    comment_good = st.text_area("コメント（長所）")
    comment_bad = st.text_area("コメント（短所）")
    comment_other = st.text_area("コメント（その他）")
    player_info = st.text_area("選手情報")

    st.subheader("🎥 映像・備考")
    col8, col9 = st.columns(2)
    with col8:
        highlight1 = st.text_input("ハイライト映像(1)のURL")
    with col9:
        highlight2 = st.text_input("ハイライト映像(2)のURL")
    note = st.text_area("その他/備考")

    submitted = st.form_submit_button("☑️ 登録する")

    if submitted:
        cur.execute("""
        INSERT INTO players (
            entry_date, category, scout_name, player_name, club, under_club, info_date, agent,
            contract_term, salary, details, height, weight, position1, position2,
            position_number, foot, birthdate, nationality,
            tech, tactics, physical, mental, potential, average, summary,
            comment_good, comment_bad, comment_other, player_info,
            highlight1, highlight2, note
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry_date, category, scout_name, player_name, club, under_club, info_date, agent,
            contract_term, salary, details, height, weight, position1, position2,
            position_number, foot, birthdate, nationality,
            tech, tactics, physical, mental, potential, average, summary,
            comment_good, comment_bad, comment_other, player_info,
            highlight1, highlight2, note
        ))
        conn.commit()
        st.success(f"✅ {player_name} の情報を保存しました！")

        if highlight1:
            st.video(highlight1)
        if highlight2:
            st.video(highlight2)

# データベース閉じる
conn.close()
