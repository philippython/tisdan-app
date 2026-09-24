"""All data the bot needs from the Tisdan backend.

When API_BASE is set the backend is the only source of truth: if a call
fails we return nothing and the conversation says the service is
temporarily unavailable. The built-in demo data is used only when API_BASE
is not configured at all (local demos without a backend).
"""
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import logging
import os

import httpx
from dotenv import load_dotenv

# Load .env file if present so API_BASE can be set for local development
load_dotenv()

logger = logging.getLogger("tisdan.bot.data")

API_BASE = (os.environ.get("API_BASE") or "").rstrip("/")
BOT_API_KEY = os.environ.get("BOT_API_KEY", "")
DEMO_MODE = not API_BASE

if DEMO_MODE:
    logger.warning("API_BASE not set: the bot is running on built-in DEMO data")
else:
    logger.info("data_provider: using API_BASE=%s", API_BASE)

DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Used when a branch has no schedule configured in the portal yet.
DEFAULT_SCHEDULE = [
    {"day": d, "opening_time": "07:00", "closing_time": "19:00"} for d in DAY_ORDER[:6]
] + [{"day": "Sunday", "opening_time": "08:00", "closing_time": "14:00"}]


def normalize_phone_number(number: Optional[str]) -> Optional[str]:
    if not number:
        return None
    s = number.strip()
    if s.startswith("whatsapp:"):
        s = s[len("whatsapp:") :]
    s = s.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if s.startswith("0") and len(s) >= 10:
        s = "+234" + s[1:]
    elif s.startswith("234") and not s.startswith("+234"):
        s = "+" + s
    elif not s.startswith("+"):
        s = "+" + s
    return s


def format_price(price: Any) -> str:
    try:
        return f"₦{float(price):,.0f}"
    except (TypeError, ValueError):
        return str(price) if price else "Contact us for price"


def _client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=API_BASE,
        timeout=10.0,
        headers={"X-Bot-Key": BOT_API_KEY},
    )


async def _get(path: str, **params) -> Optional[Any]:
    try:
        async with _client() as c:
            r = await c.get(path, params=params or None)
        if r.status_code == 200:
            return r.json()
        if r.status_code != 404:
            logger.warning("GET %s failed: HTTP %s - %s", path, r.status_code, r.text[:300])
    except Exception as exc:
        logger.warning("GET %s failed: %s", path, exc)
    return None


async def _post(path: str, payload: Dict[str, Any]) -> Optional[Any]:
    try:
        async with _client() as c:
            r = await c.post(path, json=payload)
        if r.status_code in (200, 201):
            return r.json()
        logger.warning("POST %s failed: HTTP %s - %s", path, r.status_code, r.text[:300])
    except Exception as exc:
        logger.warning("POST %s failed: %s", path, exc)
    return None


# ── Catalogue ────────────────────────────────────────────────────────────
DEMO_BRANCHES = [
    {"id": "1", "name": "Ilesa HQ", "address": "Ilesa, Osun", "branch_code": "ILE"},
    {"id": "2", "name": "Ore Branch", "address": "Ore, Ondo", "branch_code": "ORE"},
    {"id": "3", "name": "Ibadan Branch", "address": "Ibadan, Oyo", "branch_code": "IBA"},
]

DEMO_TESTS = [
    {"id": "1", "name": "Malaria Parasite (MP)", "price": 1500, "branch_id": None},
    {"id": "2", "name": "Full Blood Count (FBC)", "price": 4500, "branch_id": None},
    {"id": "3", "name": "Malaria + FBC (combo)", "price": 5000, "branch_id": None},
    {"id": "4", "name": "Pregnancy Test", "price": 2000, "branch_id": None},
    {"id": "5", "name": "Urinalysis", "price": 3000, "branch_id": None},
    {"id": "6", "name": "Typhoid (Widal)", "price": 1500, "branch_id": None},
]


async def fetch_branches() -> List[Dict[str, Any]]:
    """Branches as a list of dicts with id, name, address, branch_code."""
    if DEMO_MODE:
        return DEMO_BRANCHES
    data = await _get("/branches/")
    return data if isinstance(data, list) else []


async def fetch_branch_schedule(branch_id: str) -> List[Dict[str, Any]]:
    """Opening days for a branch, Monday first, with Title-case day names."""
    schedules: List[Dict[str, Any]] = []
    if not DEMO_MODE:
        data = await _get("/branch-schedules/")
        if isinstance(data, list):
            schedules = [
                dict(s, day=str(s.get("day", "")).strip().title())
                for s in data
                if str(s.get("branch_id")) == str(branch_id)
            ]
    if not schedules:
        return DEFAULT_SCHEDULE
    rank = {d: i for i, d in enumerate(DAY_ORDER)}
    return sorted(schedules, key=lambda s: rank.get(s["day"], 99))


async def fetch_test_catalog() -> List[Dict[str, Any]]:
    if DEMO_MODE:
        return DEMO_TESTS
    data = await _get("/tests/")
    return data if isinstance(data, list) else []


