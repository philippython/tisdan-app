"""Bot ↔ backend integration test.

Starts the real backend (with a throwaway SQLite DB) and drives WhatsApp
conversations through the bot's /sms webhook.

Run from tisdan-bot/ (needs the backend's virtualenv at
../tisdan-backend/fastapivenv, or set BACKEND_PYTHON):
    python -m unittest discover -s tests -v
"""
import os
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import xml.etree.ElementTree as ET

import httpx

HERE = os.path.dirname(os.path.abspath(__file__))
BOT_DIR = os.path.dirname(HERE)
BACKEND_DIR = os.path.join(os.path.dirname(BOT_DIR), "tisdan-backend")
BACKEND_PYTHON = os.environ.get("BACKEND_PYTHON") or os.path.join(
    BACKEND_DIR, "fastapivenv", "Scripts" if os.name == "nt" else "bin", "python"
)
KEY = "integration-bot-key"


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


PORT = _free_port()
API = f"http://127.0.0.1:{PORT}"

os.environ.update(API_BASE=API, BOT_API_KEY=KEY, TWILIO_ACCOUNT_SID="", TWILIO_AUTH_TOKEN="")
sys.path.insert(0, BOT_DIR)

from fastapi.testclient import TestClient  # noqa: E402

import service.flows as flows  # noqa: E402
from main import app  # noqa: E402

OUTBOX = []  # messages the bot pushed (not replies), e.g. referral notices
flows.send_whatsapp_message = lambda to, body: OUTBOX.append((to, body)) or True


class BotFlowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tmp = tempfile.mkdtemp()
        env = dict(
            os.environ,
            ENVIRONMENT="local",
            DATABASE_URL=f"sqlite:///{os.path.join(tmp, 'bot-test.db')}",
            BOT_API_KEY=KEY,
            SECRET_KEY="integration-secret",
            TISDAN_BOT_URL="http://127.0.0.1:9",  # notifications go nowhere
            ADMIN_PASSWORD="adminpass123",
        )
        subprocess.run(
            [BACKEND_PYTHON, "scripts/create_admin.py", "admin@example.com", "Admin", "08011111111"],
            cwd=BACKEND_DIR, env=env, check=True, capture_output=True,
        )
        cls.backend = subprocess.Popen(
            [BACKEND_PYTHON, "-m", "uvicorn", "app.main:app", "--port", str(PORT)],
            cwd=BACKEND_DIR, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        for _ in range(100):
            try:
                if httpx.get(f"{API}/health").status_code == 200:
                    break
            except httpx.HTTPError:
                time.sleep(0.2)
        else:
            raise RuntimeError("backend did not start")

        token = httpx.post(f"{API}/auth/login", data={"username": "admin@example.com", "password": "adminpass123"}).json()["access_token"]
        cls.admin = {"Authorization": f"Bearer {token}"}
        branch = httpx.post(f"{API}/branches/", json={"name": "Ilesa HQ", "address": "1 Main St, Ilesa", "branch_code": "IL-01"}, headers=cls.admin).json()
        cls.branch = branch
        httpx.post(f"{API}/branch-schedules/", json={"branch_id": branch["id"], "day": "MONDAY", "opening_time": "08:00", "closing_time": "17:00"}, headers=cls.admin)
        httpx.post(f"{API}/tests/", json={"name": "Malaria Parasite", "description": "MP", "price": 1500}, headers=cls.admin)
        cls.coordinator = httpx.post(f"{API}/users/", json={"email": "coord@example.com", "password": "coordpass1", "full_name": "Kemi Coordinator", "phone_number": "08055555555", "role": "COORDINATOR"}, headers=cls.admin).json()

        cls.bot = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        cls.backend.terminate()
        cls.backend.wait(timeout=10)

    def say(self, phone, text):
        r = self.bot.post("/sms", data={"From": f"whatsapp:{phone}", "Body": text, "To": "whatsapp:+1"})
        self.assertEqual(r.status_code, 200, r.text)
        return ET.fromstring(r.text).find("Message").text

    def test_send_endpoint_requires_key(self):
        self.assertEqual(self.bot.post("/send", json={"to": "+1", "body": "x"}).status_code, 401)
        r = self.bot.post("/send", json={"to": "+1", "body": "x"}, headers={"X-Bot-Key": KEY})
        self.assertEqual(r.json(), {"ok": False})  # Twilio not configured in tests

    def test_booking_then_result_lookup(self):
        phone = "+2348030001111"
        self.assertIn("Welcome", self.say(phone, "hi"))
        self.assertIn("Ilesa HQ", self.say(phone, "1"))
        reply = self.say(phone, "1")
        self.assertIn("Malaria Parasite", reply)
        self.assertIn("₦1,500", reply)
        self.assertIn("Monday (08:00 – 17:00)", self.say(phone, "1"))
        self.assertIn("full name", self.say(phone, "1"))
        self.say(phone, "Tunde Bakare")
        self.assertIn("Confirm this booking", self.say(phone, "SKIP"))
        confirmed = self.say(phone, "1")
        self.assertIn("Booking Confirmed", confirmed)

        bookings = httpx.get(f"{API}/bookings/", headers=self.admin).json()
        booking = next(b for b in bookings if b["patient_phone"] == phone)
        self.assertEqual(booking["patient_name"], "Tunde Bakare")
        self.assertIn(booking["id"], confirmed)

        # result not released yet
        self.say(phone, "0")
        self.say(phone, "2")
        self.assertIn("not ready yet", self.say(phone, "CONFIRM"))

        httpx.post(f"{API}/results/", json={"booking_id": booking["id"], "result_text": "Negative", "status": "RELEASED"}, headers=self.admin)
        self.say(phone, "0")
        self.say(phone, "2")
        found = self.say(phone, "CONFIRM")
        self.assertIn("Negative", found)
        self.assertIn("Tunde Bakare", found)

        # lookup by reference from another phone
        other = "+2348030002222"
        self.say(other, "hi")
        self.say(other, "2")
        self.assertIn("Negative", self.say(other, booking["id"]))

    def test_custom_test_name(self):
        phone = "+2348030003333"
        self.say(phone, "hi")
        self.say(phone, "1")
        self.say(phone, "1")
        self.say(phone, "C")
        self.assertIn("couldn't find", self.say(phone, "Brain MRI"))
        self.assertIn("Malaria Parasite", self.say(phone, "malaria"))

    def test_coordinator_referral(self):
        coords = httpx.get(f"{API}/coordinators/", headers=self.admin).json()
        code = next(c["referral_code"] for c in coords if c["user_id"] == self.coordinator["id"])
        phone = "+2348055555555"
        self.assertIn("Invalid coordinator code", self.say(phone, "REF NOT-A-CODE"))
        self.assertIn("Referral mode activated", self.say(phone, f"ref {code}"))
        OUTBOX.clear()
        reply = self.say(phone, "NAME: Ada Obi\nPHONE: 2348034512345\nTEST: Malaria\nBRANCH: Ilesa")
        self.assertIn("Referral registered", reply)
        self.assertIn("+2348034512345", reply)
        self.assertNotIn("++", reply)
        self.assertEqual(OUTBOX[0][0], "+2348034512345")
        self.assertIn("1 Main St, Ilesa", OUTBOX[0][1])

        referrals = httpx.get(f"{API}/referrals/", headers=self.admin).json()
        self.assertEqual([r["patient_name"] for r in referrals], ["Ada Obi"])
        self.assertEqual(referrals[0]["branch_name"], "Ilesa HQ")


if __name__ == "__main__":
    unittest.main()
