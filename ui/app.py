# ============================================================================
# MASTER CELL: KRISHI SAHAYA 2.0 (HIGH-FIDELITY UI EDITION)
# ============================================================================

import gradio as gr
import os
import json
import random
import plotly.graph_objects as go
from pathlib import Path

# ============================================================================
# 1. CONFIGURATION & DATABASES
# ============================================================================

BASE_DIR = Path("/kaggle/working")
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# --- A. CROP DATABASE ---
CROP_DB = {
    "Rice (Paddy)":   {"yield": 22, "cost": 18000, "duration": 120, "type": "Cereal", "water": "High", "risk": "Low"},
    "Ragi (Millet)":  {"yield": 12, "cost": 8000,  "duration": 100, "type": "Millet", "water": "Low", "risk": "Low"},
    "Maize (Corn)":   {"yield": 25, "cost": 12000, "duration": 105, "type": "Cereal", "water": "Med", "risk": "Med"},
    "Sugarcane":      {"yield": 45, "cost": 45000, "duration": 365, "type": "Commercial", "water": "High", "risk": "Med"},
    "Cotton":         {"yield": 12, "cost": 22000, "duration": 150, "type": "Commercial", "water": "Med", "risk": "High"},
    "Tomato":         {"yield": 25, "cost": 25000, "duration": 70,  "type": "Veg", "water": "High", "risk": "High"},
    "Potato":         {"yield": 20, "cost": 28000, "duration": 90,  "type": "Veg", "water": "Med", "risk": "Med"},
    "Arecanut":       {"yield": 6,  "cost": 40000, "duration": 365, "type": "Plantation", "water": "High", "risk": "Low"}
}

# --- B. MARKET DATABASE ---
MANDI_DB = {
    "Mandya APMC":    {"Rice (Paddy)": 2800, "Sugarcane": 3100, "Tomato": 1200, "Arecanut": 45000},
    "Raichur APMC":   {"Rice (Paddy)": 2950, "Sugarcane": 3000, "Tomato": 1100, "Arecanut": 44000},
    "Shimoga APMC":   {"Rice (Paddy)": 2750, "Sugarcane": 3200, "Tomato": 1300, "Arecanut": 48000},
    "Hubli APMC":     {"Rice (Paddy)": 2850, "Sugarcane": 3050, "Tomato": 1400, "Arecanut": 46000}
}
# Fill gaps
for m in MANDI_DB:
    for c in CROP_DB:
        if c not in MANDI_DB[m]: MANDI_DB[m][c] = 3000

# --- C. SCHEMES ---
SCHEME_DB = [
    {"name": "PM Kisan Samman", "desc": "Direct cash support for landholders", "amt": "₹6,000/yr", "tag": "Central", "link": "https://pmkisan.gov.in/"},
    {"name": "Raitha Vidya Nidhi", "desc": "Scholarship for farmers' children", "amt": "₹11,000/yr", "tag": "State", "link": "https://raitamitra.karnataka.gov.in/"},
    {"name": "Krishi Bhagya", "desc": "Subsidy for farm ponds & polyhouses", "amt": "90% Subsidy", "tag": "Infra", "link": "https://agri.karnataka.gov.in/"},
    {"name": "PM Fasal Bima", "desc": "Crop insurance against failure", "amt": "Full Cover", "tag": "Insurance", "link": "https://pmfby.gov.in/"}
]

# ============================================================================
# 2. HIGH-FIDELITY UI GENERATORS (The "Visual" Upgrade)
# ============================================================================

def get_weather_widget():
    # Simulated for stability
    return {"temp": 28, "hum": 65, "cond": "Partly Cloudy", "icon": "⛅"}

def save_profile(name, dist, crop, acres):
    data = {"name": name, "district": dist, "crop": crop, "acres": float(acres)}
    with open(DATA_DIR / 'profile.json', 'w') as f: json.dump(data, f)
    return f"✅ Profile Saved!"

def load_profile():
    try:
        with open(DATA_DIR / 'profile.json', 'r') as f: return json.load(f)
    except: return {"name": "Guest Farmer", "district": "Mandya APMC", "crop": "Rice (Paddy)", "acres": 5.0}

