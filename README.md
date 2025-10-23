# 🧬 genome_server

**Local Flask backend prototype** for genomic file handling, exploration, and analysis.

This project is an early-stage backend used to experiment with bioinformatics workflows — specifically, parsing FASTA files, inspecting chromosome sequences, and performing small-scale analyses like substring matches or region extractions.  
It’s **not production-ready** and currently serves as a functional scaffold for future work in genome data pipelines and bioinformatics backend design.

---

## ⚗️ Overview

- Upload & parse FASTA files using Biopython utilities  
- Store metadata for uploaded files in an SQLite dev database  
- Extract regions or summarize sequences  
- Run substring / motif matches against genome data  
- Compute reverse complements and related sequence utilities  

Routes render templates for quick local testing and exploration.

---

## 🧩 Tech Stack

| Layer | Tool |
|-------|------|
| Framework | Flask |
| Language | Python 3.10+ |
| DB | SQLite (SQLAlchemy ORM) |
| Utilities | Biopython |
| Templates | Jinja2 |
| Server | Werkzeug (Flask dev server) |

---

## 📁 Project Structure

- **app/** – main application package  
  - **\_\_init\_\_.py** – initializes the app factory  
  - **routes/** – contains all route blueprints  
    - **auth_routes.py** – handles upload, parsing, and analysis endpoints  
  - **models/** – defines ORM models such as `FileRecord`  
  - **utils/** – helper functions for parsing, validation, and sequence operations  
  - **templates/** – HTML templates (`upload.html`, `summary.html`, etc.)  
  - **db.py** – SQLAlchemy database configuration  
  - **myFlaskApp.py** – application factory (`create_app`)  
- **requirements.txt** – Python dependencies  
- **README.md** – project documentation  

---

## ⚙️ Setup

### Clone and create environment
```bash
git clone https://github.com/pguardado/genome_server.git
cd genome_server

python3 -m venv env
source env/bin/activate

pip install -U pip setuptools wheel
[ -f requirements.txt ] && pip install -r requirements.txt
