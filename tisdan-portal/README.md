# Tisdan Portal — Frontend

React + Vite admin portal for the Tisdan Diagnostic Centre backend.

## Quick start

```bash
# 1. Install dependencies
npm install

# 2. Set your backend URL
cp .env.example .env
# Edit .env → VITE_API_URL=http://your-backend:8000

# 3. Run dev server
npm run dev
# Opens at http://localhost:5173
```

## Build for production

```bash
npm run build
# Output in /dist — serve with any static host
```

## Roles & access

| Role        | Access                                              |
|-------------|-----------------------------------------------------|
| ADMIN       | Everything — all pages, full CRUD                   |
| STAFF       | Bookings, Results, Patients, Customers, Tests, Broadcast |
| DOCTOR      | Dashboard, Bookings, Results, Patients              |
| COORDINATOR | My Referrals page only                              |

## Project structure

```
src/
  App.jsx              # Root router
  main.jsx             # Entry point
  index.css            # Global styles
  lib/
    api.js             # Fetch helpers + token management
    theme.js           # Colors, formatters
  hooks/
    useAuth.jsx        # Auth context + login/logout
    useApi.js          # API request hook
    useToast.js        # Toast notifications
  components/
    ui.jsx             # Badge, Toast, Modal, Table, Card, etc.
    CrudPage.jsx       # Reusable CRUD table + form modal
    Sidebar.jsx        # Navigation sidebar
    Layout.jsx         # Page shell (sidebar + topbar + outlet)
  pages/
    Login.jsx
    Dashboard.jsx
    Bookings.jsx
    Results.jsx
    Coordinators.jsx
    Broadcast.jsx
    OtherPages.jsx     # Staff, Patients, Customers, Tests, Branches, Payments, Users, Doctors
```

## Backend CORS

Make sure your FastAPI app allows requests from `http://localhost:5173`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
