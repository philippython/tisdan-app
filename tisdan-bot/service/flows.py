from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

from .data_provider import (
    fetch_branches,
    fetch_price_list,
    fetch_result_by_phone,
    fetch_result_by_reference,
    fetch_test_catalog,
    validate_coordinator,
    register_referral,
    create_booking,
    fetch_branch_schedule,
)
from .sessions import get_session, reset_to_main_menu, update_state
from .twilio_client import send_whatsapp_message
from typing import Optional
from datetime import datetime, timedelta



def build_response(message: str) -> Response:
    response = MessagingResponse()
    response.message(message)
    return Response(content=str(response), media_type="application/xml")


async def main_menu_text(is_first_contact: bool) -> str:
    if is_first_contact:
        return (
            "Hello! 👋 Welcome to *Tisdan Care Medical Services*.\n\n"
            "I'm your Tisdan health assistant. I can help you with:\n\n"
            "*1* — Book a test appointment\n"
            "*2* — Get your test results\n"
            "*3* — View our test prices\n"
            "*4* — Find a branch near you\n"
            "*5* — Speak to our team\n\n"
            "Reply with a number (1–5) to continue.\n— Tisdan Care ✅"
        )

    return (
        "Welcome back! 😊 How can we help you today?\n\n"
        "*1* — Book a test appointment\n"
        "*2* — Get your test results\n"
        "*3* — View our test prices\n"
        "*4* — Find a branch near you\n"
        "*5* — Speak to our team\n\n"
        "Reply with a number to continue."
    )


async def price_list_text() -> str:
    price_sections = await fetch_price_list()
    lines = ["Tisdan Care — Test Prices 🧪\n\n"]
    for section in price_sections:
        lines.append(f"*{section['category']}:*\n")
        for item in section["items"]:
            lines.append(f"🔹 {item['name']} — {item['price']}\n")
        lines.append("\n")
    lines.append("Reply *1* to book a test, *0* for main menu.")
    return "".join(lines)


async def branch_locator_text() -> str:
    branches = await fetch_branches()
    lines = ["Tisdan Care Branches 📍\n\n"]
    for i, branch in enumerate(branches, start=1):
        # API branch schema: id, name, address, branch_code
        name = branch.get("name", "Unknown")
        address = branch.get("address", "Address not available")
        code = branch.get("branch_code", "")
        lines.extend([
            f"*{i}* — {name} {f'({code})' if code else ''}\n",
            f"📍 {address}\n",
            "\n",
        ])
    lines.append("All results delivered to WhatsApp. Walk-ins welcome.\n\nReply *1* to book | *0* for main menu.")
    return "".join(lines)


def speak_to_team_text() -> str:
    return (
        "Thanks for reaching out!\n\n"
        "A member of the Tisdan team will contact you shortly.\n"
        "For urgent support, call +2347033444515.\n\n"
        "Reply *0* to return to the main menu."
    )


async def booking_branch_text() -> str:
    branches = await fetch_branches()
    lines = [
        "Great! Let's book your test. 🏥\n\n"
        "Which branch would you like to visit?\n\n"
    ]
    for i, branch in enumerate(branches, start=1):
        name = branch.get("name", "Unknown")
        hours = branch.get("hours") or branch.get("opening_time", "Hours not available")
        lines.append(f"*{i}* — {name} ({hours})\n")
    lines.append("\nReply *0* at any time to return to the main menu.")
    return "".join(lines)


async def booking_day_text(branch_id: str) -> str:
    """Show available days and times for the selected branch."""
    schedules = await fetch_branch_schedule(branch_id)
    lines = [
        "Great! When would you like to visit?\n\n"
        "Choose a day:\n\n"
    ]
    
    for i, sched in enumerate(schedules, start=1):
        day = sched.get("day", "Unknown")
        opening = sched.get("opening_time", "07:00").split(":")[:2]  # Get HH:MM
        closing = sched.get("closing_time", "19:00").split(":")[:2]
        opening_str = ":".join(opening)
        closing_str = ":".join(closing)
        lines.append(f"*{i}* — {day} ({opening_str} – {closing_str})\n")
    
    lines.append("\nReply with a number, or *0* to go back.")
    return "".join(lines)


