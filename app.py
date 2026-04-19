import streamlit as st
from supabase import create_client, Client
import uuid
from datetime import datetime

# ─────────────────────────────────────────────
#  CONFIG & CONNECTION
# ─────────────────────────────────────────────
SUPABASE_URL = "https://xtjnatjxsxbyrwkqytqd.supabase.co"
SUPABASE_KEY = "sb_publishable_NPbMYsWC7UhEaVmMKga16w_LjITdW7w"

st.set_page_config(
    page_title="Jawhar ERP — Petty Cash",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS — ULTRA PREMIUM DARK GOLD THEME
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: #06080D;
    font-family: 'Inter', sans-serif;
    color: #EAE0CC;
    min-height: 100vh;
    background-image:
        radial-gradient(ellipse 100% 60% at 50% -10%, rgba(212,175,55,0.07) 0%, transparent 65%),
        radial-gradient(ellipse 50% 50% at 95% 85%,  rgba(212,175,55,0.04) 0%, transparent 55%),
        radial-gradient(ellipse 30% 30% at 5%  20%,  rgba(212,175,55,0.03) 0%, transparent 50%);
}

#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A0C12 0%, #080A0F 100%) !important;
    border-right: 1px solid rgba(212,175,55,0.18) !important;
    box-shadow: 4px 0 30px rgba(0,0,0,0.4) !important;
}
[data-testid="stSidebarContent"] { padding: 0 !important; }

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea textarea {
    background: rgba(255,255,255,0.025) !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
    border-radius: 10px !important;
    color: #EAE0CC !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.93rem !important;
    padding: 0.65rem 1rem !important;
    transition: border-color 0.25s, box-shadow 0.25s, background 0.25s;
    caret-color: #D4AF37;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: rgba(212,175,55,0.6) !important;
    background: rgba(212,175,55,0.04) !important;
    box-shadow: 0 0 0 3px rgba(212,175,55,0.08), 0 2px 12px rgba(0,0,0,0.3) !important;
    outline: none !important;
}
.stTextInput label, .stNumberInput label, .stTextArea label, .stSelectbox label {
    color: rgba(234,224,204,0.5) !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.025) !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
    border-radius: 10px !important;
    color: #EAE0CC !important;
}

.stButton > button {
    background: linear-gradient(135deg, #C9A227 0%, #F0D060 45%, #C9A227 100%) !important;
    color: #06080D !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.65rem 1.8rem !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(212,175,55,0.25), 0 1px 0 rgba(255,255,255,0.1) inset !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 35px rgba(212,175,55,0.4) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(212,175,55,0.12) !important;
    gap: 0 !important;
    padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: rgba(234,224,204,0.4) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.85rem 1.6rem !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    color: #D4AF37 !important;
    border-bottom: 2px solid #D4AF37 !important;
    background: transparent !important;
}

[data-testid="stFileUploader"] {
    border: 1.5px dashed rgba(212,175,55,0.25) !important;
    border-radius: 14px !important;
    background: rgba(212,175,55,0.015) !important;
    transition: all 0.25s !important;
    padding: 0.5rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(212,175,55,0.55) !important;
    background: rgba(212,175,55,0.03) !important;
}

[data-testid="stExpander"] {
    border: 1px solid rgba(212,175,55,0.12) !important;
    border-radius: 12px !important;
    background: rgba(255,255,255,0.015) !important;
    overflow: hidden !important;
}

.stSuccess > div {
    background: rgba(39,174,96,0.08) !important;
    border: 1px solid rgba(39,174,96,0.25) !important;
    border-left: 3px solid #27ae60 !important;
    color: #5dda8a !important;
    border-radius: 10px !important;
}
.stError > div {
    background: rgba(192,57,43,0.08) !important;
    border: 1px solid rgba(192,57,43,0.25) !important;
    border-left: 3px solid #c0392b !important;
    color: #e87060 !important;
    border-radius: 10px !important;
}
.stWarning > div {
    background: rgba(212,175,55,0.07) !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
    border-left: 3px solid #D4AF37 !important;
    border-radius: 10px !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(212,175,55,0.05) 0%, rgba(255,255,255,0.02) 100%) !important;
    border: 1px solid rgba(212,175,55,0.14) !important;
    border-radius: 14px !important;
    padding: 1.4rem 1.6rem !important;
    position: relative !important;
    overflow: hidden !important;
    transition: border-color 0.3s, box-shadow 0.3s !important;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(212,175,55,0.35), transparent);
}
[data-testid="stMetricLabel"] {
    color: rgba(234,224,204,0.45) !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
}
[data-testid="stMetricValue"] {
    color: #D4AF37 !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 2.1rem !important;
    font-weight: 600 !important;
    line-height: 1.1 !important;
}

