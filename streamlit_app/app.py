from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
import html

import requests
import streamlit as st

from api_client import (
    BackendUnavailable,
    add_milestone,
    create_contract,
    get_contract_summary,
    get_milestone,
    get_overdue_milestones,
    get_payment_summary,
    health_check,
    record_payment,
    update_milestone_status,
)
from components import (
    hero,
    info_row,
    kpi_card,
    milestone_summary,
    page_header,
    progress_bar,
    status_pill,
    workflow,
)
from styles import APP_CSS


st.set_page_config(
    page_title="FreelanceOps",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    APP_CSS,
    unsafe_allow_html=True,
)


def money(value) -> str:
    try:
        return f"${Decimal(str(value)):,.2f}"
    except (InvalidOperation, TypeError, ValueError):
        return "$0.00"


def format_deadline(value) -> str:
    try:
        parsed = date.fromisoformat(str(value))
        return f"{parsed.strftime('%b')} {parsed.day}, {parsed.year}"
    except (TypeError, ValueError):
        return str(value)


def parse_positive_id(value) -> tuple[int | None, bool]:
    if value is None:
        return None, False

    text = str(value).strip()

    if not text:
        return None, False

    try:
        parsed = int(text)
    except (TypeError, ValueError):
        return None, True

    if parsed <= 0:
        return None, True

    return parsed, False


def api_error(
    exc: Exception,
    not_found_message: str | None = None,
) -> None:
    if isinstance(exc, BackendUnavailable):
        st.error(
            "Backend API is unavailable. "
            "Check the API_BASE_URL configuration or backend deployment."
        )
        return

    if isinstance(exc, requests.HTTPError):
        response = exc.response

        if (
            response is not None
            and response.status_code == 404
            and not_found_message
        ):
            st.warning(not_found_message)
            return

        try:
            payload = response.json() if response is not None else {}
        except (ValueError, TypeError):
            payload = {}

        if response is not None and response.status_code == 422:
            st.warning(
                "Please check the entered values and try again."
            )
            return

        detail = (
            payload.get("detail", "Request failed.")
            if isinstance(payload, dict)
            else str(payload)
        )

        if not detail:
            detail = "Request failed."

        if response is not None and response.status_code >= 500:
            st.error(
                "The backend could not complete this request. "
                "Please try again."
            )
        else:
            st.error(str(detail))
        return

    if isinstance(exc, (requests.Timeout, requests.RequestException)):
        st.error(
            "The backend request timed out or was interrupted. "
            "Please try again."
        )
        return

    st.error(
        "An unexpected error occurred while contacting the backend."
    )


def backend_is_available() -> bool:
    try:
        health_check()
        return True
    except Exception:
        return False


def set_flash(
    message: str,
    kind: str = "success",
) -> None:
    st.session_state["_flash_message"] = message
    st.session_state["_flash_kind"] = kind


def show_flash() -> None:
    message = st.session_state.pop(
        "_flash_message",
        None,
    )

    kind = st.session_state.pop(
        "_flash_kind",
        "success",
    )

    if not message:
        return

    if kind == "success":
        st.success(message)
    elif kind == "warning":
        st.warning(message)
    elif kind == "error":
        st.error(message)
    else:
        st.info(message)


def load_context(
    contract_id: int | None,
    milestone_id: int | None,
) -> dict:
    context = {
        "contract_summary": None,
        "contract_warning": None,
        "milestone": None,
        "milestone_warning": None,
        "context_warning": None,
    }

    if contract_id is not None:
        try:
            context["contract_summary"] = get_contract_summary(
                contract_id
            )
        except requests.HTTPError as exc:
            if (
                exc.response is not None
                and exc.response.status_code == 404
            ):
                context["contract_warning"] = (
                    f"Contract #{contract_id} was not found."
                )
            else:
                context["contract_warning"] = (
                    "Contract details are temporarily unavailable."
                )
        except Exception:
            context["contract_warning"] = (
                "Contract details are temporarily unavailable."
            )

    if milestone_id is not None:
        try:
            context["milestone"] = get_milestone(
                milestone_id
            )
        except requests.HTTPError as exc:
            if (
                exc.response is not None
                and exc.response.status_code == 404
            ):
                context["milestone_warning"] = (
                    f"Milestone #{milestone_id} was not found."
                )
            else:
                context["milestone_warning"] = (
                    "Milestone details are temporarily unavailable."
                )
        except Exception:
            context["milestone_warning"] = (
                "Milestone details are temporarily unavailable."
            )

    contract_summary = context["contract_summary"]
    milestone = context["milestone"]

    if (
        contract_id is not None
        and contract_summary is not None
        and milestone is not None
        and int(milestone.get("contract_id", -1)) != contract_id
    ):
        context["context_warning"] = (
            "The selected milestone belongs to a different contract."
        )

    return context


