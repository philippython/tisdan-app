# Tisdan: Deployment & Launch Guide

This guide takes the three Tisdan apps from this repository to a live production launch. It assumes one Ubuntu 22.04/24.04 server and a domain you control. Commands are copy-paste ready; replace `example.com` with your domain.

---

## 1. How the pieces fit

```
 Patients / coordinators                         Clinic staff
   (WhatsApp)                                    (browser)
       │                                             │
       ▼                                             ▼
 Twilio WhatsApp ──POST /sms──▶ tisdan-bot      tisdan-portal (static React site)
       ▲                        :8001               │  https://admin.example.com
       │   /send (X-Bot-Key)      │  X-Bot-Key      │  Bearer JWT
       └──────────────────────────┼─────────────────┤
                                  ▼                 ▼
                             tisdan-backend (FastAPI) :8002 ──▶ SQLite / Postgres
                             https://api.example.com
                                  ▲
                                  └── Paystack webhook
```

| App | Folder | Local port | Public URL (example) |
|---|---|---|---|
| Backend API | `tisdan-backend/` | 8002 | `https://api.example.com` |
| WhatsApp bot | `tisdan-bot/` | 8001 | `https://bot.example.com` |
| Admin portal | `tisdan-portal/` | 5173 (dev) | `https://admin.example.com` |

**Trust between services.** The bot and backend share one secret, `BOT_API_KEY`:
- The bot sends it as `X-Bot-Key` when it reads the catalogue, creates customers and bookings, looks up results, and registers referrals.
- The backend sends it when it asks the bot to deliver a WhatsApp message through `/send`.

Staff use the portal with a normal email and password login, which issues a JWT. Each role only sees what it needs:

| Role | What they can do |
|---|---|
| ADMIN | Everything, including creating users |
| STAFF | Bookings, results, customers, tests, branches, schedules, payments, broadcasts |
| DOCTOR | Read bookings, results and patients |
| COORDINATOR | Their own referral code and their own referrals only |
| CLIENT | Can't use the portal. Clients use WhatsApp. |

---

## 2. Before launch: accounts and decisions

Complete these first, because some take days to approve.

1. **Server:** any VPS with 1 vCPU and 1–2 GB RAM, running Ubuntu, with ports 80 and 443 open.
2. **DNS:** create three `A` records pointing to the server: `api.`, `bot.` and `admin.`.
3. **Twilio WhatsApp sender.** The sandbox number (`+14155238886`) only works for phones that have joined the sandbox, so a real launch needs a production WhatsApp sender:
   - Register it in Twilio Console → Messaging → Senders → WhatsApp senders.
   - This requires a Meta Business account and business verification.
   - ⚠️ **The 24-hour rule.** WhatsApp only allows free-form messages within 24 hours of the patient's last message. Many of the backend's messages are sent later than that: results released days after booking, broadcasts, booking status changes and payment receipts.
   - For those messages to arrive in production, create **approved Content Templates** in Twilio, and switch those sends to the template API. See §10.
4. **Paystack (optional):** a live secret key (`sk_live_…`) from Dashboard → Settings → API Keys & Webhooks.
5. **Secrets:** generate two long random strings, one for `SECRET_KEY` and one for `BOT_API_KEY`:
   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(48))"
   ```

---

## 3. Server preparation

```bash
sudo apt update && sudo apt install -y python3 python3-venv python3-pip git nginx certbot python3-certbot-nginx sqlite3
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt install -y nodejs

sudo useradd --system --create-home --home-dir /opt/tisdan --shell /bin/bash tisdan
sudo -u tisdan git clone https://github.com/philippython/tisdan-app.git /opt/tisdan/app
sudo mkdir -p /var/lib/tisdan && sudo chown tisdan:tisdan /var/lib/tisdan   # database lives outside the repo
```

---

## 4. Backend (`tisdan-backend`)

```bash
cd /opt/tisdan/app/tisdan-backend
sudo -u tisdan python3 -m venv .venv
sudo -u tisdan .venv/bin/pip install -r requirements.txt
sudo -u tisdan cp .env.example .env && sudo -u tisdan nano .env
```

Production `.env`:

```ini
ENVIRONMENT=production
SECRET_KEY=<random string #1>
BOT_API_KEY=<random string #2>
DATABASE_URL=sqlite:////var/lib/tisdan/tisdan.db
FRONTEND_HOST=https://admin.example.com
TISDAN_BOT_URL=http://127.0.0.1:8001
PAYSTACK_SECRET_KEY=sk_live_xxx
```

With `ENVIRONMENT=production`, the API **refuses to start** if `SECRET_KEY` or `BOT_API_KEY` is missing. This is deliberate, so a misconfigured server fails loudly.

> **Postgres instead of SQLite?** Recommended once you have several busy branches. Run `pip install "psycopg[binary]"` and set `DATABASE_URL=postgresql+psycopg://user:pass@host:5432/tisdan`. Tables are created automatically on first start.