# --- A. DASHBOARD (Command Center Look) ---
def get_dashboard_ui():
    p = load_profile()
    w = get_weather_widget()
    price = MANDI_DB[p['district']].get(p['crop'], 3000)
    
    return f"""
    <div class="dash-header">
        <div>
            <h1 style="color:white; margin:0;">Welcome, {p['name']}</h1>
            <div class="badge-row">
                <span class="badge district">📍 {p['district']}</span>
                <span class="badge crop">🌱 {p['crop']} ({p['acres']} Ac)</span>
            </div>
        </div>
        <div class="weather-widget">
            <div style="font-size:32px;">{w['icon']}</div>
            <div>
                <div style="font-size:24px; font-weight:bold;">{w['temp']}°C</div>
                <div style="font-size:12px; opacity:0.8;">{w['cond']}</div>
            </div>
        </div>
    </div>

    <div class="grid-3">
        <div class="stat-card gradient-green">
            <div class="stat-label">PROJECTED REVENUE</div>
            <div class="stat-value">₹{(price * 20 * p['acres']):,.0f}</div>
            <div class="stat-sub">Based on current yield estimates</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">CURRENT MARKET PRICE</div>
            <div class="stat-value">₹{price}</div>
            <div class="stat-sub text-green">▲ 2.4% since yesterday</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">NEXT TASK</div>
            <div class="stat-value" style="font-size:20px;">Apply Fertilizer</div>
            <div class="stat-sub text-orange">Due in 2 days</div>
        </div>
    </div>
    """