def confirm_booking_text(session: dict[str, str]) -> str:
    return (
        "Here is your booking summary:\n\n"
        f"📍 *Branch:* {session['branch_name']}\n"
        f"🧪 *Test:* {session['test_name']}\n"
        f"💰 *Price:* {session['test_price']}\n"
        f"📅 *Day:* {session['appointment_day']}\n"
        f"🕐 *Hours:* {session['appointment_hours']}\n"
        f"👤 *Name:* {session['patient_name']}\n\n"
        "Please reply:\n"
        "*1* — Confirm this booking ✅\n"
        "*2* — Change something ✏️\n"
        "*0* — Cancel"
    )


def booking_confirmation_text(session: dict[str, str]) -> str:
    return (
        "✅ *Booking Confirmed!*\n\n"
        f"Your booking reference is: *{session['booking_ref']}*\n\n"
        f"📍 Tisdan Care, {session['branch_name']}\n"
        f"📅 {session['appointment_day']} — {session['appointment_hours']}\n"
        f"🧪 {session['test_name']}\n"
        f"💰 {session['test_price']} (pay at reception)\n\n"
        "*Please bring this reference number.* No fasting required for malaria test.\n\n"
        "Your result will be sent to this WhatsApp number when ready (same day for malaria).\n\n"
        "Questions? Reply *5* to speak to our team.\n— Tisdan Care ✅"
    )


def result_found_text(reference: str, result: dict[str, str]) -> str:
    return (
        "Found it! ✅\n\n"
        f"*Patient:* {result['name']}\n"
        f"*Test:* {result['test']}\n"
        f"*Date:* {result['date']}\n"
        f"*Branch:* {result['branch']}\n\n"
        f"*Result:* {result['result']}\n\n"
        "_Result issued by Tisdan Care Medical Services, Ilesa. For clinical interpretation, please speak to your doctor or visit us._\n\n"
        f"Reference: {reference}\n— Tisdan Care 🏥"
    )


def coordinator_activation_text(code: str) -> str:
    return (
        f"👋 Hello! Referral mode activated for coordinator *{code}*.\n\n"
        "Please send the patient's details in this format:\n\n"
        "NAME: [Patient full name]\n"
        "PHONE: [Patient WhatsApp number — include country code, e.g. 2348012345678]\n"
        "TEST: [Test requested]\n"
        "BRANCH: [Ilesa / Ore / Ibadan]\n\n"
        "Example:\n"
        "NAME: Adesola Okunola\n"
        "PHONE: 2348034512345\n"
        "TEST: FBC + Malaria\n"
        "BRANCH: Ilesa"
    )


def coordinator_confirmation_text(referral: dict[str, str]) -> str:
    return (
        "✅ Referral registered!\n\n"
        f"*Patient:* {referral['patient_name']}\n"
        f"*Phone:* +{referral['patient_phone']}\n"
        f"*Test:* {referral['test_name']}\n"
        f"*Branch:* {referral['branch_name']}\n"
        f"*Your code:* {referral['coordinator_code']}\n"
        f"*Referral ID:* {referral['id']}\n\n"
        "The patient will receive a WhatsApp message from Tisdan shortly.\n"
        f"Your commission ({referral['commission']}) is logged and will be paid at month end."
    )


def patient_referral_message(referral: dict[str, str]) -> str:
    return (
        f"Hello *{referral['patient_name']}*! 👋\n\n"
        "You've been referred to *Tisdan Care* by one of our community partners.\n\n"
        f"Your test: *{referral['test_name']}*\n"
        f"Branch: *{referral['branch_name']}*\n"
        "Price: *₦5,000*\n\n"
        "📍 Address: " + referral['branch_name'].split()[0] + ", Osun State\n"
        "🕐 Open Mon–Sat from 7am\n\n"
        f"Please mention referral code *{referral['id']}* when you arrive.\n\n"
        "Questions? Just reply here and we'll help.\n"
        "— Tisdan Care Medical Services ✅"
    )


