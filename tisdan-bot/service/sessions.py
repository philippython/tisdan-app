from typing import Any

sessions: dict[str, dict[str, Any]] = {}


def get_session(phone: str) -> dict[str, Any]:
    return sessions.setdefault(phone, {"state": "main_menu", "seen": False})


def reset_to_main_menu(session: dict[str, Any]) -> dict[str, Any]:
    session.update({"state": "main_menu"})
    return session


def update_state(session: dict[str, Any], state: str, **kwargs: Any) -> dict[str, Any]:
    session["state"] = state
    session.update(kwargs)
    return session
