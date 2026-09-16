APP_CSS = """
<style>

/* -------------------------------------------------------
   GLOBAL
------------------------------------------------------- */

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at top right, rgba(99,102,241,0.08), transparent 32%),
        radial-gradient(circle at top left, rgba(14,165,233,0.06), transparent 28%),
        #f8fafc;
}

[data-testid="stHeader"] {
    background: rgba(248, 250, 252, 0.8);
    backdrop-filter: blur(10px);
}

.block-container {
    max-width: 1380px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

html, body, [class*="css"] {
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

/* -------------------------------------------------------
   SIDEBAR
------------------------------------------------------- */

[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #1e293b;
}

[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

[data-testid="stSidebar"] .stRadio label {
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
}

.sidebar-brand {
    padding: 0.8rem 0 1.4rem 0;
}

.sidebar-brand-title {
    color: white;
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -0.03em;
}

.sidebar-brand-subtitle {
    color: #94a3b8;
    font-size: 0.80rem;
    margin-top: 0.2rem;
}

.sidebar-footer {
    margin-top: 2rem;
    padding: 1rem;
    border-radius: 14px;
    background: #111c30;
    border: 1px solid #22314c;
}

.sidebar-footer-title {
    color: #f8fafc;
    font-weight: 700;
    font-size: 0.86rem;
}

.sidebar-footer-text {
    color: #94a3b8;
    font-size: 0.75rem;
    line-height: 1.5;
}

/* -------------------------------------------------------
   HERO
------------------------------------------------------- */

.hero {
    padding: 1.8rem 2rem;
    border-radius: 24px;
    background:
        linear-gradient(135deg, #0f172a 0%, #1e293b 55%, #312e81 100%);
    margin-bottom: 1.6rem;
    box-shadow:
        0 18px 45px rgba(15, 23, 42, 0.16);
}

.hero-eyebrow {
    color: #a5b4fc;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

.hero-title {
    color: white;
    font-size: 2.3rem;
    font-weight: 850;
    letter-spacing: -0.045em;
    margin-top: 0.4rem;
    line-height: 1.1;
}

.hero-subtitle {
    color: #cbd5e1;
    font-size: 0.98rem;
    max-width: 780px;
    margin-top: 0.7rem;
    line-height: 1.65;
}

.hero-badges {
    margin-top: 1.1rem;
}

.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.08);
    color: #e2e8f0;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 999px;
    padding: 0.38rem 0.75rem;
    margin-right: 0.35rem;
    font-size: 0.76rem;
    font-weight: 600;
}

/* -------------------------------------------------------
   PAGE HEADERS
------------------------------------------------------- */

.page-title {
    color: #0f172a;
    font-size: 1.65rem;
    font-weight: 800;
    letter-spacing: -0.035em;
    margin-bottom: 0.2rem;
}

.page-description {
    color: #64748b;
    font-size: 0.92rem;
    margin-bottom: 1.3rem;
}

/* -------------------------------------------------------
   KPI CARDS
------------------------------------------------------- */

.kpi-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 1.15rem 1.25rem;
    box-shadow:
        0 4px 18px rgba(15, 23, 42, 0.045);
    min-height: 128px;
}

.kpi-label {
    color: #64748b;
    font-size: 0.78rem;
    font-weight: 650;
    text-transform: uppercase;
    letter-spacing: 0.055em;
}

.kpi-value {
    color: #0f172a;
    font-size: 1.75rem;
    font-weight: 820;
    letter-spacing: -0.04em;
    margin-top: 0.35rem;
}

.kpi-helper {
    color: #94a3b8;
    font-size: 0.75rem;
    margin-top: 0.35rem;
}

/* -------------------------------------------------------
   CONTENT CARDS
------------------------------------------------------- */

.panel {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 1.4rem;
    box-shadow:
        0 6px 20px rgba(15, 23, 42, 0.04);
    margin-bottom: 1rem;
}

.panel-title {
    color: #0f172a;
    font-size: 1rem;
    font-weight: 760;
    margin-bottom: 0.25rem;
}

.panel-subtitle {
    color: #64748b;
    font-size: 0.80rem;
    margin-bottom: 1rem;
}

/* -------------------------------------------------------
   STATUS PILLS
------------------------------------------------------- */

.status-pill {
    display: inline-flex;
    align-items: center;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.73rem;
    padding: 0.35rem 0.7rem;
}

.status-pending {
    background: #fff7ed;
    color: #c2410c;
}

.status-in_progress {
    background: #eff6ff;
    color: #1d4ed8;
}

.status-submitted {
    background: #f5f3ff;
    color: #6d28d9;
}

.status-approved {
    background: #ecfdf5;
    color: #047857;
}

.status-paid {
    background: #dcfce7;
    color: #166534;
}

.status-disputed {
    background: #fef2f2;
    color: #b91c1c;
}

/* -------------------------------------------------------
   INFO ROWS
------------------------------------------------------- */

.info-row {
    display: flex;
    justify-content: space-between;
    padding: 0.72rem 0;
    border-bottom: 1px solid #f1f5f9;
}

.info-row:last-child {
    border-bottom: none;
}

.info-label {
    color: #64748b;
    font-size: 0.82rem;
}

.info-value {
    color: #0f172a;
    font-size: 0.84rem;
    font-weight: 700;
}

/* -------------------------------------------------------
   PROGRESS
------------------------------------------------------- */

.progress-shell {
    height: 9px;
    background: #e2e8f0;
    border-radius: 999px;
    overflow: hidden;
    margin-top: 0.55rem;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #6366f1, #0ea5e9);
    border-radius: 999px;
}

/* -------------------------------------------------------
   WORKFLOW
------------------------------------------------------- */

.workflow {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.35rem;
    padding: 0.8rem 0;
}

.workflow-step {
    border-radius: 10px;
    border: 1px solid #e2e8f0;
    background: white;
    padding: 0.45rem 0.65rem;
    color: #334155;
    font-size: 0.72rem;
    font-weight: 700;
}

.workflow-arrow {
    color: #94a3b8;
}

/* -------------------------------------------------------
   INPUTS
------------------------------------------------------- */

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input {
    border-radius: 12px !important;
}

div[data-baseweb="select"] > div {
    border-radius: 12px !important;
}

.stButton > button,
.stFormSubmitButton > button {
    border-radius: 12px;
    min-height: 46px;
    font-weight: 700;
    border: none;
}

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: linear-gradient(
        135deg,
        #4f46e5,
        #6366f1
    );
}

/* -------------------------------------------------------
   TABLE
------------------------------------------------------- */

[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
}

/* -------------------------------------------------------
   SECTION SPACING
------------------------------------------------------- */

.section-gap {
    height: 0.75rem;
}

.small-muted {
    color: #64748b;
    font-size: 0.78rem;
}

</style>
"""