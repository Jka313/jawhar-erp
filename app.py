import streamlit as st
from supabase import create_client, Client
import base64
import uuid
from datetime import datetime
import io

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
#  GLOBAL CSS — PREMIUM DARK GOLD THEME
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── RESET & BASE ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: #080A0F;
    font-family: 'DM Sans', sans-serif;
    color: #E8DCC8;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(212,175,55,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 40% 40% at 90% 80%, rgba(212,175,55,0.04) 0%, transparent 50%);
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #0D1017 !important;
    border-right: 1px solid rgba(212,175,55,0.2) !important;
}
[data-testid="stSidebar"] .stMarkdown { color: #E8DCC8; }

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > div,
.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(212,175,55,0.25) !important;
    border-radius: 10px !important;
    color: #E8DCC8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: #D4AF37 !important;
    box-shadow: 0 0 0 3px rgba(212,175,55,0.1) !important;
    outline: none !important;
}
.stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {
    color: rgba(232,220,200,0.6) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #D4AF37 0%, #F5D060 50%, #D4AF37 100%) !important;
    color: #080A0F !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.65rem 1.8rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(212,175,55,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 30px rgba(212,175,55,0.45) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── DANGER BUTTON ── */
button[data-testid*="reject"], [class*="danger"] button {
    background: linear-gradient(135deg, #c0392b, #e74c3c) !important;
    box-shadow: 0 4px 20px rgba(192,57,43,0.3) !important;
    color: white !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(212,175,55,0.15) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: rgba(232,220,200,0.45) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.75rem 1.5rem !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    color: #D4AF37 !important;
    border-bottom: 2px solid #D4AF37 !important;
    background: transparent !important;
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    border: 1.5px dashed rgba(212,175,55,0.3) !important;
    border-radius: 12px !important;
    background: rgba(212,175,55,0.02) !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(212,175,55,0.6) !important;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: rgba(212,175,55,0.05) !important;
    border: 1px solid rgba(212,175,55,0.15) !important;
    border-radius: 10px !important;
    color: #E8DCC8 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.streamlit-expanderContent {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(212,175,55,0.1) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
}

/* ── ALERTS ── */
.stSuccess { background: rgba(39,174,96,0.1) !important; border-left: 3px solid #27ae60 !important; color: #2ecc71 !important; border-radius: 8px !important; }
.stError { background: rgba(192,57,43,0.1) !important; border-left: 3px solid #c0392b !important; color: #e74c3c !important; border-radius: 8px !important; }
.stWarning { background: rgba(212,175,55,0.08) !important; border-left: 3px solid #D4AF37 !important; border-radius: 8px !important; }
.stInfo { background: rgba(52,152,219,0.08) !important; border-left: 3px solid #3498db !important; border-radius: 8px !important; }

/* ── METRIC ── */
[data-testid="stMetric"] {
    background: rgba(212,175,55,0.04) !important;
    border: 1px solid rgba(212,175,55,0.12) !important;
    border-radius: 12px !important;
    padding: 1.2rem 1.5rem !important;
}
[data-testid="stMetricLabel"] { color: rgba(232,220,200,0.55) !important; font-size: 0.75rem !important; text-transform: uppercase !important; letter-spacing: 0.1em !important; }
[data-testid="stMetricValue"] { color: #D4AF37 !important; font-family: 'Playfair Display', serif !important; font-size: 1.9rem !important; }
[data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

/* ── DATAFRAME ── */
.stDataFrame { border: 1px solid rgba(212,175,55,0.15) !important; border-radius: 10px !important; overflow: hidden !important; }

/* ── DIVIDER ── */
hr { border-color: rgba(212,175,55,0.12) !important; margin: 1.5rem 0 !important; }

/* ── CUSTOM CARDS ── */
.card {
    background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(212,175,55,0.03) 100%);
    border: 1px solid rgba(212,175,55,0.15);
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, box-shadow 0.3s;
}
.card:hover { border-color: rgba(212,175,55,0.35); box-shadow: 0 8px 40px rgba(212,175,55,0.08); }
.card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(212,175,55,0.4), transparent);
}

.badge {
    display: inline-block;
    padding: 0.2rem 0.75rem;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.badge-pending { background: rgba(241,196,15,0.15); color: #f1c40f; border: 1px solid rgba(241,196,15,0.3); }
.badge-approved { background: rgba(39,174,96,0.15); color: #27ae60; border: 1px solid rgba(39,174,96,0.3); }
.badge-rejected { background: rgba(192,57,43,0.15); color: #e74c3c; border: 1px solid rgba(192,57,43,0.3); }

.logo-text {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    background: linear-gradient(135deg, #D4AF37, #F5D060, #D4AF37);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.02em;
}

.page-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #E8DCC8;
    margin-bottom: 0.25rem;
}
.page-subtitle {
    font-size: 0.88rem;
    color: rgba(232,220,200,0.45);
    margin-bottom: 2rem;
    letter-spacing: 0.05em;
}
.section-title {
    font-size: 0.78rem;
    font-weight: 600;
    color: #D4AF37;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 1rem;
}
.stat-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}
.stat-box {
    flex: 1;
    min-width: 120px;
    background: rgba(212,175,55,0.04);
    border: 1px solid rgba(212,175,55,0.12);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}
.stat-box .val { font-family: 'Playfair Display', serif; font-size: 1.7rem; color: #D4AF37; }
.stat-box .lbl { font-size: 0.72rem; color: rgba(232,220,200,0.45); text-transform: uppercase; letter-spacing: 0.08em; margin-top: 0.2rem; }

.req-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(212,175,55,0.12);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.req-card:hover { border-color: rgba(212,175,55,0.3); }
.req-card .branch { font-size: 0.78rem; color: rgba(232,220,200,0.45); text-transform: uppercase; letter-spacing: 0.08em; }
.req-card .amount { font-family: 'Playfair Display', serif; font-size: 1.5rem; color: #D4AF37; margin: 0.2rem 0; }
.req-card .reason { font-size: 0.9rem; color: rgba(232,220,200,0.75); }
.req-card .meta { font-size: 0.75rem; color: rgba(232,220,200,0.35); margin-top: 0.5rem; }

.login-container {
    max-width: 420px;
    margin: 5vh auto 0;
    padding: 2.5rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(212,175,55,0.2);
    border-radius: 20px;
    box-shadow: 0 30px 80px rgba(0,0,0,0.5), 0 0 0 1px rgba(212,175,55,0.05) inset;
    position: relative;
}
.login-container::before {
    content: '';
    position: absolute; top: 0; left: 50%; transform: translateX(-50%);
    width: 60%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(212,175,55,0.6), transparent);
}

.gold-line {
    width: 40px; height: 2px;
    background: linear-gradient(90deg, #D4AF37, #F5D060);
    border-radius: 2px;
    margin: 0.5rem 0 1.5rem;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SUPABASE CLIENT (cached)
# ─────────────────────────────────────────────
@st.cache_resource
def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()


# ─────────────────────────────────────────────
#  SESSION DEFAULTS
# ─────────────────────────────────────────────
for k, v in {"user": None, "page": "login"}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def format_iqd(amount: float) -> str:
    return f"{amount:,.0f} IQD"

def format_date(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y · %H:%M")
    except:
        return iso or "—"

def status_badge(status: str) -> str:
    cls = {"pending": "badge-pending", "approved": "badge-approved", "rejected": "badge-rejected"}.get(status, "badge-pending")
    icons = {"pending": "⏳", "approved": "✅", "rejected": "❌"}
    label = {"pending": "Pending", "approved": "Approved", "rejected": "Rejected"}
    return f'<span class="badge {cls}">{icons.get(status,"")} {label.get(status, status)}</span>'

def upload_invoice_image(file_bytes: bytes, filename: str) -> str | None:
    """Upload image to Supabase Storage and return public URL."""
    try:
        ext = filename.rsplit(".", 1)[-1].lower()
        unique_name = f"invoices/{uuid.uuid4()}.{ext}"
        res = supabase.storage.from_("invoices").upload(
            path=unique_name,
            file=file_bytes,
            file_options={"content-type": f"image/{ext}"}
        )
        # Get public URL
        public_url = supabase.storage.from_("invoices").get_public_url(unique_name)
        return public_url
    except Exception as e:
        st.error(f"Image upload failed: {e}")
        return None


# ─────────────────────────────────────────────
#  LOGIN PAGE
# ─────────────────────────────────────────────
def page_login():
    # Centered golden logo header
    st.markdown("""
    <div style="text-align:center; padding: 3rem 0 1rem;">
        <div style="font-size: 2.8rem; margin-bottom: 0.5rem;">💎</div>
        <div style="font-family:'Playfair Display',serif; font-size:2.2rem; font-weight:700;
             background:linear-gradient(135deg,#D4AF37,#F5D060,#C9A227);
             -webkit-background-clip:text; -webkit-text-fill-color:transparent;
             background-clip:text; letter-spacing:0.05em;">
            JAWHAR ERP
        </div>
        <div style="color:rgba(232,220,200,0.4); font-size:0.8rem; letter-spacing:0.2em;
             text-transform:uppercase; margin-top:0.3rem;">
            Petty Cash Management System
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 1.2, 1])
    with col_m:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("""
        <p class="section-title" style="text-align:center; margin-bottom:1.5rem;">
            Authorized Access Only
        </p>
        """, unsafe_allow_html=True)

        email = st.text_input("Email Address", placeholder="you@jawhar.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        if st.button("Sign In →", use_container_width=True):
            if not email or not password:
                st.warning("Please enter both email and password.")
            else:
                with st.spinner("Authenticating…"):
                    try:
                        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                        st.session_state.user = res.user
                        st.success("Access granted. Loading dashboard…")
                        st.rerun()
                    except Exception as e:
                        st.error("Authentication failed. Please check your credentials.")

        st.markdown("""
        <p style="text-align:center; color:rgba(232,220,200,0.25); font-size:0.75rem; margin-top:1.5rem;">
            Protected system — unauthorized access is prohibited
        </p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SIDEBAR (authenticated)
# ─────────────────────────────────────────────
def render_sidebar(user_email: str, is_admin: bool):
    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 1.5rem 0.5rem 1rem;">
            <div class="logo-text">💎 JAWHAR</div>
            <div style="font-size:0.72rem; color:rgba(232,220,200,0.35); letter-spacing:0.15em; text-transform:uppercase; margin-top:0.15rem;">
                {"Management Portal" if is_admin else "Branch Portal"}
            </div>
        </div>
        <hr style="margin:0 0 1rem;">
        <div style="font-size:0.72rem; color:rgba(232,220,200,0.4); text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.5rem;">
            Signed in as
        </div>
        <div style="font-size:0.88rem; color:#D4AF37; font-weight:500; word-break:break-all; margin-bottom:1.5rem;">
            {user_email}
        </div>
        """, unsafe_allow_html=True)

        if is_admin:
            st.markdown('<p class="section-title">Navigation</p>', unsafe_allow_html=True)
            if st.button("📊  Dashboard", use_container_width=True):
                st.session_state.page = "admin_dashboard"
                st.rerun()
            if st.button("📋  All Requests", use_container_width=True):
                st.session_state.page = "admin_all"
                st.rerun()
            if st.button("🏪  Branches", use_container_width=True):
                st.session_state.page = "admin_branches"
                st.rerun()

        st.markdown("<div style='flex:1'></div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button("⎋  Sign Out", use_container_width=True):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()


# ─────────────────────────────────────────────
#  ADMIN — DASHBOARD
# ─────────────────────────────────────────────
def page_admin_dashboard():
    st.markdown('<div class="page-title">Command Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Real-time overview of all petty cash activity</div>', unsafe_allow_html=True)

    try:
        all_reqs = supabase.table("petty_cash_requests").select("*, branches(branch_name)").execute().data or []
    except:
        all_reqs = []

    pending  = [r for r in all_reqs if r.get("status") == "pending"]
    approved = [r for r in all_reqs if r.get("status") == "approved"]
    rejected = [r for r in all_reqs if r.get("status") == "rejected"]
    total_approved_amt = sum(r.get("amount", 0) for r in approved)

    # ── Stats ──
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("⏳ Pending", len(pending))
    c2.metric("✅ Approved", len(approved))
    c3.metric("❌ Rejected", len(rejected))
    c4.metric("💰 Total Disbursed", format_iqd(total_approved_amt))

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Pending Requests ──
    st.markdown('<p class="section-title">Pending Approvals</p>', unsafe_allow_html=True)

    if not pending:
        st.info("✨ No pending requests — you're all caught up.")
    else:
        for r in pending:
            branch_name = r.get("branches", {}).get("branch_name", "Unknown Branch") if r.get("branches") else r.get("branch_id", "Branch")
            created = format_date(r.get("created_at", ""))
            amt = r.get("amount", 0)
            reason = r.get("reason", "—")

            st.markdown(f"""
            <div class="req-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.5rem;">
                    <div>
                        <div class="branch">🏪 {branch_name}</div>
                        <div class="amount">{format_iqd(amt)}</div>
                        <div class="reason">{reason}</div>
                        <div class="meta">Submitted {created}</div>
                    </div>
                    <div>{status_badge("pending")}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if r.get("invoice_image_url"):
                with st.expander("🖼 View Invoice Image"):
                    st.image(r["invoice_image_url"], use_column_width=True)

            col_a, col_r, col_s = st.columns([1, 1, 2])
            with col_a:
                if st.button("✅ Approve", key=f"approve_{r['id']}"):
                    supabase.table("petty_cash_requests").update({"status": "approved"}).eq("id", r["id"]).execute()
                    st.success("Request approved!")
                    st.rerun()
            with col_r:
                if st.button("❌ Reject", key=f"reject_{r['id']}"):
                    supabase.table("petty_cash_requests").update({"status": "rejected"}).eq("id", r["id"]).execute()
                    st.warning("Request rejected.")
                    st.rerun()
            st.markdown("<hr style='margin:0.75rem 0'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ADMIN — ALL REQUESTS
# ─────────────────────────────────────────────
def page_admin_all():
    st.markdown('<div class="page-title">All Requests</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Complete history of petty cash submissions</div>', unsafe_allow_html=True)

    try:
        all_reqs = supabase.table("petty_cash_requests").select("*, branches(branch_name)").order("created_at", desc=True).execute().data or []
    except:
        all_reqs = []
        st.warning("Could not load requests. Check database configuration.")

    # Filters
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_status = st.selectbox("Filter by Status", ["All", "Pending", "Approved", "Rejected"])
    with col_f2:
        search = st.text_input("Search by reason or branch…", placeholder="e.g. electricity")

    if filter_status != "All":
        all_reqs = [r for r in all_reqs if r.get("status") == filter_status.lower()]
    if search:
        s = search.lower()
        all_reqs = [r for r in all_reqs if s in (r.get("reason","") or "").lower()
                    or s in (r.get("branches",{}) or {}).get("branch_name","").lower()]

    if not all_reqs:
        st.info("No requests match your filters.")
        return

    for r in all_reqs:
        branch_name = (r.get("branches") or {}).get("branch_name", r.get("branch_id", "Unknown"))
        status = r.get("status", "pending")
        st.markdown(f"""
        <div class="req-card">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <div class="branch">🏪 {branch_name}</div>
                    <div class="amount">{format_iqd(r.get('amount',0))}</div>
                    <div class="reason">{r.get('reason','—')}</div>
                    <div class="meta">{format_date(r.get('created_at',''))}</div>
                </div>
                {status_badge(status)}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if r.get("invoice_image_url"):
            with st.expander("🖼 Invoice"):
                st.image(r["invoice_image_url"], use_column_width=True)

        if status == "pending":
            ca, cr, _ = st.columns([1,1,3])
            if ca.button("✅ Approve", key=f"a2_{r['id']}"):
                supabase.table("petty_cash_requests").update({"status": "approved"}).eq("id", r["id"]).execute()
                st.rerun()
            if cr.button("❌ Reject", key=f"r2_{r['id']}"):
                supabase.table("petty_cash_requests").update({"status": "rejected"}).eq("id", r["id"]).execute()
                st.rerun()
        st.markdown("<hr style='margin:0.5rem 0'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ADMIN — BRANCHES
# ─────────────────────────────────────────────
def page_admin_branches():
    st.markdown('<div class="page-title">Branch Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Spending summary per branch</div>', unsafe_allow_html=True)

    try:
        reqs = supabase.table("petty_cash_requests").select("*, branches(branch_name)").execute().data or []
    except:
        reqs = []
        st.warning("Could not load data.")

    from collections import defaultdict
    branch_stats: dict = defaultdict(lambda: {"total": 0, "pending": 0, "approved": 0, "rejected": 0, "count": 0})

    for r in reqs:
        bn = (r.get("branches") or {}).get("branch_name", r.get("branch_id", "Unknown"))
        status = r.get("status", "pending")
        amt = r.get("amount", 0)
        branch_stats[bn]["count"] += 1
        branch_stats[bn]["total"] += amt
        branch_stats[bn][status] = branch_stats[bn].get(status, 0) + 1

    if not branch_stats:
        st.info("No branch data available yet.")
        return

    for branch, stats in sorted(branch_stats.items()):
        st.markdown(f"""
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
                <div>
                    <div style="font-size:0.78rem; color:rgba(232,220,200,0.4); text-transform:uppercase; letter-spacing:0.1em;">Branch</div>
                    <div style="font-family:'Playfair Display',serif; font-size:1.4rem; color:#E8DCC8; margin:0.1rem 0;">{branch}</div>
                    <div style="font-size:0.85rem; color:rgba(232,220,200,0.5);">{stats['count']} requests · {format_iqd(stats['total'])} total</div>
                </div>
                <div style="display:flex; gap:0.75rem; flex-wrap:wrap;">
                    {status_badge("pending")} <span style="font-size:0.9rem">{stats['pending']}</span> &nbsp;
                    {status_badge("approved")} <span style="font-size:0.9rem">{stats['approved']}</span> &nbsp;
                    {status_badge("rejected")} <span style="font-size:0.9rem">{stats['rejected']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  BRANCH — PORTAL
# ─────────────────────────────────────────────
def page_branch_portal(user):
    user_email = user.email
    user_id = user.id

    st.markdown('<div class="page-title">Branch Portal</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">Logged in as {user_email}</div>', unsafe_allow_html=True)

    # Try to get branch info from user metadata or a lookup table
    try:
        branch_data = supabase.table("branches").select("*").eq("user_id", user_id).execute().data
        branch_name = branch_data[0]["branch_name"] if branch_data else user_email.split("@")[0].title()
        branch_id = branch_data[0]["id"] if branch_data else None
    except:
        branch_name = user_email.split("@")[0].title()
        branch_id = None

    tab1, tab2 = st.tabs(["📤  Submit Invoice", "📜  My Requests"])

    # ── TAB 1: SUBMIT ──
    with tab1:
        st.markdown('<p class="section-title">New Petty Cash Request</p>', unsafe_allow_html=True)

        with st.form("submit_form", clear_on_submit=True):
            amt = st.number_input("Amount (IQD)", min_value=0, step=500, format="%d",
                                   help="Enter the exact amount spent")
            reason = st.text_area("Description / Reason",
                                   placeholder="e.g. Monthly electricity bill for Al-Mansour branch",
                                   height=100)
            invoice_file = st.file_uploader(
                "Upload Receipt or Invoice",
                type=["png", "jpg", "jpeg", "pdf"],
                help="Supported: PNG, JPG, PDF"
            )

            submitted = st.form_submit_button("Submit Request →", use_container_width=True)

            if submitted:
                errors = []
                if amt <= 0:         errors.append("Amount must be greater than 0.")
                if not reason.strip(): errors.append("Please provide a description.")
                if not invoice_file:  errors.append("Please upload an invoice image.")

                if errors:
                    for e in errors:
                        st.error(e)
                else:
                    image_url = None
                    with st.spinner("Uploading invoice…"):
                        if invoice_file:
                            file_bytes = invoice_file.read()
                            image_url = upload_invoice_image(file_bytes, invoice_file.name)

                    with st.spinner("Submitting request…"):
                        payload = {
                            "user_id": user_id,
                            "branch_id": branch_id,
                            "amount": amt,
                            "reason": reason.strip(),
                            "status": "pending",
                            "invoice_image_url": image_url,
                        }
                        try:
                            supabase.table("petty_cash_requests").insert(payload).execute()
                            st.success("✅ Request submitted successfully! Management will review it shortly.")
                        except Exception as e:
                            st.error(f"Submission failed: {e}")

    # ── TAB 2: HISTORY ──
    with tab2:
        st.markdown('<p class="section-title">Your Request History</p>', unsafe_allow_html=True)

        try:
            my_reqs = supabase.table("petty_cash_requests").select("*").eq("user_id", user_id).order("created_at", desc=True).execute().data or []
        except:
            my_reqs = []
            st.warning("Could not load history.")

        if not my_reqs:
            st.info("You haven't submitted any requests yet.")
        else:
            # Mini stats
            total_submitted = sum(r.get("amount", 0) for r in my_reqs)
            total_approved  = sum(r.get("amount", 0) for r in my_reqs if r.get("status") == "approved")
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Submitted", len(my_reqs))
            c2.metric("Approved Amount", format_iqd(total_approved))
            c3.metric("Pending", sum(1 for r in my_reqs if r.get("status") == "pending"))

            st.markdown("<hr>", unsafe_allow_html=True)

            for r in my_reqs:
                status = r.get("status", "pending")
                st.markdown(f"""
                <div class="req-card">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.5rem;">
                        <div>
                            <div class="amount">{format_iqd(r.get('amount',0))}</div>
                            <div class="reason">{r.get('reason','—')}</div>
                            <div class="meta">{format_date(r.get('created_at',''))}</div>
                        </div>
                        {status_badge(status)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if r.get("invoice_image_url"):
                    with st.expander("🖼 Invoice"):
                        st.image(r["invoice_image_url"], use_column_width=True)


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
        pages = {
            "admin_dashboard": page_admin_dashboard,
            "admin_all":       page_admin_all,
            "admin_branches":  page_admin_branches,
        }
        # Main content padding
        st.markdown("<div style='padding: 2rem 3rem;'>", unsafe_allow_html=True)
        pages[st.session_state.page]()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='padding: 2rem 3rem;'>", unsafe_allow_html=True)
        page_branch_portal(user)
        st.markdown("</div>", unsafe_allow_html=True)
