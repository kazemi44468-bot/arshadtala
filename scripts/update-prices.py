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


def find_number(text: str, pattern: str):
    match = re.search(pattern, text, flags=re.IGNORECASE)
    return match.group(1).replace(",", "") if match else None


def collect():
    response = requests.get(SOURCE_URL, timeout=30, headers={"User-Agent": "Mozilla/5.0 (compatible; ArshadtalaPriceBot/1.0; +https://github.com/kazemi44468-bot/arshadtala)"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    text = clean(soup.get_text(" ", strip=True))

    prices = {
        "ounce": find_number(text, r"ا[ٌُ]?نس\s*\$?\s*([\d,]+)"),
        "emami": find_number(text, r"سکه\s+طرح\s+جدید\s+([\d,]+)"),
        "mesghal": find_number(text, r"مظنه\s+تهران\s+([\d,]+)"),
        "bahar": find_number(text, r"سکه\s+طرح\s+قدیم\s+([\d,]+)"),
        "gold18": find_number(text, r"طلا\s+18\s+عیار\s+([\d,]+)"),
        "half": find_number(text, r"نیم\s+سکه\s+([\d,]+)"),
        "gold24": find_number(text, r"طلا\s+24\s+عیار\s+([\d,]+)"),
        "quarter": find_number(text, r"ربع\s+سکه\s+([\d,]+)"),
        "gerami": find_number(text, r"سکه\s+گرمی\s+([\d,]+)"),
        "dollar": find_number(text, r"دلار\s+([\d,]+)"),
        "euro": find_number(text, r"یورو\s+([\d,]+)"),
        "dirham": find_number(text, r"درهم\s+([\d,]+)"),
    }

    source_updated_at = None
    match = re.search(r"آخرین\s+بروزرسانی:\s*([0-9۰-۹]{1,2}\s+[^\s]+\s+[0-9۰-۹]{4}\s*-\s*[0-9۰-۹]{1,2}:[0-9۰-۹]{2}:[0-9۰-۹]{2})", text)
    if match:
        source_updated_at = match.group(1).strip()

    if not any(prices.values()):
        raise RuntimeError("No recognizable live prices were found on the union board")

    return {"source": SOURCE_URL, "sourceName": "اتحادیه فروشندگان و سازندگان طلا، جواهر، نقره و سکه تهران", "updatedAt": datetime.now(timezone.utc).isoformat(), "sourceUpdatedAt": source_updated_at, "status": "ok", "prices": prices}


def write_json(payload):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    payload = collect()
    write_json(payload)
    print(json.dumps(payload, ensure_ascii=False))