def render_sidebar_context(
    contract_id: int | None,
    milestone_id: int | None,
    context: dict,
) -> None:
    st.markdown(
        '<div class="active-context-heading">ACTIVE CONTEXT</div>',
        unsafe_allow_html=True,
    )

    if contract_id is None:
        st.markdown(
            '<div class="context-empty">No contract selected.</div>',
            unsafe_allow_html=True,
        )
    elif context["contract_summary"] is None:
        st.markdown(
            (
                '<div class="context-warning">'
                f'{html.escape(context["contract_warning"] or "Contract details are unavailable.")}'
                '</div>'
            ),
            unsafe_allow_html=True,
        )
    else:
        summary = context["contract_summary"]
        st.markdown(
            (
                '<div class="context-block">'
                '<div class="context-block-label">Contract</div>'
                '<div class="context-block-title">'
                f'Contract #{html.escape(str(summary["contract_id"]))} · '
                f'{html.escape(str(summary["title"]))}'
                '</div>'
                '<div class="context-block-meta">'
                f'Total {html.escape(money(summary["total_value"]))} · '
                f'Allocated {html.escape(money(summary["allocated_amount"]))}'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

    if milestone_id is None:
        st.markdown(
            '<div class="context-empty">No milestone selected.</div>',
            unsafe_allow_html=True,
        )
    elif context["milestone"] is None:
        st.markdown(
            (
                '<div class="context-warning">'
                f'{html.escape(context["milestone_warning"] or "Milestone details are unavailable.")}'
                '</div>'
            ),
            unsafe_allow_html=True,
        )
    else:
        milestone = context["milestone"]
        st.markdown(
            (
                '<div class="context-block">'
                '<div class="context-block-label">Milestone</div>'
                '<div class="context-block-title">'
                f'Milestone #{html.escape(str(milestone["id"]))} · '
                f'{html.escape(str(milestone["title"]))}'
                '</div>'
                f'{status_pill(str(milestone.get("status", "unknown")))}'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

    if context["context_warning"]:
        st.markdown(
            (
                '<div class="context-warning">'
                f'{html.escape(context["context_warning"])}'
                '</div>'
            ),
            unsafe_allow_html=True,
        )


def render_payment_context(milestone: dict) -> None:
    status = str(milestone.get("status", "unknown"))
    st.markdown(
        (
            '<div class="payment-context">'
            '<div>'
            f'<div class="payment-context-title">Milestone #{html.escape(str(milestone["id"]))}</div>'
            f'<div class="payment-context-meta">'
            f'{html.escape(str(milestone["title"]))}<br>'
            f'Status: {html.escape(status.replace("_", " ").title())}<br>'
            f'Value: {html.escape(money(milestone["amount"]))}'
            '</div>'
            '</div>'
            f'<div class="payment-context-status">{status_pill(status)}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def display_status(status: str) -> str:
    return str(status or "unknown").replace("_", " ").title()


def normalize_active_id(value) -> int | None:
    parsed, invalid = parse_positive_id(value)
    return None if invalid else parsed


next_contract_id = st.session_state.pop(
    "_next_contract_id",
    None,
)

if next_contract_id is not None:
    st.session_state["active_contract_id"] = normalize_active_id(
        next_contract_id
    )
    st.session_state["active_milestone_id"] = None
    st.session_state["milestone_id_input"] = ""

next_milestone_id = st.session_state.pop(
    "_next_milestone_id",
    None,
)

if next_milestone_id is not None:
    st.session_state["active_milestone_id"] = normalize_active_id(
        next_milestone_id
    )
    st.session_state["milestone_id_input"] = str(
        next_milestone_id
    )

next_milestone_input = st.session_state.pop(
    "_next_milestone_input",
    None,
)

if next_milestone_input is not None:
    st.session_state["milestone_id_input"] = str(
        next_milestone_input
    )

form_reset_keys = {
    "new_contract_title": "",
    "new_contract_value": 0.01,
    "new_client_name": "",
    "new_client_email": "",
    "new_freelancer_name": "",
    "new_freelancer_email": "",
    "milestone_title": "",
    "milestone_amount": 0.01,
}

for form_key, form_value in form_reset_keys.items():
    next_form_key = f"_next_{form_key}"
    if next_form_key in st.session_state:
        st.session_state[form_key] = st.session_state.pop(
            next_form_key
        )
    else:
        st.session_state.setdefault(
            form_key,
            form_value,
        )

active_contract_id = normalize_active_id(
    st.session_state.get(
        "active_contract_id",
        None,
    )
)
active_milestone_id = normalize_active_id(
    st.session_state.get(
        "active_milestone_id",
        None,
    )
)

if active_contract_id is None:
    active_milestone_id = None

st.session_state["active_contract_id"] = active_contract_id
st.session_state["active_milestone_id"] = active_milestone_id


def set_context_notice(
    message: str | None,
    kind: str = "warning",
) -> None:
    if message:
        st.session_state["_context_notice"] = message
        st.session_state["_context_notice_kind"] = kind
    else:
        st.session_state.pop(
            "_context_notice",
            None,
        )
        st.session_state.pop(
            "_context_notice_kind",
            None,
        )


def load_contract_from_input() -> None:
    raw_id = str(
        st.session_state.get(
            "contract_id_input",
            "",
        )
    ).strip()
    contract_id, invalid = parse_positive_id(raw_id)

    if invalid or contract_id is None:
        set_context_notice(
            "Enter a positive whole-number contract ID."
        )
        return

    try:
        get_contract_summary(contract_id)
    except requests.HTTPError as exc:
        if (
            exc.response is not None
            and exc.response.status_code == 404
        ):
            set_context_notice(
                f"Contract #{contract_id} was not found."
            )
        else:
            set_context_notice(
                "Contract details are temporarily unavailable."
            )
        return
    except Exception:
        set_context_notice(
            "Contract details are temporarily unavailable."
        )
        return

    st.session_state["active_contract_id"] = contract_id
    st.session_state["active_milestone_id"] = None
    st.session_state["_next_milestone_input"] = ""
    set_context_notice(None)
    st.rerun()


def load_milestone_from_input() -> None:
    contract_id = normalize_active_id(
        st.session_state.get(
            "active_contract_id",
            None,
        )
    )

    if contract_id is None:
        set_context_notice(
            "Load a contract before loading a milestone."
        )
        return

    raw_id = str(
        st.session_state.get(
            "milestone_id_input",
            "",
        )
    ).strip()
    milestone_id, invalid = parse_positive_id(raw_id)

    if invalid or milestone_id is None:
        set_context_notice(
            "Enter a positive whole-number milestone ID."
        )
        return

    try:
        milestone = get_milestone(milestone_id)
    except requests.HTTPError as exc:
        if (
            exc.response is not None
            and exc.response.status_code == 404
        ):
            set_context_notice(
                f"Milestone #{milestone_id} was not found."
            )
        else:
            set_context_notice(
                "Milestone details are temporarily unavailable."
            )
        return
    except Exception:
        set_context_notice(
            "Milestone details are temporarily unavailable."
        )
        return

    try:
        milestone_contract_id = int(
            milestone["contract_id"]
        )
    except (KeyError, TypeError, ValueError):
        set_context_notice(
            "Milestone details are temporarily unavailable."
        )
        return

    if milestone_contract_id != contract_id:
        set_context_notice(
            f"Milestone #{milestone_id} belongs to Contract "
            f"#{milestone_contract_id}."
        )
        return

    st.session_state["active_milestone_id"] = milestone_id
    set_context_notice(None)
    st.rerun()


def resolve_context(
    contract_id: int | None,
    milestone_id: int | None,
) -> tuple[int | None, int | None, dict]:
    context = load_context(
        contract_id,
        milestone_id,
    )
    resolved_contract_id = (
        contract_id
        if context["contract_summary"] is not None
        else None
    )
    resolved_milestone_id = (
        milestone_id
        if context["milestone"] is not None
        else None
    )

    if resolved_milestone_id is not None:
        try:
            milestone_contract_id = int(
                context["milestone"]["contract_id"]
            )
        except (KeyError, TypeError, ValueError):
            milestone_contract_id = -1

        if (
            resolved_contract_id is None
            or milestone_contract_id != resolved_contract_id
        ):
            resolved_milestone_id = None
            context["context_warning"] = (
                "The selected milestone belongs to a different contract."
            )

    if (
        resolved_contract_id != contract_id
        or resolved_milestone_id != milestone_id
    ):
        st.session_state["active_contract_id"] = (
            resolved_contract_id
        )
        st.session_state["active_milestone_id"] = (
            resolved_milestone_id
        )

    return (
        resolved_contract_id,
        resolved_milestone_id,
        context,
    )


backend_ok = backend_is_available()

with st.sidebar:
    st.markdown(
        (
            '<div class="sidebar-brand">'
            '<div class="sidebar-brand-title">'
            '◈ FreelanceOps'
            '</div>'
            '<div class="sidebar-brand-subtitle">'
            'Contract operations workspace'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Workspace",
        [
            "Overview",
            "New Contract",
            "Milestones",
            "Payments",
            "Workflow",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("Change context")

    contract_input_value = st.session_state.get(
        "contract_id_input",
        "",
    )
    milestone_input_value = st.session_state.get(
        "milestone_id_input",
        "",
    )

    contract_input_args = {
        "placeholder": "Enter contract ID",
        "key": "contract_id_input",
    }
    if "contract_id_input" not in st.session_state:
        contract_input_args["value"] = (
            "" if contract_input_value is None
            else str(contract_input_value)
        )
    st.text_input(
        "Contract ID",
        **contract_input_args,
    )

    if st.button(
        "Load Contract",
        use_container_width=True,
        key="load_contract_button",
    ):
        load_contract_from_input()

    milestone_input_args = {
        "placeholder": "Enter milestone ID",
        "key": "milestone_id_input",
    }
    if "milestone_id_input" not in st.session_state:
        milestone_input_args["value"] = (
            "" if milestone_input_value is None
            else str(milestone_input_value)
        )
    st.text_input(
        "Milestone ID",
        **milestone_input_args,
    )

    if st.button(
        "Load Milestone",
        use_container_width=True,
        key="load_milestone_button",
    ):
        load_milestone_from_input()

    context_notice = st.session_state.get(
        "_context_notice",
        None,
    )

    if context_notice:
        notice_kind = st.session_state.get(
            "_context_notice_kind",
            "warning",
        )
        notice_class = (
            "context-warning"
            if notice_kind == "warning"
            else "context-empty"
        )
        st.markdown(
            (
                f'<div class="{notice_class}">'
                f'{html.escape(str(context_notice))}'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

    if backend_ok:
        (
            active_contract_id,
            active_milestone_id,
            context,
        ) = resolve_context(
            active_contract_id,
            active_milestone_id,
        )
    else:
        active_contract_id = None
        active_milestone_id = None
        context = {
            "contract_summary": None,
            "contract_warning": None,
            "milestone": None,
            "milestone_warning": None,
            "context_warning": None,
        }

    render_sidebar_context(
        active_contract_id,
        active_milestone_id,
        context,
    )

    st.markdown(
        (
            '<div class="sidebar-footer">'
            '<div class="sidebar-footer-title">'
            'Backend architecture'
            '</div>'
            '<div class="sidebar-footer-text">'
            'Streamlit → FastAPI → Service Layer '
            '→ SQLAlchemy → SQLite'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

st.markdown(
    hero(),
    unsafe_allow_html=True,
)

show_flash()

if not backend_ok:
    st.error(
        "Backend API is currently unreachable."
    )
    st.caption(
        "Local development: make sure FastAPI is running. "
        "Deployment: verify API_BASE_URL points to the Railway backend."
    )
    st.stop()


if page == "Overview":
    section_title = "Operations Overview"
    section_description = (
        "Financial position, allocation and deadline health "
        "for the selected contract."
    )
    st.markdown(
        page_header(
            section_title,
            section_description,
        ),
        unsafe_allow_html=True,
    )

    if active_contract_id is None:
        if context["contract_warning"]:
            st.warning(context["contract_warning"])
        else:
            st.info(
                "No contract selected yet. "
                "Create your first contract from 'New Contract', "
                "or enter an ID in the sidebar."
            )
    elif context["contract_summary"] is None:
        st.warning(
            context["contract_warning"]
            or f"Contract #{active_contract_id} was not found."
        )
    else:
        summary = context["contract_summary"]
        total_value = Decimal(
            str(summary["total_value"])
        )
        total_paid = Decimal(
            str(summary["total_paid"])
        )
        allocated = Decimal(
            str(summary["allocated_amount"])
        )
        unallocated = Decimal(
            str(summary["unallocated_amount"])
        )
        outstanding = Decimal(
            str(summary["outstanding_amount"])
        )
        pending = Decimal(
            str(summary["pending_amount"])
        )
        overdue_count = int(
            summary["overdue_milestones"]
        )

        paid_percent = (
            float(total_paid / total_value * 100)
            if total_value > 0
            else 0.0
        )
        allocation_percent = (
            float(allocated / total_value * 100)
            if total_value > 0
            else 0.0
        )

        k1, k2, k3, k4 = st.columns(4)

        with k1:
            st.markdown(
                kpi_card(
                    "Contract Value",
                    money(total_value),
                    "Agreed contract value",
                ),
                unsafe_allow_html=True,
            )

        with k2:
            st.markdown(
                kpi_card(
                    "Collected",
                    money(total_paid),
                    f"{paid_percent:.0f}% received",
                ),
                unsafe_allow_html=True,
            )

        with k3:
            st.markdown(
                kpi_card(
                    "Outstanding",
                    money(outstanding),
                    "Remaining balance",
                ),
                unsafe_allow_html=True,
            )

        with k4:
            st.markdown(
                kpi_card(
                    "Overdue",
                    str(overdue_count),
                    (
                        "No overdue work"
                        if overdue_count == 0
                        else "Requires attention"
                    ),
                ),
                unsafe_allow_html=True,
            )

        st.write("")

        left, right = st.columns(
            [1.15, 0.85]
        )

        with left:
            with st.container(
                border=True
            ):
                st.subheader(
                    "Contract allocation"
                )
                st.caption(
                    "How much of the agreed contract "
                    "value has been assigned to milestones."
                )
                st.markdown(
                    info_row(
                        "Allocated",
                        money(allocated),
                    ),
                    unsafe_allow_html=True,
                )
                st.markdown(
                    info_row(
                        "Unallocated",
                        money(unallocated),
                    ),
                    unsafe_allow_html=True,
                )
                st.markdown(
                    progress_bar(
                        allocation_percent
                    ),
                    unsafe_allow_html=True,
                )
                st.caption(
                    f"{allocation_percent:.1f}% "
                    "of contract value allocated"
                )

            with st.container(
                border=True
            ):
                st.subheader(
                    "Payment collection"
                )
                st.caption(
                    "Cash received against the "
                    "total contract value."
                )
                st.markdown(
                    info_row(
                        "Received",
                        money(total_paid),
                    ),
                    unsafe_allow_html=True,
                )
                st.markdown(
                    info_row(
                        "Pending allocated work",
                        money(pending),
                    ),
                    unsafe_allow_html=True,
                )
                st.markdown(
                    info_row(
                        "Outstanding contract balance",
                        money(outstanding),
                    ),
                    unsafe_allow_html=True,
                )
                st.markdown(
                    progress_bar(
                        paid_percent
                    ),
                    unsafe_allow_html=True,
                )
                st.caption(
                    f"{paid_percent:.1f}% collected"
                )

        with right:
            with st.container(
                border=True
            ):
                st.subheader(
                    "Milestone lifecycle"
                )
                st.caption(
                    "Transitions are controlled "
                    "by the backend state machine."
                )
                active_status = None
                selected_milestone = context["milestone"]
                if (
                    selected_milestone is not None
                    and int(
                        selected_milestone.get(
                            "contract_id",
                            -1,
                        )
                    )
                    == active_contract_id
                ):
                    active_status = str(
                        selected_milestone.get(
                            "status",
                            "",
                        )
                    )
                st.markdown(
                    workflow(
                        active_status
                    ),
                    unsafe_allow_html=True,
                )
                st.caption(
                    "Submitted work can branch into "
                    "a disputed state and return for revision."
                )

            with st.container(
                border=True
            ):
                st.subheader(
                    "Deadline watch"
                )
                st.caption(
                    "Past-deadline milestones that "
                    "are not approved are overdue."
                )

                try:
                    overdue = get_overdue_milestones()
                except Exception as exc:
                    api_error(exc)
                else:
                    contract_overdue = [
                        item
                        for item in overdue
                        if int(
                            item["contract_id"]
                        )
                        == active_contract_id
                    ]

                    if not contract_overdue:
                        st.success(
                            "No overdue milestones."
                        )
                    else:
                        for item in contract_overdue:
                            st.markdown(
                                f"**{html.escape(item['title'])}**"
                            )
                            days_overdue = item.get(
                                "days_overdue",
                                "Unknown",
                            )
                            st.caption(
                                f"Due {item['deadline']} · "
                                f"{days_overdue} days overdue"
                            )
                            st.markdown(
                                status_pill(
                                    str(
                                        item["status"]
                                    )
                                ),
                                unsafe_allow_html=True,
                            )
                            st.divider()


elif page == "New Contract":
    st.markdown(
        page_header(
            "Create Contract",
            "Capture the commercial agreement before "
            "planning delivery milestones.",
        ),
        unsafe_allow_html=True,
    )

    left, right = st.columns(
        [1.35, 0.65]
    )

    with left:
        with st.container(
            border=True
        ):
            with st.form(
                "create_contract_form"
            ):
                st.subheader(
                    "Contract details"
                )
                title = st.text_input(
                    "Contract title",
                    placeholder=(
                        "e.g. SaaS Backend Development"
                    ),
                    key="new_contract_title",
                )

                c1, c2 = st.columns(2)

                with c1:
                    total_value = st.number_input(
                        "Total contract value",
                        min_value=0.01,
                        step=100.0,
                        key="new_contract_value",
                    )

                with c2:
                    start_date = st.date_input(
                        "Start date",
                        value=date.today(),
                        key="new_contract_start_date",
                    )

                st.markdown("#### Client")

                c1, c2 = st.columns(2)

                with c1:
                    client_name = st.text_input(
                        "Client name",
                        key="new_client_name",
                    )

                with c2:
                    client_email = st.text_input(
                        "Client email",
                        key="new_client_email",
                    )

                st.markdown("#### Freelancer")

                c1, c2 = st.columns(2)

                with c1:
                    freelancer_name = st.text_input(
                        "Freelancer name",
                        key="new_freelancer_name",
                    )

                with c2:
                    freelancer_email = st.text_input(
                        "Freelancer email",
                        key="new_freelancer_email",
                    )

                submitted = st.form_submit_button(
                    "Create contract",
                    type="primary",
                    use_container_width=True,
                )

            if submitted:
                validation_errors = []
                clean_title = str(title).strip()
                clean_client_name = str(client_name).strip()
                clean_client_email = str(client_email).strip()
                clean_freelancer_name = str(
                    freelancer_name
                ).strip()
                clean_freelancer_email = str(
                    freelancer_email
                ).strip()

                if not clean_title:
                    validation_errors.append(
                        "Contract title is required."
                    )

                if not clean_client_name:
                    validation_errors.append(
                        "Client name is required."
                    )

                if not clean_client_email:
                    validation_errors.append(
                        "Client email is required."
                    )

                if not clean_freelancer_name:
                    validation_errors.append(
                        "Freelancer name is required."
                    )

                if not clean_freelancer_email:
                    validation_errors.append(
                        "Freelancer email is required."
                    )

                try:
                    clean_total_value = Decimal(
                        str(total_value)
                    )
                    if clean_total_value <= 0:
                        raise InvalidOperation
                except (InvalidOperation, TypeError, ValueError):
                    validation_errors.append(
                        "Total contract value must be positive."
                    )
                    clean_total_value = None

                if validation_errors:
                    for error in validation_errors:
                        st.warning(error)
                else:
                    payload = {
                        "title": clean_title,
                        "total_value": str(
                            clean_total_value
                        ),
                        "start_date": start_date.isoformat(),
                        "client": {
                            "name": clean_client_name,
                            "email": clean_client_email,
                        },
                        "freelancer": {
                            "name": clean_freelancer_name,
                            "email": clean_freelancer_email,
                        },
                    }

                    try:
                        result = create_contract(
                            payload
                        )
                        new_contract_id = int(
                            result["id"]
                        )
                        st.session_state[
                            "active_contract_id"
                        ] = new_contract_id
                        st.session_state[
                            "active_milestone_id"
                        ] = None
                        st.session_state[
                            "_next_contract_id"
                        ] = new_contract_id
                        st.session_state[
                            "_next_milestone_id"
                        ] = None
                        st.session_state[
                            "_next_milestone_input"
                        ] = ""
                        set_context_notice(None)
                        st.session_state[
                            "_next_new_contract_title"
                        ] = ""
                        st.session_state[
                            "_next_new_contract_value"
                        ] = 0.01
                        st.session_state[
                            "_next_new_client_name"
                        ] = ""
                        st.session_state[
                            "_next_new_client_email"
                        ] = ""
                        st.session_state[
                            "_next_new_freelancer_name"
                        ] = ""
                        st.session_state[
                            "_next_new_freelancer_email"
                        ] = ""
                        set_flash(
                            f"Contract #{new_contract_id} "
                            "created successfully."
                        )
                        st.rerun()
                    except Exception as exc:
                        api_error(exc)

    with right:
        with st.container(
            border=True
        ):
            st.subheader(
                "Business rules"
            )
            st.caption(
                "The API protects these "
                "contract invariants."
            )
            st.markdown(
                info_row(
                    "Contract value",
                    "Must be positive",
                ),
                unsafe_allow_html=True,
            )
            st.markdown(
                info_row(
                    "Milestone allocation",
                    "Cannot exceed contract",
                ),
                unsafe_allow_html=True,
            )
            st.markdown(
                info_row(
                    "Financial precision",
                    "Decimal",
                ),
                unsafe_allow_html=True,
            )


elif page == "Milestones":
    st.markdown(
        page_header(
            "Milestone Planning",
            "Allocate contract value into "
            "controlled delivery stages.",
        ),
        unsafe_allow_html=True,
    )

    if active_contract_id is None:
        if context["contract_warning"]:
            st.warning(context["contract_warning"])
        else:
            st.info(
                "Select a Contract ID in the sidebar "
                "or create a new contract first."
            )
    elif context["contract_summary"] is None:
        st.warning(
            context["contract_warning"]
            or f"Contract #{active_contract_id} was not found."
        )
    else:
        summary = context["contract_summary"]
        unallocated = Decimal(
            str(summary["unallocated_amount"])
        )

        left, right = st.columns(
            [1.2, 0.8]
        )

        with left:
            if unallocated <= 0:
                with st.container(
                    border=True
                ):
                    st.success(
                        "Contract fully allocated."
                    )
                    st.caption(
                        "No additional milestone allocation "
                        "is available for this contract."
                    )
            else:
                with st.container(
                    border=True
                ):
                    st.subheader(
                        f"Contract #{active_contract_id}"
                    )
                    with st.form(
                        "milestone_form"
                    ):
                        title = st.text_input(
                            "Milestone title",
                            placeholder=(
                                "e.g. REST API delivery"
                            ),
                            key="milestone_title",
                        )

                        c1, c2 = st.columns(2)

                        with c1:
                            amount = st.number_input(
                                "Milestone amount",
                                min_value=0.01,
                                step=100.0,
                                key="milestone_amount",
                            )

                        with c2:
                            deadline = st.date_input(
                                "Delivery deadline",
                                value=(
                                    date.today()
                                    + timedelta(days=30)
                                ),
                                key="milestone_deadline",
                            )

                        submitted = st.form_submit_button(
                            "Add milestone",
                            type="primary",
                            use_container_width=True,
                        )

                    if submitted:
                        validation_errors = []
                        clean_title = str(title).strip()
                        if not clean_title:
                            validation_errors.append(
                                "Milestone title is required."
                            )

                        try:
                            clean_amount = Decimal(
                                str(amount)
                            )
                            if clean_amount <= 0:
                                raise InvalidOperation
                        except (InvalidOperation, TypeError, ValueError):
                            validation_errors.append(
                                "Milestone amount must be positive."
                            )
                            clean_amount = None

                        if validation_errors:
                            for error in validation_errors:
                                st.warning(error)
                        else:
                            payload = {
                                "title": clean_title,
                                "amount": str(clean_amount),
                                "deadline": deadline.isoformat(),
                            }

                            try:
                                result = add_milestone(
                                    active_contract_id,
                                    payload,
                                )
                                new_milestone_id = int(
                                    result["id"]
                                )
                                st.session_state[
                                    "active_milestone_id"
                                ] = new_milestone_id
                                st.session_state[
                                    "_next_contract_id"
                                ] = active_contract_id
                                st.session_state[
                                    "_next_milestone_id"
                                ] = new_milestone_id
                                st.session_state[
                                    "_next_milestone_input"
                                ] = str(new_milestone_id)
                                set_context_notice(None)
                                st.session_state[
                                    "_next_milestone_title"
                                ] = ""
                                st.session_state[
                                    "_next_milestone_amount"
                                ] = 0.01
                                set_flash(
                                    f"Milestone #{new_milestone_id} "
                                    "created successfully."
                                )
                                st.rerun()
                            except Exception as exc:
                                api_error(
                                    exc,
                                    not_found_message=(
                                        f"Contract #{active_contract_id} "
                                        "was not found."
                                    ),
                                )

        with right:
            with st.container(
                border=True
            ):
                st.subheader(
                    "Available allocation"
                )
                st.caption(
                    "Contract value available "
                    "for additional milestones."
                )
                st.markdown(
                    info_row(
                        "Contract value",
                        money(
                            summary[
                                "total_value"
                            ]
                        ),
                    ),
                    unsafe_allow_html=True,
                )
                st.markdown(
                    info_row(
                        "Allocated",
                        money(
                            summary[
                                "allocated_amount"
                            ]
                        ),
                    ),
                    unsafe_allow_html=True,
                )
                st.markdown(
                    info_row(
                        "Available",
                        money(
                            summary[
                                "unallocated_amount"
                            ]
                        ),
                    ),
                    unsafe_allow_html=True,
                )

                if unallocated <= 0:
                    st.success(
                        "Contract fully allocated."
                    )


elif page == "Payments":
    st.markdown(
        page_header(
            "Payment Ledger",
            "Record staged payments and track "
            "the remaining milestone balance.",
        ),
        unsafe_allow_html=True,
    )

    if active_milestone_id is None:
        if context["milestone_warning"]:
            st.warning(context["milestone_warning"])
        else:
            st.info(
                "Select a Milestone ID in the sidebar "
                "or create a milestone first."
            )
    elif context["milestone"] is None:
        st.warning(
            context["milestone_warning"]
            or f"Milestone #{active_milestone_id} was not found."
        )
    else:
        milestone = context["milestone"]
        milestone_id = int(milestone["id"])
        render_payment_context(milestone)

        try:
            payment = get_payment_summary(
                milestone_id
            )
        except Exception as exc:
            api_error(
                exc,
                not_found_message=(
                    f"Milestone #{milestone_id} was not found."
                ),
            )
        else:
            milestone_amount = Decimal(
                str(payment["milestone_amount"])
            )
            amount_paid = Decimal(
                str(payment["amount_paid"])
            )
            outstanding = Decimal(
                str(payment["outstanding_amount"])
            )
            percent = (
                float(
                    amount_paid
                    / milestone_amount
                    * 100
                )
                if milestone_amount > 0
                else 0.0
            )

            left, right = st.columns(
                [1.05, 0.95]
            )

            with left:
                if outstanding <= 0:
                    st.markdown(
                        (
                            '<div class="payment-complete">'
                            'Payment complete — no outstanding balance.'
                            '</div>'
                        ),
                        unsafe_allow_html=True,
                    )
                else:
                    with st.container(
                        border=True
                    ):
                        st.subheader(
                            "Record payment"
                        )
                        with st.form(
                            "payment_form"
                        ):
                            payment_amount = st.number_input(
                                "Payment amount",
                                min_value=0.01,
                                max_value=float(outstanding),
                                value=float(outstanding),
                                step=50.0,
                                key="payment_amount",
                            )
                            reference = st.text_input(
                                "Payment reference",
                                placeholder=(
                                    "e.g. BANK-2026-001"
                                ),
                                key="payment_reference",
                            )
                            submitted = st.form_submit_button(
                                "Record payment",
                                type="primary",
                                use_container_width=True,
                            )

                        if submitted:
                            validation_errors = []
                            try:
                                clean_payment_amount = Decimal(
                                    str(payment_amount)
                                )
                                if clean_payment_amount <= 0:
                                    raise InvalidOperation
                                if clean_payment_amount > outstanding:
                                    raise InvalidOperation
                            except (InvalidOperation, TypeError, ValueError):
                                validation_errors.append(
                                    "Enter a payment amount within the outstanding balance."
                                )

                            if validation_errors:
                                for error in validation_errors:
                                    st.warning(error)
                            else:
                                payload = {
                                    "amount": str(
                                        clean_payment_amount
                                    ),
                                    "reference": (
                                        str(reference).strip()
                                        or None
                                    ),
                                }
                                previous_status = str(
                                    milestone.get(
                                        "status",
                                        "",
                                    )
                                ).lower()

                                try:
                                    record_payment(
                                        milestone_id,
                                        payload,
                                    )
                                    refreshed_milestone = get_milestone(
                                        milestone_id
                                    )
                                    refreshed_status = str(
                                        refreshed_milestone.get(
                                            "status",
                                            "",
                                        )
                                    ).lower()

                                    if (
                                        refreshed_status == "paid"
                                        and previous_status != "paid"
                                    ):
                                        set_flash(
                                            "Full payment received. "
                                            "Milestone automatically moved to Paid."
                                        )
                                    else:
                                        set_flash(
                                            "Payment recorded successfully. "
                                            f"Current status: {display_status(refreshed_status)}."
                                        )

                                    st.rerun()
                                except Exception as exc:
                                    api_error(
                                        exc,
                                        not_found_message=(
                                            f"Milestone #{milestone_id} "
                                            "was not found."
                                        ),
                                    )

            with right:
                with st.container(
                    border=True
                ):
                    st.subheader(
                        "Payment position"
                    )
                    st.markdown(
                        info_row(
                            "Milestone value",
                            money(
                                milestone_amount
                            ),
                        ),
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        info_row(
                            "Received",
                            money(
                                amount_paid
                            ),
                        ),
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        info_row(
                            "Outstanding",
                            money(
                                outstanding
                            ),
                        ),
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        progress_bar(
                            percent
                        ),
                        unsafe_allow_html=True,
                    )
                    st.caption(
                        f"{percent:.1f}% collected"
                    )


elif page == "Workflow":
    st.markdown(
        page_header(
            "Milestone Workflow",
            "Move work through controlled lifecycle "
            "states enforced by the backend.",
        ),
        unsafe_allow_html=True,
    )

    if active_milestone_id is None:
        if context["milestone_warning"]:
            st.warning(context["milestone_warning"])
        else:
            st.info(
                "Select a Milestone ID in the sidebar "
                "or create a milestone first."
            )
    elif context["milestone"] is None:
        st.warning(
            context["milestone_warning"]
            or f"Milestone #{active_milestone_id} was not found."
        )
    else:
        milestone = context["milestone"]
        milestone_id = int(milestone["id"])
        status = str(milestone.get("status", "unknown")).lower()

        st.markdown(
            milestone_summary(
                milestone_id,
                str(milestone["title"]),
                status,
                money(milestone["amount"]),
                format_deadline(
                    milestone["deadline"]
                ),
                int(milestone["contract_id"]),
            ),
            unsafe_allow_html=True,
        )

        st.markdown(
            workflow(
                status
            ),
            unsafe_allow_html=True,
        )

        def apply_transition(
            target_status: str,
        ) -> None:
            try:
                result = update_milestone_status(
                    milestone_id,
                    target_status,
                )
                set_flash(
                    "Transition accepted. "
                    f"Current status: {display_status(result['status'])}."
                )
                st.rerun()
            except Exception as exc:
                api_error(
                    exc,
                    not_found_message=(
                        f"Milestone #{milestone_id} was not found."
                    ),
                )

        if status == "pending":
            st.subheader(
                "Available action"
            )
            if st.button(
                "Start Work",
                type="primary",
                use_container_width=True,
                key="start_work_action",
            ):
                apply_transition(
                    "in_progress"
                )

        elif status == "in_progress":
            st.subheader(
                "Available action"
            )
            if st.button(
                "Submit Work",
                type="primary",
                use_container_width=True,
                key="submit_work_action",
            ):
                apply_transition(
                    "submitted"
                )

        elif status == "submitted":
            st.subheader(
                "Available actions"
            )
            approve_column, dispute_column = st.columns(2)
            with approve_column:
                if st.button(
                    "Approve",
                    type="primary",
                    use_container_width=True,
                    key="approve_action",
                ):
                    apply_transition(
                        "approved"
                    )
            with dispute_column:
                if st.button(
                    "Raise Dispute",
                    use_container_width=True,
                    key="dispute_action",
                ):
                    apply_transition(
                        "disputed"
                    )

        elif status == "disputed":
            st.subheader(
                "Available actions"
            )
            return_column, resubmit_column = st.columns(2)
            with return_column:
                if st.button(
                    "Return to Work",
                    use_container_width=True,
                    key="return_to_work_action",
                ):
                    apply_transition(
                        "in_progress"
                    )
            with resubmit_column:
                if st.button(
                    "Resubmit",
                    type="primary",
                    use_container_width=True,
                    key="resubmit_action",
                ):
                    apply_transition(
                        "submitted"
                    )

        elif status == "approved":
            payment_error = None
            payment = None

            try:
                payment = get_payment_summary(
                    milestone_id
                )
            except Exception as exc:
                payment_error = exc

            st.subheader(
                "Payment progress"
            )

            if payment is None:
                st.warning(
                    "Payment progress is temporarily unavailable."
                )
            else:
                milestone_amount = Decimal(
                    str(payment["milestone_amount"])
                )
                amount_paid = Decimal(
                    str(payment["amount_paid"])
                )
                outstanding = Decimal(
                    str(payment["outstanding_amount"])
                )
                percent = (
                    float(
                        amount_paid
                        / milestone_amount
                        * 100
                    )
                    if milestone_amount > 0
                    else 0.0
                )

                with st.container(
                    border=True
                ):
                    st.markdown(
                        info_row(
                            "Milestone value",
                            money(
                                milestone_amount
                            ),
                        ),
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        info_row(
                            "Received",
                            money(
                                amount_paid
                            ),
                        ),
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        info_row(
                            "Outstanding",
                            money(
                                outstanding
                            ),
                        ),
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        progress_bar(
                            percent
                        ),
                        unsafe_allow_html=True,
                    )
                    st.caption(
                        f"{percent:.1f}% collected"
                    )

                if outstanding > 0:
                    st.markdown(
                        (
                            '<div class="payment-notice">'
                            'Full payment is required before this milestone can become Paid.'
                            '</div>'
                        ),
                        unsafe_allow_html=True,
                    )
                else:
                    st.subheader(
                        "Available action"
                    )
                    if st.button(
                        "Mark Paid",
                        type="primary",
                        use_container_width=True,
                        key="mark_paid_action",
                    ):
                        apply_transition(
                            "paid"
                        )

            if payment_error is not None:
                api_error(
                    payment_error,
                    not_found_message=(
                        f"Milestone #{milestone_id} was not found."
                    ),
                )

        elif status == "paid":
            st.success(
                "Milestone completed and fully paid."
            )
        else:
            st.warning(
                "This milestone has an unrecognized status. "
                "Refresh the page to load the latest backend state."
            )
