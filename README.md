# Web-Scrape Case Study

## ✨ Project Overview

This project is a comprehensive web scraping case study targeting The Dyrt's interactive map interface to extract campground data across the United States. The scraper interacts with the backend API used by the map interface (exposed via network activity), parses relevant data, validates it using `pydantic`, and persists it into a PostgreSQL database via a Dockerized environment.

---

## 🔢 Objectives

The aim is to:

* Scrape campground data from the US region using The Dyrt's hidden API endpoint.
* Normalize and validate the data against a defined schema.
* Store the validated data into PostgreSQL.
* Schedule periodic scrapes using cron.
* Implement update functionality for existing records.
* Ensure error handling and retries.

---

## 📅 Requirements (As per Original `README.md`)

| Requirement                                                               | Points |
| ------------------------------------------------------------------------- | ------ |
| Connect Docker container to PostgreSQL and create tables                  | 15     |
| Scrape all US campground data using The Dyrt map interface API            | 30     |
| Validate data using `pydantic` (fields defined in `campground.py`)        | 15     |
| Cron-like job scheduling for regular updates                              | 15     |
| Update existing records if already present                                | 10     |
| Error handling and retry logic                                            | 15     |
| **Bonus:** Use ORM, logging, API endpoint, async, reverse geocoding, etc. | Bonus  |

---

## ✅ Work Completed

### 1. Dockerized Infrastructure

* Docker Compose file successfully configured to start:

  * PostgreSQL (user: `user`, password: `password`, db: `case_study`)
  * Python scraper container
* Dockerfile includes:

  * Python 3.10-slim base
  * Installation of system packages (e.g., `cron`)
  * Pip installation of Python dependencies
  * Cron job configured to run the scraper every 30 minutes

**Status:** ✅ Completed (15/15)

---

### 2. Database Model Creation

* `src/models/campground_orm.py` defines SQLAlchemy ORM model.
* `main.py` creates tables with `Base.metadata.create_all`.

**Status:** ✅ Completed (tables created, verified in DB)

---

### 3. Data Scraping Implementation

* Implemented `src/scraper/scraper.py`

  * API endpoint reverse-engineered from network traffic.
  * Bounding box set for full US region.
  * `requests` used for HTTP GET.

**Status:** ✅ Basic implementation completed
**Note:** API fetches sample data but may require pagination or bbox chunking to scale for entire US.

---

### 4. Pydantic Data Validation

* `src/models/campground.py` contains `Campground` class using aliases.
* Validation errors are caught and logged.

**Status:** ✅ Fully functional

---

### 5. Cron Scheduling

* `cronjob` file runs scraper every 30 mins and logs output.
* Confirmed inclusion in Dockerfile and cron installation.

**Status:** ✅ Completed and integrated

---

### 6. Data Upsert (Update Existing Records)

* SQL query uses `ON CONFLICT (id) DO UPDATE` logic.

**Status:** ✅ Completed and tested with PostgreSQL upsert logic

---

### 7. Error Handling

* HTTP errors caught via `try/except`, retry logic planned.
* `ValidationError` handled with logs.
* DB errors wrapped in try/except.

**Status:** ✅ Basic error handling in place

---

## 🔹 Bonus Features (Partially Completed)

| Feature                | Status | Notes                                    |
| ---------------------- | ------ | ---------------------------------------- |
| ORM Integration        | ✅ Yes  | Used SQLAlchemy ORM                      |
| Logging                | ✅ Yes  | Basic logging via `logging` module       |
| Async / Multithreading | ❌ No   | Could use `aiohttp` or `httpx` for async |
| Flask/FastAPI endpoint | ❌ No   | Not implemented                          |
| Reverse Geocoding      | ❌ No   | Could be added via `geopy` or Google API |

---

## 📊 Current Gaps / To-Do

* ❌ **Full-scale scraping**: Current bbox is too large for full data retrieval; implement tiled bounding boxes + pagination.
* ❌ **API endpoint**: Add FastAPI interface for on-demand scraping.
* ❌ **Async performance**: Improve scraper speed and retry using `asyncio` or `httpx.AsyncClient`.
* ❌ **Address resolution**: Derive human-readable addresses from lat/lon using Nominatim or Google Maps API.
* ❌ **Unit tests**: Add test coverage for parsing, DB insertions.

---

## 🧱 Technologies Used

* Python 3.10
* Docker + Docker Compose
* PostgreSQL 13
* SQLAlchemy (ORM)
* Pydantic 2.x
* Cron (via Debian in container)
* Requests (HTTP client)

---

## 📃 File Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── cronjob
├── main.py
├── requirements.txt
├── src
│   ├── scraper
│   │   └── scraper.py
│   ├── db
│   │   └── database.py
│   └── models
│       ├── campground.py
│       └── campground_orm.py
└── README.md
```

---

## ✍️ Contact

For questions or collaboration:
**LinkedIn:** [Orhan YARDIM](https://www.linkedin.com/in/orhan-yardim/)

---

## 🌟 Author Notes

This project demonstrates a well-structured full-stack scraping pipeline from network analysis to database population. To productionize, add monitoring, retry middleware, and expose API endpoints.

---

