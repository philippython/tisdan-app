from typing import Any, Dict, List, Optional
import os
import httpx


# Base URL for the backend API. If unset, data_provider keeps using in-memory fallbacks.
API_BASE = os.environ.get("API_BASE")


async def _get_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=5.0)


async def fetch_branches() -> List[Dict[str, Any]]:
    """Fetch branches from API /branches/ or return fallback data.

    Returns a list of dicts containing at least `id` and `name`.
    """
    if API_BASE:
        try:
            async with await _get_client() as c:
                r = await c.get(f"{API_BASE.rstrip('/')}/branches/")
                r.raise_for_status()
                data = r.json()
                if isinstance(data, list):
                    return data
        except Exception:
            pass

    # Fallback static data
    return [
        {"id": "1", "name": "Ilesa HQ", "hours": "Mon–Sat 7am–7pm, Sun 8am–2pm", "phone": "+2347033444515", "address": "Ilesa, Osun"},
        {"id": "2", "name": "Ore Branch", "hours": "Mon–Sat 7am–7pm", "phone": "+2347033444515", "address": "Ore, Ondo"},
        {"id": "3", "name": "Ibadan Branch", "hours": "Mon–Sat 7am–7pm", "phone": "+2347033444515", "address": "Ibadan, Oyo"},
    ]


async def fetch_test_catalog() -> List[Dict[str, Any]]:
    """Fetch tests from API /tests/ or return fallback list."""
    if API_BASE:
        try:
            async with await _get_client() as c:
                r = await c.get(f"{API_BASE.rstrip('/')}/tests/")
                r.raise_for_status()
                data = r.json()
                if isinstance(data, list):
                    return data
        except Exception:
            pass

    return [
        {"id": "1", "name": "Malaria Parasite (MP)", "price": "₦1,500"},
        {"id": "2", "name": "Full Blood Count (FBC)", "price": "₦4,500"},
        {"id": "3", "name": "Malaria + FBC (combo)", "price": "₦5,000"},
        {"id": "4", "name": "Pregnancy Test", "price": "₦2,000"},
        {"id": "5", "name": "Urinalysis", "price": "₦3,000"},
        {"id": "6", "name": "Typhoid (Widal)", "price": "₦1,500"},
        {"id": "7", "name": "HIV Test", "price": "₦2,000"},
        {"id": "8", "name": "Abdominal Scan", "price": "₦5,000"},
    ]


async def fetch_customers() -> List[Dict[str, Any]]:
    """Fetch customers from API /customers/ or return empty list.

    Customers are people who book tests. Returns list of customer dicts.
    """
    if API_BASE:
        try:
            async with await _get_client() as c:
                r = await c.get(f"{API_BASE.rstrip('/')}/customers/")
                r.raise_for_status()
                data = r.json()
                if isinstance(data, list):
                    return data
        except Exception:
            pass

    return []


async def fetch_price_list() -> List[Dict[str, Any]]:
    """Return tests grouped as a single category if API doesn't provide price sections."""
    tests = await fetch_test_catalog()
    items = []
    for t in tests:
        items.append({"name": t.get("name", "Unknown"), "price": t.get("price", "Contact for price")})
    return [{"category": "All Tests", "items": items}]


# Results fallback store (kept for quick demo / offline use)
RESULTS_DB: Dict[str, Dict[str, str]] = {
    "TSC-20260414-0047": {
        "name": "Blessing Oladele",
        "test": "Malaria Parasite (MP)",
        "date": "14 April 2026",
        "branch": "Ilesa HQ",
        "result": "✅ Negative for Malaria Parasite",
    }
}

PHONE_INDEX: Dict[str, str] = {
    "+2347033444515": "TSC-20260414-0047",
}


async def fetch_result_by_reference(reference: str) -> Optional[Dict[str, Any]]:
    """Try API /results/{reference} then fall back to local DB.

    Attempts to enrich result using related endpoints when available.
    """
    if API_BASE:
        try:
            async with await _get_client() as c:
                r = await c.get(f"{API_BASE.rstrip('/')}/results/{reference}")
                if r.status_code == 200:
                    data = r.json()
                    # map API fields to internal display shape where possible
                    mapped = {
                        "reference": reference,
                        "result_text": data.get("result_text") or data.get("result") or "",
                        "status": data.get("status"),
                        "uploaded_at": data.get("uploaded_at"),
                    }
                    # try to resolve booking/test/branch names if booking_id present
                    booking_id = data.get("booking_id")
                    if booking_id:
                        try:
                            b = await c.get(f"{API_BASE.rstrip('/')}/bookings/{booking_id}")
                            if b.status_code == 200:
                                booking = b.json()
                                mapped.update({
                                    "date": booking.get("booking_date"),
                                    "branch": booking.get("branch_id"),
                                    "test": booking.get("test_id"),
                                })
                                # fetch test name
                                test_id = booking.get("test_id")
                                if test_id:
                                    t = await c.get(f"{API_BASE.rstrip('/')}/tests/{test_id}")
                                    if t.status_code == 200:
                                        mapped["test"] = t.json().get("name")
                                # fetch branch name
                                branch_id = booking.get("branch_id")
                                if branch_id:
                                    br = await c.get(f"{API_BASE.rstrip('/')}/branches/{branch_id}")
                                    if br.status_code == 200:
                                        mapped["branch"] = br.json().get("name")
                        except Exception:
                            pass
                    return mapped
        except Exception:
            pass

    # local fallback
    return RESULTS_DB.get(reference)


