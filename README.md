# non-profits-data-enrichment

A FastAPI-based research tool for uploading, cleaning, and enriching nonprofit organizations IRS datasets with **geolocation**, **Census tract** mapping, and **social media page recommendations** to support social network analysis and research on nonprofit social capital.

---

## Features
- Non profits IRS data (CSV / XLSX) upload and validation.
- Address geocoding 
- Census tract lookup using the U.S. Census API.  
- Social media recommendation via a matching API (fuzzy name matching + ML).  
- Bootstrap frontend + RESTful FastAPI backend. 
- Enriched data is downloadable as a CSV file.

---

## Quick start
Python 3.10+ recommended.

Install dependencies:
pip install -r requirements.txt

Clone, create a venv, install dependencies, and run locally:
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/non-profits-data-enrichment.git
cd non-profits-data-enrichment
python -m venv venv
venv\Scripts\activate #Linux: source venv/bin/activate
pip install -r requirements.txt
fastapi dev main.py

Open: http://localhost:8000

---