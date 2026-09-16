import os

import requests


BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
)

DEFAULT_TIMEOUT = 10


class BackendUnavailable(Exception):
    pass


def _handle_request(
    method: str,
    endpoint: str,
    **kwargs,
):
    try:
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            timeout=DEFAULT_TIMEOUT,
            **kwargs,
        )

        response.raise_for_status()

        return response.json()

    except requests.ConnectionError as exc:
        raise BackendUnavailable(
            "Cannot connect to the backend API. "
            "Make sure FastAPI is running."
        ) from exc


def health_check():
    return _handle_request(
        "GET",
        "/health",
    )


def create_contract(payload: dict):
    return _handle_request(
        "POST",
        "/contracts",
        json=payload,
    )


def add_milestone(
    contract_id: int,
    payload: dict,
):
    return _handle_request(
        "POST",
        f"/contracts/{contract_id}/milestones",
        json=payload,
    )


def update_milestone_status(
    milestone_id: int,
    status: str,
):
    return _handle_request(
        "PATCH",
        f"/milestones/{milestone_id}/status",
        json={
            "status": status,
        },
    )


def record_payment(
    milestone_id: int,
    payload: dict,
):
    return _handle_request(
        "POST",
        f"/milestones/{milestone_id}/payments",
        json=payload,
    )


def get_payment_summary(
    milestone_id: int,
):
    return _handle_request(
        "GET",
        f"/milestones/{milestone_id}/payments/summary",
    )


def get_contract_summary(
    contract_id: int,
):
    return _handle_request(
        "GET",
        f"/contracts/{contract_id}/summary",
    )


def get_overdue_milestones():
    return _handle_request(
        "GET",
        "/milestones/overdue",
    )