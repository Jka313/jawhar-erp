import streamlit as st
from supabase import create_client, Client
import uuid
from datetime import datetime, date
from collections import defaultdict
import io

# ─────────────────────────────────────────────
#  CONFIG & CONNECTION
# ─────────────────────────────────────────────
SUPABASE_URL = "https://xtjnatjxsxbyrwkqytqd.supabase.co"
SUPABASE_KEY = "sb_publishable_NPbMYsWC7UhEaVmMKga16w_LjITdW7w"

# Monthly spending limit per user (IQD) — change as needed
MONTHLY_LIMIT = 500_000

st.set_page_config(
    page_title="Jawhar ERP — Petty Cash",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS — ULTRA PREMIUM DARK GOLD
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Inter:wght@300;400;500;600&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}

.stApp{
    background:#06080D;
    font-family:'Inter',sans-serif;
    color:#EAE0CC;
    background-image:
        radial-gradient(ellipse 110% 55% at 50% -5%, rgba(212,175,55,0.09) 0%,transparent 60%),
        radial-gradient(ellipse 55% 55% at 95% 90%,  rgba(212,175,55,0.05) 0%,transparent 55%),
        radial-gradient(ellipse 35% 35% at 3%  15%,  rgba(212,175,55,0.04) 0%,transparent 50%);
}

#MainMenu,footer,header,.stDeployButton,
[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important;}
.block-container{padding:0!important;max-width:100%!important;}

/* SIDEBAR */
[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#090B10 0%,#06080D 100%)!important;
    border-right:1px solid rgba(212,175,55,0.15)!important;
    box-shadow:6px 0 40px rgba(0,0,0,0.5)!important;
}
[data-testid="stSidebarContent"]{padding:0!important;}

/* INPUTS */
.stTextInput>div>div>input,
.stNumberInput>div>div>input,
.stTextArea textarea{
    background:rgba(255,255,255,0.022)!important;
    border:1px solid rgba(212,175,55,0.18)!important;
    border-radius:11px!important;
    color:#EAE0CC!important;
    font-family:'Inter',sans-serif!important;
    font-size:0.92rem!important;
    padding:0.68rem 1.05rem!important;
    transition:border-color .25s,box-shadow .25s,background .25s;
    caret-color:#D4AF37;
}
.stTextInput>div>div>input:focus,
.stNumberInput>div>div>input:focus,
.stTextArea textarea:focus{
    border-color:rgba(212,175,55,0.55)!important;
    background:rgba(212,175,55,0.035)!important;
    box-shadow:0 0 0 3px rgba(212,175,55,0.07),0 2px 14px rgba(0,0,0,0.35)!important;
    outline:none!important;
}
.stTextInput label,.stNumberInput label,.stTextArea label,.stSelectbox label,
.stDateInput label{
    color:rgba(234,224,204,0.45)!important;
    font-size:0.7rem!important;
    font-weight:500!important;
    letter-spacing:0.11em!important;
    text-transform:uppercase!important;
}
.stSelectbox>div>div,.stDateInput>div>div>input{
    background:rgba(255,255,255,0.022)!important;
    border:1px solid rgba(212,175,55,0.18)!important;
    border-radius:11px!important;
    color:#EAE0CC!important;
}