hr { border: none !important; border-top: 1px solid rgba(212,175,55,0.1) !important; margin: 1.8rem 0 !important; }

/* ── CUSTOM COMPONENTS ── */
.page-wrap { padding: 2.5rem 3rem 4rem; max-width: 1100px; }
.page-header { margin-bottom: 2.5rem; }
.page-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.4rem; font-weight: 600; color: #EAE0CC;
    line-height: 1.1; letter-spacing: -0.01em;
}
.page-subtitle {
    font-size: 0.85rem; color: rgba(234,224,204,0.38);
    margin-top: 0.35rem; letter-spacing: 0.06em;
}
.title-line {
    width: 36px; height: 2px;
    background: linear-gradient(90deg, #D4AF37, #F0D060);
    border-radius: 2px; margin: 0.7rem 0 0;
}
.section-label {
    font-size: 0.7rem; font-weight: 600; color: #D4AF37;
    text-transform: uppercase; letter-spacing: 0.14em;
    margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;
}
.section-label::after {
    content: ''; flex: 1; height: 1px;
    background: rgba(212,175,55,0.12);
}
.req-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.025) 0%, rgba(212,175,55,0.02) 100%);
    border: 1px solid rgba(212,175,55,0.11);
    border-radius: 16px; padding: 1.5rem 1.8rem;
    margin-bottom: 0.85rem; position: relative;
    overflow: hidden; transition: border-color 0.25s, box-shadow 0.25s, transform 0.2s;
}
.req-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(212,175,55,0.25), transparent);
}
.req-card:hover {
    border-color: rgba(212,175,55,0.28);
    box-shadow: 0 10px 40px rgba(0,0,0,0.25), 0 0 0 1px rgba(212,175,55,0.05);
    transform: translateY(-1px);
}
.req-card .r-email { font-size: 0.72rem; color: rgba(234,224,204,0.38); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.3rem; }
.req-card .r-amount { font-family: 'Cormorant Garamond', serif; font-size: 1.7rem; font-weight: 600; color: #D4AF37; line-height: 1.1; }
.req-card .r-reason { font-size: 0.9rem; color: rgba(234,224,204,0.72); margin: 0.35rem 0 0.2rem; }
.req-card .r-meta { font-size: 0.72rem; color: rgba(234,224,204,0.3); margin-top: 0.4rem; }
.badge {
    display: inline-flex; align-items: center; gap: 0.3rem;
    padding: 0.22rem 0.8rem; border-radius: 20px;
    font-size: 0.68rem; font-weight: 600;
    letter-spacing: 0.09em; text-transform: uppercase;
}
.badge-pending  { background: rgba(241,196,15,0.12);  color: #f1c40f; border: 1px solid rgba(241,196,15,0.28); }
.badge-approved { background: rgba(39,174,96,0.12);   color: #4cd884; border: 1px solid rgba(39,174,96,0.28); }
.badge-rejected { background: rgba(192,57,43,0.12);   color: #e87060; border: 1px solid rgba(192,57,43,0.28); }
.branch-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.025) 0%, rgba(212,175,55,0.02) 100%);
    border: 1px solid rgba(212,175,55,0.11); border-radius: 16px;
    padding: 1.6rem 1.8rem; margin-bottom: 0.85rem;
    position: relative; overflow: hidden; transition: border-color 0.25s, box-shadow 0.25s;
}
.branch-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(212,175,55,0.2), transparent);
}
.branch-card:hover { border-color: rgba(212,175,55,0.28); box-shadow: 0 8px 30px rgba(0,0,0,0.2); }
.empty-state { text-align: center; padding: 3.5rem 2rem; color: rgba(234,224,204,0.3); }
.empty-state .icon { font-size: 2.5rem; margin-bottom: 0.75rem; opacity: 0.6; }
.empty-state .msg { font-size: 0.92rem; }

