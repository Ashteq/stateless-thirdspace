import streamlit as st
import streamlit.components.v1 as components
import os
import textwrap
from backend.agent import get_agent_response
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Third Space", layout="wide", initial_sidebar_state="collapsed")

# Bulletproof trick to completely hide default Streamlit Emojis/Avatars
TRANSPARENT_GIF = "data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=="

# ----------------- STRICT INTRO STATE GATEKEEPER -----------------
if "intro_done" not in st.session_state:
    st.session_state.intro_done = False

if not st.session_state.intro_done:
    intro_css = textwrap.dedent("""
    <style>
        .stApp { background-color: #000000 !important; }
        header[data-testid="stHeader"] { display: none !important; }
        .enter-btn-container { display: flex; justify-content: center; margin-top: 10px; }
        .stButton>button {
            background: #18181b !important;
            color: #ffffff !important;
            border: 1px solid #3f3f46 !important;
            border-radius: 0px !important; 
            padding: 15px 40px !important;
            font-family: 'Helvetica Neue', sans-serif !important;
            font-size: 14px !important;
            letter-spacing: 2px !important;
            text-transform: uppercase !important;
            transition: all 0.3s ease-in-out !important;
            margin-top: -20px;
        }
        .stButton>button:hover {
            background: #27272a !important;
            border-color: #e4e4e7 !important;
        }
    </style>
    """)
    st.markdown(intro_css, unsafe_allow_html=True)
    
    try:
        with open("assets/intro_sequence.html", "r", encoding="utf-8") as f:
            components.html(f.read(), height=750, scrolling=False)
    except FileNotFoundError:
        st.error("Could not find 'assets/intro_sequence.html'.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("ENTER THE SPACE ➔", use_container_width=True):
            st.session_state.intro_done = True
            st.rerun()
            
    st.stop()


# ----------------- MAIN APPLICATION (POST-INTRO) -----------------

global_css = textwrap.dedent("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    
    /* SOLID BLACK BACKGROUND WITH BRIGHTER GLOBAL TEXT */
    .stApp, .main, .block-container { 
        background-color: #000000 !important;
        background-image: none !important;
        color: #f8fafc !important; 
        padding-bottom: 50px !important; 
    }
    
    .powered-header {
        position: fixed;
        top: 15px;
        right: 25px;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 11px;
        color: #d4d4d8; 
        letter-spacing: 2px;
        text-transform: uppercase;
        z-index: 9999;
        font-weight: bold;
        text-align: right;
        line-height: 1.5;
    }

    /* TOP CENTER 3D LOGO */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 10px;
        margin-bottom: 30px;
        perspective: 1200px;
    }
    .spinning-wrapper {
        position: relative;
        width: 50px;
        height: 50px;
        transform-style: preserve-3d;
        animation: continuousSpin 12s linear infinite;
    }
    @keyframes continuousSpin {
        0% { transform: rotateX(60deg) rotateZ(0deg); }
        100% { transform: rotateX(60deg) rotateZ(360deg); }
    }
    .axis {
        position: absolute;
        width: 50px;
        height: 50px;
        transform-style: preserve-3d;
    }
    .axis.red { background-color: #f4f4f5; transform: rotateY(90deg) translateZ(25px); }
    .axis.yellow { background-color: #e4e4e7; transform: rotateX(90deg) translateZ(25px); }
    .axis.blue { background-color: #d4d4d8; transform: translateZ(25px); }
    
    .header-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #ffffff;
        margin-top: 30px;
    }

    /* ADJACENT SQUARED TABS */
    div[data-testid="column"] { 
        padding: 0 !important; 
    }
    .stButton>button {
        background-color: #18181b !important;
        color: #f8fafc !important;
        border-radius: 0px !important; 
        padding: 12px 30px !important;
        border: 1px solid #3f3f46 !important;
        font-family: 'Helvetica Neue', sans-serif !important;
        font-weight: 500 !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin: 0 !important;
    }
    .stButton>button:hover {
        background-color: #27272a !important;
        color: #ffffff !important;
    }
</style>
""")
st.markdown(global_css, unsafe_allow_html=True)

st.markdown(
    """<div class='powered-header'>POWERED BY QLOO<br><span style="font-size: 9px; letter-spacing: 1px; color: #a1a1aa;">AKANKSHA SHARMA</span></div>""", 
    unsafe_allow_html=True
)
st.markdown(textwrap.dedent("""
<div class="header-container">
    <div class="spinning-wrapper">
        <div class="axis red"></div>
        <div class="axis yellow"></div>
        <div class="axis blue"></div>
    </div>
    <div class="header-title">THIRD SPACE</div>
</div>
"""), unsafe_allow_html=True)

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "active_chat_tab" not in st.session_state:
    st.session_state.active_chat_tab = "B2C"
if "qloo_payload" not in st.session_state:
    st.session_state.qloo_payload = {"status": "Awaiting first query..."}

# Navigation Bar Layout
col1, col2, col3 = st.columns(3, gap="small")
with col1:
    if st.button("Home", use_container_width=True): st.session_state.current_page = "Home"
with col2:
    if st.button("Qloo Integration", use_container_width=True): st.session_state.current_page = "Qloo Integration"
with col3:
    if st.button("Chats", use_container_width=True): st.session_state.current_page = "Chats"

st.markdown("<hr style='border: none; height: 1px; background-color: #3f3f46; margin-top: 10px; margin-bottom: 30px;'/>", unsafe_allow_html=True)

# ----------------- PAGE VIEWS -----------------

if st.session_state.current_page == "Home":
    home_content = """<h2 style='color:#ffffff; font-family:Helvetica; letter-spacing: 2px;'>About Third Space</h2>
<div style='padding: 10px 0; color:#e4e4e7; line-height: 1.8; font-family: sans-serif;'>
<p style='font-size: 16px; margin-bottom: 30px;'>Third Space is a platform engineered to bridge the widening gap between digital culture and physical community. We address the modern isolation crisis by mapping your digital media affinities directly to real-world environments.</p>
<div style='display: flex; gap: 40px; flex-wrap: wrap;'>
<div style='flex: 1; min-width: 300px;'>
<h3 style='color: #ffffff; border-bottom: 1px solid #3f3f46; padding-bottom: 10px;'>B2C: The Digital Off-Ramp</h3>
<p><strong>The Isolation Crisis:</strong> Big tech recommendation algorithms have optimized for endless scrolling, creating a paradox where society is more digitally connected, yet physically more isolated than ever before. We are trapped in algorithmic echo chambers that prioritize platform engagement over genuine human connection.</p>
<p><strong>Discord for Real Life:</strong> Just as Discord helps you find hyper-specific digital "servers" based on your niche interests, Third Space helps you find your physical servers. We use cultural data to guide you to real-world hangout spots in your exact neighborhood where your type of people already congregate.</p>
<p><strong>The Human Element:</strong> Instead of a sterile search bar, our B2C chat interface acts as an empathetic algorithmic wellbeing coach. The AI is explicitly programmed as a "Prudent Cooperator"—it validates your media tastes and anticipates your mood, but it avoids being an enabler of addiction. It gently and firmly nudges you to log off and step outside into a physical Third Space (a cafe, lounge, or arcade) where serendipity and offline connection thrive.</p>
</div>
<div style='flex: 1; min-width: 300px;'>
<h3 style='color: #ffffff; border-bottom: 1px solid #3f3f46; padding-bottom: 10px;'>B2B: Third-Space Architect</h3>
<p><strong>The Real Estate Challenge:</strong> On the enterprise side, Third Space acts as a formal real estate consultant analyzing demographic viability for commercial developers and urban planners. With shifting urban populations and remote work, developers need to know exactly what kind of physical space a specific neighborhood's culture actually wants before they build it.</p>
<p><strong>Data-Driven Urban Planning:</strong> The B2B persona ingests target demographic data provided by real estate developers (e.g., "Remote software engineers who listen to specific tech podcasts"). It queries taste clusters to understand the broader cultural affinities and behavioral patterns of this specific demographic group.</p>
<p><strong>Finding Cultural Gaps:</strong> It cross-references this behavioral profile with Locality Intelligence for a specific physical neighborhood to identify "cultural gaps"—amenities that the demographic loves but are currently missing in that area. This provides highly lucrative, data-backed recommendations for what commercial spaces to build to guarantee foot traffic.</p>
</div>
</div>
</div>"""
    st.markdown(home_content, unsafe_allow_html=True)

elif st.session_state.current_page == "Qloo Integration":
    qloo_content = """<h2 style='color:#ffffff; font-family:Helvetica; letter-spacing: 2px;'>Qloo Architecture & Prompting Guide</h2>
<div style='padding: 10px 0; color:#e4e4e7; line-height: 1.8; font-family: sans-serif;'>
<div style='display: flex; gap: 40px; flex-wrap: wrap;'>
<div style='flex: 1; min-width: 300px;'>
<h3 style='color: #ffffff; border-bottom: 1px solid #3f3f46; padding-bottom: 10px;'>How We Integrated Qloo</h3>
<p><strong>Stakeholder View:</strong> Our application is built entirely upon Qloo's Cultural Graph API, acting as the intelligent bridge between digital culture and physical community. We map the culture, not the individual, operating on stateless inference so zero Personally Identifiable Information (PII) is ever retained, ensuring complete user privacy.</p>
<p><strong>B2C (Digital Off-Ramp):</strong> Powered by Groq's low-latency Llama-3 models and LangChain, the agent autonomously triggers external tools. We utilize Qloo's <code>/search</code> endpoint to accurately identify specific media entities mentioned by the user. We then pass those entity IDs to the <code>/v2/insights</code> endpoint, explicitly filtering by <code>urn:entity:place</code> to translate digital media affinities into highly correlated physical locations.</p>
<p><strong>B2B (Third-Space Architect):</strong> We flip the API logic. We leverage demographic taste clusters and cross-reference them with Locality Intelligence to architecturally map cultural gaps for developers, revealing what spaces a neighborhood is missing.</p>
<p><strong>Live Telemetry:</strong> The <strong>Developer Console</strong> (located on the right side of the Chat interface) displays the live Qloo JSON payload. This allows stakeholders to monitor the exact stateless data powering the AI's recommendations in real-time.</p>
</div>
<div style='flex: 1; min-width: 300px;'>
<h3 style='color: #ffffff; border-bottom: 1px solid #3f3f46; padding-bottom: 10px;'>How to Prompt the Agents</h3>
<h4 style='color: #ffffff; margin-top: 15px;'> Prompting the B2C Agent</h4>
<p>The B2C agent acts as a cultural matchmaker. To get the best physical recommendations, you must provide two key ingredients in your chat:</p>
<ul style='list-style-type: square; padding-left: 20px;'>
<li><strong>Your Media Tastes:</strong> Tell the agent exactly what you are listening to, watching, or reading right now (e.g., <em>"I've been listening to a lot of Radiohead and watching A24 indie films."</em>)</li>
<li><strong>Your Exact Location:</strong> You MUST tell the agent your city and neighborhood so it can map places nearby (e.g., <em>"I am currently in Williamsburg, Brooklyn."</em>)</li>
</ul>
<p><em>Example B2C Prompt:</em> "I'm listening to Kendrick Lamar and I'm currently in downtown Chicago. Where should I hang out today?"</p>
<h4 style='color: #ffffff; margin-top: 25px;'> Prompting the B2B Agent</h4>
<p>The B2B agent acts as a formal real estate consultant. It does not want personal tastes; it wants demographic profiles and development sites.</p>
<ul style='list-style-type: square; padding-left: 20px;'>
<li><strong>Target Demographic:</strong> Describe the type of people you are building for (e.g., <em>"Remote software engineers,"</em> or <em>"College students who like indie music."</em>)</li>
<li><strong>Development Site:</strong> Provide the specific city and neighborhood you plan to build in (e.g., <em>"SoMa district in San Francisco."</em>)</li>
</ul>
<p><em>Example B2B Prompt:</em> "I am building a 500-unit residential complex near NYU in Manhattan. My target demographic is Gen-Z art students. What commercial amenities should I build on the ground floor?"</p>
</div>
</div>
</div>"""
    st.markdown(qloo_content, unsafe_allow_html=True)

elif st.session_state.current_page == "Chats":
    chat_css = """<style>
.subnav-container { display: flex; gap: 0px; margin-bottom: 10px; border-bottom: 1px solid #3f3f46; padding-bottom: 10px; }
[data-testid="stChatInput"] { background-color: #18181b !important; border-radius: 0px !important; border: 1px solid #3f3f46 !important; }
[data-testid="stChatInput"] textarea, [data-testid="stChatInput"] button { font-family: 'Times New Roman', serif !important; color: #FFFFFF !important; }
</style>"""
    st.markdown(chat_css, unsafe_allow_html=True)
    
    subnav_col1, subnav_col2, _ = st.columns([1, 1, 3])
    with subnav_col1:
        if st.button("ThirdSpace (B2C)", key="btn_b2c"): st.session_state.active_chat_tab = "B2C"
    with subnav_col2:
        if st.button("ThirdSpace (B2B)", key="btn_b2b"): st.session_state.active_chat_tab = "B2B"

    if st.session_state.active_chat_tab == "B2C":
        st.markdown('<style>button[kind="secondary"]:nth-of-type(4) { border-bottom: 2px solid #FF1493 !important; color: #ffffff !important; padding-bottom: 2px !important; }</style>', unsafe_allow_html=True)
    else:
        st.markdown('<style>button[kind="secondary"]:nth-of-type(5) { border-bottom: 2px solid #e4e4e7 !important; color: #ffffff !important; padding-bottom: 2px !important; }</style>', unsafe_allow_html=True)

    chat_col, reasoning_col = st.columns([3, 1])
    
    def render_chat_html(role, content, tab):
        if tab == "B2C":
            if role == "user":
                return f"""<div style="width: 100%; display: flex; justify-content: flex-end; align-items: flex-start; margin-bottom: 15px;">
<div style="background-color: #FFFFFF; color: #FF1493; padding: 12px 20px; border-radius: 20px; font-family: 'Times New Roman', serif; font-size: 16px; max-width: 75%; text-align: left; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">{content}</div>
<div style="min-width: 12px; height: 12px; border-radius: 50%; background-color: #00BFFF; box-shadow: 0 0 10px 2px rgba(0,191,255,0.8); margin-left: 15px; margin-top: 15px;"></div>
</div>"""
            else:
                return f"""<div style="width: 100%; display: flex; justify-content: flex-start; align-items: flex-start; margin-bottom: 15px;">
<div style="min-width: 12px; height: 12px; border-radius: 50%; background-color: #FF69B4; box-shadow: 0 0 10px 2px rgba(255,105,180,0.8); margin-right: 15px; margin-top: 15px;"></div>
<div style="background-color: #FF1493; color: #FFFFFF; padding: 12px 20px; border-radius: 20px; font-family: 'Times New Roman', serif; font-size: 16px; max-width: 75%; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">{content}</div>
</div>"""
        elif tab == "B2B":
            if role == "user":
                return f"""<div style="width: 100%; display: flex; justify-content: flex-end; align-items: flex-start; margin-bottom: 15px;">
<div style="background-color: #F1F5F9; color: #000000; padding: 12px 20px; border: 1px solid #94A3B8; font-family: 'Times New Roman', serif; font-size: 16px; max-width: 75%; text-align: left;">{content}</div>
<div style="min-width: 12px; height: 12px; border-radius: 50%; background-color: #94A3B8; box-shadow: 0 0 10px 2px rgba(148,163,184,0.8); margin-left: 15px; margin-top: 15px;"></div>
</div>"""
            else:
                return f"""<div style="width: 100%; display: flex; justify-content: flex-start; align-items: flex-start; margin-bottom: 15px;">
<div style="min-width: 12px; height: 12px; border-radius: 50%; background-color: #FFFFFF; box-shadow: 0 0 10px 2px rgba(255,255,255,0.8); margin-right: 15px; margin-top: 15px;"></div>
<div style="background-color: #1E293B; color: #FFFFFF; padding: 12px 20px; border: 1px solid #475569; font-family: 'Times New Roman', serif; font-size: 16px; max-width: 75%;">{content}</div>
</div>"""

    with chat_col:
        if st.session_state.active_chat_tab == "B2C":
            if "b2c_messages" not in st.session_state:
                st.session_state.b2c_messages = [{"role": "assistant", "content": "Welcome to ThirdSpace. Tell me a bit about what you're watching or listening to right now, and please let me know your city or neighborhood so we can find your real-world match."}]
            
            chat_container = st.container()
            with chat_container:
                for msg in st.session_state.b2c_messages:
                    st.markdown(render_chat_html(msg["role"], msg["content"], "B2C"), unsafe_allow_html=True)
            
            b2c_input = st.chat_input("Enter your media tastes and city...") 
            if b2c_input:
                st.session_state.b2c_messages.append({"role": "user", "content": b2c_input})
                st.rerun() 
                
        elif st.session_state.active_chat_tab == "B2B":
            if "b2b_messages" not in st.session_state:
                st.session_state.b2b_messages = [{"role": "assistant", "content": "Welcome. To begin our site analysis, could you share the target demographic and neighborhood you are evaluating today?"}]
            
            chat_container = st.container()
            with chat_container:
                for msg in st.session_state.b2b_messages:
                    st.markdown(render_chat_html(msg["role"], msg["content"], "B2B"), unsafe_allow_html=True)
            
            b2b_input = st.chat_input("Enter target demographic and city...")
            if b2b_input:
                st.session_state.b2b_messages.append({"role": "user", "content": b2b_input})
                st.rerun() 

        # API Triggers
        if st.session_state.active_chat_tab == "B2C" and st.session_state.b2c_messages[-1]["role"] == "user":
            with st.spinner("Connecting to Qloo..."):
                response, payload = get_agent_response(st.session_state.b2c_messages[-1]["content"], "B2C")
                st.session_state.qloo_payload = payload
                st.session_state.b2c_messages.append({"role": "assistant", "content": response})
                st.rerun()

        elif st.session_state.active_chat_tab == "B2B" and st.session_state.b2b_messages[-1]["role"] == "user":
            with st.spinner("Analyzing demographics..."):
                response, payload = get_agent_response(st.session_state.b2b_messages[-1]["content"], "B2B")
                st.session_state.qloo_payload = payload
                st.session_state.b2b_messages.append({"role": "assistant", "content": response})
                st.rerun()

    with reasoning_col:
        st.markdown("""<style>
.arch-panel-block {
    background-color: #09090b; border-radius: 0px; padding: 20px; color: #d4d4d8;
    overflow-y: auto !important; overflow-x: hidden !important; border: 1px solid #3f3f46 !important; word-wrap: break-word;
}
.arch-panel-block strong { color: #ffffff; }
.arch-panel-block::-webkit-scrollbar { width: 8px; }
.arch-panel-block::-webkit-scrollbar-thumb { background-color: #3f3f46; }
</style>
<strong style='color:#ffffff;'>📡 Live Qloo API Payload:</strong>""", unsafe_allow_html=True)
        payload_container = st.container(height=600, border=True)
        with payload_container:
            st.json(st.session_state.qloo_payload)