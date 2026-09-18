APP_CSS = """
<style>

/* =======================================================
   GLOBAL
======================================================= */

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(
            circle at top right,
            rgba(99, 102, 241, 0.08),
            transparent 32%
        ),
        radial-gradient(
            circle at top left,
            rgba(14, 165, 233, 0.06),
            transparent 28%
        ),
        #f8fafc;
}

[data-testid="stHeader"] {
    background: rgba(248, 250, 252, 0.82);
    backdrop-filter: blur(10px);
}

.block-container {
    max-width: 1380px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

html,
body,
[class*="css"] {
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

main {
    overflow-x: hidden;
}


/* =======================================================
   SIDEBAR
======================================================= */

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
    color: #ffffff;
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -0.03em;
}

.sidebar-brand-subtitle {
    color: #94a3b8;
    font-size: 0.80rem;
    margin-top: 0.2rem;
}

.active-context-heading {
    color: #a5b4fc;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    margin: 0.2rem 0 0.8rem 0;
}

.context-block {
    padding: 0.8rem;
    margin-bottom: 0.65rem;
    border-radius: 14px;
    background: #111c30;
    border: 1px solid #22314c;
}

.context-block-label {
    color: #94a3b8;
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.context-block-title {
    color: #f8fafc;
    font-size: 0.86rem;
    font-weight: 750;
    line-height: 1.35;
    margin-top: 0.35rem;
    overflow-wrap: anywhere;
}

.context-block-meta {
    color: #cbd5e1;
    font-size: 0.75rem;
    line-height: 1.45;
    margin-top: 0.35rem;
    overflow-wrap: anywhere;
}

.context-block .status-pill {
    margin-top: 0.45rem;
}

.context-warning {
    color: #fbbf24;
    font-size: 0.74rem;
    line-height: 1.45;
    margin: 0.1rem 0 0.65rem 0;
    overflow-wrap: anywhere;
}

.context-empty {
    color: #94a3b8;
    font-size: 0.76rem;
    line-height: 1.45;
    margin: 0.1rem 0 0.65rem 0;
}

.sidebar-divider {
    margin: 0.8rem 0 1rem 0;
    border-color: #22314c;
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


/* =======================================================
   SIDEBAR INPUTS
======================================================= */

[data-testid="stSidebar"] [data-testid="stTextInput"] > div {
    background: #111827 !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

[data-testid="stSidebar"] [data-testid="stTextInput"] input {
    background: transparent !important;
    color: #f8fafc !important;
    border: none !important;
    border-radius: 12px !important;
    caret-color: #ffffff !important;
    min-height: 42px;
}

[data-testid="stSidebar"] [data-testid="stTextInput"] input::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}

[data-testid="stSidebar"] [data-testid="stTextInput"] label {
    color: #cbd5e1 !important;
    font-size: 0.76rem !important;
    font-weight: 650 !important;
}

[data-testid="stSidebar"] .stCaption {
    color: #94a3b8 !important;
}

[data-testid="stSidebar"] .stButton > button {
    background: #1e293b !important;
    color: #e2e8f0 !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    min-height: 40px !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #334155 !important;
    color: #ffffff !important;
    border-color: #475569 !important;
}


/* =======================================================
   HERO
======================================================= */

.hero {
    padding: 1.8rem 2rem;
    border-radius: 24px;
    background:
        linear-gradient(
            135deg,
            #0f172a 0%,
            #1e293b 55%,
            #312e81 100%
        );
    margin-bottom: 1.6rem;
    box-shadow:
        0 18px 45px
        rgba(15, 23, 42, 0.16);
}

.hero-eyebrow {
    color: #a5b4fc;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

.hero-title {
    color: #ffffff;
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
    background: rgba(255, 255, 255, 0.08);
    color: #e2e8f0;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 999px;
    padding: 0.38rem 0.75rem;
    margin-right: 0.35rem;
    font-size: 0.76rem;
    font-weight: 600;
}


/* =======================================================
   PAGE HEADERS
======================================================= */

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


/* =======================================================
   KPI CARDS
======================================================= */

.kpi-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 1.15rem 1.25rem;
    box-shadow: 0 4px 18px rgba(15, 23, 42, 0.045);
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


/* =======================================================
   CONTENT CARDS
======================================================= */

.panel {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 1.4rem;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.04);
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

.stContainer > div[data-testid="stContainer"] {
    border-radius: 20px !important;
}


/* =======================================================
   STATUS PILLS
======================================================= */

.status-pill {
    display: inline-flex;
    align-items: center;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.73rem;
    padding: 0.35rem 0.7rem;
    white-space: nowrap;
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
    background: #16a34a;
    color: #ffffff;
    box-shadow: 0 4px 12px rgba(22, 163, 74, 0.22);
}

.status-disputed {
    background: #fef2f2;
    color: #b91c1c;
}


/* =======================================================
   INFO ROWS
======================================================= */

.info-row {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.72rem 0;
    border-bottom: 1px solid #f1f5f9;
}

.info-row:last-child {
    border-bottom: none;
}

.info-label {
    color: #64748b;
    font-size: 0.82rem;
    min-width: 0;
}

.info-value {
    color: #0f172a;
    font-size: 0.84rem;
    font-weight: 700;
    text-align: right;
    overflow-wrap: anywhere;
}


/* =======================================================
   PROGRESS BAR
======================================================= */

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


/* =======================================================
   WORKFLOW
======================================================= */

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
    background: #ffffff;
    padding: 0.45rem 0.65rem;
    color: #334155;
    font-size: 0.72rem;
    font-weight: 700;
    white-space: nowrap;
}

.workflow-step-active {
    background: #312e81;
    border-color: #312e81;
    color: #ffffff;
    box-shadow: 0 5px 14px rgba(49, 46, 129, 0.2);
}

.workflow-arrow {
    color: #94a3b8;
    font-weight: 700;
}

.workflow-dispute-branch {
    display: grid;
    gap: 0.4rem;
    padding: 0.7rem 0.85rem;
    margin-top: 0.35rem;
    border-radius: 14px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
}

.workflow-dispute-row,
.workflow-dispute-return {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.4rem;
    color: #475569;
    font-size: 0.75rem;
    font-weight: 650;
}

.workflow-branch-label {
    color: #334155;
}

.workflow-branch-arrow {
    color: #6366f1;
    font-size: 1rem;
}

.workflow-disputed-step {
    border-radius: 999px;
    padding: 0.28rem 0.6rem;
    background: #fef2f2;
    color: #b91c1c;
    font-weight: 750;
}

.workflow-disputed-step-active {
    background: #b91c1c;
    color: #ffffff;
    box-shadow: 0 4px 12px rgba(185, 28, 28, 0.2);
}

.workflow-branch-separator {
    color: #94a3b8;
}


/* =======================================================
   MILESTONE SUMMARY
======================================================= */

.milestone-summary {
    padding: 1.25rem;
    border-radius: 18px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.04);
}

.milestone-summary-heading {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
}

.milestone-kicker {
    color: #6366f1;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.milestone-summary-title {
    color: #0f172a;
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    line-height: 1.3;
    margin-top: 0.25rem;
    overflow-wrap: anywhere;
}

.milestone-current-status {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.35rem;
    flex-shrink: 0;
}

.current-status-label {
    color: #64748b;
    font-size: 0.7rem;
    font-weight: 750;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.milestone-summary-details {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.8rem;
    margin-top: 1.25rem;
    padding-top: 1rem;
    border-top: 1px solid #f1f5f9;
}

.milestone-summary-details div {
    min-width: 0;
}

.milestone-summary-details span {
    display: block;
    color: #64748b;
    font-size: 0.75rem;
    margin-bottom: 0.2rem;
}

.milestone-summary-details strong {
    color: #0f172a;
    font-size: 0.9rem;
    font-weight: 750;
    overflow-wrap: anywhere;
}


/* =======================================================
   PAYMENT AND ACTION PANELS
======================================================= */

.payment-context {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
    padding: 1.1rem 1.2rem;
    margin-bottom: 1rem;
    border-radius: 18px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.04);
}

.payment-context-title {
    color: #0f172a;
    font-size: 1.05rem;
    font-weight: 800;
    line-height: 1.35;
    overflow-wrap: anywhere;
}

.payment-context-meta {
    color: #64748b;
    font-size: 0.8rem;
    line-height: 1.5;
    margin-top: 0.3rem;
}

.payment-context-status {
    flex-shrink: 0;
}

.payment-complete {
    padding: 1rem 1.1rem;
    margin-top: 1rem;
    border-radius: 14px;
    background: #ecfdf5;
    border: 1px solid #bbf7d0;
    color: #166534;
    font-weight: 700;
}

.payment-notice {
    padding: 1rem 1.1rem;
    margin-top: 1rem;
    border-radius: 14px;
    background: #fff7ed;
    border: 1px solid #fed7aa;
    color: #9a3412;
    line-height: 1.5;
}

.action-stack {
    display: grid;
    gap: 0.65rem;
    margin-top: 1rem;
}

.action-stack .stButton,
.action-stack .stFormSubmitButton {
    width: 100%;
}

.action-stack .stButton > button,
.action-stack .stFormSubmitButton > button {
    width: 100%;
}


/* =======================================================
   MAIN FORM INPUTS
======================================================= */

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input {
    border-radius: 12px !important;
}

div[data-baseweb="select"] > div {
    border-radius: 12px !important;
}


/* =======================================================
   BUTTONS
======================================================= */

.stButton > button,
.stFormSubmitButton > button {
    border-radius: 12px;
    min-height: 46px;
    font-weight: 700;
    border: none;
}

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    color: #ffffff;
}


/* =======================================================
   TABLE
======================================================= */

[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
}


/* =======================================================
   SECTION HELPERS
======================================================= */

.section-gap {
    height: 0.75rem;
}

.small-muted {
    color: #64748b;
    font-size: 0.78rem;
}


/* =======================================================
   RESPONSIVE
======================================================= */

@media (max-width: 900px) {
    .hero {
        padding: 1.4rem;
        border-radius: 18px;
    }

    .hero-title {
        font-size: 1.65rem;
    }

    .hero-subtitle {
        font-size: 0.88rem;
    }

    .hero-badge {
        margin-bottom: 0.35rem;
    }

    .kpi-value {
        font-size: 1.4rem;
    }

    .milestone-summary-heading {
        display: block;
    }

    .milestone-current-status {
        align-items: flex-start;
        margin-top: 1rem;
    }
}

@media (max-width: 650px) {
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
    }

    .hero {
        padding: 1.15rem;
    }

    .hero-title {
        font-size: 1.35rem;
    }

    .milestone-summary-details {
        grid-template-columns: 1fr;
        gap: 0.7rem;
    }

    .payment-context {
        display: block;
    }

    .payment-context-status {
        margin-top: 0.8rem;
    }

    .workflow {
        gap: 0.25rem;
    }

    .workflow-step {
        font-size: 0.68rem;
        padding: 0.4rem 0.5rem;
    }

    .info-row {
        display: block;
    }

    .info-value {
        display: block;
        text-align: left;
        margin-top: 0.2rem;
    }
}

</style>
"""