def parse_coordinator_details(text: str) -> dict[str, str] | None:
    """Parse coordinator patient details from formatted text."""
    lines = text.strip().split("\n")
    details = {}
    
    for line in lines:
        line = line.strip()
        if not line or ":" not in line:
            continue
        
        key, value = line.split(":", 1)
        key = key.strip().upper()
        value = value.strip()
        
        if key == "NAME":
            details["name"] = value
        elif key == "PHONE":
            details["phone"] = value
        elif key == "TEST":
            details["test"] = value
        elif key == "BRANCH":
            details["branch"] = value
    
    # Validate all required fields
    if all(k in details for k in ["name", "phone", "test", "branch"]):
        # Normalize branch name
        branch_input = details["branch"].lower()
        if "ilesa" in branch_input:
            details["branch"] = "Ilesa HQ"
        elif "ore" in branch_input:
            details["branch"] = "Ore Branch"
        elif "ibadan" in branch_input:
            details["branch"] = "Ibadan Branch"
        else:
            return None
        return details
    
    return None




async def process_incoming_message(from_phone: str, body: str) -> Response:
    phone = from_phone.strip()
    message = body.strip()
    normalized = message.lower()
    session = get_session(phone)

    # Coordinator referral mode detection (REF <code>)
    if normalized.startswith("ref "):
        coordinator_code = message[4:].strip().upper()
        coordinator = await validate_coordinator(coordinator_code)
        if coordinator:
            update_state(session, "coordinator_mode", coordinator_code=coordinator_code)
            return build_response(coordinator_activation_text(coordinator_code))
        return build_response("Invalid coordinator code. Please check and try again.")

    # Coordinator patient details entry
    if session["state"] == "coordinator_mode":
        details_text = message.strip()
        parsed = parse_coordinator_details(details_text)
        
        if not parsed:
            return build_response(
                "Sorry, I didn't understand that format.\n\n"
                "Please send patient details as:\n"
                "NAME: [full name]\n"
                "PHONE: [number with country code]\n"
                "TEST: [test name]\n"
                "BRANCH: [Ilesa / Ore / Ibadan]"
            )
        
        # Register the referral
        referral = await register_referral(
            session["coordinator_code"],
            parsed["name"],
            parsed["phone"],
            parsed["test"],
            parsed["branch"],
        )

        # Auto-send the patient notification if Twilio is configured.
        patient_message = patient_referral_message(referral)
        send_whatsapp_message(referral["patient_phone"], patient_message)

        # Send confirmation to coordinator
        coordinator_msg = coordinator_confirmation_text(referral)

        # Reset coordinator to main menu for next potential use
        reset_to_main_menu(session)

        return build_response(coordinator_msg)

    if normalized == "0":
        reset_to_main_menu(session)
        session["seen"] = True
        return build_response(await main_menu_text(False))

    if session["state"] == "main_menu":
        # dispatch to the appropriate handler for the main menu
        return await _handle_main_menu(session, message, normalized)

    # State-based handler registry
    STATE_HANDLERS = {
        "booking_branch": _handle_booking_branch,
        "booking_test": _handle_booking_test,
        "booking_custom_test": _handle_booking_custom_test,
        "booking_day": _handle_booking_day,
        "booking_name": _handle_booking_name,
        "booking_date": _handle_booking_date,
        "booking_confirm": _handle_booking_confirm,
        "result_search": _handle_result_search,
        "price_list": _handle_price_list,
        "branch_locator": _handle_branch_locator,
        "speak_team": _handle_speak_team,
    }

    handler = STATE_HANDLERS.get(session["state"]) if session["state"] else None
    if handler:
        return await handler(session, message, normalized, phone)

    # Fallback
    return build_response("Sorry, I didn't understand that. Reply 0 for the main menu.")


async def _handle_main_menu(session: dict, message: str, normalized: str, phone: Optional[str] = None) -> Response:
    if not session["seen"]:
        session["seen"] = True
        return build_response(await main_menu_text(True))

    if normalized == "1":
        update_state(session, "booking_branch")
        return build_response(await booking_branch_text())

    if normalized == "2":
        update_state(session, "result_search")
        return build_response(
            "To find your result, please send me either:\n"
            "— Your *booking reference* (e.g. TSC-20260414-0047)\n"
            "— Or just reply *CONFIRM* and I'll search using this phone number."
        )

    if normalized == "3":
        update_state(session, "price_list")
        return build_response(await price_list_text())

    if normalized == "4":
        update_state(session, "branch_locator")
        return build_response(await branch_locator_text())

    if normalized == "5":
        update_state(session, "speak_team")
        return build_response(speak_to_team_text())

    update_state(session, "main_menu")
    return build_response("Sorry, I didn't understand that.\n\n" + await main_menu_text(False))