Create the first admin account. This is the only way to create users until an admin exists, because `POST /users/` requires an admin login.

```bash
sudo -u tisdan .venv/bin/python scripts/create_admin.py you@yourclinic.com "Your Name" 08012345678
```

The script prompts for the password. Running it again for the same email resets that user's password and makes them an admin.

Create the service at `/etc/systemd/system/tisdan-backend.service`:

```ini
[Unit]
Description=Tisdan backend API
After=network.target

[Service]
User=tisdan
WorkingDirectory=/opt/tisdan/app/tisdan-backend
ExecStart=/opt/tisdan/app/tisdan-backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8002 --workers 2 --proxy-headers --forwarded-allow-ips=127.0.0.1
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 5. WhatsApp bot (`tisdan-bot`)

```bash
cd /opt/tisdan/app/tisdan-bot
sudo -u tisdan python3 -m venv .venv
sudo -u tisdan .venv/bin/pip install -r requirements.txt
sudo -u tisdan cp .env.example .env && sudo -u tisdan nano .env
```

```ini
API_BASE=http://127.0.0.1:8002
BOT_API_KEY=<random string #2 — same as the backend>
TWILIO_ACCOUNT_SID=ACxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxx
TWILIO_WHATSAPP_FROM=whatsapp:+234XXXXXXXXXX
TWILIO_WEBHOOK_URL=https://bot.example.com/sms
```

`/etc/systemd/system/tisdan-bot.service`:

```ini
[Unit]
Description=Tisdan WhatsApp bot
After=network.target tisdan-backend.service

[Service]
User=tisdan
WorkingDirectory=/opt/tisdan/app/tisdan-bot
ExecStart=/opt/tisdan/app/tisdan-bot/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8001 --workers 1 --proxy-headers --forwarded-allow-ips=127.0.0.1
Restart=always

[Install]
WantedBy=multi-user.target
```

> ⚠️ Keep the bot at **`--workers 1`**. Conversation state (for example "this user is halfway through a booking") is held in memory. Multiple workers would lose track of conversations, and a restart resets conversations in progress.

Start both services:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now tisdan-backend tisdan-bot
curl -s localhost:8002/health && curl -s localhost:8001/health
```

---

## 6. Admin portal (`tisdan-portal`)

The API URL is compiled into the site at build time:

```bash
cd /opt/tisdan/app/tisdan-portal
echo "VITE_API_URL=https://api.example.com" | sudo -u tisdan tee .env
sudo -u tisdan npm ci && sudo -u tisdan npm run build      # outputs dist/
```

---

## 7. Nginx and HTTPS

Create `/etc/nginx/sites-available/tisdan`:

```nginx
server {
    server_name api.example.com;
    client_max_body_size 5m;
    location / {
        proxy_pass http://127.0.0.1:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    server_name bot.example.com;
    # Only Twilio's webhook needs to be public. /send stays internal.
    location = /sms {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    location = /health { proxy_pass http://127.0.0.1:8001; }
    location / { return 404; }
}

server {
    server_name admin.example.com;
    root /opt/tisdan/app/tisdan-portal/dist;
    location / { try_files $uri /index.html; }   # single-page app routing
}
```

```bash
sudo ln -s /etc/nginx/sites-available/tisdan /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d api.example.com -d bot.example.com -d admin.example.com
```

---

## 8. Connect the external services

- **Twilio:** Console → your WhatsApp sender → "A message comes in" → `https://bot.example.com/sms` (method **POST**). `TWILIO_WEBHOOK_URL` must be exactly this URL, because it is used to verify Twilio's signature.
- **Paystack:** Dashboard → Settings → API Keys & Webhooks → Webhook URL: `https://api.example.com/payments/paystack/webhook`. Paid transactions then flip to **COMPLETED** automatically and the payer receives a WhatsApp receipt. Staff can also mark cash payments COMPLETED on the Payments tab.

---

## 9. Launch day

### 9.1 Load real data (portal, as admin)

1. **Branches:** add each branch with a short code (for example `IL-01`).
2. **Schedules:** add one row per opening day for each branch. The WhatsApp bot offers exactly these days. If a branch has none, it falls back to Mon–Sat 07:00–19:00 and Sun 08:00–14:00.
3. **Diagnostic Tests:** name, description and price. Leave Branch blank for tests offered everywhere.
4. **Users:** create STAFF, DOCTOR and COORDINATOR accounts. Staff, doctor and coordinator records are created automatically. Each coordinator gets a referral code such as `REF-1A2B3C4D`, shown on the Coordinators tab.

