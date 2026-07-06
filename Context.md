# HSC Academic Management System — Project Context

> **Institution:** Moinuddin Adarsha Mohila College, Sylhet, Bangladesh  
> **Purpose:** Full-stack web application for managing HSC (Higher Secondary Certificate) students, teachers, marks, and academic results.

---

## 1. Project Overview

This is a **Python Flask** monolith that serves both a REST API and all HTML pages from the same process. The system manages the complete academic lifecycle of HSC students across **Class-XI** and **Class-XII**, covering three academic groups: **Science**, **Humanities**, and **Business**.

Key capabilities:
- Student enrollment, profile management, and bulk import
- Marks entry per subject, per exam, per student (with CQ / MCQ / Practical components)
- Automatic GPA and grade calculation following Bangladesh HSC rules
- Result cards, admit cards, and tabulation sheets (printable)
- Teacher management
- Class promotion workflow (Class-XI → Class-XII)
- Graduate archival
- A public **Student Self-Service Portal** (no login required)
- A public **Result Summary** page (accessible via QR code)

---

## 2. Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| ORM | Flask-SQLAlchemy |
| Database | PostgreSQL (primary) / SQLite (local fallback) |
| Auth | Server-side Flask sessions (cookie-based) |
| CORS | flask-cors |
| Excel import | openpyxl |
| WSGI server | Gunicorn (for deployment) |
| Environment | python-dotenv |
| Frontend | Vanilla HTML + CSS + JavaScript (no framework) |
| Font | Kalpurush (Bangla font, injected server-side at runtime) |

---

## 3. File & Directory Structure

```
1234/
├── app.py                        # Main Flask application (2770 lines)
├── models.py                     # SQLAlchemy ORM models
├── db_init.py                    # DB initialisation & JSON migration tool
├── requirements.txt              # Python dependencies
├── Procfile / Procfile.txt       # Gunicorn entry for Render/Heroku
├── .env                          # Active secrets (gitignored)
├── .env.example                  # Template for environment variables
├── .gitignore
├── hsc_academy.db                # SQLite fallback DB (local dev)
├── students_dump.json            # JSON snapshot of student data
│
├── HTML Pages (served by Flask)
│   ├── index.html                # Main dashboard/home (auth-gated)
│   ├── login.html                # Login page
│   ├── dashboard.html            # Dashboard stats view
│   ├── student.html              # Single student detail view
│   ├── student-list.html         # Student list and search
│   ├── student-portal.html       # Public student self-service portal
│   ├── marks-entry.html          # Subject-level batch marks entry
│   ├── marks-input.html          # Per-student marks input form
│   ├── Teachers.html             # Teacher management page
│   ├── Result-card.html          # Printable result card generator
│   ├── Admit-card.html           # Printable admit card generator
│   ├── analytics.html            # Analytics dashboard
│   ├── result_analytics.html     # Tabulation sheet generator
│   ├── result_summery.html       # Public result summary (QR code target)
│   ├── std_result_view.html      # Student result view
│   ├── bulk-photo.html           # Bulk photo upload page
│   └── database.html             # Raw database viewer
│
├── static/                       # Static assets (CSS, JS, images)
├── photos/                       # Uploaded student photo files
│
├── Utility / Migration Scripts
│   ├── migrate_sqlite_to_postgres.py
│   ├── MIGRATION_optional_subject.py
│   ├── student_import_template.py
│   ├── render_init.py
│   ├── check_students.py
│   ├── check_names.py
│   ├── check_extra_names.py
│   ├── check_optional.py
│   ├── check_humanities_opt.py
│   ├── fix_social_work_code.py
│   ├── insert_ict_marks.py
│   ├── insert_ict_humanities_direct.py
│   ├── search_detailed.py
│   ├── verify_marks.py
│   └── submit_*.py               # One-off mark submission scripts
│
└── .agents/skills/               # Antigravity agent skills
```

---

## 4. Database Models (`models.py`)

### `Student` — table: `students`
Represents an **active** enrolled student.

| Column | Type | Notes |
|---|---|---|
| `id` | String(50) PK | UUID hex (16 chars) |
| `name` | String(255) | Required |
| `roll` | String(50) | Required, non-globally-unique |
| `reg` | String(50) | Registration number |
| `cls` | String(50) | `"Class-XI"` or `"Class-XII"` |
| `group` | String(50) | `"Science"`, `"Humanities"`, or `"Business"` |
| `section` | String(50) | |
| `father` | String(255) | |
| `mother` | String(255) | |
| `dob` | String(50) | Date of birth |
| `phone` | String(20) | |
| `religion` | String(50) | |
| `year` | String(10) | Academic year, e.g. `"2024"` |
| `session` | String(50) | Session, e.g. `"2024-2025"` |
| `photo` | Text | Relative URL: `/photos/<id>.jpg` |
| `photo_base64` | Text (deferred) | Full base64 data URL backup |
| `optional_subjects` | String(50) | Chosen optional codes e.g. `"178/179"` |
| `student_submitted` | Boolean | True once self-submitted via portal |
| `created_at` | DateTime | Auto-set |