async def _handle_booking_branch(session: dict, message: str, normalized: str, phone: Optional[str] = None) -> Response:
    branches = await fetch_branches()
    valid_choices = [str(i) for i in range(1, len(branches) + 1)]

    # Accept numeric selection mapped to the branch index
    if normalized.isdigit() and normalized in valid_choices:
        idx = int(normalized) - 1
        branch = branches[idx]
        branch_id = branch.get("id")
        branch_name = branch.get("name", "Unknown")
        update_state(session, "booking_test", branch_id=branch_id, branch_name=branch_name)
        return build_response(await booking_test_text(branch_name))

    return build_response(
        "Please choose a branch by replying with one of: "
        + ", ".join(valid_choices)
        + ".\nReply 0 to return to the main menu."
    )


async def _handle_booking_test(session: dict, message: str, normalized: str, phone: Optional[str] = None) -> Response:
    if normalized == "10":
        return build_response(await price_list_text())

    if normalized == "9":
        update_state(session, "booking_custom_test")
        return build_response(
            "Please type the name of the test or package you want.\n"
            "Reply 0 to return to the main menu."
        )

    tests = await fetch_test_catalog()
    valid_choices = [str(i) for i in range(1, len(tests) + 1)]

    if normalized.isdigit() and normalized in valid_choices:
        idx = int(normalized) - 1
        test = tests[idx]
        update_state(session, "booking_day", test_name=test.get("name"), test_price=str(test.get("price")))
        return build_response(await booking_day_text(session.get("branch_id")))

    return build_response(
        "Please choose a valid test number: " + ", ".join(valid_choices) + ".\n"
        "Or reply 9 to type a custom test name, 10 to view full price list, or 0 to return to the main menu."
    )


async def _handle_booking_custom_test(session: dict, message: str, normalized: str, phone: Optional[str] = None) -> Response:
    update_state(session, "booking_day", test_name=message, test_price="Contact front desk for price")
    return build_response(
        f"Got it — *{message}* at *{session['branch_name']}*. ✅\n\n"
        "When would you like to visit?\n\n" + await booking_day_text(session.get("branch_id"))
    )


async def _handle_booking_day(session: dict, message: str, normalized: str, phone: Optional[str] = None) -> Response:
    """Handle day selection with time slots."""
    schedules = await fetch_branch_schedule(session.get("branch_id"))
    valid_choices = [str(i) for i in range(1, len(schedules) + 1)]

    if normalized.isdigit() and normalized in valid_choices:
        idx = int(normalized) - 1
        schedule = schedules[idx]
        day = schedule.get("day", "Unknown")
        opening = schedule.get("opening_time", "07:00").split(":")[:2]
        closing = schedule.get("closing_time", "19:00").split(":")[:2]
        hours_str = ":".join(opening) + " – " + ":".join(closing)
        
        update_state(session, "booking_name", appointment_day=day, appointment_hours=hours_str)
        return build_response(
            f"Perfect! Booking for *{day}* ({hours_str}). ✅\n\n"
            "Please send me your *full name* as it should appear on your result."
        )

    return build_response(
        "Please choose a valid day number: " + ", ".join(valid_choices) + ".\n"
        "Reply 0 to return to the main menu."
    )


async def _handle_booking_name(session: dict, message: str, normalized: str, phone: Optional[str] = None) -> Response:
    update_state(session, "booking_confirm", patient_name=message, booking_ref="TSC-20260414-0047")
    return build_response(confirm_booking_text(session))