### 9.2 End-to-end smoke test (about 15 minutes)

| # | Do this | Expect |
|---|---|---|
| 1 | Log in to the portal as admin | Dashboard loads with no errors |
| 2 | WhatsApp "hi" to the clinic number | Welcome menu |
| 3 | Reply `1`, then pick a branch, test and day, send your name, then `SKIP` and `1` | "Booking Confirmed" with a reference. Booking appears in the portal's **Bookings** tab with your name and phone. Staff and admins get a "New Booking" WhatsApp |
| 4 | In the portal, edit the booking and set Status = CONFIRMED | Patient receives "Your booking has been confirmed" |
| 5 | **Results** → New Result for that booking, Status = *Pending* | No WhatsApp sent. Dashboard shows it under Pending Results |
| 6 | WhatsApp `0`, `2`, `CONFIRM` | "Your result is not ready yet" |
| 7 | Edit the result and set Status = *Released* | Patient receives the result on WhatsApp |
| 8 | WhatsApp `0`, `2`, `CONFIRM` | The result is shown |
| 9 | From a coordinator's phone: `REF <their code>`, then the NAME/PHONE/TEST/BRANCH block | "Referral registered". Patient gets an invitation. Referral shows on **Referrals** (admin) and on the coordinator's own page |
| 10 | Log in to the portal as that coordinator | Sees only their own code and referrals |
| 11 | Create a booking for a registered user in the portal and accept "send a payment link" | Paystack page opens. After paying, **Payments** shows COMPLETED |
| 12 | **Broadcast** → General | Every customer receives it |

---

## 10. Operations

**Logs**
```bash
journalctl -u tisdan-backend -f
journalctl -u tisdan-bot -f
```
Every failed WhatsApp send is logged, with the reason.

**Backups.** Nightly copy of the SQLite database, keeping 14 days:
```bash
sudo -u tisdan crontab -e
# add:
0 2 * * * sqlite3 /var/lib/tisdan/tisdan.db ".backup /var/lib/tisdan/backup-$(date +\%F).db" && find /var/lib/tisdan -name 'backup-*.db' -mtime +14 -delete
```
Copy backups off the server as well (for example to S3 or Google Drive).

**Deploying updates**
```bash
cd /opt/tisdan/app && sudo -u tisdan git pull
sudo -u tisdan tisdan-backend/.venv/bin/pip install -r tisdan-backend/requirements.txt
sudo -u tisdan tisdan-bot/.venv/bin/pip install -r tisdan-bot/requirements.txt
(cd tisdan-portal && sudo -u tisdan npm ci && sudo -u tisdan npm run build)
sudo systemctl restart tisdan-backend tisdan-bot
```

**Tests.** Run these before every deploy:
```bash
cd tisdan-backend && .venv/bin/python -m unittest discover -s tests      # API tests
cd ../tisdan-bot && BACKEND_PYTHON=../tisdan-backend/.venv/bin/python \
  .venv/bin/python -m unittest discover -s tests                          # bot ↔ backend conversations
```

**Schema changes.** New *tables* are created automatically at startup. New *columns* on existing tables are not. Add an Alembic migration in `tisdan-backend/alembic/versions/` for those.

---

## 11. Running everything locally

```bash
# terminal 1: backend
cd tisdan-backend && cp .env.example .env    # the defaults work locally
python -m venv .venv && .venv/Scripts/pip install -r requirements.txt   # Linux/macOS: .venv/bin/
python scripts/create_admin.py admin@example.com "Admin" 08000000000
uvicorn app.main:app --port 8002 --reload

# terminal 2: bot (without Twilio credentials it replies but can't push messages)
cd tisdan-bot && cp .env.example .env && pip install -r requirements.txt
uvicorn main:app --port 8001 --reload

# terminal 3: portal
cd tisdan-portal && cp .env.example .env && npm install && npm run dev   # http://localhost:5173
```

To chat with the bot locally, expose it with `ngrok http 8001` and point the Twilio sandbox webhook at `https://<id>.ngrok.app/sms`.

---

## 12. Known limitations and next steps

- **WhatsApp templates (needed at launch):** see §2.3. Results, status updates, receipts and broadcasts sent more than 24 hours after a patient's last message need approved templates. Until they exist, those messages only reach patients who messaged recently.
- **Bot conversations are in memory:** a restart resets conversations that are in progress. Move them to Redis or the database if this becomes a problem.
- **`tisdan-backend/tisdan.db` is still tracked in git.** Production uses `DATABASE_URL` outside the repo (§4), so this doesn't affect a live server. Once you've copied any data you need, run `git rm --cached tisdan-backend/tisdan.db` so development data never ships.
