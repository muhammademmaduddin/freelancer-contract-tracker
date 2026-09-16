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
    safe_status = html.escape(status)
    display = status.replace("_", " ").title()

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


def workflow() -> str:
    states = [
        "Pending",
        "In Progress",
        "Submitted",
        "Approved",
        "Paid",
    ]

    items = []

    for index, state in enumerate(states):
        items.append(
            f'<span class="workflow-step">{state}</span>'
        )

        if index < len(states) - 1:
            items.append(
                '<span class="workflow-arrow">→</span>'
            )

    return '<div class="workflow">' + "".join(items) + '</div>'