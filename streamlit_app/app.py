from datetime import date
from decimal import Decimal

import requests
import streamlit as st

from api_client import (
    BackendUnavailable,
    add_milestone,
    create_contract,
    get_contract_summary,
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
    page_header,
    progress_bar,
    status_pill,
    workflow,
)
from styles import APP_CSS


# =========================================================
# PAGE CONFIG
# =========================================================

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


# =========================================================
# HELPERS
# =========================================================

def money(value) -> str:
    try:
        return f"${Decimal(str(value)):,.2f}"
    except Exception:
        return "$0.00"


def api_error(exc: Exception) -> None:
    if isinstance(exc, BackendUnavailable):
        st.error(
            "Backend API is unavailable. "
            "Make sure FastAPI is running on port 8000."
        )
        return

    if isinstance(exc, requests.HTTPError):
        try:
            payload = exc.response.json()
            detail = payload.get(
                "detail",
                "Request failed.",
            )
        except Exception:
            detail = str(exc)

        st.error(detail)
        return

    st.error(str(exc))


def section_header(
    title: str,
    description: str,
) -> None:
    st.markdown(
        page_header(
            title,
            description,
        ),
        unsafe_allow_html=True,
    )


def backend_is_available() -> bool:
    try:
        health_check()
        return True
    except Exception:
        return False


