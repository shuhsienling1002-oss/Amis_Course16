import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 16: O Patiyamay", page_icon="🛒", layout="centered")

# --- CSS 美化 ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #FFF3E0 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #FF9800;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #E65100; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #FFF8E1;
        border-left: 5px solid #FFB74D;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #FFE0B2; color: #E65100; border: 2px solid #FF9800; padding: 12px;
    }
    .stButton>button:hover { background-color: #FFCC80; border-color: #F57C00; }
    .stProgress > div > div > div > div { background-color: #FF9800; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 16 校正版) ---
vocab_data = [
    {"amis": "Patiyamay", "chi": "商店 / 市場", "icon": "🏪", "source": "Dict: Tiyam"},
    {"amis": "Payso", "chi": "錢", "icon": "💰", "source": "Unit 11"},
    {"amis": "'Aca", "chi": "價格 / 價錢", "icon": "🏷️", "source": "Row 2259"},
    {"amis": "Matekes", "chi": "貴", "icon": "📈", "source": "Row 2259"},
    {"amis": "Caay ka tekes", "chi": "便宜 (不貴)", "icon": "📉", "source": "Grammar (Negation)"},
    {"amis": "Micakay", "chi": "買", "icon": "🛒", "source": "Dict: Buy"},
    {"amis": "Pacakay", "chi": "賣", "icon": "🤝", "source": "Dict: Sell"},
    {"amis": "Dateng", "chi": "蔬菜", "icon": "🥬", "source": "Row 7640"},
    {"amis": "Titi", "chi": "肉", "icon": "🥩", "source": "Row 11"},
    {"amis": "Po'ot", "chi": "刀子 (易混淆詞)", "icon": "🔪", "source": "Row 3205"}, # 特別列出以釐清
]

sentences = [
    {"amis": "Pina ko 'aca?", "chi": "價錢多少？(多少錢)", "icon": "❓", "source": "Row 1871 (Modified)"},
    {"amis": "Micakay kako to dateng.", "chi": "我買菜。", "icon": "🥬", "source": "Mi-cakay"},
    {"amis": "Tada matekes.", "chi": "太貴了。", "icon": "💸", "source": "Row 2259 (Modified)"},
    {"amis": "Caay ka tekes ko 'aca.", "chi": "價格很便宜(不貴)。", "icon": "📉", "source": "Grammar"},
    {"amis": "Tayra ci ina i patiyamay.", "chi": "媽媽去市場。", "icon": "🚶‍♀️", "source": "Dict: Patiyamay"},
]

# --- 3. 隨機題庫 (同步更新) ---
raw_quiz_pool = [
    {
        "q": "Pina ko 'aca? (這句話是什麼意思？)",
        "audio": "Pina ko 'aca",
        "options": ["多少錢？", "這是什麼？", "你去哪裡？"],
        "ans": "多少錢？",
        "hint": "'Aca 是價格"
    },
    {
        "q": "Micakay kako to dateng.",
        "audio": "Micakay kako to dateng",
        "options": ["我買菜", "我賣菜", "我吃菜"],
        "ans": "我買菜",
        "hint": "Micakay 是買 (主動)"
    },
    {
        "q": "Tada matekes! (老闆開價太高時你會說...)",
        "audio": "Tada matekes",
        "options": ["太貴了", "太便宜了", "太好吃了"],
        "ans": "太貴了",
        "hint": "Matekes 是貴 (Row 2259)"
    },
    {
        "q": "單字測驗：Patiyamay",
        "audio": "Patiyamay",
        "options": ["商店 / 市場", "學校", "家"],
        "ans": "商店 / 市場",
        "hint": "做生意(Tiyam)的地方"
    },
    {
        "q": "單字測驗：Po'ot (易混淆詞)",
        "audio": "Po'ot",
        "options": ["刀子", "貴", "便宜"],
        "ans": "刀子",
        "hint": "注意！Po'ot 是刀子，不是貴喔！(Row 3205)"
    },
    {
        "q": "Tayra ci ina i patiyamay.",
        "audio": "Tayra ci ina i patiyamay",
        "options": ["媽媽去市場", "媽媽在煮飯", "媽媽去學校"],
        "ans": "媽媽去市場",
        "hint": "Tayra 是去"
    },
    {
        "q": "「賣」東西的阿美語怎麼說？",
        "audio": None,
        "options": ["Pacakay", "Micakay", "Komaen"],
        "ans": "Pacakay",
        "hint": "Pa- 開頭通常有「給」的意思 -> 給人買 -> 賣"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌
    selected_questions = random.sample(raw_quiz_pool, 3)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #E65100;'>Unit 16: O Patiyamay</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>市場買賣 (Data Verified)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #EF6C00;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 3)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 3**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #FFE0B2; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #E65100;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會正確的買賣用語了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 3)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()