async def fetch_result_by_phone(phone: str) -> Optional[Dict[str, Any]]:
    """Resolve results by phone number by searching users -> bookings -> results when API present.

    Falls back to local index if API not available.
    """
    if API_BASE:
        try:
            async with await _get_client() as c:
                # Prefer customers (people who book tests) when resolving by phone
                cust_resp = await c.get(f"{API_BASE.rstrip('/')}/customers/")
                if cust_resp.status_code == 200:
                    customers = cust_resp.json()
                    customer = next((x for x in customers if x.get("phone_number") == phone or x.get("phone_number") == phone.lstrip("+")), None)
                    if customer:
                        customer_id = customer.get("id")
                        # fetch bookings and find customer's booking ids
                        b = await c.get(f"{API_BASE.rstrip('/')}/bookings/")
                        if b.status_code == 200:
                            bookings = b.json()
                            customer_bookings = [bk for bk in bookings if bk.get("user_id") == customer_id]
                            # for each booking try to find result
                            r = await c.get(f"{API_BASE.rstrip('/')}/results/")
                            if r.status_code == 200:
                                results = r.json()
                                for bk in customer_bookings:
                                    match = next((res for res in results if res.get("booking_id") == bk.get("id")), None)
                                    if match:
                                        return await fetch_result_by_reference(match.get("id"))

                # Fallback to users endpoint if customers didn't match or aren't present
                u = await c.get(f"{API_BASE.rstrip('/')}/users/")
                if u.status_code == 200:
                    users = u.json()
                    user = next((x for x in users if x.get("phone_number") == phone or x.get("phone_number") == phone.lstrip("+")), None)
                    if user:
                        user_id = user.get("id")
                        # fetch bookings and find user's booking ids
                        b = await c.get(f"{API_BASE.rstrip('/')}/bookings/")
                        if b.status_code == 200:
                            bookings = b.json()
                            user_bookings = [bk for bk in bookings if bk.get("user_id") == user_id]
                            # for each booking try to find result
                            r = await c.get(f"{API_BASE.rstrip('/')}/results/")
                            if r.status_code == 200:
                                results = r.json()
                                for bk in user_bookings:
                                    match = next((res for res in results if res.get("booking_id") == bk.get("id")), None)
                                    if match:
                                        return await fetch_result_by_reference(match.get("id"))
        except Exception:
            pass

    # fallback
    reference = PHONE_INDEX.get(phone)
    if reference:
        return RESULTS_DB.get(reference)
    return None


# Coordinator & Referral Management (local fallback)
COORDINATORS: Dict[str, Dict[str, str]] = {
    "PHARM-ILE-007": {"name": "Ilesa Pharmacy", "commission": "₦300", "type": "pharmacy"},
    "CHEW-ORE-001": {"name": "Ore Community Health Worker", "commission": "₦300", "type": "chew"},
    "CHURCH-IBA-002": {"name": "Ibadan Church", "commission": "₦200", "type": "church"},
}

REFERRALS: Dict[str, Dict[str, str]] = {}
REFERRAL_COUNTER: int = 0


async def validate_coordinator(code: str) -> Optional[Dict[str, Any]]:
    """Validate coordinator code; prefer API `/coordinators/` when available."""
    if API_BASE:
        try:
            async with await _get_client() as c:
                r = await c.get(f"{API_BASE.rstrip('/')}/coordinators/")
                r.raise_for_status()
                for coord in r.json():
                    if coord.get("referral_code") == code:
                        return coord
        except Exception:
            pass

    return COORDINATORS.get(code)


async def register_referral(
    coordinator_code: str,
    patient_name: str,
    patient_phone: str,
    test_name: str,
    branch_name: str,
) -> Dict[str, Any]:
    """Register a referral locally. If you have a referrals endpoint, this can be updated to POST there."""
    global REFERRAL_COUNTER
    REFERRAL_COUNTER += 1

    referral_id = f"REF-20260414-{REFERRAL_COUNTER:04d}"
    coordinator = COORDINATORS.get(coordinator_code, {"name": coordinator_code, "commission": "₦0"})

    referral_data = {
        "id": referral_id,
        "coordinator_code": coordinator_code,
        "coordinator_name": coordinator.get("name"),
        "patient_name": patient_name,
        "patient_phone": patient_phone,
        "test_name": test_name,
        "branch_name": branch_name,
        "commission": coordinator.get("commission"),
        "status": "registered",
    }

    REFERRALS[referral_id] = referral_data
    return referral_data


async def fetch_referral_by_id(referral_id: str) -> Optional[Dict[str, Any]]:
    return REFERRALS.get(referral_id)
