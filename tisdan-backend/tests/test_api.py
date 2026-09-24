"""End-to-end API tests against a throwaway SQLite database.

Run from tisdan-backend/:
    python -m unittest discover -s tests -v
"""
import hashlib
import hmac
import json
import os
import sys
import tempfile
import unittest

_tmpdir = tempfile.mkdtemp()
os.environ.update(
    ENVIRONMENT="local",
    DATABASE_URL=f"sqlite:///{os.path.join(_tmpdir, 'test.db')}",
    BOT_API_KEY="test-bot-key",
    PAYSTACK_SECRET_KEY="sk_test_dummy",
    SECRET_KEY="test-secret",
)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient  # noqa: E402

import app.utils.bot_notify as bot_notify  # noqa: E402
from app.main import app  # noqa: E402
from scripts.create_admin import create_admin  # noqa: E402

SENT = []  # (to, body) of every WhatsApp message the backend tried to send


class _SyncExecutor:
    def submit(self, fn, *args):
        fn(*args)


bot_notify._executor = _SyncExecutor()
bot_notify.send_whatsapp_via_bot = lambda to, body: SENT.append((to, body)) or True

BOT = {"X-Bot-Key": "test-bot-key"}


class ApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.client.__enter__()  # run startup (creates tables)
        create_admin("admin@example.com", "Ada Admin", "08011111111", "adminpass123")
        cls.admin = cls.auth("admin@example.com", "adminpass123")

        c = cls.client
        cls.branch = c.post("/branches/", json={"name": "Ilesa HQ", "address": "1 Main St", "branch_code": "IL-01"}, headers=cls.admin).json()
        cls.test = c.post("/tests/", json={"name": "Malaria", "description": "MP", "price": 1500, "branch_id": cls.branch["id"]}, headers=cls.admin).json()

    @classmethod
    def tearDownClass(cls):
        cls.client.__exit__(None, None, None)

    @classmethod
    def auth(cls, email, password):
        r = cls.client.post("/auth/login", data={"username": email, "password": password})
        assert r.status_code == 200, r.text
        return {"Authorization": f"Bearer {r.json()['access_token']}"}

    def make_user(self, role, email, phone="08022222222", password="userpass123"):
        r = self.client.post("/users/", json={
            "email": email, "password": password, "full_name": f"{role.title()} Person",
            "phone_number": phone, "role": role,
        }, headers=self.admin)
        self.assertEqual(r.status_code, 201, r.text)
        return r.json()

    def bot_booking(self, phone, name="Bola Customer"):
        customer = self.client.post("/bot/customers/", json={"full_name": name, "phone_number": phone}, headers=BOT).json()
        r = self.client.post("/bookings/", json={
            "customer_id": customer["id"], "test_id": self.test["id"],
            "branch_id": self.branch["id"], "booking_date": "2030-01-07T07:00:00",
        }, headers=BOT)
        self.assertEqual(r.status_code, 201, r.text)
        return customer, r.json()

    # ── security ──────────────────────────────────────────────
    def test_health(self):
        self.assertEqual(self.client.get("/health").json(), {"status": "ok"})

    def test_sensitive_endpoints_need_auth(self):
        c = self.client
        self.assertEqual(c.post("/users/", json={"email": "x@y.z", "password": "p", "full_name": "x", "phone_number": "1", "role": "ADMIN"}).status_code, 401)
        for path in ("/patients/", "/results/", "/customers/", "/payments/", "/referrals/", "/doctors/"):
            self.assertEqual(c.get(path).status_code, 401, path)
        self.assertEqual(c.get("/bot/results", params={"phone": "1"}, headers={"X-Bot-Key": "wrong"}).status_code, 401)
        # public catalogue stays public for the bot and website
        for path in ("/branches/", "/tests/", "/branch-schedules/"):
            self.assertEqual(c.get(path).status_code, 200, path)

    def test_staff_cannot_create_users(self):
        self.make_user("STAFF", "staff1@example.com", password="staffpass123")
        staff = self.auth("staff1@example.com", "staffpass123")
        r = self.client.post("/users/", json={"email": "evil@x.io", "password": "p", "full_name": "E", "phone_number": "1", "role": "ADMIN"}, headers=staff)
        self.assertEqual(r.status_code, 403)

    # ── updates ───────────────────────────────────────────────
    def test_partial_update_and_clearing_optional_field(self):
        c = self.client
        t = c.post("/tests/", json={"name": "FBC", "description": "Full blood", "price": 4500, "branch_id": self.branch["id"]}, headers=self.admin).json()
        # clear branch (-> all branches) and send a null for a required field
        r = c.put(f"/tests/{t['id']}", json={"branch_id": None, "name": None, "price": "5000"}, headers=self.admin)
        self.assertEqual(r.status_code, 200, r.text)
        self.assertIsNone(r.json()["branch_id"])
        self.assertEqual(r.json()["name"], "FBC")
        self.assertEqual(r.json()["price"], 5000)

    def test_branch_schedules_list_and_edit(self):
        c = self.client
        for day in ("TUESDAY", "MONDAY"):
            r = c.post("/branch-schedules/", json={"branch_id": self.branch["id"], "day": day, "opening_time": "08:00", "closing_time": "17:00"}, headers=self.admin)
            self.assertEqual(r.status_code, 201, r.text)
        rows = c.get("/branch-schedules/").json()
        self.assertEqual([r["day"] for r in rows][:2], ["MONDAY", "TUESDAY"])
        self.assertEqual(rows[0]["branch_name"], "Ilesa HQ")
        r = c.put(f"/branch-schedules/{rows[0]['id']}", json=dict(rows[0], closing_time="18:30:00"), headers=self.admin)
        self.assertEqual((r.status_code, r.json()["closing_time"]), (200, "18:30:00"), r.text)

    def test_user_edit_without_password_keeps_login(self):
        u = self.make_user("CLIENT", "client1@example.com", password="clientpass1")
        row = dict(u, password="", full_name="Renamed Client")  # what the portal sends
        r = self.client.put(f"/users/{u['id']}", json=row, headers=self.admin)
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.json()["full_name"], "Renamed Client")
        self.auth("client1@example.com", "clientpass1")

    def test_role_change_creates_role_record(self):
        u = self.make_user("CLIENT", "tobecoord@example.com")
        self.client.put(f"/users/{u['id']}", json={"role": "COORDINATOR"}, headers=self.admin)
        coords = self.client.get("/coordinators/", headers=self.admin).json()
        self.assertIn(u["id"], [c["user_id"] for c in coords])

    # ── bookings & results ───────────────────────────────────
    def test_booking_status_update_notifies_patient(self):
        _, booking = self.bot_booking("08030000001")
        self.assertEqual(booking["patient_name"], "Bola Customer")
        self.assertEqual(booking["test_name"], "Malaria")
        SENT.clear()
        r = self.client.put(f"/bookings/{booking['id']}", json={"status": "CONFIRMED"}, headers=self.admin)
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.json()["status"], "CONFIRMED")
        self.assertIn("+2348030000001", [to for to, _ in SENT])

    def test_result_release_flow_and_bot_lookup(self):
        c = self.client
        _, booking = self.bot_booking("08030000002", name="Chidi Result")
        SENT.clear()
        res = c.post("/results/", json={"booking_id": booking["id"], "result_text": "Negative", "status": "PENDING"}, headers=self.admin).json()
        self.assertEqual(SENT, [], "pending results must not be sent to the patient")
        self.assertEqual(res["patient_name"], "Chidi Result")

        lookup = c.get("/bot/results", params={"phone": "+2348030000002"}, headers=BOT).json()
        self.assertEqual((lookup["results"], lookup["pending"]), ([], 1))

        c.put(f"/results/{res['id']}", json={"status": "RELEASED"}, headers=self.admin)
        self.assertEqual([to for to, _ in SENT], ["+2348030000002"])

        for params in ({"phone": "2348030000002"}, {"reference": booking["id"]}, {"reference": res["id"]}):
            lookup = c.get("/bot/results", params=params, headers=BOT).json()
            self.assertEqual(len(lookup["results"]), 1, params)
            self.assertEqual(lookup["results"][0]["result_text"], "Negative")

        found = c.get("/results/by-customer-name/", params={"name": "chidi"}, headers=self.admin)
        self.assertEqual(found.status_code, 200, found.text)
        self.assertEqual(len(found.json()), 1)

    def test_deleting_referenced_branch_is_refused(self):
        self.bot_booking("08030000003")
        r = self.client.delete(f"/branches/{self.branch['id']}", headers=self.admin)
        self.assertEqual(r.status_code, 409, r.text)

    # ── coordinators & referrals ─────────────────────────────
    def test_referrals_are_scoped_to_their_coordinator(self):
        c = self.client
        self.make_user("COORDINATOR", "coord1@example.com", password="coordpass1")
        self.make_user("COORDINATOR", "coord2@example.com", password="coordpass2")
        coord1 = self.auth("coord1@example.com", "coordpass1")
        coord2 = self.auth("coord2@example.com", "coordpass2")

        mine = c.get("/coordinators/", headers=coord1).json()
        self.assertEqual(len(mine), 1)
        code = mine[0]["referral_code"]

        self.assertEqual(c.get(f"/bot/coordinators/{code.lower()}", headers=BOT).status_code, 200)
        self.assertEqual(c.get("/bot/coordinators/NOPE-123", headers=BOT).status_code, 404)

        r = c.post("/referrals/", json={"coordinator_code": code, "patient_name": "Pat", "patient_phone": "+2348099999999", "test_name": "Malaria", "branch_name": "Ilesa HQ"}, headers=BOT)
        self.assertEqual(r.status_code, 201, r.text)

        self.assertEqual(len(c.get("/referrals/", headers=coord1).json()), 1)
        self.assertEqual(len(c.get("/referrals/", headers=coord2).json()), 0)
        self.assertEqual(c.get(f"/referrals/{r.json()['id']}", headers=coord2).status_code, 404)
        self.assertEqual(c.get("/coordinators/", headers=coord1).json()[0]["referral_count"], 1)

        upd = c.put(f"/referrals/{r.json()['id']}", json={"status": "completed"}, headers=self.admin)
        self.assertEqual(upd.json()["status"], "completed")

    # ── payments ─────────────────────────────────────────────
    def test_paystack_webhook_marks_payment_completed(self):
        c = self.client
        payer = self.make_user("CLIENT", "payer@example.com", phone="08077777777")
        p = c.post("/payments/", json={"amount": 1500, "payer_id": payer["id"], "payment_for": "TEST", "reference": "TSDN-TEST1"}, headers=self.admin).json()
        self.assertEqual((p["status"], p["currency"], p["payer_name"]), ("PENDING", "NGN", "Client Person"))

        event = json.dumps({"event": "charge.success", "data": {"reference": "TSDN-TEST1", "status": "success"}}).encode()
        self.assertEqual(c.post("/payments/paystack/webhook", content=event, headers={"x-paystack-signature": "bad"}).status_code, 401)

        sig = hmac.new(b"sk_test_dummy", event, hashlib.sha512).hexdigest()
        SENT.clear()
        r = c.post("/payments/paystack/webhook", content=event, headers={"x-paystack-signature": sig})
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(c.get(f"/payments/{p['id']}", headers=self.admin).json()["status"], "COMPLETED")
        self.assertIn("+2348077777777", [to for to, _ in SENT])


if __name__ == "__main__":
    unittest.main()