# =========================================================
# SIDEBAR
# =========================================================

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

    st.caption("ACTIVE CONTEXT")

    current_contract = st.number_input(
        "Contract ID",
        min_value=1,
        value=int(
            st.session_state.get(
                "contract_id",
                1,
            )
        ),
        step=1,
        key="sidebar_contract_id",
    )

    current_milestone = st.number_input(
        "Milestone ID",
        min_value=1,
        value=int(
            st.session_state.get(
                "milestone_id",
                1,
            )
        ),
        step=1,
        key="sidebar_milestone_id",
    )

    st.session_state["contract_id"] = int(
        current_contract
    )

    st.session_state["milestone_id"] = int(
        current_milestone
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


# =========================================================
# HERO
# =========================================================

st.markdown(
    hero(),
    unsafe_allow_html=True,
)


# =========================================================
# BACKEND HEALTH
# =========================================================

backend_ok = backend_is_available()

if backend_ok:
    st.success(
        "Backend API connected",
        icon="✅",
    )
else:
    st.error(
        "Backend API is offline. "
        "Start FastAPI on http://127.0.0.1:8000"
    )

    st.code(
        "python -m uvicorn app.main:app "
        "--host 127.0.0.1 --port 8000",
        language="bash",
    )

    st.stop()


# =========================================================
# OVERVIEW
# =========================================================

if page == "Overview":

    section_header(
        "Operations Overview",
        "Financial position, allocation and deadline health "
        "for the selected contract.",
    )

    contract_id = st.session_state["contract_id"]

    try:
        summary = get_contract_summary(
            contract_id
        )

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
            float(
                total_paid
                / total_value
                * 100
            )
            if total_value > 0
            else 0.0
        )

        allocation_percent = (
            float(
                allocated
                / total_value
                * 100
            )
            if total_value > 0
            else 0.0
        )

        # ---------------------------------------------
        # KPI CARDS
        # ---------------------------------------------

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

        # ---------------------------------------------
        # LEFT COLUMN
        # ---------------------------------------------

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

        # ---------------------------------------------
        # RIGHT COLUMN
        # ---------------------------------------------

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

                st.markdown(
                    workflow(),
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

                overdue = (
                    get_overdue_milestones()
                )

                contract_overdue = [
                    item
                    for item in overdue
                    if item["contract_id"]
                    == contract_id
                ]

                if not contract_overdue:
                    st.success(
                        "No overdue milestones."
                    )

                else:
                    for item in contract_overdue:

                        st.markdown(
                            f"**{item['title']}**"
                        )

                        st.caption(
                            f"Due {item['deadline']} · "
                            f"{item['days_overdue']} "
                            "days overdue"
                        )

                        st.markdown(
                            status_pill(
                                item["status"]
                            ),
                            unsafe_allow_html=True,
                        )

                        st.divider()

    except Exception as exc:
        api_error(exc)

        st.info(
            "Choose an existing Contract ID "
            "from the sidebar or create a new contract."
        )


# =========================================================
# NEW CONTRACT
# =========================================================

elif page == "New Contract":

    section_header(
        "Create Contract",
        "Capture the commercial agreement before "
        "planning delivery milestones.",
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
                )

                c1, c2 = st.columns(2)

                with c1:
                    total_value = (
                        st.number_input(
                            "Total contract value",
                            min_value=0.01,
                            step=100.0,
                        )
                    )

                with c2:
                    start_date = (
                        st.date_input(
                            "Start date",
                            value=date.today(),
                        )
                    )

                st.markdown(
                    "#### Client"
                )

                c1, c2 = st.columns(2)

                with c1:
                    client_name = (
                        st.text_input(
                            "Client name"
                        )
                    )

                with c2:
                    client_email = (
                        st.text_input(
                            "Client email"
                        )
                    )

                st.markdown(
                    "#### Freelancer"
                )

                c1, c2 = st.columns(2)

                with c1:
                    freelancer_name = (
                        st.text_input(
                            "Freelancer name"
                        )
                    )

                with c2:
                    freelancer_email = (
                        st.text_input(
                            "Freelancer email"
                        )
                    )

                submitted = (
                    st.form_submit_button(
                        "Create contract",
                        type="primary",
                        use_container_width=True,
                    )
                )

        if submitted:

            payload = {
                "title": title,
                "total_value": str(
                    Decimal(
                        str(total_value)
                    )
                ),
                "start_date":
                    start_date.isoformat(),
                "client": {
                    "name": client_name,
                    "email": client_email,
                },
                "freelancer": {
                    "name":
                        freelancer_name,
                    "email":
                        freelancer_email,
                },
            }

            try:
                result = create_contract(
                    payload
                )

                st.session_state[
                    "contract_id"
                ] = result["id"]

                st.success(
                    "Contract created successfully."
                )

                with st.container(
                    border=True
                ):

                    st.subheader(
                        "Contract ready"
                    )

                    st.markdown(
                        info_row(
                            "Contract ID",
                            result["id"],
                        ),
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        info_row(
                            "Title",
                            result["title"],
                        ),
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        info_row(
                            "Value",
                            money(
                                result[
                                    "total_value"
                                ]
                            ),
                        ),
                        unsafe_allow_html=True,
                    )

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


# =========================================================
# MILESTONES
# =========================================================

elif page == "Milestones":

    contract_id = (
        st.session_state[
            "contract_id"
        ]
    )

    section_header(
        "Milestone Planning",
        f"Allocate Contract #{contract_id} "
        "into controlled delivery stages.",
    )

    left, right = st.columns(
        [1.2, 0.8]
    )

    with left:

        with st.container(
            border=True
        ):

            with st.form(
                "milestone_form"
            ):

                title = st.text_input(
                    "Milestone title",
                    placeholder=(
                        "e.g. REST API delivery"
                    ),
                )

                c1, c2 = st.columns(2)

                with c1:
                    amount = (
                        st.number_input(
                            "Milestone amount",
                            min_value=0.01,
                            step=100.0,
                        )
                    )

                with c2:
                    deadline = (
                        st.date_input(
                            "Delivery deadline"
                        )
                    )

                submitted = (
                    st.form_submit_button(
                        "Add milestone",
                        type="primary",
                        use_container_width=True,
                    )
                )

        if submitted:

            payload = {
                "title": title,
                "amount": str(
                    Decimal(str(amount))
                ),
                "deadline":
                    deadline.isoformat(),
            }

            try:
                result = add_milestone(
                    contract_id,
                    payload,
                )

                st.session_state[
                    "milestone_id"
                ] = result["id"]

                st.success(
                    f"Milestone #{result['id']} "
                    "created successfully."
                )

                st.markdown(
                    status_pill(
                        result["status"]
                    ),
                    unsafe_allow_html=True,
                )

            except Exception as exc:
                api_error(exc)

    with right:

        try:
            summary = (
                get_contract_summary(
                    contract_id
                )
            )

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

        except Exception as exc:
            api_error(exc)


# =========================================================
# PAYMENTS
# =========================================================

elif page == "Payments":

    milestone_id = (
        st.session_state[
            "milestone_id"
        ]
    )

    section_header(
        "Payment Ledger",
        f"Record staged payments against "
        f"Milestone #{milestone_id}.",
    )

    left, right = st.columns(
        [1.05, 0.95]
    )

    with left:

        with st.container(
            border=True
        ):

            with st.form(
                "payment_form"
            ):

                amount = (
                    st.number_input(
                        "Payment amount",
                        min_value=0.01,
                        step=50.0,
                    )
                )

                reference = (
                    st.text_input(
                        "Payment reference",
                        placeholder=(
                            "e.g. BANK-2026-001"
                        ),
                    )
                )

                submitted = (
                    st.form_submit_button(
                        "Record payment",
                        type="primary",
                        use_container_width=True,
                    )
                )

        if submitted:

            payload = {
                "amount": str(
                    Decimal(str(amount))
                ),
                "reference":
                    reference or None,
            }

            try:
                record_payment(
                    milestone_id,
                    payload,
                )

                st.success(
                    "Payment recorded successfully."
                )

            except Exception as exc:
                api_error(exc)

    with right:

        try:
            payment = (
                get_payment_summary(
                    milestone_id
                )
            )

            milestone_amount = Decimal(
                str(
                    payment[
                        "milestone_amount"
                    ]
                )
            )

            amount_paid = Decimal(
                str(
                    payment[
                        "amount_paid"
                    ]
                )
            )

            outstanding = Decimal(
                str(
                    payment[
                        "outstanding_amount"
                    ]
                )
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

        except Exception as exc:
            api_error(exc)


# =========================================================
# WORKFLOW
# =========================================================

elif page == "Workflow":

    milestone_id = (
        st.session_state[
            "milestone_id"
        ]
    )

    section_header(
        "Milestone Workflow",
        f"Control lifecycle transitions "
        f"for Milestone #{milestone_id}.",
    )

    with st.container(
        border=True
    ):
        st.subheader(
            "Standard lifecycle"
        )

        st.markdown(
            workflow(),
            unsafe_allow_html=True,
        )

        st.caption(
            "Submitted work can enter a disputed "
            "branch and return for revision."
        )

    left, right = st.columns(2)

    with left:

        with st.container(
            border=True
        ):

            st.subheader(
                "Apply transition"
            )

            new_status = st.selectbox(
                "New milestone status",
                [
                    "in_progress",
                    "submitted",
                    "approved",
                    "paid",
                    "disputed",
                ],
            )

            if st.button(
                "Apply transition",
                type="primary",
                use_container_width=True,
            ):

                try:
                    result = (
                        update_milestone_status(
                            milestone_id,
                            new_status,
                        )
                    )

                    st.success(
                        "Transition accepted."
                    )

                    st.markdown(
                        status_pill(
                            result["status"]
                        ),
                        unsafe_allow_html=True,
                    )

                except Exception as exc:
                    api_error(exc)

    with right:

        with st.container(
            border=True
        ):

            st.subheader(
                "State machine rules"
            )

            st.caption(
                "Status is not a free-text field."
            )

            st.markdown(
                info_row(
                    "pending → paid",
                    "Rejected",
                ),
                unsafe_allow_html=True,
            )

            st.markdown(
                info_row(
                    "submitted → approved",
                    "Allowed",
                ),
                unsafe_allow_html=True,
            )

            st.markdown(
                info_row(
                    "approved → paid",
                    "Requires full payment",
                ),
                unsafe_allow_html=True,
            )