**Relationship:** `marks` → cascade delete on student removal.

---

### `Mark` — table: `marks`
One row per **student × exam_type × subject_code**.

| Column | Type | Notes |
|---|---|---|
| `id` | Integer PK | Auto-increment |
| `student_id` | String(50) FK | → `students.id` |
| `exam_type` | String(100) | e.g. `"First Terminal"`, `"Annual"` |
| `year` | String(10) | e.g. `"2024-2025"` |
| `subject_code` | String(50) | e.g. `"101"` |
| `cq` | Integer | Creative Question marks |
| `mcq` | Integer | Multiple Choice marks |
| `prac` | Integer | Practical marks |
| `absent` | Boolean | True if student was absent |
| `selected_optional` | String(50) | Legacy optional selector (e.g. `"scienceBio"`) |
| `created_at` / `updated_at` | DateTime | |

---

### `Teacher` — table: `teachers`
Faculty member information.

| Column | Type | Notes |
|---|---|---|
| `id` | String(50) PK | `"T" + timestamp_ms` |
| `name`, `email`, `phone` | | Required |
| `subject` | String(100) | |
| `classes` | String(255) | Comma-separated |
| `qualification` | String(255) | |
| `experience` | Integer | Years |
| `empid`, `joining`, `address` | | Optional |

---

### `Setting` — table: `settings`
Key-value application settings (college name, EIIN, address, phone, etc.).

---

### `Archive` — table: `archive`
Graduated students moved from `students` after Class-XII completion. Mirrors all `Student` fields plus `total_marks`, `gpa`, and `archived_at`.

---

### `PromotionLog` — table: `promotion_logs`
Audit trail created whenever students are promoted from Class-XI → Class-XII. Records old roll, new roll, GPA, and total marks at the time of promotion.

---

## 5. Authentication & Roles

Two roles, controlled via Flask server-side sessions:

| Role | Credentials | Access |
|---|---|---|
| `admin` | Any password matching `ADMIN_PW` | Full access to all endpoints |
| `marks_entry` | `MARKS_UID` + `MARKS_PW` | Authenticated access to marks-related endpoints |

- **Public** (no auth): `/login`, `/student-portal`, `/result_summery.html`, `/std_result_view.html`, and their associated API endpoints.
- **Auth decorator** `@require_auth` — 401 if not authenticated.
- **Admin decorator** `@require_admin` — 403 if role is not `admin`.

Credentials are loaded from environment variables (`.env` file):
```
ADMIN_PW=...
MARKS_UID=...
MARKS_PW=...
SECRET_KEY=...
```

---

## 6. API Endpoints Reference

### Auth
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/login` | Public | Login; returns role |
| POST | `/api/logout` | Public | Clear session |
| GET | `/api/auth-status` | Public | Check session state |
| GET | `/api/health` | Public | DB health check |

### Students
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/students` | Auth | List/filter students (cls, group, session, q) |
| POST | `/api/students` | Auth | Add single student |
| GET | `/api/students/<sid>` | Auth | Get student by ID |
| PUT | `/api/students/<sid>` | Admin | Update student |
| DELETE | `/api/students/<sid>` | Admin | Delete student (cascade marks) |
| GET | `/api/students/<sid>/subjects` | Auth | Resolved subject list for student |
| POST | `/api/students/import/preview` | Auth | Preview Excel import |
| POST | `/api/students/import` | Auth | Bulk import from JSON |
| POST | `/api/students/bulk-import` | Auth | Alias for bulk import |
| POST | `/api/students/bulk-photo` | Auth | Batch photo upload by roll number |

### Marks
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/marks` | Auth | All marks (hierarchical dict) |
| DELETE | `/api/marks` | Admin | Clear all marks |
| GET | `/api/marks/<sid>` | Auth | Marks for one student |
| POST | `/api/marks/<sid>` | Auth | Save all marks for a student + exam |
| GET/POST | `/api/marks/batch` | Auth | Batch marks for multiple student IDs |
| POST | `/api/marks/batch-subject` | Auth | Save one subject's marks for many students |
| POST | `/api/marks/import` | Auth | Import marks from Excel rows |
| POST | `/api/marks/bulk-import` | Auth | Bulk import marks (frontend parser format) |
| DELETE | `/api/marks/<sid>/<exam_type>` | Auth | Delete marks for student + exam |

### Teachers
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/teachers` | Auth | List/search teachers |
| POST | `/api/teachers` | Admin | Add teacher |
| PUT | `/api/teachers/<tid>` | Admin | Update teacher |
| DELETE | `/api/teachers/<tid>` | Admin | Delete teacher |

