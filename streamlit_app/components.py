import html


def hero() -> str:
    return (
        '<div class="hero">'
        '<div class="hero-eyebrow">FREELANCER OPERATIONS</div>'
        '<div class="hero-title">Contract &amp; Milestone Control Center</div>'
        '<div class="hero-subtitle">'
        'Manage contract value, milestone delivery, staged payments, '
        'deadlines and disputes from one operational dashboard.'
        '</div>'
        '<div class="hero-badges">'
        '<span class="hero-badge">Contract Lifecycle</span>'
        '<span class="hero-badge">Milestone State Machine</span>'
        '<span class="hero-badge">Partial Payments</span>'
        '<span class="hero-badge">Deadline Monitoring</span>'
        '</div>'
        '</div>'
    )


def page_header(title: str, description: str) -> str:
    return (
        f'<div class="page-title">{html.escape(title)}</div>'
        f'<div class="page-description">{html.escape(description)}</div>'
    )


def kpi_card(label: str, value: str, helper: str = "") -> str:
    return (
        '<div class="kpi-card">'
        f'<div class="kpi-label">{html.escape(label)}</div>'
        f'<div class="kpi-value">{html.escape(str(value))}</div>'
        f'<div class="kpi-helper">{html.escape(helper)}</div>'
        '</div>'
    )


def info_row(label: str, value: str) -> str:
    return (
        '<div class="info-row">'
        f'<span class="info-label">{html.escape(label)}</span>'
        f'<span class="info-value">{html.escape(str(value))}</span>'
        '</div>'
    )


def status_pill(status: str) -> str:
    normalized = str(status or "unknown").lower()
    safe_status = html.escape(normalized)
    display = normalized.replace("_", " ").title()

    return (
        f'<span class="status-pill status-{safe_status}">'
        f'{html.escape(display)}'
        '</span>'
    )


def progress_bar(percent: float) -> str:
    percent = max(0, min(100, percent))

    return (
        '<div class="progress-shell">'
        f'<div class="progress-fill" style="width:{percent:.1f}%"></div>'
        '</div>'
    )


def milestone_summary(
    milestone_id: int,
    title: str,
    status: str,
    value: str,
    deadline: str,
    contract_id: int,
) -> str:
    return (
        '<div class="milestone-summary">'
        '<div class="milestone-summary-heading">'
        '<div>'
        f'<div class="milestone-kicker">Milestone #{html.escape(str(milestone_id))}</div>'
        f'<div class="milestone-summary-title">{html.escape(title)}</div>'
        '</div>'
        '<div class="milestone-current-status">'
        '<span class="current-status-label">Current status</span>'
        f'{status_pill(status)}'
        '</div>'
        '</div>'
        '<div class="milestone-summary-details">'
        f'<div><span>Milestone value</span><strong>{html.escape(value)}</strong></div>'
        f'<div><span>Deadline</span><strong>{html.escape(deadline)}</strong></div>'
        f'<div><span>Contract</span><strong>#{html.escape(str(contract_id))}</strong></div>'
        '</div>'
        '</div>'
    )


def workflow(current_status: str | None = None) -> str:
    states = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("submitted", "Submitted"),
        ("approved", "Approved"),
        ("paid", "Paid"),
    ]

    normalized_status = str(current_status or "").lower()
    items = []

    for index, (status, label) in enumerate(states):
        active_class = (
            " workflow-step-active"
            if status == normalized_status
            else ""
        )
        items.append(
            f'<span class="workflow-step{active_class}">{label}</span>'
        )

        if index < len(states) - 1:
            items.append(
                '<span class="workflow-arrow">→</span>'
            )

    disputed_class = (
        " workflow-disputed-step-active"
        if normalized_status == "disputed"
        else ""
    )

    return (
        '<div class="workflow">'
        + "".join(items)
        + '</div>'
        + '<div class="workflow-dispute-branch">'
        + '<div class="workflow-dispute-row">'
        + '<span class="workflow-branch-label">Submitted</span>'
        + '<span class="workflow-branch-arrow">↓</span>'
        + f'<span class="workflow-disputed-step{disputed_class}">Disputed</span>'
        + '</div>'
        + '<div class="workflow-dispute-return">'
        + '<span>↙</span>'
        + '<span>In Progress</span>'
        + '<span class="workflow-branch-separator">/</span>'
        + '<span>Submitted</span>'
        + '<span>↘</span>'
        + '</div>'
        + '</div>'
    )
