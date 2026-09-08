import json
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://www.estjt.ir/tv/"
ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "prices.json"

DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").translate(DIGITS)).strip()


def numeric(value: str):
    value = clean(value).replace(",", "").replace("،", "")
    match = re.search(r"[-+]?\d+(?:\.\d+)?", value)
    return match.group(0) if match else None


def normalize_label(label: str) -> str:
    return clean(label).replace("ي", "ی").replace("ك", "ک").replace("‌", " ")


def extract_rows(html: str):
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for table in soup.find_all("table"):
        for tr in table.find_all("tr"):
            cells = [clean(c.get_text(" ", strip=True)) for c in tr.find_all(["th", "td"])]
            cells = [c for c in cells if c]
            if len(cells) >= 2:
                rows.append((normalize_label(cells[0]), cells[-1]))
    for tr in soup.select("[role='row']"):
        cells = [clean(c.get_text(" ", strip=True)) for c in tr.select("[role='cell'],[role='gridcell'],[role='columnheader']")]
        if len(cells) >= 2:
            rows.append((normalize_label(cells[0]), cells[-1]))
    return rows


def find_value(rows, aliases):
    for label, value in rows:
        low = label.lower()
        if any(alias in low for alias in aliases):
            number = numeric(value)
            if number:
                return number
    return None


def collect():
    response = requests.get(
        SOURCE_URL,
        timeout=30,
        headers={"User-Agent": "Mozilla/5.0 (compatible; ArshadtalaPriceBot/1.0; +https://github.com/kazemi44468-bot/arshadtala)"},
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    print("SOURCE_STATUS", response.status_code, "BYTES", len(response.text), "TITLE", clean(soup.title.get_text(" ", strip=True) if soup.title else ""))
    scripts = [s.get("src") for s in soup.find_all("script") if s.get("src")]
    print("SCRIPT_SRCS", json.dumps(scripts[:30], ensure_ascii=False))
    text = clean(soup.get_text(" ", strip=True))
    print("PAGE_TEXT_HEAD", text[:2500])

    rows = extract_rows(response.text)
    print("TABLE_ROWS", json.dumps(rows[:100], ensure_ascii=False))

    prices = {
        "gold18": find_value(rows, ["طلای 18", "18 عیار", "گرم طلای 18"]),
        "melted": find_value(rows, ["آبشده نقدی", "آبشده", "آب شده"]),
        "mesghal": find_value(rows, ["مظنه", "مثقال"]),
        "emami": find_value(rows, ["سکه امامی", "امامی"]),
        "bahar": find_value(rows, ["سکه بهار", "بهار آزادی", "سکه قدیم"]),
        "half": find_value(rows, ["نیم سکه", "نیم‌سکه"]),
        "quarter": find_value(rows, ["ربع سکه", "ربع‌سکه"]),
        "gerami": find_value(rows, ["سکه گرمی", "یک گرمی", "یک‌گرمی"]),
        "dollar": find_value(rows, ["دلار"]),
        "euro": find_value(rows, ["یورو"]),
        "dirham": find_value(rows, ["درهم"]),
        "ounce": find_value(rows, ["اونس جهانی", "اونس طلا", "انس جهانی", "انس طلا"]),
    }
    if not any(prices.values()):
        raise RuntimeError("No recognizable price rows were found on the union page")
    return {"source": SOURCE_URL, "sourceName": "اتحادیه فروشندگان و سازندگان طلا، جواهر، نقره و سکه تهران", "updatedAt": datetime.now(timezone.utc).isoformat(), "status": "ok", "prices": prices}


def write_json(payload):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    payload = collect()
    write_json(payload)
    print(json.dumps(payload, ensure_ascii=False))