### Results & Analytics
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/stats` | Auth | Dashboard statistics |
| GET | `/api/export/csv` | Auth | Export results as CSV |
| GET | `/api/tabulation-sheet/filters` | Auth | Filter options for tabulation sheet |
| GET | `/api/tabulation-sheet` | Auth | Tabulation sheet data |
| GET | `/api/analyze-promotion` | Auth | List Class-XI students eligible for promotion |
| POST | `/api/execute-promotion` | Auth | Promote Class-XI → Class-XII |
| GET | `/api/analyze-archive-candidates` | Auth | List passable Class-XII students |
| POST | `/api/archive-graduates` | Auth | Move passing Class-XII to archive |
| GET | `/api/archive` | Auth | List archived graduates |
| POST | `/api/generate-rolls` | Auth | Generate roll assignments by GPA rank |
| GET | `/api/detain-list` | Auth | List failed Class-XI students |
| POST | `/api/re-enroll/<sid>` | Auth | Re-enroll a detained student |
| GET | `/api/generate-certificate/<sid>` | Auth | Student TC/certificate data |

### Settings
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/settings` | Auth | All settings as key-value dict |
| POST | `/api/settings` | Auth | Upsert settings |

### Public (No Auth)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/student-portal/lookup` | Find student by cls+group+session+roll |
| POST | `/api/student-portal/submit/<sid>` | Student uploads photo + optional subject |
| GET | `/api/public/result-summary` | Full result for one student (QR page) |
| GET | `/api/public/result` | Search result by cls+group+roll |

---

## 7. Subject & Grading System

### Subject List
Subjects are defined in the `SUBJECT_LIST` dict in `app.py`. Each subject has:
- `name` — display name
- `code` — Bangladesh board subject code (string)
- `hasPrac` — whether it has a practical component
- `cqMax` — max CQ marks (50, 70, or 100)
- `mcqMax` — max MCQ marks (0, 25, or 30)
- `optional` — whether it's an optional subject

**Class-XI** shows only **1st Paper** subjects; **Class-XII** shows only **2nd Paper** subjects.

**Sociology (116)** and **Islamic History & Culture (267)** are dynamically renamed to append `1st Paper` / `2nd Paper` based on class.

### Subject Codes by Group

**Science** (13 subjects): Bangla 1&2, English 1&2, ICT, Physics 1&2, Chemistry 1&2, + Optional: Biology 1&2 OR Higher Math 1&2

**Humanities** (17 subjects): Bangla 1&2, English 1&2, ICT, Civics & Good Governance 1&2, Economics 1&2, Sociology, Social Work 1&2, Islamic History & Culture + Optional: Logic 1&2 OR Home Science 1&2

**Business** (15 subjects): Bangla 1&2, English 1&2, ICT, Accounting 1&2, Business Org. & Mgmt 1&2, Finance Banking & Insurance 1&2 + Optional: Economics 1&2 OR Home Science 1&2

### Grading Scale (Bangladesh HSC)

| Total Marks | Grade | GPA |
|---|---|---|
| 80–100 | A+ | 5.0 |
| 70–79 | A | 4.0 |
| 60–69 | A- | 3.5 |
| 50–59 | B | 3.0 |
| 40–49 | C | 2.0 |
| 33–39 | D | 1.0 |
| < 33 | F | 0.0 |

### Pass Mark Rules (component-level)

| Subject type | CQ pass | MCQ pass | Practical pass |
|---|---|---|---|
| CQ-only (English 1st/2nd, 100 marks) | 33/100 | N/A | N/A |
| Theory only (CQ 70 + MCQ 30) | 23/70 | 10/30 | N/A |
| With practical (CQ 50 + MCQ 25 + Prac 25) | 17/50 | 8/25 | 8/25 |

A student **fails a subject** if they fail any single component, regardless of total. Compulsory subject failure means overall GPA = 0. Optional subject failure does NOT cause overall failure (4th subject rule: only GPA > 2.0 contributes to overall GPA).

---

## 8. Photo Management

- Photos are stored as **base64 data URLs** in `photo_base64` column (deferred load) for persistence across container restarts.
- A file copy is also saved to `photos/<student_id>.ext` for fast serving.
- On startup, a migration runs to move inline `data:` URLs from `photo` column → `photo_base64`, then replaces with a `/photos/...` URL.
- The `/photos/<filename>` route performs lazy restore from DB if the file is missing on disk (handles ephemeral hosting).