/* BUTTONS */
.stButton>button{
    background:linear-gradient(135deg,#B8942A 0%,#EEC84A 45%,#B8942A 100%)!important;
    background-size:200% auto!important;
    color:#06080D!important;
    border:none!important;
    border-radius:11px!important;
    font-family:'Inter',sans-serif!important;
    font-weight:600!important;
    font-size:0.87rem!important;
    letter-spacing:0.045em!important;
    padding:0.67rem 1.8rem!important;
    cursor:pointer!important;
    transition:all .3s ease!important;
    box-shadow:0 4px 22px rgba(212,175,55,0.22),0 1px 0 rgba(255,255,255,0.08) inset!important;
}
.stButton>button:hover{
    background-position:right center!important;
    transform:translateY(-2px)!important;
    box-shadow:0 8px 36px rgba(212,175,55,0.38)!important;
}
.stButton>button:active{transform:translateY(0)!important;}

/* TABS */
.stTabs [data-baseweb="tab-list"]{
    background:transparent!important;
    border-bottom:1px solid rgba(212,175,55,0.1)!important;
    gap:0!important;padding:0!important;
}
.stTabs [data-baseweb="tab"]{
    background:transparent!important;
    color:rgba(234,224,204,0.38)!important;
    font-family:'Inter',sans-serif!important;
    font-size:0.87rem!important;font-weight:500!important;
    border:none!important;border-bottom:2px solid transparent!important;
    padding:.9rem 1.7rem!important;transition:all .2s!important;
}
.stTabs [aria-selected="true"]{
    color:#D4AF37!important;
    border-bottom:2px solid #D4AF37!important;
    background:transparent!important;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"]{
    border:1.5px dashed rgba(212,175,55,0.22)!important;
    border-radius:14px!important;
    background:rgba(212,175,55,0.012)!important;
    transition:all .25s!important;padding:.5rem!important;
}
[data-testid="stFileUploader"]:hover{
    border-color:rgba(212,175,55,0.5)!important;
    background:rgba(212,175,55,0.025)!important;
}

/* EXPANDER */
[data-testid="stExpander"]{
    border:1px solid rgba(212,175,55,0.11)!important;
    border-radius:12px!important;
    background:rgba(255,255,255,0.012)!important;
    overflow:hidden!important;
}

/* ALERTS */
.stSuccess>div{background:rgba(39,174,96,0.07)!important;border:1px solid rgba(39,174,96,0.22)!important;border-left:3px solid #27ae60!important;color:#5dda8a!important;border-radius:11px!important;}
.stError>div{background:rgba(192,57,43,0.07)!important;border:1px solid rgba(192,57,43,0.22)!important;border-left:3px solid #c0392b!important;color:#e87060!important;border-radius:11px!important;}
.stWarning>div{background:rgba(212,175,55,0.06)!important;border:1px solid rgba(212,175,55,0.18)!important;border-left:3px solid #D4AF37!important;border-radius:11px!important;}
.stInfo>div{background:rgba(99,130,200,0.06)!important;border:1px solid rgba(99,130,200,0.18)!important;border-left:3px solid #6382c8!important;border-radius:11px!important;}

/* METRIC */
[data-testid="stMetric"]{
    background:linear-gradient(140deg,rgba(212,175,55,0.055) 0%,rgba(255,255,255,0.018) 100%)!important;
    border:1px solid rgba(212,175,55,0.13)!important;
    border-radius:15px!important;padding:1.4rem 1.6rem!important;
    position:relative!important;overflow:hidden!important;
    transition:border-color .3s,box-shadow .3s!important;
}
[data-testid="stMetric"]::before{
    content:'';position:absolute;top:0;left:0;right:0;height:1px;
    background:linear-gradient(90deg,transparent,rgba(212,175,55,0.38),transparent);
}
[data-testid="stMetric"]:hover{
    border-color:rgba(212,175,55,0.26)!important;
    box-shadow:0 8px 32px rgba(212,175,55,0.07)!important;
}
[data-testid="stMetricLabel"]{color:rgba(234,224,204,0.42)!important;font-size:0.7rem!important;font-weight:500!important;text-transform:uppercase!important;letter-spacing:0.13em!important;}
[data-testid="stMetricValue"]{color:#D4AF37!important;font-family:'Cormorant Garamond',serif!important;font-size:2.15rem!important;font-weight:600!important;line-height:1.1!important;}

hr{border:none!important;border-top:1px solid rgba(212,175,55,0.09)!important;margin:2rem 0!important;}

/* ── CUSTOM COMPONENTS ── */
.page-wrap{padding:2.5rem 3rem 4rem;max-width:1120px;}
.page-header{margin-bottom:2.6rem;}
.page-title{font-family:'Cormorant Garamond',serif;font-size:2.5rem;font-weight:600;color:#EAE0CC;line-height:1.1;letter-spacing:-0.01em;}
.page-subtitle{font-size:0.83rem;color:rgba(234,224,204,0.35);margin-top:.4rem;letter-spacing:.06em;}
.title-line{width:38px;height:2px;background:linear-gradient(90deg,#D4AF37,#EEC84A);border-radius:2px;margin:.75rem 0 0;}

.sec-label{
    font-size:0.68rem;font-weight:600;color:#C9A227;
    text-transform:uppercase;letter-spacing:.15em;
    margin-bottom:1rem;display:flex;align-items:center;gap:.6rem;
}
.sec-label::after{content:'';flex:1;height:1px;background:rgba(212,175,55,0.1);}

/* REQUEST CARD */
.req-card{
    background:linear-gradient(140deg,rgba(255,255,255,0.022) 0%,rgba(212,175,55,0.018) 100%);
    border:1px solid rgba(212,175,55,0.1);
    border-radius:16px;padding:1.5rem 1.8rem;
    margin-bottom:.85rem;position:relative;overflow:hidden;
    transition:border-color .25s,box-shadow .25s,transform .2s;
}
.req-card::before{
    content:'';position:absolute;top:0;left:0;right:0;height:1px;
    background:linear-gradient(90deg,transparent,rgba(212,175,55,0.22),transparent);
}
.req-card:hover{
    border-color:rgba(212,175,55,0.26);
    box-shadow:0 12px 45px rgba(0,0,0,0.28),0 0 0 1px rgba(212,175,55,0.04);
    transform:translateY(-1px);
}
.req-card .r-sub{font-size:.7rem;color:rgba(234,224,204,.35);text-transform:uppercase;letter-spacing:.1em;margin-bottom:.25rem;}
.req-card .r-amt{font-family:'Cormorant Garamond',serif;font-size:1.75rem;font-weight:600;color:#D4AF37;line-height:1.1;}
.req-card .r-reason{font-size:.89rem;color:rgba(234,224,204,.7);margin:.3rem 0 .2rem;}
.req-card .r-note{font-size:.82rem;color:rgba(232,100,80,.75);margin:.3rem 0;font-style:italic;}
.req-card .r-meta{font-size:.7rem;color:rgba(234,224,204,.28);margin-top:.4rem;}

/* BADGE */
.badge{display:inline-flex;align-items:center;gap:.3rem;padding:.22rem .85rem;border-radius:20px;font-size:.67rem;font-weight:600;letter-spacing:.09em;text-transform:uppercase;}
.badge-pending {background:rgba(241,196,15,0.11); color:#f1c40f;border:1px solid rgba(241,196,15,0.26);}
.badge-approved{background:rgba(39,174,96,0.11);  color:#4cd884;border:1px solid rgba(39,174,96,0.26);}
.badge-rejected{background:rgba(192,57,43,0.11);  color:#e87060;border:1px solid rgba(192,57,43,0.26);}

/* BRANCH / ANALYTICS CARD */
.a-card{
    background:linear-gradient(140deg,rgba(255,255,255,0.022) 0%,rgba(212,175,55,0.018) 100%);
    border:1px solid rgba(212,175,55,0.1);border-radius:16px;
    padding:1.6rem 1.8rem;margin-bottom:.85rem;position:relative;overflow:hidden;
    transition:border-color .25s,box-shadow .25s;
}
.a-card::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,0.18),transparent);}
.a-card:hover{border-color:rgba(212,175,55,0.26);box-shadow:0 8px 32px rgba(0,0,0,0.22);}

/* LIMIT BAR */
.limit-bar-wrap{margin:.5rem 0 .2rem;}
.limit-bar-bg{background:rgba(255,255,255,0.06);border-radius:6px;height:6px;overflow:hidden;}
.limit-bar-fill{height:100%;border-radius:6px;transition:width .6s ease;}

/* LOGIN */
.login-gem{font-size:3rem;text-align:center;margin-bottom:.6rem;filter:drop-shadow(0 0 24px rgba(212,175,55,0.35));}
.login-title{font-family:'Cormorant Garamond',serif;font-size:2.7rem;font-weight:700;text-align:center;background:linear-gradient(135deg,#A87C1A,#EEC84A,#B8942A);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:.08em;line-height:1;}
.login-sub{text-align:center;font-size:.67rem;color:rgba(234,224,204,.25);letter-spacing:.22em;text-transform:uppercase;margin:.4rem 0 2rem;}
.login-box{background:linear-gradient(160deg,rgba(255,255,255,0.032) 0%,rgba(212,175,55,0.018) 100%);border:1px solid rgba(212,175,55,0.16);border-radius:22px;padding:2.6rem 2.3rem;box-shadow:0 45px 110px rgba(0,0,0,.6);position:relative;overflow:hidden;}
.login-box::before{content:'';position:absolute;top:0;left:50%;transform:translateX(-50%);width:50%;height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,.7),transparent);}
.login-box::after{content:'';position:absolute;bottom:-70px;right:-70px;width:200px;height:200px;background:radial-gradient(circle,rgba(212,175,55,.04) 0%,transparent 70%);pointer-events:none;}
.login-footer{text-align:center;font-size:.68rem;color:rgba(234,224,204,.18);margin-top:1.6rem;letter-spacing:.05em;}

/* SIDEBAR NAV BUTTONS */
[data-testid="stSidebar"] .stButton>button{
    background:transparent!important;color:rgba(234,224,204,.5)!important;
    border:1px solid rgba(212,175,55,0.07)!important;border-radius:10px!important;
    font-size:.84rem!important;font-weight:400!important;box-shadow:none!important;
    padding:.6rem 1rem!important;text-align:left!important;
    transition:all .2s!important;letter-spacing:.01em!important;
}
[data-testid="stSidebar"] .stButton>button:hover{
    background:rgba(212,175,55,0.065)!important;color:#D4AF37!important;
    border-color:rgba(212,175,55,0.22)!important;transform:none!important;box-shadow:none!important;
}

/* CHART CONTAINER */
.chart-wrap{
    background:linear-gradient(140deg,rgba(255,255,255,0.018) 0%,rgba(212,175,55,0.012) 100%);
    border:1px solid rgba(212,175,55,0.1);border-radius:16px;
    padding:1.4rem 1.6rem;margin-bottom:1.2rem;position:relative;overflow:hidden;
}
.chart-wrap::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,0.2),transparent);}

/* EMPTY STATE */
.empty-state{text-align:center;padding:3.5rem 2rem;color:rgba(234,224,204,.28);}
.empty-state .icon{font-size:2.4rem;margin-bottom:.7rem;opacity:.55;}
.empty-state .msg{font-size:.9rem;}

/* SCROLLBAR */
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:rgba(212,175,55,0.18);border-radius:10px;}
::-webkit-scrollbar-thumb:hover{background:rgba(212,175,55,0.38);}
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
        ext  = filename.rsplit(".", 1)[-1].lower()
        ct   = "application/pdf" if ext == "pdf" else f"image/{ext}"
        path = f"invoices/{uuid.uuid4()}.{ext}"
        supabase.storage.from_("invoices").upload(path=path, file=file_bytes, file_options={"content-type": ct})
        return supabase.storage.from_("invoices").get_public_url(path)
    except Exception as e:
        st.error(f"Image upload failed: {e}")
        return None

def fetch_all_requests():
    try:    return supabase.table("petty_cash_requests").select("*").order("created_at", desc=True).execute().data or []
    except: return []

def get_user_monthly_spent(user_id: str) -> float:
    """Return total approved+pending IQD for current calendar month."""
    try:
        now = datetime.utcnow()
        start = f"{now.year}-{now.month:02d}-01T00:00:00"
        rows = (supabase.table("petty_cash_requests")
                .select("amount,status")
                .eq("user_id", user_id)
                .gte("created_at", start)
                .in_("status", ["approved", "pending"])
                .execute().data or [])
        return sum(float(r.get("amount", 0)) for r in rows)
    except:
        return 0.0

def limit_bar_html(spent: float, limit: float) -> str:
    pct = min(spent / limit * 100, 100) if limit > 0 else 0
    color = "#D4AF37" if pct < 70 else ("#e87060" if pct >= 90 else "#f1c40f")
    return f"""
    <div class="limit-bar-wrap">
        <div style="display:flex;justify-content:space-between;font-size:.72rem;color:rgba(234,224,204,.4);margin-bottom:.35rem;">
            <span>Monthly Usage</span>
            <span>{format_iqd(spent)} / {format_iqd(limit)}</span>
        </div>
        <div class="limit-bar-bg">
            <div class="limit-bar-fill" style="width:{pct:.1f}%;background:{color};"></div>
        </div>
    </div>"""

def generate_pdf_report(reqs: list, month_label: str) -> bytes:
    """Generate a simple text-based PDF report using only stdlib."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        gold = colors.HexColor("#D4AF37")
        dark = colors.HexColor("#1a1a2e")

        title_style = ParagraphStyle("title", parent=styles["Title"], fontSize=20, textColor=gold, spaceAfter=4)
        sub_style   = ParagraphStyle("sub",   parent=styles["Normal"], fontSize=10, textColor=colors.HexColor("#888888"), spaceAfter=16)
        normal      = ParagraphStyle("n",     parent=styles["Normal"], fontSize=9,  textColor=colors.HexColor("#333333"))

        total = sum(float(r.get("amount", 0)) for r in reqs)
        elements = [
            Paragraph("💎 JAWHAR ERP", title_style),
            Paragraph(f"Approved Petty Cash Report — {month_label}", sub_style),
            Paragraph(f"Generated: {datetime.now().strftime('%d %b %Y %H:%M')}  |  Total Records: {len(reqs)}  |  Total Amount: {format_iqd(total)}", normal),
            Spacer(1, 0.5*cm),
        ]

        data = [["#", "Date", "User", "Amount (IQD)", "Reason"]]
        for i, r in enumerate(reqs, 1):
            uid = (r.get("user_id") or "")[:12] + "…"
            data.append([
                str(i),
                format_date(r.get("created_at", ""))[:11],
                uid,
                f"{float(r.get('amount',0)):,.0f}",
                (r.get("reason","") or "")[:55],
            ])
        data.append(["", "", "TOTAL", f"{total:,.0f}", ""])

        tbl = Table(data, colWidths=[1*cm, 3.2*cm, 4*cm, 3.2*cm, 6.5*cm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND",  (0,0), (-1,0),  gold),
            ("TEXTCOLOR",   (0,0), (-1,0),  colors.black),
            ("FONTNAME",    (0,0), (-1,0),  "Helvetica-Bold"),
            ("FONTSIZE",    (0,0), (-1,0),  9),
            ("ALIGN",       (0,0), (-1,-1), "LEFT"),
            ("ALIGN",       (3,0), (3,-1),  "RIGHT"),
            ("ROWBACKGROUNDS", (0,1), (-1,-2), [colors.HexColor("#f9f9f9"), colors.white]),
            ("BACKGROUND",  (0,-1), (-1,-1), colors.HexColor("#FFF8E1")),
            ("FONTNAME",    (0,-1), (-1,-1), "Helvetica-Bold"),
            ("GRID",        (0,0),  (-1,-1), 0.4, colors.HexColor("#dddddd")),
            ("TOPPADDING",  (0,0),  (-1,-1), 5),
            ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ]))
        elements += [tbl]
        doc.build(elements)
        return buf.getvalue()
    except ImportError:
        # Fallback: plain-text CSV bytes if reportlab not installed
        lines = ["JAWHAR ERP — Approved Petty Cash Report", f"Month: {month_label}", f"Generated: {datetime.now()}", ""]
        lines.append("Date,User,Amount IQD,Reason")
        for r in reqs:
            uid = (r.get("user_id") or "")[:16]
            lines.append(f"{format_date(r.get('created_at',''))},{uid},{float(r.get('amount',0)):.0f},{r.get('reason','')}")
        lines.append(f",,TOTAL {sum(float(r.get('amount',0)) for r in reqs):.0f},")
        return "\n".join(lines).encode("utf-8")


# ─────────────────────────────────────────────
#  LOGIN PAGE
# ─────────────────────────────────────────────
def page_login():
    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        st.markdown("""
        <div style="padding:4rem 0 1.5rem;text-align:center;">
            <div class="login-gem">💎</div>
            <div class="login-title">JAWHAR</div>
            <div class="login-sub">Petty Cash Management System</div>
        </div>
        <div class="login-box">
        """, unsafe_allow_html=True)

        email    = st.text_input("Email Address", placeholder="you@jawhar.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

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
                        st.error("Access denied — please check your credentials.")

        st.markdown('<p class="login-footer">Restricted system · Authorized personnel only</p>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar(user_email: str, is_admin: bool):
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:1.9rem 1.4rem 1rem;">
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.45rem;font-weight:700;
                 background:linear-gradient(135deg,#C9A227,#EEC84A,#C9A227);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                 background-clip:text;letter-spacing:.06em;">💎 JAWHAR ERP</div>
            <div style="font-size:.62rem;color:rgba(234,224,204,.26);letter-spacing:.18em;
                 text-transform:uppercase;margin-top:.2rem;">
                {"Management" if is_admin else "Branch Portal"}
            </div>
        </div>
        <div style="margin:0 1.1rem;height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,0.18),transparent);"></div>
        <div style="padding:.9rem 1.4rem .5rem;">
            <div style="font-size:.62rem;color:rgba(234,224,204,.28);text-transform:uppercase;letter-spacing:.12em;margin-bottom:.35rem;">Account</div>
            <div style="font-size:.82rem;color:#D4AF37;font-weight:500;word-break:break-all;margin-bottom:1.4rem;">{user_email}</div>
        """, unsafe_allow_html=True)

        if is_admin:
            st.markdown("""<div style="font-size:.62rem;color:rgba(234,224,204,.28);text-transform:uppercase;letter-spacing:.12em;margin-bottom:.55rem;">Navigation</div>""", unsafe_allow_html=True)
            nav = [
                ("admin_dashboard", "📊  Dashboard"),
                ("admin_analytics", "📈  Analytics"),
                ("admin_all",       "📋  All Requests"),
                ("admin_branches",  "🏪  Branches"),
            ]
            for key, label in nav:
                if st.button(label, use_container_width=True, key=f"nav_{key}"):
                    st.session_state.page = key
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
        st.markdown("""<div style="margin:0 1.1rem;height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,0.1),transparent);margin-bottom:.75rem;"></div>""", unsafe_allow_html=True)

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
    </div>""", unsafe_allow_html=True)

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
    st.markdown('<div class="sec-label">Pending Approvals</div>', unsafe_allow_html=True)

    if not pending:
        st.markdown('<div class="empty-state"><div class="icon">✨</div><div class="msg">All caught up — no pending requests.</div></div>', unsafe_allow_html=True)
    else:
        for r in pending:
            uid = r.get("user_id", "")
            short_uid = uid[:14] + "…" if len(uid) > 14 else uid
            st.markdown(f"""
            <div class="req-card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:.5rem;">
                    <div>
                        <div class="r-sub">User: {short_uid}</div>
                        <div class="r-amt">{format_iqd(r.get('amount',0))}</div>
                        <div class="r-reason">{r.get('reason','—')}</div>
                        <div class="r-meta">Submitted {format_date(r.get('created_at',''))}</div>
                    </div>
                    <div>{status_badge("pending")}</div>
                </div>
            </div>""", unsafe_allow_html=True)

            if r.get("invoice_image_url"):
                with st.expander("🖼  View Invoice"):
                    st.image(r["invoice_image_url"], use_column_width=True)

            ca, cr, _, _ = st.columns([1, 1, 0.2, 2])
            with ca:
                if st.button("✅  Approve", key=f"ap_{r['id']}"):
                    supabase.table("petty_cash_requests").update({"status": "approved"}).eq("id", r["id"]).execute()
                    st.rerun()
            with cr:
                # Rejection with note
                if st.button("❌  Reject", key=f"rj_{r['id']}"):
                    st.session_state[f"show_reject_{r['id']}"] = True
                    st.rerun()

            # Rejection note form
            if st.session_state.get(f"show_reject_{r['id']}"):
                with st.form(key=f"reject_form_{r['id']}"):
                    note = st.text_input("Reason for rejection (will be shown to submitter)", placeholder="e.g. Missing valid receipt", key=f"note_{r['id']}")
                    c_confirm, c_cancel, _ = st.columns([1, 1, 2])
                    if c_confirm.form_submit_button("Confirm Reject"):
                        supabase.table("petty_cash_requests").update({"status": "rejected", "admin_note": note}).eq("id", r["id"]).execute()
                        st.session_state.pop(f"show_reject_{r['id']}", None)
                        st.rerun()
                    if c_cancel.form_submit_button("Cancel"):
                        st.session_state.pop(f"show_reject_{r['id']}", None)
                        st.rerun()

            st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ADMIN — ANALYTICS  (NEW)
# ─────────────────────────────────────────────
def page_admin_analytics():
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        HAS_PLOTLY = True
    except ImportError:
        HAS_PLOTLY = False

    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Analytics</div>
        <div class="page-subtitle">Visual insights into petty cash spending</div>
        <div class="title-line"></div>
    </div>""", unsafe_allow_html=True)

    all_reqs = fetch_all_requests()
    if not all_reqs:
        st.markdown('<div class="empty-state"><div class="icon">📈</div><div class="msg">No data available yet.</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    approved = [r for r in all_reqs if r.get("status") == "approved"]

    # ── Date range filter ──
    st.markdown('<div class="sec-label">Date Filter</div>', unsafe_allow_html=True)
    cf1, cf2 = st.columns(2)
    with cf1: date_from = st.date_input("From", value=date(date.today().year, 1, 1))
    with cf2: date_to   = st.date_input("To",   value=date.today())

    def in_range(r):
        try:
            dt = datetime.fromisoformat(r.get("created_at","").replace("Z","+00:00")).date()
            return date_from <= dt <= date_to
        except: return True

    approved_f = [r for r in approved if in_range(r)]
    all_f      = [r for r in all_reqs if in_range(r)]

    # ── KPIs ──
    st.markdown("<hr>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Approved Requests", len(approved_f))
    c2.metric("Total Approved",    format_iqd(sum(float(r.get("amount",0)) for r in approved_f)))
    c3.metric("Avg per Request",   format_iqd(sum(float(r.get("amount",0)) for r in approved_f) / max(len(approved_f),1)))

    if not HAS_PLOTLY:
        st.info("Install plotly for interactive charts: `pip install plotly`")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    GOLD  = "#D4AF37"
    GOLD2 = "#EEC84A"
    GREEN = "#4cd884"
    RED   = "#e87060"
    BG    = "rgba(0,0,0,0)"
    PAPER = "rgba(0,0,0,0)"
    FONT  = "#EAE0CC"
    GRID  = "rgba(212,175,55,0.07)"

    chart_layout = dict(
        paper_bgcolor=PAPER, plot_bgcolor=BG,
        font=dict(family="Inter", color=FONT, size=11),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(212,175,55,0.15)", borderwidth=1),
    )

    # ── 1. Monthly spending bar chart ──
    st.markdown('<div class="sec-label">Monthly Approved Spending</div>', unsafe_allow_html=True)
    monthly: dict = defaultdict(float)
    for r in approved_f:
        try:
            dt = datetime.fromisoformat(r.get("created_at","").replace("Z","+00:00"))
            key = dt.strftime("%b %Y")
            monthly[key] += float(r.get("amount", 0))
        except: pass

    if monthly:
        months = list(monthly.keys())
        amounts = [monthly[m] for m in months]
        fig1 = go.Figure(go.Bar(
            x=months, y=amounts,
            marker=dict(color=GOLD, opacity=0.85,
                        line=dict(color=GOLD2, width=1)),
            hovertemplate="<b>%{x}</b><br>%{y:,.0f} IQD<extra></extra>",
        ))
        fig1.update_layout(**chart_layout, height=300,
            yaxis=dict(gridcolor=GRID, tickformat=",.0f"),
            xaxis=dict(gridcolor=GRID))
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ── 2. Status distribution pie ──
    st.markdown('<div class="sec-label">Request Status Distribution</div>', unsafe_allow_html=True)
    status_counts = defaultdict(int)
    for r in all_f: status_counts[r.get("status","pending")] += 1
    if status_counts:
        labels = list(status_counts.keys())
        values = [status_counts[l] for l in labels]
        color_map = {"pending": "#f1c40f", "approved": GREEN, "rejected": RED}
        colors_list = [color_map.get(l, GOLD) for l in labels]
        fig2 = go.Figure(go.Pie(
            labels=[l.capitalize() for l in labels], values=values,
            marker=dict(colors=colors_list, line=dict(color="#06080D", width=3)),
            hole=0.55,
            hovertemplate="<b>%{label}</b><br>%{value} requests (%{percent})<extra></extra>",
            textfont=dict(color=FONT),
        ))
        fig2.update_layout(**chart_layout, height=300,
            annotations=[dict(text=f"<b>{sum(values)}</b><br>total", x=0.5, y=0.5,
                              font=dict(size=14, color=FONT), showarrow=False)])
        c_left, c_right = st.columns(2)
        with c_left:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

        # ── 3. Top spenders bar ──
        with c_right:
            user_totals: dict = defaultdict(float)
            for r in approved_f:
                uid = (r.get("user_id") or "unknown")[:10] + "…"
                user_totals[uid] += float(r.get("amount", 0))
            if user_totals:
                sorted_users = sorted(user_totals.items(), key=lambda x: -x[1])[:8]
                uids    = [u for u,_ in sorted_users]
                amounts = [a for _,a in sorted_users]
                fig3 = go.Figure(go.Bar(
                    x=amounts, y=uids, orientation="h",
                    marker=dict(color=GOLD2, opacity=0.8),
                    hovertemplate="%{y}<br><b>%{x:,.0f} IQD</b><extra></extra>",
                ))
                fig3.update_layout(**chart_layout, height=300,
                    title=dict(text="Top Spenders", font=dict(color=FONT, size=13)),
                    xaxis=dict(gridcolor=GRID, tickformat=",.0f"),
                    yaxis=dict(gridcolor=GRID))
                st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
                st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
                st.markdown('</div>', unsafe_allow_html=True)

    # ── EXPORT PDF ──
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Export Report</div>', unsafe_allow_html=True)
    month_options = sorted(set(
        datetime.fromisoformat(r.get("created_at","2024-01-01").replace("Z","+00:00")).strftime("%Y-%m")
        for r in approved if r.get("created_at")
    ), reverse=True)

    if month_options:
        sel_month = st.selectbox("Select Month", month_options, key="export_month")
        export_reqs = [r for r in approved if r.get("created_at","").startswith(sel_month)]
        col_info, col_btn = st.columns([2, 1])
        col_info.markdown(f"""
        <div style="font-size:.85rem;color:rgba(234,224,204,.55);padding:.6rem 0;">
            {len(export_reqs)} approved requests · {format_iqd(sum(float(r.get('amount',0)) for r in export_reqs))} total
        </div>""", unsafe_allow_html=True)
        with col_btn:
            if st.button("⬇  Download Report", key="dl_pdf"):
                pdf_bytes = generate_pdf_report(export_reqs, sel_month)
                ext = "pdf" if pdf_bytes[:4] == b"%PDF" else "csv"
                st.download_button(
                    label=f"📄 Save {sel_month}.{ext}",
                    data=pdf_bytes,
                    file_name=f"jawhar_report_{sel_month}.{ext}",
                    mime="application/pdf" if ext=="pdf" else "text/csv",
                    key="save_pdf",
                )
    else:
        st.info("No approved requests to export.")

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ADMIN — ALL REQUESTS
# ─────────────────────────────────────────────
def page_admin_all():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="page-header">
        <div class="page-title">All Requests</div>
        <div class="page-subtitle">Complete history with date filtering</div>
        <div class="title-line"></div>
    </div>""", unsafe_allow_html=True)

    all_reqs = fetch_all_requests()

    cf1, cf2, cf3, cf4 = st.columns(4)
    with cf1: fstatus  = st.selectbox("Status", ["All", "Pending", "Approved", "Rejected"])
    with cf2: search   = st.text_input("Search reason…", placeholder="e.g. electricity")
    with cf3: dt_from  = st.date_input("From date", value=None, key="af_from")
    with cf4: dt_to    = st.date_input("To date",   value=None, key="af_to")

    if fstatus != "All":
        all_reqs = [r for r in all_reqs if r.get("status") == fstatus.lower()]
    if search:
        s = search.lower()
        all_reqs = [r for r in all_reqs if s in (r.get("reason","") or "").lower()]
    if dt_from:
        all_reqs = [r for r in all_reqs if r.get("created_at","") >= dt_from.isoformat()]
    if dt_to:
        all_reqs = [r for r in all_reqs if r.get("created_at","")[:10] <= dt_to.isoformat()]

    st.markdown(f'<div class="sec-label">{len(all_reqs)} Result{"s" if len(all_reqs)!=1 else ""}</div>', unsafe_allow_html=True)

    if not all_reqs:
        st.markdown('<div class="empty-state"><div class="icon">🔍</div><div class="msg">No requests match your filters.</div></div>', unsafe_allow_html=True)
    else:
        for r in all_reqs:
            status = r.get("status", "pending")
            uid    = r.get("user_id", "")
            short  = uid[:14] + "…" if len(uid) > 14 else uid
            note_html = f'<div class="r-note">⚠ Admin note: {r["admin_note"]}</div>' if r.get("admin_note") else ""
            st.markdown(f"""
            <div class="req-card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:.5rem;">
                    <div>
                        <div class="r-sub">{short}</div>
                        <div class="r-amt">{format_iqd(r.get('amount',0))}</div>
                        <div class="r-reason">{r.get('reason','—')}</div>
                        {note_html}
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
                if cr.button("❌ Reject",  key=f"r2_{r['id']}"):
                    st.session_state[f"show_reject2_{r['id']}"] = True
                    st.rerun()
                if st.session_state.get(f"show_reject2_{r['id']}"):
                    with st.form(key=f"rf2_{r['id']}"):
                        note = st.text_input("Rejection reason", key=f"rn2_{r['id']}")
                        c1b, c2b, _ = st.columns([1,1,2])
                        if c1b.form_submit_button("Confirm"):
                            supabase.table("petty_cash_requests").update({"status":"rejected","admin_note":note}).eq("id",r["id"]).execute()
                            st.session_state.pop(f"show_reject2_{r['id']}", None)
                            st.rerun()
                        if c2b.form_submit_button("Cancel"):
                            st.session_state.pop(f"show_reject2_{r['id']}", None)
                            st.rerun()
            st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ADMIN — BRANCHES
# ─────────────────────────────────────────────
def page_admin_branches():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Branch Overview</div>
        <div class="page-subtitle">Spending summary with monthly limits</div>
        <div class="title-line"></div>
    </div>""", unsafe_allow_html=True)

    all_reqs = fetch_all_requests()
    stats: dict = defaultdict(lambda: {"total": 0.0, "pending": 0, "approved": 0, "rejected": 0, "count": 0, "monthly": 0.0})
    now = datetime.utcnow()
    month_prefix = f"{now.year}-{now.month:02d}"

    for r in all_reqs:
        key = r.get("user_id", "Unknown")
        s   = r.get("status", "pending")
        amt = float(r.get("amount", 0))
        stats[key]["count"] += 1
        stats[key]["total"] += amt
        stats[key][s] = stats[key].get(s, 0) + 1
        if r.get("created_at","").startswith(month_prefix) and s in ("approved","pending"):
            stats[key]["monthly"] += amt

    if not stats:
        st.markdown('<div class="empty-state"><div class="icon">🏪</div><div class="msg">No data yet.</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="sec-label">{len(stats)} User{"s" if len(stats)!=1 else ""}</div>', unsafe_allow_html=True)
        for uid, s in sorted(stats.items(), key=lambda x: -x[1]["total"]):
            short = uid[:18] + "…" if len(uid) > 18 else uid
            bar   = limit_bar_html(s["monthly"], MONTHLY_LIMIT)
            st.markdown(f"""
            <div class="a-card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;">
                    <div style="flex:1;min-width:220px;">
                        <div style="font-size:.68rem;color:rgba(234,224,204,.32);text-transform:uppercase;letter-spacing:.1em;margin-bottom:.3rem;">User ID</div>
                        <div style="font-family:'Cormorant Garamond',serif;font-size:1.25rem;color:#EAE0CC;font-weight:600;margin-bottom:.5rem;">{short}</div>
                        {bar}
                        <div style="font-size:.75rem;color:rgba(234,224,204,.42);margin-top:.4rem;">
                            {s['count']} requests · {format_iqd(s['total'])} lifetime
                        </div>
                    </div>
                    <div style="display:flex;gap:1.5rem;align-items:center;flex-wrap:wrap;">
                        <div style="text-align:center;">
                            <div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;color:#f1c40f;">{s['pending']}</div>
                            <div style="font-size:.62rem;color:rgba(234,224,204,.3);text-transform:uppercase;letter-spacing:.08em;">Pending</div>
                        </div>
                        <div style="text-align:center;">
                            <div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;color:#4cd884;">{s['approved']}</div>
                            <div style="font-size:.62rem;color:rgba(234,224,204,.3);text-transform:uppercase;letter-spacing:.08em;">Approved</div>
                        </div>
                        <div style="text-align:center;">
                            <div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;color:#e87060;">{s['rejected']}</div>
                            <div style="font-size:.62rem;color:rgba(234,224,204,.3);text-transform:uppercase;letter-spacing:.08em;">Rejected</div>
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

    # Monthly limit check
    spent_this_month = get_user_monthly_spent(user_id)
    remaining = max(MONTHLY_LIMIT - spent_this_month, 0)
    st.markdown(limit_bar_html(spent_this_month, MONTHLY_LIMIT), unsafe_allow_html=True)
    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)

    try:
        branch_data = supabase.table("branches").select("*").eq("user_id", user_id).execute().data
        branch_id = branch_data[0]["id"] if branch_data else None
    except:
        branch_id = None

    tab1, tab2 = st.tabs(["📤  Submit Invoice", "📜  My Requests"])

    with tab1:
        st.markdown('<div class="sec-label">New Petty Cash Request</div>', unsafe_allow_html=True)

        if remaining <= 0:
            st.error(f"⚠ Monthly limit reached ({format_iqd(MONTHLY_LIMIT)}). No new requests can be submitted this month.")
        else:
            if spent_this_month > MONTHLY_LIMIT * 0.8:
                st.warning(f"⚠ You've used {spent_this_month/MONTHLY_LIMIT*100:.0f}% of your monthly limit. Remaining: {format_iqd(remaining)}")

            with st.form("submit_form", clear_on_submit=True):
                amt          = st.number_input("Amount (IQD)", min_value=0, step=500, format="%d", help="Enter the exact amount spent")
                reason       = st.text_area("Description / Reason", placeholder="e.g. Monthly electricity bill", height=100)
                invoice_file = st.file_uploader("Upload Receipt or Invoice", type=["png","jpg","jpeg","pdf"])
                submitted    = st.form_submit_button("Submit Request  →", use_container_width=True)

                if submitted:
                    errors = []
                    if amt <= 0:              errors.append("Amount must be greater than 0.")
                    if not reason.strip():    errors.append("Please provide a description.")
                    if not invoice_file:      errors.append("Please upload an invoice or receipt.")
                    if amt > remaining:       errors.append(f"Amount exceeds your remaining monthly limit of {format_iqd(remaining)}.")
                    for e in errors: st.error(e)

                    if not errors:
                        image_url = None
                        with st.spinner("Uploading invoice…"):
                            image_url = upload_invoice_image(invoice_file.read(), invoice_file.name)
                        with st.spinner("Submitting request…"):
                            try:
                                supabase.table("petty_cash_requests").insert({
                                    "user_id":           user_id,
                                    "branch_id":         branch_id,
                                    "amount":            amt,
                                    "reason":            reason.strip(),
                                    "status":            "pending",
                                    "invoice_image_url": image_url,
                                }).execute()
                                st.success("✅ Request submitted successfully! Management will review it shortly.")
                            except Exception as e:
                                st.error(f"Submission failed: {e}")

    with tab2:
        st.markdown('<div class="sec-label">Your Request History</div>', unsafe_allow_html=True)
        try:
            my_reqs = supabase.table("petty_cash_requests").select("*").eq("user_id", user_id).order("created_at", desc=True).execute().data or []
        except:
            my_reqs = []
            st.warning("Could not load history.")

        if not my_reqs:
            st.markdown('<div class="empty-state"><div class="icon">📋</div><div class="msg">No requests submitted yet.</div></div>', unsafe_allow_html=True)
        else:
            total_approved = sum(float(r.get("amount",0)) for r in my_reqs if r.get("status") == "approved")
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Requests",  len(my_reqs))
            c2.metric("Approved Amount", format_iqd(total_approved))
            c3.metric("Pending",         sum(1 for r in my_reqs if r.get("status") == "pending"))
            st.markdown("<hr>", unsafe_allow_html=True)

            for r in my_reqs:
                status = r.get("status", "pending")
                note_html = f'<div class="r-note">⚠ Admin note: {r["admin_note"]}</div>' if r.get("admin_note") else ""
                st.markdown(f"""
                <div class="req-card">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:.5rem;">
                        <div>
                            <div class="r-amt">{format_iqd(r.get('amount',0))}</div>
                            <div class="r-reason">{r.get('reason','—')}</div>
                            {note_html}
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
        valid_pages = ("admin_dashboard","admin_analytics","admin_all","admin_branches")
        if st.session_state.page not in valid_pages:
            st.session_state.page = "admin_dashboard"
        {
            "admin_dashboard": page_admin_dashboard,
            "admin_analytics": page_admin_analytics,
            "admin_all":       page_admin_all,
            "admin_branches":  page_admin_branches,
        }[st.session_state.page]()
    else:
        page_branch_portal(user)
