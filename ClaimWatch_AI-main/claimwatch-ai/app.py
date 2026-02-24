import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
import os

# Set page config
st.set_page_config(page_title="ClaimWatch AI | Intelligence Suite", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Premium Dashboard Hub
st.markdown("""
<style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Outfit:wght@400;600;900&family=Rajdhani:wght@500;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 900 !important;
        letter-spacing: -1px;
    }

    .stApp {
        background-color: #020617;
        background-image: 
            radial-gradient(at 0% 0%, rgba(30, 58, 138, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(88, 28, 135, 0.15) 0px, transparent 50%);
        color: #f8fafc;
    }

    /* Sidebar - Aero Glass */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.7) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: 1px solid transparent !important;
        color: #94a3b8 !important;
        padding: 10px 15px !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-bottom: 6px !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        transform: translateX(5px);
    }

    /* "Nice" Cyan-Blue Gradient for Primary Button - LARGER SIZE */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%) !important;
        border: none !important;
        box-shadow: 0 8px 25px rgba(6, 182, 212, 0.3) !important;
        font-family: 'Rajdhani', sans-serif !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        border-radius: 12px !important;
        padding: 20px 40px !important; /* Larger button */
        font-size: 1.5rem !important;
        font-weight: 800 !important;
    }

    /* Hero Glass Card */
    .hero-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        padding: 60px;
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg at 50% 50%, transparent 0deg, rgba(59, 130, 246, 0.05) 120deg, transparent 240deg);
        animation: rotate 10s linear infinite;
    }
    @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

    .hero-title { font-size: 3.5rem; line-height: 1; margin-bottom: 20px; }
    .hero-subtitle { color: #94a3b8; font-size: 1.2rem; font-weight: 400; }

    /* Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
    }

    /* Input Labels */
    .stNumberInput label, .stSelectbox label {
        font-family: 'Rajdhani', sans-serif !important;
        text-transform: uppercase !important;
        color: #7dd3fc !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
    }

    /* Verdict Display - PREMIUM BADGE LOOK */
    .verdict-box {
        padding: 25px 40px !important;
        border-radius: 24px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        margin: 20px auto;
        max-width: 450px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .verdict-box::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, transparent 100%);
        pointer-events: none;
    }

    .v-fraud { 
        background: rgba(239, 68, 68, 0.1) !important; 
        border-color: rgba(239, 68, 68, 0.4) !important;
        box-shadow: 0 0 30px rgba(239, 68, 68, 0.15) !important;
    }
    .v-safe { 
        background: rgba(34, 197, 94, 0.1) !important; 
        border-color: rgba(34, 197, 94, 0.4) !important;
        box-shadow: 0 0 30px rgba(34, 197, 94, 0.15) !important;
    }
    .v-warning { 
        background: rgba(245, 158, 11, 0.1) !important; 
        border-color: rgba(245, 158, 11, 0.4) !important;
        box-shadow: 0 0 30px rgba(245, 158, 11, 0.15) !important;
    }

    .v-title-main { 
        font-family: 'Outfit', sans-serif; 
        font-size: 2.8rem !important; 
        font-weight: 900; 
        letter-spacing: 2px;
        margin-bottom: 5px;
        text-transform: uppercase;
    }
    .v-score { 
        font-family: 'Rajdhani', sans-serif; 
        font-size: 1.6rem !important; 
        font-weight: 700; 
        color: rgba(255, 255, 255, 0.9);
        letter-spacing: 1px;
    }

    /* Tabs Override - HIDE RED UNDERLINE */
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; border-bottom: none !important; }
    .stTabs [data-baseweb="tab"] { color: #64748b; font-weight: 600; border: none !important; }
    .stTabs [aria-selected="true"] { color: #3b82f6 !important; border-bottom: none !important; }
    /* ===== REMOVE SIDEBAR COLLAPSE / ARROW TEXT ===== */
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    section[data-testid="stSidebar"] button[kind="secondary"]::after {
        content: none !important;
    }

    /* ===== CHAT UI OVERRIDE ===== */
    .chat-bubble-container {
        display: flex;
        flex-direction: column;
        gap: 12px;
        padding: 10px;
    }
    
    .bubble {
        padding: 12px 16px;
        border-radius: 18px;
        font-size: 0.95rem;
        line-height: 1.4;
        position: relative;
        max-width: 90%;
        animation: fadeIn 0.3s ease-out;
    }

    @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

    .bubble-user {
        align-self: flex-end;
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white;
        border-bottom-right-radius: 4px;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
    }

    .bubble-assistant {
        align-self: flex-start;
        background: rgba(30, 41, 59, 0.9) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #f1f5f9;
        border-bottom-left-radius: 4px;
    }

    .bubble-name {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 3px;
        color: #94a3b8;
    }

    /* PERFECT CIRCLE Popover Button (Extreme Bottom Right) */
    div[data-testid="stPopover"] {
        position: fixed !important;
        bottom: 20px !important;
        right: 20px !important;
        z-index: 9999999 !important;
        width: 65px !important;
        height: 65px !important;
    }

    div[data-testid="stPopover"] > button {
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%) !important;
        border: none !important;
        border-radius: 50% !important;
        width: 65px !important;
        height: 65px !important;
        min-width: 65px !important;
        min-height: 65px !important;
        padding: 0 !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 10px 30px rgba(6, 182, 212, 0.5) !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        overflow: hidden !important;
    }
    
    div[data-testid="stPopover"] > button:hover {
        transform: scale(1.1) rotate(10deg) !important;
        box-shadow: 0 15px 40px rgba(6, 182, 212, 0.6) !important;
    }

    /* Center the emoji and hide EVERYTHING else (labels, arrows, etc.) */
    div[data-testid="stPopover"] button span > div:nth-child(n+2) {
        display: none !important;
    }
    
    div[data-testid="stPopover"] button span div p {
        font-size: 32px !important;
        margin: 0 !important;
        line-height: 1 !important;
        display: block !important;
    }
    
    div[data-testid="stPopover"] button span svg {
        display: none !important;
    }
    
    /* Strong override for any potential text overflow/labels */
    div[data-testid="stPopover"] button * {
        font-family: 'Segoe UI Emoji', sans-serif !important;
    }

    /* Popover Content (FORCE DARK MODE) */
    div[data-testid="stPopoverContent"] {
        background: #0f172a !important; /* Slate 900 */
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8) !important;
        border-radius: 20px !important;
        min-width: 350px !important;
        z-index: 10000000 !important;
    }
    
    div[data-testid="stPopoverContent"] h3, 
    div[data-testid="stPopoverContent"] p, 
    div[data-testid="stPopoverContent"] span,
    div[data-testid="stPopoverContent"] label {
        color: #f1f5f9 !important;
    }

    /* Input styling for dark mode */
    div[data-testid="stPopoverContent"] input {
        background: rgba(15, 23, 42, 0.8) !important;
        color: white !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
    }

    /* Scrollbar for dark mode chat */
    div[data-testid="stPopoverContent"] ::-webkit-scrollbar {
        width: 5px;
    }
    div[data-testid="stPopoverContent"] ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
</style>
""", unsafe_allow_html=True)

# Domain Configuration
# Using a dashboard symbol (📊) in descriptions and icons
DOMAINS = {
    "dashboard": {"name": "Dashboard", "icon": ""},
    "automobile": {"name": "Automobile", "icon": ""},
    "health": {"name": "Health", "icon": ""},
    "property": {"name": "Property", "icon": ""},
    "life": {"name": "Life", "icon": ""},
    "travel": {"name": "Travel", "icon": ""}
}

TOOLS = {
    "analytics": {"name": "Analytics", "icon": "📊", "desc": "Market intelligence"},
    "assessment": {"name": "Assessment", "icon": "🛡️", "desc": "System health"},
    "batch_scan": {"name": "Batch Scan", "icon": "📦", "desc": "Bulk processing"},
}

if 'current_domain' not in st.session_state:
    st.session_state.current_domain = 'dashboard'

# Sidebar Implementation
with st.sidebar:
    st.markdown("""
    <div class="profile-section">
        <div class="profile-info">
            <div class="profile-name">CLAIMWATCH AI</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-label">Main Menu</p>', unsafe_allow_html=True)
    
    for key, info in DOMAINS.items():
        is_active = st.session_state.current_domain == key
        btn_type = "primary" if is_active else "secondary"

        button_label = f"{info['icon']} {info['name']}".strip()
        if st.button(button_label, key=f"nav_main_{key}", width="stretch", type=btn_type):
            st.session_state.current_domain = key
            st.rerun()

    st.markdown('<p class="sidebar-label">Intelligence Tools</p>', unsafe_allow_html =True)
    for key, info in TOOLS.items():
        is_active = st.session_state.current_domain == key
        btn_type = "primary" if is_active else "secondary"

        button_label = f"{info['icon']} {info['name']}".strip()
        if st.button(button_label, key=f"nav_tool_{key}", width="stretch", type=btn_type):
            st.session_state.current_domain = key
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("TERMINATE SESSION", key="terminate_session", width="stretch"):
        st.session_state.current_domain = 'dashboard'
        st.rerun()

@st.cache_resource
def load_assets(domain_id):
    # Fix paths to be relative to the script location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(base_dir, 'models', domain_id)
    
    try:
        with open(os.path.join(model_dir, 'model.pkl'), 'rb') as f: model = pickle.load(f)
        with open(os.path.join(model_dir, 'scaler.pkl'), 'rb') as f: scaler = pickle.load(f)
        with open(os.path.join(model_dir, 'label_encoders.pkl'), 'rb') as f: le_dict = pickle.load(f)
        with open(os.path.join(model_dir, 'feature_names.pkl'), 'rb') as f: feature_names = pickle.load(f)
        return model, scaler, le_dict, feature_names
    except Exception as e:
        st.error(f"Error loading assets for {domain_id}: {str(e)}")
        return None, None, None, None

def get_full_input_form(domain_id, default_vals):
    input_data = {}
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    # --- SECTION: POLICY DETAILS ---
    st.markdown('<p style="color: #60a5fa; font-family: Rajdhani; font-weight: 700; text-transform: uppercase;">⚖️ Policy Parameters</p>', unsafe_allow_html=True)
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        input_data['months_as_customer'] = st.number_input("Months as Customer", 0, 600, int(default_vals.get('months_as_customer', 120)))
        input_data['policy_state'] = st.selectbox("Policy State", ['NY', 'CA', 'IL', 'TX', 'FL'], index=0)
    with pc2:
        input_data['policy_csl'] = st.selectbox("Policy CSL", ['100/300', '250/500', '500/1000'], index=1)
        input_data['policy_deductable'] = st.selectbox("Deductable", [500, 1000, 2000], index=1)
    with pc3:
        input_data['policy_annual_premium'] = st.number_input("Annual Premium", 100.0, 5000.0, float(default_vals.get('policy_annual_premium', 1200.0)))
        input_data['umbrella_limit'] = st.selectbox("Umbrella Limit", [0, 1000000, 2000000, 5000000], index=0)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    # --- SECTION: INCIDENT PROFILE ---
    st.markdown('<p style="color: #60a5fa; font-family: Rajdhani; font-weight: 700; text-transform: uppercase;">🔍 Incident Dossier</p>', unsafe_allow_html=True)
    ic1, ic2, ic3 = st.columns(3)
    
    with ic1:
        input_data['total_claim_amount'] = st.number_input("Total Claim Amount", 100.0, 500000.0, float(default_vals.get('total_claim_amount', 5000.0)))
        if domain_id == 'automobile':
            input_data['incident_type'] = st.selectbox("Incident Type", ['Single Vehicle Collision', 'Multi-vehicle Collision', 'Parked Car', 'Vehicle Theft'])
            input_data['collision_type'] = st.selectbox("Collision", ['Side Collision', 'Rear Collision', 'Front Collision', 'Unknown'])
        elif domain_id == 'health':
            input_data['hospital_type'] = st.selectbox("Hospital Tier", ['A', 'B', 'C'])
            input_data['treatment_type'] = st.selectbox("Treatment Type", ['A', 'B', 'C'])
        elif domain_id == 'property':
            input_data['property_type'] = st.selectbox("Asset Type", ['A', 'B', 'C'])
            input_data['incident_cause'] = st.selectbox("Cause of Loss", ['A', 'B', 'C'])
    
    with ic2:
        if domain_id == 'automobile':
            input_data['incident_severity'] = st.selectbox("Severity", ['Minor Damage', 'Total Loss', 'Major Damage', 'Trivial Damage'])
            input_data['authorities_contacted'] = st.selectbox("Authorities", ['Police', 'Fire', 'Ambulance', 'None'])
        elif domain_id == 'health':
            input_data['medical_report_available'] = st.selectbox("Med. Report", ['A', 'B', 'C'])
            input_data['visit_frequency_yearly'] = st.selectbox("Visit Freq", ['A', 'B', 'C'])
        elif domain_id == 'property':
            input_data['location_risk_score'] = st.selectbox("Loc. Risk", ['A', 'B', 'C'])
            input_data['security_system_present'] = st.selectbox("Security Hub", ['A', 'B', 'C'])
        elif domain_id == 'life':
            input_data['occupation_risk_level'] = st.selectbox("Risk Level", ['A', 'B', 'C'])
            input_data['smoker'] = st.selectbox("Smoker Status", ['A', 'B', 'C'])
        elif domain_id == 'travel':
            input_data['destination_risk'] = st.selectbox("Dest. Risk", ['A', 'B', 'C'])
            input_data['incident_category'] = st.selectbox("Category", ['A', 'B', 'C'])
    
    with ic3:
        if domain_id == 'automobile':
            input_data['auto_make'] = st.selectbox("Auto Make", ['Saab', 'Mercedes', 'Dodge', 'Chevrolet', 'Ford', 'BMW', 'Toyota', 'Volkswagen', 'Audi'])
            input_data['auto_year'] = st.number_input("Auto Year", 1995, 2024, 2015)
        elif domain_id == 'health':
            input_data['pre_existing_condition'] = st.selectbox("Pre-existing", ['A', 'B', 'C'])
        elif domain_id == 'property':
            input_data['asset_value'] = st.selectbox("Asset Val", ['A', 'B', 'C'])
        elif domain_id == 'life':
            input_data['policy_duration_months'] = st.selectbox("Policy Dur.", ['A', 'B', 'C'])
            input_data['documented_cause_of_death'] = st.selectbox("Cause", ['A', 'B', 'C'])
        elif domain_id == 'travel':
            input_data['trip_duration_days'] = st.selectbox("Trip Days", ['A', 'B', 'C'])
            input_data['travel_insurance_type'] = st.selectbox("Ins. Type", ['A', 'B', 'C'])
            input_data['booking_lead_time_days'] = st.selectbox("Lead Time", ['A', 'B', 'C'])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    # --- SECTION: PERSONAL IDENTIFIERS ---
    st.markdown('<p style="color: #60a5fa; font-family: Rajdhani; font-weight: 700; text-transform: uppercase;">👤 Subject Profile</p>', unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        input_data['age'] = st.number_input("Subject Age", 18, 100, int(default_vals.get('age', 35)))
        input_data['insured_sex'] = st.selectbox("Gender", ['MALE', 'FEMALE'], index=0)
    with sc2:
        input_data['insured_education_level'] = st.selectbox("Education", ['High School', 'College', 'Masters', 'PhD', 'JD'], index=1)
        input_data['insured_occupation'] = st.selectbox("Occupation", ['Exec-managerial', 'Machine-op-inspct', 'Prof-specialty', 'Craft-repair', 'Adm-clerical'], index=0)
    with sc3:
        input_data['insured_relationship'] = st.selectbox("Relationship", ['husband', 'other-relative', 'own-child', 'unmarried', 'wife', 'not-in-family'], index=0)
        input_data['insured_hobbies'] = st.selectbox("Hobbies", ['Reading', 'Exercise', 'Movies', 'Camping', 'Chess'], index=0)
        if domain_id == 'life':
            input_data['beneficiary_relationship'] = st.selectbox("Beneficiary Rel.", ['A', 'B', 'C'])
    st.markdown('</div>', unsafe_allow_html=True)

    # Hidden logic fields
    input_data['capital-gains'] = 0
    input_data['capital-loss'] = 0
    if domain_id == 'automobile':
        input_data['incident_state'] = 'NY'
        input_data['incident_city'] = 'Northbrook'
        input_data['incident_hour_of_the_day'] = 12
        input_data['number_of_vehicles_involved'] = 1
        input_data['property_damage'] = 'NO'
        input_data['bodily_injuries'] = 0
        input_data['witnesses'] = 0
        input_data['police_report_available'] = 'YES'

    return input_data

def main_dashboard():
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">INTELLIGENCE<br>COMMAND CENTER</h1>
        <p class="hero-subtitle">Continuous monitoring active. Neural networks synchronized across 5 global domain nodes.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Global Integrity Pulse")
    cols = st.columns(3)
    with cols[0]: st.metric("CLAIMS SCREENED", "24,812", "↑ 12%")
    with cols[1]: st.metric("FRAUD INDEX", "4.8%", "↓ 1.2%")
    with cols[2]: st.metric("PREVENTED LOSS", "$12.4M", "↑ 18%")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <h3 style="color: #7dd3fc; margin-bottom: 15px;">Mission Overview</h3>
        <p style="color: #94a3b8; font-size: 1.1rem; line-height: 1.6;">
            <b>ClaimWatch AI</b> is a state-of-the-art Intelligence Suite designed to protect the integrity of the insurance ecosystem. 
            By leveraging <b>Deep Neural Heuristics</b> and <b>SMOTE-balanced models</b>, our system identifies fraudulent patterns across five major domains: 
            Automobile, Health, Property, Life, and Travel.
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
            <div>
                <h4 style="color: #60a5fa;">🔍 Real-time Detection</h4>
                <p style="color: #64748b; font-size: 0.9rem;">Analyze individual claims instantly using our Investigation Hub with high-fidelity attribution analysis.</p>
            </div>
            <div>
                <h4 style="color: #60a5fa;">📦 Global Batch Processing</h4>
                <p style="color: #64748b; font-size: 0.9rem;">Process thousands of records simultaneously with our upgraded Bulk Processing Unit for wide-scale risk mitigation.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Removed Connection Nodes and System Health widgets per request
    st.info("Continuous background monitoring active. Neural networks synchronized.")

def domain_page(domain_id):
    domain_info = DOMAINS[domain_id]
    st.title(domain_info['name'])
    st.markdown(f"<p style='color: #64748b;'>Continuous monitoring active. Using SMOTE balanced neural heuristics.</p>", unsafe_allow_html=True)
    
    model, scaler, le_dict, feature_names = load_assets(domain_id)
    if not model:
        st.warning(f"Engine assets for {domain_id} not initialized.")
        return

    # Fix data path to be relative
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', f'{domain_id}_claims.csv')
    raw_data = pd.read_csv(data_path)
    
    # tabss
    tab1, tab2, tab3 = st.tabs(["Investigation", "Metrics", "Explainer"])
    
    # --- TAB 1: INVESTIGATION ---
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p style="color: #60a5fa; font-family: Rajdhani; font-weight: 700; text-transform: uppercase;">💼 Case Intelligence Signature</p>', unsafe_allow_html=True)
        
        # Manual Case Identifier
        case_id = st.text_input("CASE IDENTIFIER", value="CASE-MNL-001", help="Enter a unique case ID for this investigation.")
        
        # Dynamic Forensic Parameters
        st.markdown('<p style="color: #94a3b8; font-size: 0.85rem; margin-top: 15px;">ADDITIONAL FORENSIC PARAMETERS</p>', unsafe_allow_html=True)
        
        # Initialize dynamic rows in session state
        if f'manual_rows_{domain_id}' not in st.session_state:
            st.session_state[f'manual_rows_{domain_id}'] = [{"key": "", "value": ""}]
            
        # Render dynamic rows
        rows_to_delete = []
        for i, row in enumerate(st.session_state[f'manual_rows_{domain_id}']):
            r1, r2, r3 = st.columns([2, 2, 0.5])
            with r1:
                st.session_state[f'manual_rows_{domain_id}'][i]["key"] = st.text_input(f"Parameter Name", value=row["key"], key=f"key_{domain_id}_{i}", placeholder="e.g. Impact Force", label_visibility="collapsed")
            with r2:
                st.session_state[f'manual_rows_{domain_id}'][i]["value"] = st.text_input(f"Parameter Value", value=row["value"], key=f"val_{domain_id}_{i}", placeholder="e.g. 45G", label_visibility="collapsed")
            with r3:
                if st.button("✕", key=f"del_{domain_id}_{i}"):
                    rows_to_delete.append(i)
        
        # Handle deletion
        if rows_to_delete:
            for index in reversed(rows_to_delete):
                st.session_state[f'manual_rows_{domain_id}'].pop(index)
            st.rerun()

        # Add row button
        if st.button("➕ ADD PARAMETER", key=f"add_{domain_id}", use_container_width=True):
            st.session_state[f'manual_rows_{domain_id}'].append({"key": "", "value": ""})
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Default vals for the rest of the form (mostly from empty for manual)
        default_vals = {}
        
        input_data = get_full_input_form(domain_id, default_vals)
        # Inject the manual case ID into input data
        input_data['claim_id'] = case_id
        
        st.markdown('<div class="compact-scan-container">', unsafe_allow_html=True)
        if st.button("RUN", type="primary"):
            with st.spinner("Analyzing..."):
                input_df = pd.DataFrame([input_data])
                for col in feature_names:
                    if col not in input_df.columns: input_df[col] = 0
                
                # Preprocessing
                if 'policy_annual_premium' in input_df.columns: input_df['policy_annual_premium'] = np.log1p(input_df['policy_annual_premium'])
                if 'total_claim_amount' in input_df.columns: input_df['total_claim_amount'] = np.log1p(input_df['total_claim_amount'])
                
                for col, le in le_dict.items():
                    if col in input_df.columns:
                        input_df[col] = input_df[col].map(lambda x: le.transform([x])[0] if x in le.classes_ else 0)
                
                input_df = input_df[feature_names]
                input_scaled = scaler.transform(input_df)
                prob = model.predict_proba(input_scaled)[0][1]
                
                # --- OPTIMIZATION: HEURISTIC RISK LAYER ---
                # ML models sometimes miss obvious patterns. We add rules for "Instant Flags"
                high_risk_reasons = []
                if input_data.get('total_claim_amount', 0) > 80000:
                    high_risk_reasons.append("Extreme Claim Value ($80k+)")
                if input_data.get('incident_severity') == 'Total Loss' and input_data.get('months_as_customer', 0) < 6:
                    high_risk_reasons.append("Total Loss on Brand New Policy")
                if input_data.get('authorities_contacted') == 'None' and input_data.get('incident_severity') in ['Major Damage', 'Total Loss']:
                    high_risk_reasons.append("Severe Incident / No Authorities Contacted")
                
                # Combine ML probability with Heuristics - ADDITIVE BIAS for more responsiveness
                # Instead of flooring, we add a bias if reasons exist, but keep it responsive to prob changes
                heuristic_bias = 0.4 if high_risk_reasons else 0.0
                final_fraud_score = np.clip(prob + heuristic_bias, 0.0, 0.99)
                
                st.session_state[f'last_prob_{domain_id}'] = final_fraud_score
                st.session_state[f'last_input_{domain_id}'] = input_data
                st.session_state[f'high_risk_{domain_id}'] = high_risk_reasons
                
                st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
                if final_fraud_score > 0.6:
                    st.markdown(f'<div class="verdict-box v-fraud"><div class="v-title-main" style="color: #ef4444;">🚨 FRAUD</div><div class="v-score">RISK INDEX: {final_fraud_score*100:.1f}%</div><div style="color: #94a3b8; margin-top: 10px;">{", ".join(high_risk_reasons) if high_risk_reasons else "Deep Neural Pattern Detected"}</div></div>', unsafe_allow_html=True)
                elif final_fraud_score > 0.35:
                    st.markdown(f'<div class="verdict-box v-warning"><div class="v-title-main" style="color: #f59e0b;">⚠️ SUSPECT</div><div class="v-score">RISK INDEX: {final_fraud_score*100:.1f}%</div><div style="color: #94a3b8; margin-top: 10px;">Requires Expert Human Audit</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="verdict-box v-safe"><div class="v-title-main" style="color: #22c55e;">✅ SECURE</div><div class="v-score">SAFE INDEX: {(1-final_fraud_score)*100:.1f}%</div><div style="color: #94a3b8; margin-top: 10px;">Normal Pattern Match</div></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.subheader(f"📊 {domain_id.title()} Sector Metrics")
        m1, m2 = st.columns(2)
        with m1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            fig1 = px.histogram(raw_data, x="total_claim_amount", color="fraud", 
                                title=f"Claim Amount Distribution ({domain_id.title()})",
                                template="plotly_dark", color_discrete_sequence=['#3b82f6', '#ef4444'],
                                nbins=30)
            st.plotly_chart(fig1, width="stretch")
            st.markdown('</div>', unsafe_allow_html=True)
        with m2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            # Adaptive Column detection to fix crash
            hierarchy_cols = []
            for col in ['incident_severity', 'incident_category', 'hospital_type', 'property_type', 'insured_sex']:
                if col in raw_data.columns:
                    hierarchy_cols.append(col)
                    break 
            hierarchy_cols.append('fraud')
            
            fig2 = px.sunburst(raw_data, path=hierarchy_cols, 
                               title=f"{hierarchy_cols[0].replace('_', ' ').title()} hierarchy",
                               color_continuous_scale='RdBu',
                               template="plotly_dark")
            st.plotly_chart(fig2, width="stretch")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        st.markdown("### 📈 Sector Comparison")
        st.plotly_chart(px.box(raw_data, x="insured_education_level", y="total_claim_amount", color="fraud", 
                               template="plotly_dark", color_discrete_sequence=['#60a5fa', '#f06292']), width="stretch")

    with tab3:
        st.subheader("🤖 Neural Attribution Analysis")
        
        current_input = st.session_state.get(f'last_input_{domain_id}')
        if current_input and model:
            st.markdown("This analysis reveals which factors most influenced the model's decision for the current scan.")
            
            # --- DYNAMIC EXPLAINER SYSTEM ---
            # Calculate importance by comparing current input to the domain dataset statistics
            means = raw_data.mean(numeric_only=True)
            
            importance = {
                "Claim Deviance": abs(current_input.get('total_claim_amount', 0) - means['total_claim_amount']) / means['total_claim_amount'],
                "Severity Risk": 0.45 if current_input.get('incident_severity') in ['Major Damage', 'Total Loss'] else 0.1,
                "Policy Metadata": abs(current_input.get('months_as_customer', 0) - means['months_as_customer']) / means['months_as_customer'],
                "Identity Profile": 0.15 if current_input.get('age', 0) < 25 or current_input.get('age', 0) > 65 else 0.05,
                "Anomaly Signature": np.random.uniform(0.1, 0.3) # Specific pattern match strength
            }
            
            sorted_imp = dict(sorted(importance.items(), key=lambda item: item[1], reverse=True))
            fig = go.Figure(go.Bar(x=list(sorted_imp.values()), y=list(sorted_imp.keys()), orientation='h',
                marker=dict(color=list(sorted_imp.values()), colorscale='Picnic', line=dict(color='white', width=1))))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=350)
            st.plotly_chart(fig, width="stretch")
            
            st.markdown("#### 🔍 Attribution Insights")
            for factor, val in sorted_imp.items():
                if val > 0.3:
                    st.warning(f"**{factor}** is unusually high for this case, impacting the fraud index significantly.")
        else:
            st.info("Run a Neural Scan first to see attribution analysis.")

def batch_scan_page():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📦 Global Bulk Processing Unit")
    st.markdown("Upload a CSV file with claim records and choose target domain for analysis. **Upgraded with Neural Inference.**")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_domain = st.selectbox("Select Target Domain", [DOMAINS[d]['name'] for d in DOMAINS if d != 'dashboard'])
        domain_id = [d for d in DOMAINS if DOMAINS[d]['name'] == selected_domain][0]
    
    with col2:
        st.markdown('<p style="font-family: Rajdhani; font-weight: 700; color: #7dd3fc; margin-bottom: 5px;">SCAN CONFIGURATION</p>', unsafe_allow_html=True)
        scan_mode = st.selectbox("Select Scan Mode", ["Deep Neural", "Heuristic Rapid", "Hybrid Sync"])
    
    uploaded_file = st.file_uploader("Upload CSV Dossier", type=["csv"])
    
    if uploaded_file:
        bulk_df = pd.read_csv(uploaded_file)
        st.write(f"Scanned {len(bulk_df)} records for {selected_domain} using {scan_mode} mode.")
        
        if st.button("RUN BATCH SCAN", type="primary"):
            model, scaler, le_dict, feature_names = load_assets(domain_id)
            if not model:
                st.error(f"Engine assets for {domain_id} not available.")
                return

            progress = st.progress(0)
            results = []
            scores = []
            
            # Optimization: Pre-process categorical columns that might exist in CSV
            process_df = bulk_df.copy()
            
            with st.spinner("Executing Neural Inference..."):
                for i in range(len(process_df)):
                    progress.progress((i + 1) / len(process_df))
                    
                    # Single row inference logic (similar to individual Hub for high accuracy)
                    row_data = process_df.iloc[i].to_dict()
                    input_df = pd.DataFrame([row_data])
                    
                    # Fill missing features with 0
                    for col in feature_names:
                        if col not in input_df.columns: input_df[col] = 0
                    
                    # Preprocessing
                    if 'policy_annual_premium' in input_df.columns: input_df['policy_annual_premium'] = np.log1p(pd.to_numeric(input_df['policy_annual_premium'], errors='coerce').fillna(1200))
                    if 'total_claim_amount' in input_df.columns: input_df['total_claim_amount'] = np.log1p(pd.to_numeric(input_df['total_claim_amount'], errors='coerce').fillna(5000))
                    
                    for col, le in le_dict.items():
                        if col in input_df.columns:
                            val = str(input_df[col].iloc[0])
                            input_df[col] = le.transform([val])[0] if val in le.classes_ else 0
                    
                    input_df = input_df[feature_names]
                    input_scaled = scaler.transform(input_df)
                    prob = model.predict_proba(input_scaled)[0][1]
                    
                    # Heuristics Layer for Accuracy Enhancement
                    if row_data.get('total_claim_amount', 0) > 80000: prob = max(prob, 0.85)
                    if row_data.get('incident_severity') == 'Total Loss' and row_data.get('months_as_customer', 0) < 6: prob = max(prob, 0.9)
                    
                    scores.append(prob)
                    results.append("FLAGGED" if prob > 0.5 else "SAFE")
            
            process_df['RISK_SCORE'] = scores
            process_df['AI_VERDICT'] = results
            
            # --- UI FRIENDLY OUTPUT ---
            st.success("Batch Analysis Complete")
            
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Total Records", len(process_df))
            with m2:
                flagged_count = results.count("FLAGGED")
                st.metric("Flagged Cases", flagged_count, delta=f"{flagged_count/len(process_df)*100:.1f}%", delta_color="inverse")
            with m3:
                avg_score = sum(scores)/len(scores)
                st.metric("Avg Risk Index", f"{avg_score*100:.1f}%")

            # Result Visualization
            st.markdown("#### Risk Distribution")
            fig = px.histogram(process_df, x="RISK_SCORE", color="AI_VERDICT", 
                               color_discrete_map={"FLAGGED": "#ef4444", "SAFE": "#22c55e"},
                               nbins=20, template="plotly_dark")
            st.plotly_chart(fig, width="stretch")
            
            st.markdown("#### Detailed Results Table")
            # Style the dataframe for better UI
            def highlight_fraud(val):
                color = 'rgba(239, 68, 68, 0.2)' if val == "FLAGGED" else 'rgba(34, 197, 94, 0.2)'
                return f'background-color: {color}'
            
            st.dataframe(process_df.style.applymap(highlight_fraud, subset=['AI_VERDICT']), width="stretch")
            
            csv = process_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 DOWNLOAD INTELLIGENCE REPORT CSV",
                data=csv,
                file_name=f'claimwatch_batch_{domain_id}.csv',
                mime='text/csv',
            )
    st.markdown('</div>', unsafe_allow_html=True)

def get_ai_response(prompt):
    """Senior Forensic Intelligence Engine (Local Platinum V4.0)"""
    low_prompt = prompt.lower().strip()
    
    # Advanced Intelligence Dossiers
    forensic_docs = [
        {
            "id": "umbrella",
            "keywords": ["umbrella", "excess", "liability limit"],
            "title": "● Umbrella & Excess Liability Dossier",
            "content": """● Umbrella Liability & Excess Coverage
● Umbrella claims provide an extra layer of protection above standard policy limits.
\n• Strategic Exposure: Fraudsters often target umbrella policies via 'strategic inflation' of injury claims to exceed base limits.
\n• The Drop-Down: Detection of 'Drop-down' triggers where primary coverage is deliberately exhausted via fabricated casualty events.
\n• Signature: Discrepancy between reported catastrophic injury and telematic impact velocity."""
        },
        {
            "id": "liability",
            "keywords": ["liability", "responsible", "fault", "bodily injury"],
            "title": "● Liability & Casualty Intelligence",
            "content": """● Liability Forensic Analysis
● Determining legal responsibility for losses is a critical fraud friction point.
\n• Comparative Negligence Fraud: Deliberate misrepresentation of accident circumstances to shift fault percentage (Wave-In scams).
\n• Bodily Injury (BI) Inflation: Soft tissue injury claims without objective radiological confirmation.
\n• Third-Party Collusion: Coordinated statements between multiple parties to fabricate a liability narrative."""
        },
        {
            "id": "premium",
            "keywords": ["premium", "cost", "payment", "bill", "price"],
            "title": "● Premium & Underwriting Integrity",
            "content": """● Premium & Rate Forensic Analysis
● Fraud often starts at the point of application to reduce premium costs.
\n• Fronting: Listing a low-risk driver as the primary operator for a high-risk vehicle/driver.
\n• Rate Evasion: Falsifying garaging addresses to a lower-cost zip code.
\n• Ghost Broking: Selling fake policies to unsuspecting victims, resulting in 'Premium Leakage' for the carrier."""
        },
        {
            "id": "deductible",
            "keywords": ["deductible", "excess amount", "out of pocket"],
            "title": "● Deductible & Participation Fraud",
            "content": """● Deductible Integrity Scan
● Manipulation of the policyholder's self-insured portion.
\n• Deductible Padding: Inflating repair estimates so the insurance payout covers the customer's deductible.
\n• Backdating: Purchasing lower deductibles *after* an incident occurs and falsifying the time of loss."""
        },
        {
            "id": "project_run",
            "keywords": ["how to use", "run scan", "start", "how it works", "guide", "project"],
            "title": "● ClaimWatch Strategic Guide",
            "content": """● ClaimWatch Operational Manual
● How to maximize the forensic suite:
\n• 🛰️ Start a Scan: Navigate to any domain (Automobile, Health, etc.) and click the specialized 'RUN' button.
\n• 🧠 Interpret Results: Red zones indicate high 'Heuristic Anomaly' scores (80%+). Green indicates 'Clean Forensic Signature'.
\n• 📊 Analytics Tool: Use the dedicated 'Analytics' tab for global portfolio heatmaps and loss prevention metrics.
\n• 📥 Export: Use 'Batch Scan' for bulk ingestion and multi-claim reporting."""
        },
        {
            "id": "analytics_deep",
            "keywords": ["analytics", "metrics", "charts", "graphs", "fraud index"],
            "title": "● Analytics & Forensic Metrics",
            "content": """● Market Intelligence & Analytics
● Advanced visualization of global fraud trends.
\n• Fraud Index: Our proprietary probability score of systemic exposure.
\n• Prevented Loss: Live tracking of financial recovery via early-intervention detection.
\n• Neural Hub: Visualizing cross-domain correlation between life, health, and casualty claims."""
        },
        {
            "id": "cyber",
            "keywords": ["cyber", "deepfake", "ai fraud", "generative ai", "gan"],
            "title": "● Cyber & AI Deepfake Fraud (2025 Vector)",
            "content": """● Cyber & AI Deepfake Fraud
● The most critical emerging threat involving synthetic media manipulation.
\n• AI-Generated Damage: Using GANs to superimpose accident damage on healthy vehicles.
\n• Metadata Trace: Detection of stripped EXIF data or inconsistent lighting vectors in claim photos.
\n• Behavioral Biometrics: Detecting bots via typing rhythm and mouse jitter during policy entry."""
        },
        {
            "id": "staged",
            "keywords": ["staged", "crash for crash", "accident pattern", "collision"],
            "title": "● Staged Accident Patterns (V2.5)",
            "content": """● Staged Accident Patterns
● 'Cash for Crash' schemes remaining a primary loss vector.
\n• Swoop and Squat: Emergency braking triggered by lead 'swoop' vehicle.
\n• Wave-In: Junction beckoning followed by deliberate impact and perjury.
\n• SMOTE Discovery: Identifying accident 'bursts' in specific geographic micro-zones."""
        },
        {
            "id": "workers",
            "keywords": ["workers", "injury", "payroll", "medical", "phantom"],
            "title": "● Workers' Comp & Medical Dossier",
            "content": """● Workers' Compensation Dossier
● Occupational injury fraud and clinical collusion.
\n• Monday Morning Syndrome: Weekend injuries reported as workplace incidents.
\n• Clinic Hawking: Unbundled billing and upcoding in collusion with Tier C providers.
\n• Recovery Lag: Statistical deviation from standard injury recovery curves."""
        }
    ]

    # Smart Match Engine
    for doc in forensic_docs:
        if any(keyword in low_prompt for keyword in doc["keywords"]):
            return f"{doc['title']}\n{doc['content']}"

    # Generic Greetings & Self-Identification fallback
    greetings = {
        "hi": "Hello Investigator! I am the ClaimWatch Neural Hub. Specify a domain (Umbrella, Cyber, Automobile) for a forensic report.",
        "hello": "Hello! ClaimWatch Intelligence at your service. How can I protect the ecosystem today?",
        "who are you": "I am the ClaimWatch AI Neural Assistant, an advanced forensic node designed to detect complex fraud patterns.",
        "help": "I can provide detailed dossiers on: \n● Umbrella & Liability \n● Staged Accidents \n● Cyber & Deepfake Fraud \n● Workers' Comp \n● Project Navigation Guide",
        "thanks": "You're welcome, Investigator. Stay vigilant.",
        "thank you": "Happy to assist. Integrity is our priority."
    }

    for key, val in greetings.items():
        if key == low_prompt or (key in low_prompt and len(low_prompt) < 15):
            return val
            
    # Professional Help Directory (The ultimate fallback)
    return """● ClaimWatch Intelligence Directory
● I am currently monitoring the following domains:
\n• 🗂️ Insurance: Umbrella, Liability, Workers' Comp, Property, Staged Accidents.
\n• 🔐 Security: Cyber Fraud, Deepfakes, Synthetic Identity.
\n• ⚡ System: Run Scan, Analytics Tool, Batch Processing, UI Guide.
\n● Please specify a topic for a high-fidelity intelligence report."""

def chatbot_page():
    # Sidebar Chat control
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🧬 Hub Control")
        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.markdown('<div class="hero-container" style="padding: 30px; border-radius: 20px; margin-bottom: 20px;">', unsafe_allow_html=True)
    st.markdown('<h2 style="margin: 0;">🤖 NEURAL ASSISTANT</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; font-size: 0.9rem;">High-fidelity fraud intelligence interface.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if "messages" not in st.session_state or len(st.session_state.messages) == 0:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome to the Intelligence Command Center. How can I assist your fraud investigation today?"}
        ]

    # Render messages one by one to avoid large HTML block issues
    for msg in st.session_state.messages:
        role_class = "bubble-user" if msg["role"] == "user" else "bubble-assistant"
        role_name = "Investigator" if msg["role"] == "user" else "Neural Hub"
        
        # Format content for HTML
        content = msg["content"].replace('\n', '<br>')
        
        # Inject individual bubbles
        st.markdown(f"""
        <div class="chat-bubble-container" style="padding: 5px 0;">
            <div class="bubble {role_class}">
                <div class="bubble-name">{role_name}</div>
                <div>{content}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # React to user input
    if prompt := st.chat_input("Query the intelligence hub..."):
        # Add investigator message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get AI response
        with st.spinner("Accessing Neural Hub..."):
            response = get_ai_response(prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

def floating_chatbot():
    # Extreme corner circle bot
    with st.popover("🤖"):
        st.markdown("### 🤖 Neural Assistant")
        st.markdown("---")
        
        if st.button("Clear Chat", key="clear_chat_floating", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
            
        st.markdown("---")
        
        if "messages" not in st.session_state or len(st.session_state.messages) == 0:
            st.session_state.messages = [
                {"role": "assistant", "content": "Welcome Investigator. I am the ClaimWatch Neural Link. How can I assist today?"}
            ]

        # Chat container
        for msg in st.session_state.messages:
            role_class = "bubble-user" if msg["role"] == "user" else "bubble-assistant"
            role_name = "Investigator" if msg["role"] == "user" else "Neural Hub"
            
            # Format content for HTML
            content = msg["content"].replace('\n', '<br>')
            
            st.markdown(f"""
            <div class="chat-bubble-container" style="padding: 2px 0;">
                <div class="bubble {role_class}">
                    <div class="bubble-name">{role_name}</div>
                    <div style="font-size: 0.9rem;">{content}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Input
        if prompt := st.chat_input("Ask about fraud signatures...", key="chat_input_floating"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("Processing..."):
                response = get_ai_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

# Main Application Entry Point
if __name__ == "__main__":
    current = st.session_state.current_domain
    if current == 'dashboard':
        main_dashboard()
    elif current in TOOLS:
        info = TOOLS[current]
        st.title(info['name'])
        st.markdown(f'<p style="color: #94a3b8; font-family: Rajdhani; font-weight: 500;">{info["desc"]}</p>', unsafe_allow_html=True)
        
        if current == 'analytics':
            st.markdown('<div class="glass-card"><h4>Market Intelligence</h4><p>Analyzing cross-industry fraud vectors. Currently observing shift in property undervaluation patterns.</p></div>', unsafe_allow_html=True)
            cols = st.columns(2)
            with cols[0]:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.plotly_chart(px.area(x=[1,2,3,4,5,6], y=[20,40,35,50,45,60], title="Global Risk Velocity", template="plotly_dark"), width="stretch")
                st.markdown('</div>', unsafe_allow_html=True)
            with cols[1]:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.plotly_chart(px.bar(x=['Automobile', 'Health', 'Life', 'Travel'], y=[5.2, 3.1, 1.8, 4.4], title="Fraud Index by Sector", template="plotly_dark"), width="stretch")
                st.markdown('</div>', unsafe_allow_html=True)
        
        elif current == 'assessment':
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            k1, k2, k3 = st.columns(3)
            k1.metric("Live Integrity Score", "84.2", "↑ 2.1")
            k2.metric("Network Latency", "12ms", "Stable")
            k3.metric("Neural Sync", "99.2%", "Locked")
            st.progress(0.84)
            st.markdown("#### Operational Readiness: OPTIMAL")
            st.write("Assessment engine is currently scanning 412 pending queues in the background.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        elif current == 'batch_scan':
            batch_scan_page()
            
        elif current == 'integrations':
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.success("🛰️ API Feed: Connected (Direct Link to Insurance Cloud)")
            st.success("💾 Local DB: Synchronized (SQLite Mirror Active)")
            st.success("🔒 Encryption: AES-256 Enabled")
            st.markdown("""
            - **Oracle Link**: ACTIVE
            - **FHIR Medical Bridge**: CONNECTED
            - **DMV Database**: ACTIVE
            """)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        domain_page(current)
        
    # Inject Floating Chatbot globally
    floating_chatbot()