async def _handle_booking_date(session: dict, message: str, normalized: str, phone: Optional[str] = None) -> Response:
    # Validate user-provided date input. Accept formats like:
    # - '14 April 2026', '14 Apr 2026'
    # - '2026-04-14', '14/04/2026', '14-04-2026'
    # - 'today', 'tomorrow'
    # - 'walk-in' / 'walk in'

    def _parse_user_date(text: str):
        t = text.strip().lower()
        if t in ("walk-in", "walk in", "walkin"):
            return "Walk-in"
        if t == "today":
            return datetime.utcnow().date()
        if t == "tomorrow":
            return (datetime.utcnow() + timedelta(days=1)).date()

        formats = [
            "%d %B %Y",
            "%d %b %Y",
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%d-%m-%Y",
        ]
        for fmt in formats:
            try:
                parsed = datetime.strptime(text.strip(), fmt).date()
                return parsed
            except Exception:
                continue
        return None

    parsed = _parse_user_date(message)
    if parsed is None:
        return build_response(
            "I couldn't understand that date. Please reply with a date like '14 April 2026', '2026-04-14', 'today', 'tomorrow', or 'walk-in'.\n\nReply 0 to cancel."
        )

    # If walk-in, store a human-friendly label
    if isinstance(parsed, str) and parsed == "Walk-in":
        appointment_label = "Walk-in"
    else:
        # parsed is a date object
        if parsed < datetime.utcnow().date():
            return build_response("Please choose today or a future date.")
        appointment_label = parsed.strftime("%d %B %Y")

    update_state(session, "booking_confirm", appointment_date=appointment_label, booking_ref="TSC-20260414-0047")
    return build_response(confirm_booking_text(session))


async def _handle_booking_confirm(session: dict, message: str, normalized: str, phone: Optional[str] = None) -> Response:
    if normalized == "1":
        # Attempt to create the booking
        booking = await create_booking(
            phone=phone,
            name=session.get("patient_name", "Unknown"),
            branch_id=session.get("branch_id"),
            test_name=session.get("test_name", ""),
            appointment_day=session.get("appointment_day", "Monday"),
            appointment_hours=session.get("appointment_hours", "07:00 – 19:00")
        )
        
        if booking and booking.get("id"):
            session["booking_ref"] = booking["id"]
            update_state(session, "main_menu")
            return build_response(booking_confirmation_text(session))

        return build_response(
            "Sorry, I couldn't save your booking right now. Please try again or contact the clinic at +2347033444515."
        )
    if normalized == "2":
        update_state(session, "booking_branch")
        return build_response("No problem — let's restart your booking.\n\n" + await booking_branch_text())
    if normalized == "0":
        update_state(session, "main_menu")
        return build_response(await main_menu_text(False))
    return build_response("Please reply with 1 to confirm, 2 to change something, or 0 to cancel.")


async def _handle_result_search(session: dict, message: str, normalized: str, phone: Optional[str] = None) -> Response:
    if normalized == "confirm":
        result = await fetch_result_by_phone(phone)
        if result:
            update_state(session, "main_menu")
            return build_response(result_found_text(phone, result))
        return build_response("Sorry, I couldn't find your result using this phone number.")

    result = await fetch_result_by_reference(message)
    if result:
        update_state(session, "main_menu")
        return build_response(result_found_text(message, result))

    return build_response(
        "I couldn't find a result with that reference.\n"
        "Please send a valid booking reference or reply CONFIRM."
    )


async def _handle_price_list(session: dict, message: str, normalized: str, phone: Optional[str] = None) -> Response:
    if normalized == "1":
        update_state(session, "booking_branch")
        return build_response(await booking_branch_text())
    if normalized == "0":
        update_state(session, "main_menu")
        return build_response(await main_menu_text(False))
    return build_response("Reply 1 to book a test or 0 for the main menu.")


async def _handle_branch_locator(session: dict, message: str, normalized: str, phone: Optional[str] = None) -> Response:
    if normalized == "1":
        update_state(session, "booking_branch")
        return build_response(await booking_branch_text())
    if normalized == "0":
        update_state(session, "main_menu")
        return build_response(await main_menu_text(False))
    return build_response("Reply 1 to start booking or 0 to return to the main menu.")


async def _handle_speak_team(session: dict, message: str, normalized: str, phone: Optional[str] = None) -> Response:
    if normalized == "0":
        update_state(session, "main_menu")
        return build_response(await main_menu_text(False))
    return build_response(
        "Reply 0 to return to the main menu or call +2347033444515 for urgent support."
    )