/* Sidebar nav buttons */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: rgba(234,224,204,0.55) !important;
    border: 1px solid rgba(212,175,55,0.08) !important;
    border-radius: 9px !important;
    font-size: 0.85rem !important;
    font-weight: 400 !important;
    box-shadow: none !important;
    padding: 0.6rem 1rem !important;
    text-align: left !important;
    transition: all 0.2s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(212,175,55,0.07) !important;
    color: #D4AF37 !important;
    border-color: rgba(212,175,55,0.25) !important;
    transform: none !important;
    box-shadow: none !important;
}

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(212,175,55,0.2); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(212,175,55,0.4); }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SUPABASE CLIENT
# ─────────────────────────────────────────────
@st.cache_resource
def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

for k, v in {"user": None, "page": "login"}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def format_iqd(amount) -> str:
    try:    return f"{float(amount):,.0f} IQD"
    except: return "0 IQD"

def format_date(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y · %H:%M")
    except: return iso or "—"

def status_badge(status: str) -> str:
    cfg = {
        "pending":  ("badge-pending",  "●", "Pending"),
        "approved": ("badge-approved", "●", "Approved"),
        "rejected": ("badge-rejected", "●", "Rejected"),
    }
    cls, icon, label = cfg.get(status, cfg["pending"])
    return f'<span class="badge {cls}">{icon} {label}</span>'

def upload_invoice_image(file_bytes: bytes, filename: str):
    try:
        ext = filename.rsplit(".", 1)[-1].lower()
        ct  = "application/pdf" if ext == "pdf" else f"image/{ext}"
        path = f"invoices/{uuid.uuid4()}.{ext}"
        supabase.storage.from_("invoices").upload(path=path, file=file_bytes, file_options={"content-type": ct})
        return supabase.storage.from_("invoices").get_public_url(path)
    except Exception as e:
        st.error(f"Image upload failed: {e}")
        return None

def fetch_all_requests():
    try:    return supabase.table("petty_cash_requests").select("*").order("created_at", desc=True).execute().data or []
    except: return []


# ─────────────────────────────────────────────
#  LOGIN PAGE
# ─────────────────────────────────────────────
def page_login():
    st.markdown("""
    <div style="min-height:100vh; display:flex; align-items:center; justify-content:center; padding:2rem;">
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        st.markdown("""
        <div style="text-align:center; margin-bottom:2rem;">
            <div style="font-size:2.8rem; margin-bottom:0.5rem; filter:drop-shadow(0 0 20px rgba(212,175,55,0.3));">💎</div>
            <div style="font-family:'Cormorant Garamond',serif; font-size:2.6rem; font-weight:700;
                 background:linear-gradient(135deg,#B8942A,#F0D060,#C9A227);
                 -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                 background-clip:text; letter-spacing:0.08em; line-height:1;">JAWHAR</div>
            <div style="font-size:0.68rem; color:rgba(234,224,204,0.28); letter-spacing:0.22em;
                 text-transform:uppercase; margin-top:0.4rem;">Petty Cash Management</div>
        </div>
        <div style="background:linear-gradient(160deg,rgba(255,255,255,0.035) 0%,rgba(212,175,55,0.02) 100%);
             border:1px solid rgba(212,175,55,0.18); border-radius:22px; padding:2.5rem 2.2rem;
             box-shadow:0 40px 100px rgba(0,0,0,0.55); position:relative; overflow:hidden;">
            <div style="position:absolute;top:0;left:50%;transform:translateX(-50%);
                 width:55%;height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,0.7),transparent);"></div>
            <div style="position:absolute;bottom:-60px;right:-60px;width:180px;height:180px;
                 background:radial-gradient(circle,rgba(212,175,55,0.05) 0%,transparent 70%);pointer-events:none;"></div>
        </div>
        """, unsafe_allow_html=True)

        email    = st.text_input("Email Address", placeholder="you@jawhar.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        if st.button("Sign In  →", use_container_width=True):
            if not email or not password:
                st.warning("Please enter your email and password.")
            else:
                with st.spinner("Verifying credentials…"):
                    try:
                        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                        st.session_state.user = res.user
                        st.rerun()
                    except:
                        st.error("Access denied. Please check your credentials.")

        st.markdown("""
        <p style="text-align:center;color:rgba(234,224,204,0.2);font-size:0.7rem;
           margin-top:1.5rem;letter-spacing:0.05em;">
            Restricted system · Authorized personnel only
        </p>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar(user_email: str, is_admin: bool):
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:1.8rem 1.4rem 1rem;">
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.5rem;font-weight:700;
                 background:linear-gradient(135deg,#C9A227,#F0D060,#C9A227);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                 background-clip:text;letter-spacing:0.06em;">💎 JAWHAR ERP</div>
            <div style="font-size:0.65rem;color:rgba(234,224,204,0.28);letter-spacing:0.18em;
                 text-transform:uppercase;margin-top:0.2rem;">
                {"Management" if is_admin else "Branch Portal"}
            </div>
        </div>
        <div style="margin:0 1rem;height:1px;
             background:linear-gradient(90deg,transparent,rgba(212,175,55,0.2),transparent);"></div>
        <div style="padding:1rem 1.4rem 0.5rem;">
            <div style="font-size:0.65rem;color:rgba(234,224,204,0.3);text-transform:uppercase;
                 letter-spacing:0.12em;margin-bottom:0.4rem;">Account</div>
            <div style="font-size:0.82rem;color:#D4AF37;font-weight:500;word-break:break-all;margin-bottom:1.4rem;">
                {user_email}
            </div>
        """, unsafe_allow_html=True)

        if is_admin:
            st.markdown("""
            <div style="font-size:0.65rem;color:rgba(234,224,204,0.3);text-transform:uppercase;
                 letter-spacing:0.12em;margin-bottom:0.6rem;">Navigation</div>
            """, unsafe_allow_html=True)
            for key, label in [
                ("admin_dashboard", "📊  Dashboard"),
                ("admin_all",       "📋  All Requests"),
                ("admin_branches",  "🏪  Branches"),
            ]:
                if st.button(label, use_container_width=True, key=f"nav_{key}"):
                    st.session_state.page = key
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="margin:0 1rem;height:1px;
             background:linear-gradient(90deg,transparent,rgba(212,175,55,0.12),transparent);
             margin-bottom:0.8rem;"></div>
        """, unsafe_allow_html=True)

        if st.button("⎋  Sign Out", use_container_width=True, key="signout"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()


# ─────────────────────────────────────────────
#  ADMIN — DASHBOARD
# ─────────────────────────────────────────────
def page_admin_dashboard():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Command Center</div>
        <div class="page-subtitle">Real-time overview of all petty cash activity</div>
        <div class="title-line"></div>
    </div>
    """, unsafe_allow_html=True)

    all_reqs = fetch_all_requests()
    pending  = [r for r in all_reqs if r.get("status") == "pending"]
    approved = [r for r in all_reqs if r.get("status") == "approved"]
    rejected = [r for r in all_reqs if r.get("status") == "rejected"]
    total_amt = sum(float(r.get("amount", 0)) for r in approved)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("⏳  Pending",         len(pending))
    c2.metric("✅  Approved",        len(approved))
    c3.metric("❌  Rejected",        len(rejected))
    c4.metric("💰  Total Disbursed", format_iqd(total_amt))

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Pending Approvals</div>', unsafe_allow_html=True)

    if not pending:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">✨</div>
            <div class="msg">All caught up — no pending requests.</div>
        </div>""", unsafe_allow_html=True)
    else:
        for r in pending:
            uid = r.get("user_id", "Unknown")
            short_uid = uid[:14] + "…" if len(uid) > 14 else uid
            st.markdown(f"""
            <div class="req-card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.5rem;">
                    <div>
                        <div class="r-email">User: {short_uid}</div>
                        <div class="r-amount">{format_iqd(r.get('amount',0))}</div>
                        <div class="r-reason">{r.get('reason','—')}</div>
                        <div class="r-meta">{format_date(r.get('created_at',''))}</div>
                    </div>
                    <div>{status_badge("pending")}</div>
                </div>
            </div>""", unsafe_allow_html=True)

            if r.get("invoice_image_url"):
                with st.expander("🖼  View Invoice"):
                    st.image(r["invoice_image_url"], use_column_width=True)

            ca, cr, _ = st.columns([1, 1, 2.5])
            with ca:
                if st.button("✅  Approve", key=f"ap_{r['id']}"):
                    supabase.table("petty_cash_requests").update({"status": "approved"}).eq("id", r["id"]).execute()
                    st.rerun()
            with cr:
                if st.button("❌  Reject", key=f"rj_{r['id']}"):
                    supabase.table("petty_cash_requests").update({"status": "rejected"}).eq("id", r["id"]).execute()
                    st.rerun()
            st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ADMIN — ALL REQUESTS
# ─────────────────────────────────────────────
def page_admin_all():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="page-header">
        <div class="page-title">All Requests</div>
        <div class="page-subtitle">Complete history of petty cash submissions</div>
        <div class="title-line"></div>
    </div>""", unsafe_allow_html=True)

    all_reqs = fetch_all_requests()
    cf1, cf2 = st.columns(2)
    with cf1: fstatus = st.selectbox("Status", ["All", "Pending", "Approved", "Rejected"])
    with cf2: search  = st.text_input("Search reason…", placeholder="e.g. electricity")

    if fstatus != "All":
        all_reqs = [r for r in all_reqs if r.get("status") == fstatus.lower()]
    if search:
        s = search.lower()
        all_reqs = [r for r in all_reqs if s in (r.get("reason","") or "").lower()]

    st.markdown(f'<div class="section-label">{len(all_reqs)} Result{"s" if len(all_reqs)!=1 else ""}</div>', unsafe_allow_html=True)

    if not all_reqs:
        st.markdown('<div class="empty-state"><div class="icon">🔍</div><div class="msg">No requests match your filters.</div></div>', unsafe_allow_html=True)
    else:
        for r in all_reqs:
            status = r.get("status", "pending")
            uid = r.get("user_id", "Unknown")
            short_uid = uid[:14] + "…" if len(uid) > 14 else uid
            st.markdown(f"""
            <div class="req-card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.5rem;">
                    <div>
                        <div class="r-email">{short_uid}</div>
                        <div class="r-amount">{format_iqd(r.get('amount',0))}</div>
                        <div class="r-reason">{r.get('reason','—')}</div>
                        <div class="r-meta">{format_date(r.get('created_at',''))}</div>
                    </div>
                    {status_badge(status)}
                </div>
            </div>""", unsafe_allow_html=True)
            if r.get("invoice_image_url"):
                with st.expander("🖼  Invoice"):
                    st.image(r["invoice_image_url"], use_column_width=True)
            if status == "pending":
                ca, cr, _ = st.columns([1, 1, 3])
                if ca.button("✅ Approve", key=f"a2_{r['id']}"):
                    supabase.table("petty_cash_requests").update({"status": "approved"}).eq("id", r["id"]).execute()
                    st.rerun()
                if cr.button("❌ Reject", key=f"r2_{r['id']}"):
                    supabase.table("petty_cash_requests").update({"status": "rejected"}).eq("id", r["id"]).execute()
                    st.rerun()
            st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ADMIN — BRANCHES
# ─────────────────────────────────────────────
def page_admin_branches():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Branch Overview</div>
        <div class="page-subtitle">Spending summary grouped by user</div>
        <div class="title-line"></div>
    </div>""", unsafe_allow_html=True)

    all_reqs = fetch_all_requests()
    from collections import defaultdict
    stats: dict = defaultdict(lambda: {"total": 0.0, "pending": 0, "approved": 0, "rejected": 0, "count": 0})

    for r in all_reqs:
        key = r.get("user_id", "Unknown")
        s   = r.get("status", "pending")
        stats[key]["count"] += 1
        stats[key]["total"] += float(r.get("amount", 0))
        stats[key][s] = stats[key].get(s, 0) + 1

    if not stats:
        st.markdown('<div class="empty-state"><div class="icon">🏪</div><div class="msg">No data yet.</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="section-label">{len(stats)} User{"s" if len(stats)!=1 else ""}</div>', unsafe_allow_html=True)
        for uid, s in sorted(stats.items(), key=lambda x: -x[1]["total"]):
            short = uid[:16] + "…" if len(uid) > 16 else uid
            st.markdown(f"""
            <div class="branch-card">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
                    <div>
                        <div style="font-size:0.68rem;color:rgba(234,224,204,0.35);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.3rem;">User ID</div>
                        <div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;color:#EAE0CC;font-weight:600;">{short}</div>
                        <div style="font-size:0.82rem;color:rgba(234,224,204,0.45);margin-top:0.25rem;">
                            {s['count']} request{"s" if s['count']!=1 else ""} · {format_iqd(s['total'])} total
                        </div>
                    </div>
                    <div style="display:flex;gap:1.5rem;align-items:center;flex-wrap:wrap;">
                        <div style="text-align:center;">
                            <div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;color:#f1c40f;">{s['pending']}</div>
                            <div style="font-size:0.62rem;color:rgba(234,224,204,0.3);text-transform:uppercase;letter-spacing:0.08em;">Pending</div>
                        </div>
                        <div style="text-align:center;">
                            <div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;color:#4cd884;">{s['approved']}</div>
                            <div style="font-size:0.62rem;color:rgba(234,224,204,0.3);text-transform:uppercase;letter-spacing:0.08em;">Approved</div>
                        </div>
                        <div style="text-align:center;">
                            <div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;color:#e87060;">{s['rejected']}</div>
                            <div style="font-size:0.62rem;color:rgba(234,224,204,0.3);text-transform:uppercase;letter-spacing:0.08em;">Rejected</div>
                        </div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  BRANCH PORTAL
# ─────────────────────────────────────────────
def page_branch_portal(user):
    user_email = user.email
    user_id    = user.id

    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="page-header">
        <div class="page-title">Branch Portal</div>
        <div class="page-subtitle">{user_email}</div>
        <div class="title-line"></div>
    </div>""", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📤  Submit Invoice", "📜  My Requests"])

    with tab1:
        st.markdown('<div class="section-label">New Petty Cash Request</div>', unsafe_allow_html=True)
        with st.form("submit_form", clear_on_submit=True):
            amt          = st.number_input("Amount (IQD)", min_value=0, step=500, format="%d")
            reason       = st.text_area("Description / Reason", placeholder="e.g. Monthly electricity bill", height=100)
            invoice_file = st.file_uploader("Upload Receipt or Invoice", type=["png","jpg","jpeg","pdf"])
            submitted    = st.form_submit_button("Submit Request  →", use_container_width=True)

            if submitted:
                errors = []
                if amt <= 0:           errors.append("Amount must be greater than 0.")
                if not reason.strip(): errors.append("Please provide a description.")
                if not invoice_file:   errors.append("Please upload an invoice or receipt.")
                for e in errors: st.error(e)

                if not errors:
                    image_url = None
                    with st.spinner("Uploading invoice…"):
                        image_url = upload_invoice_image(invoice_file.read(), invoice_file.name)
                    with st.spinner("Submitting request…"):
                        try:
                            supabase.table("petty_cash_requests").insert({
                                "user_id":           user_id,
                                "amount":            amt,
                                "reason":            reason.strip(),
                                "status":            "pending",
                                "invoice_image_url": image_url,
                            }).execute()
                            st.success("✅ Request submitted successfully! Management will review it shortly.")
                        except Exception as e:
                            st.error(f"Submission failed: {e}")

    with tab2:
        st.markdown('<div class="section-label">Your Request History</div>', unsafe_allow_html=True)
        try:
            my_reqs = supabase.table("petty_cash_requests").select("*").eq("user_id", user_id).order("created_at", desc=True).execute().data or []
        except:
            my_reqs = []
            st.warning("Could not load history.")

        if not my_reqs:
            st.markdown('<div class="empty-state"><div class="icon">📋</div><div class="msg">No requests submitted yet.</div></div>', unsafe_allow_html=True)
        else:
            total_approved = sum(float(r.get("amount", 0)) for r in my_reqs if r.get("status") == "approved")
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Requests",  len(my_reqs))
            c2.metric("Approved Amount", format_iqd(total_approved))
            c3.metric("Pending",         sum(1 for r in my_reqs if r.get("status") == "pending"))
            st.markdown("<hr>", unsafe_allow_html=True)
            for r in my_reqs:
                status = r.get("status", "pending")
                st.markdown(f"""
                <div class="req-card">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.5rem;">
                        <div>
                            <div class="r-amount">{format_iqd(r.get('amount',0))}</div>
                            <div class="r-reason">{r.get('reason','—')}</div>
                            <div class="r-meta">{format_date(r.get('created_at',''))}</div>
                        </div>
                        {status_badge(status)}
                    </div>
                </div>""", unsafe_allow_html=True)
                if r.get("invoice_image_url"):
                    with st.expander("🖼  Invoice"):
                        st.image(r["invoice_image_url"], use_column_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ROUTER
# ─────────────────────────────────────────────
user = st.session_state.user

if user is None:
    page_login()
else:
    is_admin = user.email == "admin@jawhar.com"
    render_sidebar(user.email, is_admin)

    if is_admin:
        if st.session_state.page not in ("admin_dashboard", "admin_all", "admin_branches"):
            st.session_state.page = "admin_dashboard"
        {
            "admin_dashboard": page_admin_dashboard,
            "admin_all":       page_admin_all,
            "admin_branches":  page_admin_branches,
        }[st.session_state.page]()
    else:
        page_branch_portal(user)