---

## 9. HTML Page Serving

All HTML files are served by Flask's `_serve_html()` helper which:
1. Reads the HTML file from disk.
2. **Injects the Kalpurush Bangla font** (`fonts.maateen.me`) into `<head>`.
3. For authenticated pages, injects `window.USE_API = true; window.API_BASE = "";` for frontend API routing.

Most HTML pages require authentication (redirected to `/login` if not authenticated).

**Public pages** (no login required):
- `/login` → `login.html`
- `/student-portal` → `student-portal.html`
- `/result_summery.html`
- `/std_result_view.html`

---

## 10. Environment Variables

Defined in `.env` (never committed), documented in `.env.example`:

| Variable | Purpose | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | SQLite fallback |
| `SECRET_KEY` | Flask session secret | Random (regenerated each restart) |
| `ADMIN_PW` | Admin password | `admin1234` |
| `ADMIN_UID` | Admin username (not used for login check) | `admin` |
| `MARKS_UID` | Marks entry username | `teacher` |
| `MARKS_PW` | Marks entry password | `teacher123` |

---

## 11. Deployment

- **Procfile**: `web: gunicorn app:app` — targets Render / Heroku.
- **Database**: PostgreSQL on Render (`dpg-...` host).
- **Auto-migrations**: On startup, `app.py` runs `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` for any columns that were added after initial deployment — safe to re-run.
- The global unique constraint on `students.roll` is dropped on first migration (rolls are only unique per class+group+session, not globally).

---

## 12. Utility / One-off Scripts

These scripts in the project root were used for data migration, seeding, and verification during development. They are **not part of the running application**.

| Script | Purpose |
|---|---|
| `migrate_sqlite_to_postgres.py` | Migrate data from SQLite to PostgreSQL |
| `MIGRATION_optional_subject.py` | Backfill optional_subjects field |
| `student_import_template.py` | Generate Excel import template |
| `render_init.py` | Render.com startup init script |
| `check_students.py` | Verify student data integrity |
| `check_names.py` / `check_extra_names.py` | Name validation utilities |
| `check_optional.py` / `check_humanities_opt.py` | Optional subject checks |
| `fix_social_work_code.py` | Fix incorrect Social Work subject codes |
| `insert_ict_marks.py` / `insert_ict_humanities_direct.py` | Seed ICT marks |
| `submit_*.py` | One-off mark submission scripts for specific subjects |
| `verify_marks.py` | Verify mark data consistency |
| `search_detailed.py` | Detailed student search utility |

---

## 13. Key Business Logic

### GPA Calculation
- GPA is computed only over **compulsory** subjects in which the student appeared.
- If a student has **any absent compulsory subject** or **any F grade**, GPA = 0.
- Optional subject (4th subject rule): only the portion of GPA > 2.0 is added to the sum.
- Final GPA = `min(sum(gpa_points) / subject_count, 5.0)`.

### Merit Position
- Merit is calculated by sorting all students in the same class + group by GPA (desc), then total marks (desc).
- Used in Result Cards and the public result summary.

### Class Promotion Flow
1. Admin reviews `GET /api/analyze-promotion` — shows all Class-XI students with Pass/Fail.
2. Admin calls `POST /api/execute-promotion` with a list of student IDs.
3. Students are sorted by GPA/marks and assigned sequential new roll numbers.
4. Their `cls` is updated to `"Class-XII"` and a `PromotionLog` entry is created.

### Student Self-Service Portal
- Public-facing (no auth).
- Students find themselves by class + group + session + roll.
- Can upload a photo and select their optional subject.
- Submission is one-time only (`student_submitted` flag prevents re-submission).
- Admin can override via the admin PUT endpoint.

---

## 14. Known Design Notes & Quirks

- **Roll uniqueness**: Roll numbers are *not* globally unique — they're unique within a class+group+session context. The global unique constraint was dropped.
- **Legacy optional selector**: Old mark entries used string keys like `"scienceBio"`, `"scienceMath"` etc. The newer system stores subject code pairs like `"178/179"` in `optional_subjects`. A `LEGACY_MAP` in `app.py` bridges the two formats.
- **Sociology (116) & Islamic History (267)**: These are full-year subjects that appear as only one row, dynamically renamed per class (1st Paper for Class-XI, 2nd Paper for Class-XII).
- **Kalpurush font**: Injected at the server level into all HTML responses to ensure consistent Bangla text rendering.
- **`photo_base64` deferred**: This large column is deferred (not loaded by default) to avoid massive data in list queries. It is loaded explicitly when needed.
- **English papers**: CQ-only (100 marks, no MCQ), which changes pass-mark calculation.

---

*Generated: 2026-07-05*
