# Network Scanner

## Overview

Live Network Scanner is a **full-stack, cloud-deployed network scanning application** built with **FastAPI**. It allows users to initiate network scans, track scan progress asynchronously, and view results through a web-based dashboard or REST APIs.

The project evolved from a CLI-based scanner into a **production-style backend system** featuring background task processing, persistent storage, and a user-friendly UI.

---

## Key Features

- 🚀 **FastAPI-based REST API** with Swagger documentation
- 🔄 **Asynchronous background scans** (non-blocking API)
- 📊 **Web dashboard UI** for scan initiation and monitoring
- 🗂 **SQLite + SQLAlchemy ORM** for persistent storage
- 📈 **Scan status tracking** (`pending`, `running`, `completed`, `failed`)
- 🌐 **Public cloud deployment (Render)**
- 🧪 Fully tested locally and in cloud environment

---

## Prerequisites

Before running or contributing to this project, ensure you have the following installed:

- **Python 3.9 or later**
- **pip** (Python package manager)
- **Git** (for cloning the repository)
- **Npcap / libpcap** (required for ARP scanning on local machines)
- A system with **administrator/root privileges** (for local ARP scans)

> ⚠️ Note: ARP-based network scanning works only on local machines. In cloud deployments, this feature is safely disabled.

---

## Technology Stack

| Layer | Technologies |
|-----|-------------|
| Backend | FastAPI, Python |
| Async Processing | FastAPI BackgroundTasks |
| Database | SQLite, SQLAlchemy |
| Networking | Scapy, Socket |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Render |

---

## Project Structure

```
.
├── main.py               # FastAPI application entry point
├── tasks.py              # Background scan worker
├── models.py             # Database models
├── database.py           # Database configuration
├── network_scanner.py    # ARP-based network scanning
├── port_scanner.py       # TCP port scanning
├── utils.py              # Validation utilities
├── templates/
│   └── index.html        # Web dashboard UI
├── static/
│   ├── app.js            # Frontend logic
│   └── style.css         # Dashboard styling
├── network_scanner.db    # SQLite database
├── requirements.txt
├── README.md
└── LICENSE
```

---

## How It Works

1. User initiates a scan via UI or API
2. Scan request is stored with status `pending`
3. Background task starts the scan
4. Status updates to `running`
5. Results are saved to database
6. Status updates to `completed` or `failed`
7. UI/API retrieves results in real-time

---

## Live Website

🌐 **Live Dashboard & API:**
```
https://network-scanner-api.onrender.com
```

- Web Dashboard: `/`
- Swagger Docs: `/docs`

---

## API Endpoints

### Start Scan
```
POST /scan
```
Request Body:
```json
{
  "ip_range": "192.168.1.1/24",
  "ports": [22, 80, 443]
}
```

### Get Scan Results
```
GET /results/{scan_id}
```

### List All Scans
```
GET /results
```

Swagger Docs:
```
/docs
```

---

## Example Usage

### Using the Web Dashboard

1. Open the live site:
   ```
   https://network-scanner-api.onrender.com
   ```
2. Enter an IP range (example: `192.168.1.1/24`)
3. Enter ports (example: `22,80,443`) or leave blank for defaults
4. Click **Start Scan**
5. Watch scan status update in real time
6. View discovered hosts and open ports once completed

### Using the REST API (cURL)

Start a scan:
```bash
curl -X POST https://network-scanner-api.onrender.com/scan \
  -H "Content-Type: application/json" \
  -d '{
    "ip_range": "192.168.1.1/24",
    "ports": [22, 80]
  }'
```

Get scan results:
```bash
curl https://network-scanner-api.onrender.com/results/1
```

List all scans:
```bash
curl https://network-scanner-api.onrender.com/results
```

---

## Running Locally

### Install dependencies
```bash
pip install -r requirements.txt
```

### Start server
```bash
python -m uvicorn main:app --reload
```

Open:
```
http://127.0.0.1:8000
```

---

## Deployment Notes

- Deployed on **Render**
- ARP scanning is automatically disabled in cloud environments
- Background tasks continue to function normally

---

## Future Enhancements

- 🔐 Authentication & API security
- ⏱ Rate limiting
- 🧑 User accounts (JWT-based auth)
- 📦 Redis/Celery for distributed background jobs
- 📊 Advanced visualizations

---

## 🤝 Contributing

Contributions are welcome and appreciated! 🎉

If you’d like to contribute:

1. Fork the repository
2. Create a new feature branch (`git checkout -b feature/your-feature-name`)
3. Commit your changes (`git commit -m "Add new feature"`)
4. Push to the branch (`git push origin feature/your-feature-name`)
5. Open a Pull Request

Please ensure:
- Code is clean and well-documented
- Existing functionality is not broken
- New features include basic testing where applicable

---

## 💬 Feedback

Feedback, suggestions, and ideas are highly welcome!

If you:
- Found a bug 🐞
- Have a feature request ✨
- Want to improve performance or security 🔐

Please open an **Issue** in the GitHub repository or start a discussion.

Your feedback helps improve the project and makes it more robust for real-world usage.

---

## 🐜 License

This project is licensed under the BSD 3-Clause License. See the [LICENSE](LICENSE) file for details.