async def fetch_tests_for_branch(branch_id: Optional[str]) -> List[Dict[str, Any]]:
    """Tests offered at a branch: branch-specific ones plus all-branch ones."""
    tests = await fetch_test_catalog()
    return [t for t in tests if not t.get("branch_id") or str(t.get("branch_id")) == str(branch_id)]


async def fetch_price_list() -> List[Dict[str, Any]]:
    tests = await fetch_test_catalog()
    items = [{"name": t.get("name", "Unknown"), "price": format_price(t.get("price"))} for t in tests]
    return [{"category": "All Tests", "items": items}] if items else []


async def find_test_by_name(test_name: str) -> Optional[Dict[str, Any]]:
    """Find a test by name (case-insensitive; exact match first, then partial)."""
    wanted = test_name.strip().lower()
    if not wanted:
        return None
    tests = await fetch_test_catalog()
    for test in tests:
        if test.get("name", "").lower() == wanted:
            return test
    for test in tests:
        name = test.get("name", "").lower()
        if wanted in name or name in wanted:
            return test
    return None


# ── Results ──────────────────────────────────────────────────────────────
DEMO_RESULTS = {
    "results": [
        {
            "reference": "DEMO-0001",
            "patient_name": "Demo Patient",
            "test_name": "Malaria Parasite (MP)",
            "branch_name": "Ilesa HQ",
            "date": "14 April 2026",
            "result_text": "Negative for Malaria Parasite",
        }
    ],
    "pending": 0,
}


async def fetch_results(phone: Optional[str] = None, reference: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Released results for a phone number or booking reference.

    Returns {"results": [...], "pending": n}, or None if the backend could
    not be reached.
    """
    if DEMO_MODE:
        return DEMO_RESULTS
    params = {"phone": normalize_phone_number(phone)} if phone else {"reference": reference}
    return await _get("/bot/results", **params)


# ── Bookings ─────────────────────────────────────────────────────────────
async def find_or_create_customer(phone: str, name: str, address: Optional[str] = None) -> Optional[Dict[str, Any]]:
    payload = {"full_name": name, "phone_number": normalize_phone_number(phone)}
    if address:
        payload["address"] = address
    return await _post("/bot/customers/", payload)


def next_date_for_day(day_name: str, opening_time: str = "07:00") -> Optional[datetime]:
    """The next occurrence (after today) of `day_name`, at the opening time."""
    day = day_name.strip().title()
    if day not in DAY_ORDER:
        return None
    today = datetime.now()
    days_ahead = DAY_ORDER.index(day) - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    try:
        hour, minute = (int(x) for x in opening_time.split(":")[:2])
    except ValueError:
        hour, minute = 7, 0
    return (today + timedelta(days=days_ahead)).replace(hour=hour, minute=minute, second=0, microsecond=0)


async def create_booking(
    phone: str,
    name: str,
    branch_id: str,
    test_id: Optional[str],
    test_name: str,
    appointment_day: str,
    opening_time: str = "07:00",
    address: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Create a booking for the WhatsApp user. Returns the booking or None."""
    if DEMO_MODE:
        logger.warning("DEMO mode: booking not saved")
        return {"id": "DEMO-BOOKING"}

    booking_date = next_date_for_day(appointment_day, opening_time)
    if booking_date is None:
        logger.warning("Invalid appointment day: %s", appointment_day)
        return None

    if not test_id:
        test = await find_test_by_name(test_name)
        if not test:
            logger.warning("Test '%s' not found", test_name)
            return None
        test_id = test["id"]

    customer = await find_or_create_customer(phone, name, address=address)
    if not customer:
        return None

    return await _post(
        "/bookings/",
        {
            "customer_id": customer["id"],
            "test_id": test_id,
            "branch_id": branch_id,
            "booking_date": booking_date.isoformat(),
        },
    )


# ── Coordinators & referrals ─────────────────────────────────────────────
DEMO_COORDINATORS = {
    "PHARM-ILE-007": {"referral_code": "PHARM-ILE-007", "user_full_name": "Ilesa Pharmacy"},
}


async def validate_coordinator(code: str) -> Optional[Dict[str, Any]]:
    code = code.strip().upper()
    if DEMO_MODE:
        return DEMO_COORDINATORS.get(code)
    return await _get(f"/bot/coordinators/{code}")


async def register_referral(
    coordinator_code: str,
    patient_name: str,
    patient_phone: str,
    test_name: str,
    branch_name: str,
) -> Optional[Dict[str, Any]]:
    """Save a referral in the backend so it shows in the admin portal.
    Returns the saved referral, or None if it could not be saved."""
    payload = {
        "coordinator_code": coordinator_code,
        "patient_name": patient_name,
        "patient_phone": normalize_phone_number(patient_phone) or patient_phone,
        "test_name": test_name,
        "branch_name": branch_name,
    }
    if DEMO_MODE:
        return dict(payload, id="DEMO-REFERRAL", status="registered")
    return await _post("/referrals/", payload)
