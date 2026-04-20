import streamlit as st
from supabase import create_client, Client
import uuid
from datetime import datetime, date
from collections import defaultdict
import io

SUPABASE_URL  = "https://xtjnatjxsxbyrwkqytqd.supabase.co"
SUPABASE_KEY  = "sb_publishable_NPbMYsWC7UhEaVmMKga16w_LjITdW7w"
ADMIN_EMAIL   = "admin@jawhar.com"
DEFAULT_LIMIT = 500_000

st.set_page_config(page_title="Jawhar ERP", page_icon="💎", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@300;400;500;600&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
.stApp{background:#06080D;font-family:'Inter',sans-serif;color:#EAE0CC;
background-image:radial-gradient(ellipse 110% 55% at 50% -5%,rgba(212,175,55,.09) 0%,transparent 60%),
radial-gradient(ellipse 55% 55% at 95% 90%,rgba(212,175,55,.05) 0%,transparent 55%);}
#MainMenu,footer,header,.stDeployButton,[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important;}
.block-container{padding:0!important;max-width:100%!important;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#090B10 0%,#06080D 100%)!important;border-right:1px solid rgba(212,175,55,.15)!important;box-shadow:6px 0 40px rgba(0,0,0,.5)!important;}
[data-testid="stSidebarContent"]{padding:0!important;}
.stTextInput>div>div>input,.stNumberInput>div>div>input,.stTextArea textarea{background:rgba(255,255,255,.022)!important;border:1px solid rgba(212,175,55,.18)!important;border-radius:11px!important;color:#EAE0CC!important;font-family:'Inter',sans-serif!important;font-size:.92rem!important;padding:.68rem 1.05rem!important;transition:border-color .25s,box-shadow .25s;caret-color:#D4AF37;}
.stTextInput>div>div>input:focus,.stNumberInput>div>div>input:focus,.stTextArea textarea:focus{border-color:rgba(212,175,55,.55)!important;background:rgba(212,175,55,.035)!important;box-shadow:0 0 0 3px rgba(212,175,55,.07)!important;outline:none!important;}
.stTextInput label,.stNumberInput label,.stTextArea label,.stSelectbox label,.stDateInput label{color:rgba(234,224,204,.45)!important;font-size:.7rem!important;font-weight:500!important;letter-spacing:.11em!important;text-transform:uppercase!important;}
.stSelectbox>div>div{background:rgba(255,255,255,.022)!important;border:1px solid rgba(212,175,55,.18)!important;border-radius:11px!important;color:#EAE0CC!important;}
.stButton>button{background:linear-gradient(135deg,#B8942A 0%,#EEC84A 45%,#B8942A 100%)!important;color:#06080D!important;border:none!important;border-radius:11px!important;font-family:'Inter',sans-serif!important;font-weight:600!important;font-size:.87rem!important;letter-spacing:.045em!important;padding:.67rem 1.8rem!important;cursor:pointer!important;transition:all .3s ease!important;box-shadow:0 4px 22px rgba(212,175,55,.22)!important;}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 8px 36px rgba(212,175,55,.38)!important;}
.stButton>button:active{transform:translateY(0)!important;}
.stTabs [data-baseweb="tab-list"]{background:transparent!important;border-bottom:1px solid rgba(212,175,55,.1)!important;gap:0!important;padding:0!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:rgba(234,224,204,.38)!important;font-family:'Inter',sans-serif!important;font-size:.87rem!important;font-weight:500!important;border:none!important;border-bottom:2px solid transparent!important;padding:.9rem 1.7rem!important;transition:all .2s!important;}
.stTabs [aria-selected="true"]{color:#D4AF37!important;border-bottom:2px solid #D4AF37!important;background:transparent!important;}
[data-testid="stFileUploader"]{border:1.5px dashed rgba(212,175,55,.22)!important;border-radius:14px!important;background:rgba(212,175,55,.012)!important;padding:.5rem!important;}
[data-testid="stExpander"]{border:1px solid rgba(212,175,55,.11)!important;border-radius:12px!important;background:rgba(255,255,255,.012)!important;overflow:hidden!important;}
.stSuccess>div{background:rgba(39,174,96,.07)!important;border:1px solid rgba(39,174,96,.22)!important;border-left:3px solid #27ae60!important;color:#5dda8a!important;border-radius:11px!important;}
.stError>div{background:rgba(192,57,43,.07)!important;border:1px solid rgba(192,57,43,.22)!important;border-left:3px solid #c0392b!important;color:#e87060!important;border-radius:11px!important;}
.stWarning>div{background:rgba(212,175,55,.06)!important;border:1px solid rgba(212,175,55,.18)!important;border-left:3px solid #D4AF37!important;border-radius:11px!important;}
.stInfo>div{background:rgba(99,130,200,.06)!important;border:1px solid rgba(99,130,200,.18)!important;border-left:3px solid #6382c8!important;border-radius:11px!important;}
[data-testid="stMetric"]{background:linear-gradient(140deg,rgba(212,175,55,.055) 0%,rgba(255,255,255,.018) 100%)!important;border:1px solid rgba(212,175,55,.13)!important;border-radius:15px!important;padding:1.4rem 1.6rem!important;position:relative!important;overflow:hidden!important;}
[data-testid="stMetric"]::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,.38),transparent);}
[data-testid="stMetricLabel"]{color:rgba(234,224,204,.42)!important;font-size:.7rem!important;text-transform:uppercase!important;letter-spacing:.13em!important;}
[data-testid="stMetricValue"]{color:#D4AF37!important;font-family:'Cormorant Garamond',serif!important;font-size:2.1rem!important;font-weight:600!important;}
hr{border:none!important;border-top:1px solid rgba(212,175,55,.09)!important;margin:2rem 0!important;}
.pw{padding:2.5rem 3rem 4rem;max-width:1120px;}
.ph{margin-bottom:2.4rem;}
.pt{font-family:'Cormorant Garamond',serif;font-size:2.5rem;font-weight:600;color:#EAE0CC;line-height:1.1;}
.ps{font-size:.83rem;color:rgba(234,224,204,.35);margin-top:.4rem;letter-spacing:.06em;}
.tl{width:38px;height:2px;background:linear-gradient(90deg,#D4AF37,#EEC84A);border-radius:2px;margin:.75rem 0 0;}
.sl{font-size:.68rem;font-weight:600;color:#C9A227;text-transform:uppercase;letter-spacing:.15em;margin-bottom:1rem;display:flex;align-items:center;gap:.6rem;}
.sl::after{content:'';flex:1;height:1px;background:rgba(212,175,55,.1);}
.rc{background:linear-gradient(140deg,rgba(255,255,255,.022) 0%,rgba(212,175,55,.018) 100%);border:1px solid rgba(212,175,55,.1);border-radius:16px;padding:1.5rem 1.8rem;margin-bottom:.85rem;position:relative;overflow:hidden;transition:border-color .25s,box-shadow .25s,transform .2s;}
.rc::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,.22),transparent);}
.rc:hover{border-color:rgba(212,175,55,.26);box-shadow:0 12px 45px rgba(0,0,0,.28);transform:translateY(-1px);}
.rc .rs{font-size:.7rem;color:rgba(234,224,204,.35);text-transform:uppercase;letter-spacing:.1em;margin-bottom:.25rem;}
.rc .ra{font-family:'Cormorant Garamond',serif;font-size:1.75rem;font-weight:600;color:#D4AF37;line-height:1.1;}
.rc .rr{font-size:.89rem;color:rgba(234,224,204,.7);margin:.3rem 0 .2rem;}
.rc .rn{font-size:.82rem;color:rgba(232,100,80,.85);margin:.3rem 0;font-style:italic;padding:.3rem .7rem;background:rgba(232,100,80,.07);border-radius:6px;border-left:2px solid rgba(232,100,80,.45);}
.rc .rm{font-size:.7rem;color:rgba(234,224,204,.28);margin-top:.4rem;}
.badge{display:inline-flex;align-items:center;gap:.3rem;padding:.22rem .85rem;border-radius:20px;font-size:.67rem;font-weight:600;letter-spacing:.09em;text-transform:uppercase;}
.bp{background:rgba(241,196,15,.11);color:#f1c40f;border:1px solid rgba(241,196,15,.26);}
.ba{background:rgba(39,174,96,.11);color:#4cd884;border:1px solid rgba(39,174,96,.26);}
.br{background:rgba(192,57,43,.11);color:#e87060;border:1px solid rgba(192,57,43,.26);}
.ac{background:linear-gradient(140deg,rgba(255,255,255,.022) 0%,rgba(212,175,55,.018) 100%);border:1px solid rgba(212,175,55,.1);border-radius:16px;padding:1.6rem 1.8rem;margin-bottom:.85rem;position:relative;overflow:hidden;transition:border-color .25s;}
.ac::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,.18),transparent);}
.ac:hover{border-color:rgba(212,175,55,.26);}
.lbb{background:rgba(255,255,255,.06);border-radius:6px;height:6px;overflow:hidden;}
.lbf{height:100%;border-radius:6px;transition:width .6s ease;}
.cw{background:linear-gradient(140deg,rgba(255,255,255,.018) 0%,rgba(212,175,55,.012) 100%);border:1px solid rgba(212,175,55,.1);border-radius:16px;padding:1.4rem 1.6rem;margin-bottom:1.2rem;position:relative;overflow:hidden;}
.cw::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,.2),transparent);}
.es{text-align:center;padding:3.5rem 2rem;color:rgba(234,224,204,.28);}
.es .ei{font-size:2.4rem;margin-bottom:.7rem;opacity:.55;}
.es .em{font-size:.9rem;}
[data-testid="stSidebar"] .stButton>button{background:transparent!important;color:rgba(234,224,204,.5)!important;border:1px solid rgba(212,175,55,.07)!important;border-radius:10px!important;font-size:.84rem!important;font-weight:400!important;box-shadow:none!important;padding:.6rem 1rem!important;transition:all .2s!important;}
[data-testid="stSidebar"] .stButton>button:hover{background:rgba(212,175,55,.065)!important;color:#D4AF37!important;border-color:rgba(212,175,55,.22)!important;transform:none!important;box-shadow:none!important;}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:rgba(212,175,55,.18);border-radius:10px;}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

for k, v in {"user": None, "page": "login", "sc": False}.items():
    if k not in st.session_state:
        st.session_state[k] = v

if not st.session_state.sc:
    st.session_state.sc = True
    try: supabase.auth.sign_out()
    except: pass
    st.session_state.user = None


# ── HELPERS ──────────────────────────────────
def fiqd(a) -> str:
    try: return f"{float(a):,.0f} IQD"
    except: return "0 IQD"

def fdate(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y · %H:%M")
    except: return iso or "—"

def badge(status: str) -> str:
    m = {"pending":("bp","●","Pending"),"approved":("ba","●","Approved"),"rejected":("br","●","Rejected")}
    c, i, l = m.get(status, m["pending"])
    return f'<span class="badge {c}">{i} {l}</span>'

def upload_img(fb: bytes, fn: str):
    try:
        ext = fn.rsplit(".",1)[-1].lower()
        ct  = "application/pdf" if ext=="pdf" else f"image/{ext}"
        p   = f"invoices/{uuid.uuid4()}.{ext}"
        supabase.storage.from_("invoices").upload(path=p, file=fb, file_options={"content-type":ct})
        return supabase.storage.from_("invoices").get_public_url(p)
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return None

def fetch_reqs():
    try: return supabase.table("petty_cash_requests").select("*").order("created_at",desc=True).execute().data or []
    except: return []

def get_limit(uid: str) -> float:
    try:
        r = supabase.table("branch_limits").select("monthly_limit").eq("user_id",uid).execute().data
        if r: return float(r[0]["monthly_limit"])
    except: pass
    return DEFAULT_LIMIT

def save_limit(uid: str, lim: float) -> bool:
    try:
        supabase.table("branch_limits").upsert({"user_id":uid,"monthly_limit":lim,"updated_at":datetime.utcnow().isoformat()}).execute()
        return True
    except Exception as e:
        st.error(f"Save failed: {e}")
        return False

def monthly_spent(uid: str) -> float:
    try:
        now = datetime.utcnow()
        st_ = f"{now.year}-{now.month:02d}-01T00:00:00"
        rows = supabase.table("petty_cash_requests").select("amount,status").eq("user_id",uid).gte("created_at",st_).in_("status",["approved","pending"]).execute().data or []
        return sum(float(r.get("amount",0)) for r in rows)
    except: return 0.0

def bar_html(spent, lim, compact=False):
    pct = min(spent/lim*100,100) if lim>0 else 0
    col = "#D4AF37" if pct<70 else ("#e87060" if pct>=90 else "#f1c40f")
    sz  = ".7rem" if compact else ".72rem"
    m   = "0" if compact else ".5rem 0 .2rem"
    return f"""<div style="margin:{m};">
<div style="display:flex;justify-content:space-between;font-size:{sz};color:rgba(234,224,204,.38);margin-bottom:.3rem;">
<span>This Month</span><span style="color:rgba(234,224,204,.55);">{fiqd(spent)} / {fiqd(lim)}</span></div>
<div class="lbb"><div class="lbf" style="width:{pct:.1f}%;background:{col};"></div></div></div>"""

def make_report(reqs, month) -> bytes:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors as C
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf,pagesize=A4,leftMargin=2*cm,rightMargin=2*cm,topMargin=2*cm,bottomMargin=2*cm)
        S   = getSampleStyleSheet()
        gold= C.HexColor("#D4AF37")
        ts  = ParagraphStyle("t",parent=S["Title"],fontSize=20,textColor=gold,spaceAfter=4)
        ss  = ParagraphStyle("s",parent=S["Normal"],fontSize=10,textColor=C.HexColor("#888"),spaceAfter=14)
        ns  = ParagraphStyle("n",parent=S["Normal"],fontSize=9, textColor=C.HexColor("#333"))
        tot = sum(float(r.get("amount",0)) for r in reqs)
        els = [Paragraph("JAWHAR ERP",ts),
               Paragraph(f"Approved Petty Cash — {month}",ss),
               Paragraph(f"Generated: {datetime.now().strftime('%d %b %Y %H:%M')}  |  Records: {len(reqs)}  |  Total: {fiqd(tot)}",ns),
               Spacer(1,.4*cm)]
        data = [["#","Date","User","Amount (IQD)","Reason"]]
        for i,r in enumerate(reqs,1):
            uid = (r.get("user_id") or "")[:14]+"…"
            data.append([str(i),fdate(r.get("created_at",""))[:11],uid,f"{float(r.get('amount',0)):,.0f}",(r.get("reason","") or "")[:55]])
        data.append(["","","TOTAL",f"{tot:,.0f}",""])
        tbl = Table(data,colWidths=[.9*cm,3*cm,4.2*cm,3.2*cm,6.5*cm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),gold),("TEXTCOLOR",(0,0),(-1,0),C.black),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
            ("ROWBACKGROUNDS",(0,1),(-1,-2),[C.HexColor("#f9f9f9"),C.white]),
            ("BACKGROUND",(0,-1),(-1,-1),C.HexColor("#FFF8E1")),
            ("FONTNAME",(0,-1),(-1,-1),"Helvetica-Bold"),
            ("GRID",(0,0),(-1,-1),.4,C.HexColor("#ddd")),
            ("ALIGN",(3,0),(3,-1),"RIGHT"),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ]))
        els.append(tbl); doc.build(els)
        return buf.getvalue()
    except ImportError:
        lines = [f"JAWHAR ERP — {month}",f"Generated: {datetime.now()}","Date,User,Amount,Reason"]
        for r in reqs:
            lines.append(f"{fdate(r.get('created_at',''))},{(r.get('user_id') or '')[:16]},{float(r.get('amount',0)):.0f},{r.get('reason','')}")
        lines.append(f",,TOTAL {sum(float(r.get('amount',0)) for r in reqs):.0f},")
        return "\n".join(lines).encode("utf-8")


# ── LOGIN ─────────────────────────────────────
def page_login():
    _,col,_ = st.columns([1,1.1,1])
    with col:
        st.markdown("""
        <div style="padding:3.5rem 0 1.5rem;text-align:center;">
          <div style="font-size:3rem;filter:drop-shadow(0 0 24px rgba(212,175,55,.35));">💎</div>
          <div style="font-family:'Cormorant Garamond',serif;font-size:2.7rem;font-weight:700;
               background:linear-gradient(135deg,#A87C1A,#EEC84A,#B8942A);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               background-clip:text;letter-spacing:.08em;line-height:1;">JAWHAR</div>
          <div style="font-size:.67rem;color:rgba(234,224,204,.25);letter-spacing:.22em;
               text-transform:uppercase;margin:.4rem 0 2rem;">Petty Cash Management System</div>
        </div>
        <div style="background:linear-gradient(160deg,rgba(255,255,255,.032) 0%,rgba(212,175,55,.018) 100%);
             border:1px solid rgba(212,175,55,.16);border-radius:22px;padding:2.6rem 2.3rem;
             box-shadow:0 45px 110px rgba(0,0,0,.6);position:relative;overflow:hidden;">
          <div style="position:absolute;top:0;left:50%;transform:translateX(-50%);width:50%;height:1px;
               background:linear-gradient(90deg,transparent,rgba(212,175,55,.7),transparent);"></div>
        </div>""", unsafe_allow_html=True)

        email = st.text_input("Email Address", placeholder="you@jawhar.com", key="le")
        pw    = st.text_input("Password", type="password", placeholder="••••••••", key="lp")
        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

        if st.button("Sign In  →", use_container_width=True):
            if not email or not pw:
                st.warning("Please enter your email and password.")
            else:
                with st.spinner("Verifying…"):
                    try:
                        res = supabase.auth.sign_in_with_password({"email": email, "password": pw})
                        st.session_state.user = res.user
                        st.rerun()
                    except:
                        st.error("Access denied — please check your credentials.")

        st.markdown('<p style="text-align:center;font-size:.68rem;color:rgba(234,224,204,.18);margin-top:1.5rem;">Restricted system · Session ends on browser close</p>', unsafe_allow_html=True)


# ── SIDEBAR ───────────────────────────────────
def render_sidebar(email: str, is_admin: bool):
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:1.9rem 1.4rem 1rem;">
          <div style="font-family:'Cormorant Garamond',serif;font-size:1.45rem;font-weight:700;
               background:linear-gradient(135deg,#C9A227,#EEC84A,#C9A227);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               background-clip:text;letter-spacing:.06em;">💎 JAWHAR ERP</div>
          <div style="font-size:.62rem;color:rgba(234,224,204,.26);letter-spacing:.18em;
               text-transform:uppercase;margin-top:.2rem;">{"Management" if is_admin else "Branch Portal"}</div>
        </div>
        <div style="margin:0 1.1rem;height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,.18),transparent);"></div>
        <div style="padding:.9rem 1.4rem .5rem;">
          <div style="font-size:.62rem;color:rgba(234,224,204,.28);text-transform:uppercase;letter-spacing:.12em;margin-bottom:.35rem;">Signed in as</div>
          <div style="font-size:.82rem;color:#D4AF37;font-weight:500;word-break:break-all;margin-bottom:1.3rem;">{email}</div>
        """, unsafe_allow_html=True)

        if is_admin:
            st.markdown('<div style="font-size:.62rem;color:rgba(234,224,204,.28);text-transform:uppercase;letter-spacing:.12em;margin-bottom:.55rem;">Navigation</div>', unsafe_allow_html=True)
            for key, lbl in [
                ("admin_dashboard","📊  Dashboard"),
                ("admin_analytics","📈  Analytics"),
                ("admin_all",      "📋  All Requests"),
                ("admin_branches", "🏪  Branches"),
                ("admin_limits",   "⚙️  Branch Limits"),
            ]:
                if st.button(lbl, use_container_width=True, key=f"n_{key}"):
                    st.session_state.page = key; st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
        st.markdown('<div style="margin:0 1.1rem;height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,.1),transparent);margin-bottom:.75rem;"></div>', unsafe_allow_html=True)

        if st.button("⎋  Sign Out", use_container_width=True, key="so"):
            try: supabase.auth.sign_out()
            except: pass
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()


# ── ADMIN DASHBOARD ───────────────────────────
def page_admin_dashboard():
    st.markdown('<div class="pw">', unsafe_allow_html=True)
    st.markdown('<div class="ph"><div class="pt">Command Center</div><div class="ps">Real-time overview of all petty cash activity</div><div class="tl"></div></div>', unsafe_allow_html=True)

    all_r = fetch_reqs()
    pend  = [r for r in all_r if r.get("status")=="pending"]
    appr  = [r for r in all_r if r.get("status")=="approved"]
    rej   = [r for r in all_r if r.get("status")=="rejected"]
    tot   = sum(float(r.get("amount",0)) for r in appr)

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("⏳  Pending", len(pend))
    c2.metric("✅  Approved", len(appr))
    c3.metric("❌  Rejected", len(rej))
    c4.metric("💰  Total Disbursed", fiqd(tot))

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="sl">Pending Approvals</div>', unsafe_allow_html=True)

    if not pend:
        st.markdown('<div class="es"><div class="ei">✨</div><div class="em">All caught up — no pending requests.</div></div>', unsafe_allow_html=True)
    else:
        for r in pend:
            uid   = r.get("user_id","")
            short = uid[:14]+"…" if len(uid)>14 else uid
            st.markdown(f"""
            <div class="rc">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:.5rem;">
                <div>
                  <div class="rs">User: {short}</div>
                  <div class="ra">{fiqd(r.get('amount',0))}</div>
                  <div class="rr">{r.get('reason','—')}</div>
                  <div class="rm">Submitted {fdate(r.get('created_at',''))}</div>
                </div>
                <div>{badge("pending")}</div>
              </div>
            </div>""", unsafe_allow_html=True)

            if r.get("invoice_image_url"):
                with st.expander("🖼  View Invoice"):
                    st.image(r["invoice_image_url"], use_column_width=True)

            ca,cr,_,_ = st.columns([1,1,.2,2])
            with ca:
                if st.button("✅  Approve", key=f"ap_{r['id']}"):
                    supabase.table("petty_cash_requests").update({"status":"approved"}).eq("id",r["id"]).execute()
                    st.rerun()
            with cr:
                if st.button("❌  Reject", key=f"rj_{r['id']}"):
                    st.session_state[f"rej_{r['id']}"] = True; st.rerun()

            if st.session_state.get(f"rej_{r['id']}"):
                with st.form(key=f"rf_{r['id']}"):
                    note = st.text_input("Rejection reason (shown to submitter)", placeholder="e.g. Receipt is unclear", key=f"rn_{r['id']}")
                    cc,cx,_ = st.columns([1,1,2])
                    if cc.form_submit_button("Confirm Reject"):
                        supabase.table("petty_cash_requests").update({"status":"rejected","admin_note":note}).eq("id",r["id"]).execute()
                        st.session_state.pop(f"rej_{r['id']}",None); st.rerun()
                    if cx.form_submit_button("Cancel"):
                        st.session_state.pop(f"rej_{r['id']}",None); st.rerun()
            st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── ADMIN ANALYTICS ───────────────────────────
def page_admin_analytics():
    try:
        import plotly.graph_objects as go
        HAS = True
    except: HAS = False

    st.markdown('<div class="pw">', unsafe_allow_html=True)
    st.markdown('<div class="ph"><div class="pt">Analytics</div><div class="ps">Visual insights into petty cash spending</div><div class="tl"></div></div>', unsafe_allow_html=True)

    all_r = fetch_reqs()
    appr  = [r for r in all_r if r.get("status")=="approved"]

    st.markdown('<div class="sl">Date Range</div>', unsafe_allow_html=True)
    cf1,cf2 = st.columns(2)
    with cf1: d_from = st.date_input("From", value=date(date.today().year,1,1), key="af1")
    with cf2: d_to   = st.date_input("To",   value=date.today(), key="at1")

    def ok(r):
        try:
            d = datetime.fromisoformat(r.get("created_at","").replace("Z","+00:00")).date()
            return d_from <= d <= d_to
        except: return True

    af = [r for r in appr  if ok(r)]
    lf = [r for r in all_r if ok(r)]

    st.markdown("<hr>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    c1.metric("Approved Requests", len(af))
    c2.metric("Total Approved",    fiqd(sum(float(r.get("amount",0)) for r in af)))
    c3.metric("Avg per Request",   fiqd(sum(float(r.get("amount",0)) for r in af)/max(len(af),1)))

    if not HAS:
        st.info("Add `plotly>=5.18.0` to requirements.txt for charts.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    G="#D4AF37"; G2="#EEC84A"; GR="#4cd884"; RD="#e87060"; FT="#EAE0CC"; GD="rgba(212,175,55,0.07)"
    BL = dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
              font=dict(family="Inter",color=FT,size=11),margin=dict(l=10,r=10,t=40,b=10),
              legend=dict(bgcolor="rgba(0,0,0,0)",bordercolor="rgba(212,175,55,.15)",borderwidth=1))

    # Monthly bar
    st.markdown('<div class="sl">Monthly Approved Spending</div>', unsafe_allow_html=True)
    mo: dict = defaultdict(float)
    for r in af:
        try:
            d = datetime.fromisoformat(r.get("created_at","").replace("Z","+00:00"))
            mo[d.strftime("%b %Y")] += float(r.get("amount",0))
        except: pass
    if mo:
        ks=list(mo.keys()); vs=[mo[k] for k in ks]
        fig = go.Figure(go.Bar(x=ks,y=vs,marker=dict(color=G,opacity=.85,line=dict(color=G2,width=1)),
                               hovertemplate="<b>%{x}</b><br>%{y:,.0f} IQD<extra></extra>"))
        fig.update_layout(**BL,height=290,yaxis=dict(gridcolor=GD,tickformat=",.0f"),xaxis=dict(gridcolor=GD))
        st.markdown('<div class="cw">', unsafe_allow_html=True)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Pie + Top spenders
    st.markdown('<div class="sl">Status Distribution & Top Spenders</div>', unsafe_allow_html=True)
    cl,cr = st.columns(2)
    with cl:
        sc: dict = defaultdict(int)
        for r in lf: sc[r.get("status","pending")] += 1
        if sc:
            lb=list(sc.keys()); vl=[sc[l] for l in lb]
            cm_={"pending":"#f1c40f","approved":GR,"rejected":RD}
            fig2=go.Figure(go.Pie(labels=[l.capitalize() for l in lb],values=vl,
                marker=dict(colors=[cm_.get(l,G) for l in lb],line=dict(color="#06080D",width=3)),
                hole=.55,hovertemplate="<b>%{label}</b><br>%{value} (%{percent})<extra></extra>",
                textfont=dict(color=FT)))
            fig2.update_layout(**BL,height=290,
                annotations=[dict(text=f"<b>{sum(vl)}</b><br>total",x=.5,y=.5,font=dict(size=13,color=FT),showarrow=False)])
            st.markdown('<div class="cw">', unsafe_allow_html=True)
            st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)
    with cr:
        ut: dict = defaultdict(float)
        for r in af:
            u=(r.get("user_id") or "unknown")[:10]+"…"; ut[u]+=float(r.get("amount",0))
        if ut:
            srt=sorted(ut.items(),key=lambda x:-x[1])[:8]
            fig3=go.Figure(go.Bar(x=[a for _,a in srt],y=[u for u,_ in srt],orientation="h",
                marker=dict(color=G2,opacity=.8),hovertemplate="%{y}<br><b>%{x:,.0f} IQD</b><extra></extra>"))
            fig3.update_layout(**BL,height=290,title=dict(text="Top Spenders",font=dict(color=FT,size=13)),
                xaxis=dict(gridcolor=GD,tickformat=",.0f"),yaxis=dict(gridcolor=GD))
            st.markdown('<div class="cw">', unsafe_allow_html=True)
            st.plotly_chart(fig3,use_container_width=True,config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)

    # Export
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="sl">Export Monthly Report</div>', unsafe_allow_html=True)
    months = sorted(set(
        datetime.fromisoformat(r.get("created_at","2024-01").replace("Z","+00:00")).strftime("%Y-%m")
        for r in appr if r.get("created_at")), reverse=True)

    if months:
        sel = st.selectbox("Select Month", months, key="exp_sel")
        exp = [r for r in appr if r.get("created_at","").startswith(sel)]
        tot_exp = sum(float(r.get("amount",0)) for r in exp)
        ci,cb = st.columns([2,1])
        ci.markdown(f"<div style='font-size:.85rem;color:rgba(234,224,204,.5);padding:.6rem 0;'>{len(exp)} records · {fiqd(tot_exp)} total</div>", unsafe_allow_html=True)
        with cb:
            if st.button("⬇  Generate Report", key="gen_rep"):
                with st.spinner("Generating…"):
                    data = make_report(exp, sel)
                ext = "pdf" if data[:4]==b"%PDF" else "csv"
                st.download_button(
                    label=f"📄 Download {sel}.{ext}",
                    data=data,
                    file_name=f"jawhar_{sel}.{ext}",
                    mime="application/pdf" if ext=="pdf" else "text/csv",
                    key="dl_rep"
                )
    else:
        st.info("No approved data available for export.")
    st.markdown('</div>', unsafe_allow_html=True)


# ── ADMIN ALL REQUESTS ────────────────────────
def page_admin_all():
    st.markdown('<div class="pw">', unsafe_allow_html=True)
    st.markdown('<div class="ph"><div class="pt">All Requests</div><div class="ps">Complete history with search and date filters</div><div class="tl"></div></div>', unsafe_allow_html=True)

    all_r = fetch_reqs()

    cf1,cf2,cf3,cf4 = st.columns(4)
    with cf1: fst  = st.selectbox("Status", ["All","Pending","Approved","Rejected"], key="fst")
    with cf2: srch = st.text_input("Search reason…", placeholder="e.g. electricity", key="src")
    with cf3: df   = st.date_input("From date", value=None, key="afd")
    with cf4: dt   = st.date_input("To date",   value=None, key="atd")

    if fst!="All":  all_r=[r for r in all_r if r.get("status")==fst.lower()]
    if srch:        all_r=[r for r in all_r if srch.lower() in (r.get("reason","") or "").lower()]
    if df:          all_r=[r for r in all_r if r.get("created_at","")[:10]>=df.isoformat()]
    if dt:          all_r=[r for r in all_r if r.get("created_at","")[:10]<=dt.isoformat()]

    st.markdown(f'<div class="sl">{len(all_r)} Result{"s" if len(all_r)!=1 else ""}</div>', unsafe_allow_html=True)

    if not all_r:
        st.markdown('<div class="es"><div class="ei">🔍</div><div class="em">No requests match your filters.</div></div>', unsafe_allow_html=True)
    else:
        for r in all_r:
            s     = r.get("status","pending")
            uid   = r.get("user_id","")
            short = uid[:14]+"…" if len(uid)>14 else uid
            nh    = f'<div class="rn">⚠ Admin note: {r["admin_note"]}</div>' if r.get("admin_note") else ""
            st.markdown(f"""
            <div class="rc">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:.5rem;">
                <div>
                  <div class="rs">{short}</div>
                  <div class="ra">{fiqd(r.get('amount',0))}</div>
                  <div class="rr">{r.get('reason','—')}</div>
                  {nh}
                  <div class="rm">{fdate(r.get('created_at',''))}</div>
                </div>
                {badge(s)}
              </div>
            </div>""", unsafe_allow_html=True)

            if r.get("invoice_image_url"):
                with st.expander("🖼  Invoice"):
                    st.image(r["invoice_image_url"], use_column_width=True)

            if s=="pending":
                ca,cr,_ = st.columns([1,1,3])
                if ca.button("✅ Approve", key=f"a2_{r['id']}"):
                    supabase.table("petty_cash_requests").update({"status":"approved"}).eq("id",r["id"]).execute(); st.rerun()
                if cr.button("❌ Reject", key=f"r2_{r['id']}"):
                    st.session_state[f"rj2_{r['id']}"]=True; st.rerun()
                if st.session_state.get(f"rj2_{r['id']}"):
                    with st.form(key=f"rf2_{r['id']}"):
                        note=st.text_input("Rejection reason",key=f"rn2_{r['id']}")
                        c1b,c2b,_=st.columns([1,1,2])
                        if c1b.form_submit_button("Confirm"):
                            supabase.table("petty_cash_requests").update({"status":"rejected","admin_note":note}).eq("id",r["id"]).execute()
                            st.session_state.pop(f"rj2_{r['id']}",None); st.rerun()
                        if c2b.form_submit_button("Cancel"):
                            st.session_state.pop(f"rj2_{r['id']}",None); st.rerun()
            st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── ADMIN BRANCHES ────────────────────────────
def page_admin_branches():
    st.markdown('<div class="pw">', unsafe_allow_html=True)
    st.markdown('<div class="ph"><div class="pt">Branch Overview</div><div class="ps">Spending summary with monthly usage</div><div class="tl"></div></div>', unsafe_allow_html=True)

    all_r = fetch_reqs()
    stats: dict = defaultdict(lambda:{"total":0.,"pending":0,"approved":0,"rejected":0,"count":0,"monthly":0.})
    now=datetime.utcnow(); mp=f"{now.year}-{now.month:02d}"

    for r in all_r:
        k=r.get("user_id","Unknown"); s=r.get("status","pending"); a=float(r.get("amount",0))
        stats[k]["count"]+=1; stats[k]["total"]+=a; stats[k][s]=stats[k].get(s,0)+1
        if r.get("created_at","").startswith(mp) and s in("approved","pending"): stats[k]["monthly"]+=a

    if not stats:
        st.markdown('<div class="es"><div class="ei">🏪</div><div class="em">No data yet.</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="sl">{len(stats)} User{"s" if len(stats)!=1 else ""}</div>', unsafe_allow_html=True)
        for uid,s in sorted(stats.items(),key=lambda x:-x[1]["total"]):
            lim=get_limit(uid); short=uid[:18]+"…" if len(uid)>18 else uid
            b=bar_html(s["monthly"],lim,compact=True)
            st.markdown(f"""
            <div class="ac">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;">
                <div style="flex:1;min-width:220px;">
                  <div style="font-size:.68rem;color:rgba(234,224,204,.32);text-transform:uppercase;letter-spacing:.1em;margin-bottom:.3rem;">User ID</div>
                  <div style="font-family:'Cormorant Garamond',serif;font-size:1.25rem;color:#EAE0CC;font-weight:600;margin-bottom:.5rem;">{short}</div>
                  {b}
                  <div style="font-size:.75rem;color:rgba(234,224,204,.4);margin-top:.4rem;">{s['count']} requests · {fiqd(s['total'])} lifetime · Limit: {fiqd(lim)}/mo</div>
                </div>
                <div style="display:flex;gap:1.5rem;align-items:center;flex-wrap:wrap;">
                  <div style="text-align:center;"><div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;color:#f1c40f;">{s['pending']}</div><div style="font-size:.62rem;color:rgba(234,224,204,.3);text-transform:uppercase;">Pending</div></div>
                  <div style="text-align:center;"><div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;color:#4cd884;">{s['approved']}</div><div style="font-size:.62rem;color:rgba(234,224,204,.3);text-transform:uppercase;">Approved</div></div>
                  <div style="text-align:center;"><div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;color:#e87060;">{s['rejected']}</div><div style="font-size:.62rem;color:rgba(234,224,204,.3);text-transform:uppercase;">Rejected</div></div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── ADMIN BRANCH LIMITS ───────────────────────
def page_admin_limits():
    st.markdown('<div class="pw">', unsafe_allow_html=True)
    st.markdown('<div class="ph"><div class="pt">Branch Limits</div><div class="ps">Set monthly spending limit for each user</div><div class="tl"></div></div>', unsafe_allow_html=True)

    all_r    = fetch_reqs()
    user_ids = sorted(set(r.get("user_id","") for r in all_r if r.get("user_id")))

    if not user_ids:
        st.markdown('<div class="es"><div class="ei">⚙️</div><div class="em">No users yet. They appear here after first submission.</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    try:
        existing = {row["user_id"]:float(row["monthly_limit"])
                    for row in supabase.table("branch_limits").select("*").execute().data or []}
    except: existing={}

    st.markdown(f'<div class="sl">{len(user_ids)} User{"s" if len(user_ids)!=1 else ""}</div>', unsafe_allow_html=True)
    st.info("Changes are saved immediately when you click Save.")
    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

    now=datetime.utcnow(); mp=f"{now.year}-{now.month:02d}"

    for uid in user_ids:
        cur   = existing.get(uid, DEFAULT_LIMIT)
        short = uid[:22]+"…" if len(uid)>22 else uid
        ms    = sum(float(r.get("amount",0)) for r in all_r
                    if r.get("user_id")==uid and r.get("created_at","").startswith(mp)
                    and r.get("status") in("approved","pending"))
        pct   = min(ms/cur*100,100) if cur>0 else 0
        bc    = "#D4AF37" if pct<70 else("#e87060" if pct>=90 else "#f1c40f")

        st.markdown(f"""
        <div class="ac">
          <div style="font-size:.68rem;color:rgba(234,224,204,.32);text-transform:uppercase;letter-spacing:.1em;margin-bottom:.25rem;">User ID</div>
          <div style="font-family:'Cormorant Garamond',serif;font-size:1.15rem;color:#EAE0CC;font-weight:600;margin-bottom:.7rem;">{short}</div>
          <div style="display:flex;justify-content:space-between;font-size:.7rem;color:rgba(234,224,204,.38);margin-bottom:.3rem;">
            <span>This month: {fiqd(ms)}</span>
            <span style="color:{bc};">{pct:.0f}% used</span>
          </div>
          <div class="lbb"><div class="lbf" style="width:{pct:.1f}%;background:{bc};"></div></div>
        </div>""", unsafe_allow_html=True)

        with st.form(key=f"lf_{uid}"):
            new_lim = st.number_input("Monthly Limit (IQD)", min_value=0, value=int(cur), step=50_000, format="%d", key=f"nl_{uid}")
            if st.form_submit_button("💾  Save Limit"):
                if save_limit(uid, float(new_lim)):
                    st.success(f"✅ Saved: {fiqd(new_lim)}")
                    st.rerun()
        st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ── BRANCH PORTAL ─────────────────────────────
def page_branch(user):
    uid = user.id; email = user.email

    st.markdown('<div class="pw">', unsafe_allow_html=True)
    st.markdown(f'<div class="ph"><div class="pt">Branch Portal</div><div class="ps">{email}</div><div class="tl"></div></div>', unsafe_allow_html=True)

    lim  = get_limit(uid)
    sp   = monthly_spent(uid)
    rem  = max(lim-sp, 0)

    st.markdown(bar_html(sp, lim), unsafe_allow_html=True)
    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)

    try:
        bd = supabase.table("branches").select("*").eq("user_id",uid).execute().data
        bid= bd[0]["id"] if bd else None
    except: bid=None

    tab1,tab2 = st.tabs(["📤  Submit Invoice","📜  My Requests"])

    with tab1:
        st.markdown('<div class="sl">New Petty Cash Request</div>', unsafe_allow_html=True)
        if rem<=0:
            st.error(f"⛔ Monthly limit of {fiqd(lim)} reached. No new submissions this month.")
        else:
            if sp>lim*.8:
                st.warning(f"⚠ {sp/lim*100:.0f}% used. Remaining: {fiqd(rem)}")
            with st.form("sf", clear_on_submit=True):
                amt = st.number_input("Amount (IQD)", min_value=0, step=500, format="%d")
                rsn = st.text_area("Description / Reason", placeholder="e.g. Monthly electricity bill", height=100)
                fil = st.file_uploader("Upload Receipt or Invoice", type=["png","jpg","jpeg","pdf"])
                sub = st.form_submit_button("Submit Request  →", use_container_width=True)
                if sub:
                    errs=[]
                    if amt<=0:          errs.append("Amount must be greater than 0.")
                    if not rsn.strip(): errs.append("Please provide a description.")
                    if not fil:         errs.append("Please upload an invoice.")
                    if amt>rem:         errs.append(f"Exceeds remaining limit of {fiqd(rem)}.")
                    for e in errs: st.error(e)
                    if not errs:
                        img=None
                        with st.spinner("Uploading…"): img=upload_img(fil.read(),fil.name)
                        with st.spinner("Submitting…"):
                            try:
                                supabase.table("petty_cash_requests").insert({
                                    "user_id":uid,"branch_id":bid,"amount":amt,
                                    "reason":rsn.strip(),"status":"pending","invoice_image_url":img
                                }).execute()
                                st.success("✅ Submitted! Management will review shortly.")
                            except Exception as e: st.error(f"Failed: {e}")

    with tab2:
        st.markdown('<div class="sl">Your Request History</div>', unsafe_allow_html=True)
        try:
            my = supabase.table("petty_cash_requests").select("*").eq("user_id",uid).order("created_at",desc=True).execute().data or []
        except:
            my=[]; st.warning("Could not load history.")

        if not my:
            st.markdown('<div class="es"><div class="ei">📋</div><div class="em">No requests yet.</div></div>', unsafe_allow_html=True)
        else:
            ta=sum(float(r.get("amount",0)) for r in my if r.get("status")=="approved")
            c1,c2,c3=st.columns(3)
            c1.metric("Total Requests",  len(my))
            c2.metric("Approved Amount", fiqd(ta))
            c3.metric("Pending",         sum(1 for r in my if r.get("status")=="pending"))
            st.markdown("<hr>", unsafe_allow_html=True)
            for r in my:
                s  = r.get("status","pending")
                nh = f'<div class="rn">⚠ Admin note: {r["admin_note"]}</div>' if r.get("admin_note") else ""
                st.markdown(f"""
                <div class="rc">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:.5rem;">
                    <div>
                      <div class="ra">{fiqd(r.get('amount',0))}</div>
                      <div class="rr">{r.get('reason','—')}</div>
                      {nh}
                      <div class="rm">{fdate(r.get('created_at',''))}</div>
                    </div>
                    {badge(s)}
                  </div>
                </div>""", unsafe_allow_html=True)
                if r.get("invoice_image_url"):
                    with st.expander("🖼  Invoice"):
                        st.image(r["invoice_image_url"], use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── ROUTER ────────────────────────────────────
user = st.session_state.user

if user is None:
    page_login()
else:
    is_admin = user.email == ADMIN_EMAIL
    render_sidebar(user.email, is_admin)

    if is_admin:
        valid = ("admin_dashboard","admin_analytics","admin_all","admin_branches","admin_limits")
        if st.session_state.page not in valid:
            st.session_state.page = "admin_dashboard"
        {
            "admin_dashboard": page_admin_dashboard,
            "admin_analytics": page_admin_analytics,
            "admin_all":       page_admin_all,
            "admin_branches":  page_admin_branches,
            "admin_limits":    page_admin_limits,
        }[st.session_state.page]()
    else:
        page_branch(user)