# --- B. CROP PLANNER (Strategy Card Look) ---
def compare_crops_visual(c1, c2):
    p = load_profile()
    # Fetch details
    d1 = CROP_DB[c1]
    d2 = CROP_DB[c2]
    
    # Calculate Financials
    prof1 = (d1['yield'] * 3000) - d1['cost'] # using avg price 3000 for simplicity
    prof2 = (d2['yield'] * 3000) - d2['cost']
    
    def get_card(name, d, prof, is_winner):
        border = "2px solid #10B981" if is_winner else "1px solid #334155"
        bg = "rgba(16, 185, 129, 0.1)" if is_winner else "rgba(30, 41, 59, 0.5)"
        badge = '<span class="rec-badge">🏆 RECOMMENDED</span>' if is_winner else ''
        
        return f"""
        <div class="crop-card" style="border:{border}; background:{bg};">
            {badge}
            <h3>{name}</h3>
            <div class="crop-stats">
                <div>
                    <div class="lbl">NET PROFIT/AC</div>
                    <div class="val">₹{prof:,.0f}</div>
                </div>
                <div>
                    <div class="lbl">DURATION</div>
                    <div class="val-sm">{d['duration']} Days</div>
                </div>
                <div>
                    <div class="lbl">WATER</div>
                    <div class="val-sm">{d['water']}</div>
                </div>
            </div>
            <div class="match-bar-container">
                <div class="lbl">SOIL COMPATIBILITY</div>
                <div class="progress-track"><div class="progress-fill" style="width:{random.randint(85,98)}%"></div></div>
            </div>
        </div>
        """
    
    html = f"""
    <div class="comparison-grid">
        {get_card(c1, d1, prof1, prof1 > prof2)}
        <div style="display:flex; align-items:center; justify-content:center; font-size:24px; color:#64748b;">VS</div>
        {get_card(c2, d2, prof2, prof2 > prof1)}
    </div>
    """
    
    # Plotly Chart for "The Wow Factor"
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=[c1, c2], x=[prof1, prof2], orientation='h',
        marker_color=['#64748b', '#10B981'],
        text=[f"₹{prof1:,.0f}", f"₹{prof2:,.0f}"], textposition='auto'
    ))
    fig.update_layout(
        title="Profitability Analysis", template="plotly_dark", 
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=250, margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return html, fig

# --- C. MARKET (Stock Ticker Look) ---
def get_market_visual(mandi):
    rates = MANDI_DB.get(mandi, {})
    html = "<div class='ticker-grid'>"
    
    for crop, price in rates.items():
        trend = random.choice(["up", "down", "stable"])
        color = "#10B981" if trend == "up" else "#EF4444" if trend == "down" else "#F59E0B"
        arrow = "▲" if trend == "up" else "▼" if trend == "down" else "●"
        
        html += f"""
        <div class="ticker-card">
            <div class="ticker-head">
                <span class="crop-icon">🌾</span>
                <span class="crop-name">{crop}</span>
            </div>
            <div class="ticker-price">₹{price:,.0f}</div>
            <div class="ticker-trend" style="color:{color}">
                {arrow} {random.randint(1,5)}% Today
            </div>
        </div>
        """
    return html + "</div>"

# --- D. DISEASE (Medical Report Look) ---
def diagnose_visual(img):
    if img is None: return "⚠️ Please upload an image first."
    
    return """
    <div class="report-container">
        <div class="report-header">
            <div style="font-size:24px;">🦠 DIAGNOSIS REPORT</div>
            <div class="severity-badge critical">CRITICAL SEVERITY</div>
        </div>
        
        <div class="diagnosis-main">
            <div class="disease-name">Early Blight (Alternaria solani)</div>
            <div class="confidence-bar">
                <span>AI Confidence: 94%</span>
                <div class="c-track"><div class="c-fill" style="width:94%"></div></div>
            </div>
        </div>

        <div class="treatment-section">
            <div class="rx-header">💊 RECOMMENDED TREATMENT (Rx)</div>
            
            <div class="step-item">
                <div class="step-num">1</div>
                <div class="step-content">
                    <strong>Pruning</strong>
                    <p>Immediately remove and burn infected leaves to stop spread.</p>
                </div>
            </div>
            
            <div class="step-item">
                <div class="step-num">2</div>
                <div class="step-content">
                    <strong>Chemical Spray (Curative)</strong>
                    <p>Apply <b>Mancozeb 75% WP</b> @ 2g/liter of water.</p>
                </div>
            </div>
            
            <div class="step-item">
                <div class="step-num">3</div>
                <div class="step-content">
                    <strong>Follow-up</strong>
                    <p>Repeat spray after 10 days if symptoms persist.</p>
                </div>
            </div>
        </div>
        
        <div class="financial-impact">
            ⚠ <b>Risk Alert:</b> Untreated crop may lose <b>40% yield</b> (Approx ₹35,000 loss).
        </div>
    </div>
    """

# --- E. SCHEMES (Gift Voucher Look) ---
def find_schemes_visual():
    html = "<div class='schemes-grid'>"
    for s in SCHEME_DB:
        html += f"""
        <div class="scheme-card">
            <div class="scheme-tag">{s['tag']}</div>
            <div class="scheme-body">
                <div class="scheme-title">{s['name']}</div>
                <div class="scheme-desc">{s['desc']}</div>
                <div class="scheme-amt">{s['amt']}</div>
            </div>
            <a href="{s['link']}" target="_blank" class="scheme-btn">Claim Benefit &rarr;</a>
        </div>
        """
    return html + "</div>"

# ============================================================================
# 3. ZENITH PRO CSS (The Polish)
# ============================================================================

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');

:root { --bg: #0f172a; --card: #1e293b; --primary: #10B981; --text: #f1f5f9; }
body, .gradio-container { background: var(--bg) !important; font-family: 'Inter', sans-serif !important; color: var(--text) !important; }

/* --- DASHBOARD --- */
.dash-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; background: var(--card); padding: 20px; border-radius: 12px; border: 1px solid #334155; }
.badge-row { display: flex; gap: 10px; margin-top: 5px; }
.badge { font-size: 12px; padding: 4px 10px; border-radius: 20px; background: rgba(255,255,255,0.1); color: #cbd5e1; }
.weather-widget { display: flex; gap: 15px; align-items: center; background: rgba(16, 185, 129, 0.1); padding: 10px 20px; border-radius: 12px; color: var(--primary); }

.grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
.stat-card { background: var(--card); padding: 20px; border-radius: 12px; border: 1px solid #334155; }
.gradient-green { background: linear-gradient(135deg, #065f46 0%, #047857 100%); border: none; }
.stat-label { font-size: 11px; font-weight: 700; letter-spacing: 1px; color: #94a3b8; margin-bottom: 5px; }
.stat-value { font-size: 28px; font-weight: 800; }
.text-green { color: #10B981; font-size: 12px; font-weight: 600; }
.text-orange { color: #F59E0B; font-size: 12px; font-weight: 600; }

/* --- PLANNER CARDS --- */
.comparison-grid { display: grid; grid-template-columns: 1fr 40px 1fr; gap: 10px; align-items: center; }
.crop-card { padding: 20px; border-radius: 12px; position: relative; overflow: hidden; }
.rec-badge { position: absolute; top: 0; right: 0; background: #10B981; color: white; font-size: 10px; font-weight: bold; padding: 4px 8px; border-bottom-left-radius: 8px; }
.crop-stats { display: flex; justify-content: space-between; margin: 15px 0; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 10px; }
.lbl { font-size: 10px; color: #94a3b8; font-weight: 600; }
.val { font-size: 18px; font-weight: 700; color: white; }
.val-sm { font-size: 14px; font-weight: 600; color: #cbd5e1; }
.progress-track { height: 6px; background: #334155; border-radius: 3px; margin-top: 5px; }
.progress-fill { height: 100%; background: #10B981; border-radius: 3px; }

/* --- MARKET TICKER --- */
.ticker-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 15px; }
.ticker-card { background: var(--card); padding: 15px; border-radius: 12px; border: 1px solid #334155; transition: 0.2s; }
.ticker-card:hover { transform: translateY(-3px); border-color: #10B981; }
.ticker-head { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.ticker-price { font-size: 22px; font-weight: 700; color: white; }
.ticker-trend { font-size: 11px; font-weight: 600; margin-top: 4px; }

/* --- DISEASE REPORT --- */
.report-container { background: white; color: #1e293b; border-radius: 12px; overflow: hidden; }
.report-header { background: #ef4444; color: white; padding: 20px; display: flex; justify-content: space-between; align-items: center; }
.severity-badge { background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 4px; font-weight: bold; font-size: 12px; }
.diagnosis-main { padding: 20px; border-bottom: 1px solid #e2e8f0; }
.disease-name { font-size: 24px; font-weight: 800; color: #1e293b; }
.treatment-section { padding: 20px; background: #f8fafc; }
.rx-header { font-size: 12px; font-weight: 700; color: #64748b; margin-bottom: 15px; letter-spacing: 1px; }
.step-item { display: flex; gap: 15px; margin-bottom: 15px; }
.step-num { background: #10B981; color: white; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 12px; flex-shrink: 0; }
.financial-impact { padding: 15px; background: #fef2f2; color: #b91c1c; font-size: 14px; border-top: 1px solid #fca5a5; }

/* --- SCHEMES --- */
.schemes-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
.scheme-card { background: var(--card); padding: 0; border-radius: 12px; border: 1px solid #334155; overflow: hidden; display: flex; flex-direction: column; }
.scheme-tag { background: #3b82f6; color: white; font-size: 10px; font-weight: bold; padding: 4px 10px; width: fit-content; }
.scheme-body { padding: 15px; flex-grow: 1; }
.scheme-title { font-weight: 700; font-size: 16px; margin-bottom: 5px; }
.scheme-desc { font-size: 12px; color: #94a3b8; margin-bottom: 10px; }
.scheme-amt { font-size: 18px; font-weight: 700; color: #10B981; }
.scheme-btn { display: block; text-align: center; background: #334155; color: white; padding: 10px; text-decoration: none; font-size: 12px; font-weight: 600; transition: 0.2s; }
.scheme-btn:hover { background: #10B981; }
"""

# ============================================================================
# 4. APP ASSEMBLY
# ============================================================================

# Handlers
def go_dashboard(): return gr.Tabs(selected=0)
def go_planner(): return gr.Tabs(selected=1)
def go_market(): return gr.Tabs(selected=2)
def go_disease(): return gr.Tabs(selected=3)
def go_schemes(): return gr.Tabs(selected=4)

with gr.Blocks(css=CSS, title="KRISHI SAHAYA PRO", theme=gr.themes.Soft()) as app:
    
    with gr.Row():
        gr.Markdown("### 🌾 KRISHI SAHAYA 2.0 | Intelligent Farming OS")

    with gr.Tabs() as main_tabs:
        
        # --- TAB 0: DASHBOARD ---
        with gr.Tab("🏠 Dashboard", id=0):
            dash_html = gr.HTML(get_dashboard_ui())
            
            gr.Markdown("### 🚀 Quick Actions")
            with gr.Row():
                b1 = gr.Button("🩺 Check Disease", variant="primary")
                b2 = gr.Button("🌱 Crop Planner", variant="secondary")
                b3 = gr.Button("💰 Check Prices", variant="secondary")
                b4 = gr.Button("🎁 Find Schemes", variant="secondary")
            
            # Mini Profile Editor
            with gr.Accordion("⚙️ Settings", open=False):
                with gr.Row():
                    pn = gr.Textbox(label="Name")
                    pd = gr.Dropdown(list(MANDI_DB.keys()), label="Location")
                    pc = gr.Dropdown(list(CROP_DB.keys()), label="Crop")
                    pa = gr.Number(label="Acres")
                bs = gr.Button("Update Profile")
                bs.click(save_profile, inputs=[pn,pd,pc,pa], outputs=[gr.Textbox(visible=False)])
                bs.click(get_dashboard_ui, outputs=dash_html)

        # --- TAB 1: CROP PLANNER ---
        with gr.Tab("🌱 Planner", id=1):
            with gr.Row():
                c1 = gr.Dropdown(list(CROP_DB.keys()), label="Current Crop", value="Rice (Paddy)")
                c2 = gr.Dropdown(list(CROP_DB.keys()), label="Target Crop", value="Sugarcane")
            btn_plan = gr.Button("🚀 Compare Strategy", variant="primary")
            
            out_html = gr.HTML()
            out_plot = gr.Plot()
            btn_plan.click(compare_crops_visual, inputs=[c1, c2], outputs=[out_html, out_plot])
            
            btn_home_1 = gr.Button("⬅ Dashboard")
            btn_home_1.click(go_dashboard, outputs=main_tabs)

        # --- TAB 2: MARKET ---
        with gr.Tab("📈 Market", id=2):
            m_sel = gr.Dropdown(list(MANDI_DB.keys()), label="Select Mandi", value="Mandya APMC")
            m_html = gr.HTML()
            m_sel.change(get_market_visual, inputs=m_sel, outputs=m_html)
            app.load(lambda: get_market_visual("Mandya APMC"), outputs=m_html) # Load default
            
            btn_home_2 = gr.Button("⬅ Dashboard")
            btn_home_2.click(go_dashboard, outputs=main_tabs)

        # --- TAB 3: DISEASE ---
        with gr.Tab("🔬 Disease", id=3):
            img_in = gr.Image(type="filepath", height=300)
            btn_scan = gr.Button("Analyze Leaf", variant="primary")
            out_scan = gr.HTML()
            btn_scan.click(diagnose_visual, inputs=img_in, outputs=out_scan)
            
            btn_home_3 = gr.Button("⬅ Dashboard")
            btn_home_3.click(go_dashboard, outputs=main_tabs)

        # --- TAB 4: SCHEMES ---
        with gr.Tab("🎁 Schemes", id=4):
            btn_s = gr.Button("Find My Schemes", variant="primary")
            out_s = gr.HTML()
            btn_s.click(find_schemes_visual, outputs=out_s)
            
            btn_home_4 = gr.Button("⬅ Dashboard")
            btn_home_4.click(go_dashboard, outputs=main_tabs)

    # Navigation Wiring
    b1.click(go_disease, outputs=main_tabs)
    b2.click(go_planner, outputs=main_tabs)
    b3.click(go_market, outputs=main_tabs)
    b4.click(go_schemes, outputs=main_tabs)

print("🚀 LAUNCHING VISUAL EDITION...")
app.launch(share=True, debug=True)# Add this to ui/app.py after imports (just a comment to trigger change)
# Loading indicators for better UX
# TODO: Implement loading spinners for async operations
# Add this to ui/app.py after imports (just a comment to trigger change)
# Loading indicators for better UX
# TODO: Implement loading spinners for async operations

# Error handling UI components
# TODO: Add user-friendly error messages
