import requests
import psycopg2
from psycopg2.extras import execute_values
from pydantic import ValidationError
from src.models.campground import Campground
import time
import logging
from typing import Optional

# Logging ayarı
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# The Dyrt API endpoint (örnek bir koordinat aralığı, genişletilebilir)
API_URL = "https://thedyrt.com/api/v6/location-search-results"
PARAMS = {
    "filter[search][bbox]": "-125,24,-66,49",  # Tüm ABD’yi kapsayan kutu
    "page[size]": 500,
    "sort": "recommended"
}

# Veritabanı bağlantısı
DB_CONFIG = {
    "host": "postgres",
    "dbname": "case_study",
    "user": "user",
    "password": "password"
}


def get_address_from_coords(lat: float, lon: float) -> Optional[str]:
    try:
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json",
            "zoom": 10,
            "addressdetails": 1
        }
        headers = {
            "User-Agent": "TheDyrtScraperBot/1.0 (your_email@example.com)"
        }
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("display_name")
    except Exception as e:
        logging.warning(f"Adres alınamadı ({lat}, {lon}): {e}")
        return None


def get_campgrounds():
    try:
        logging.info("Veriler API'den çekiliyor...")
        response = requests.get(API_URL, params=PARAMS)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    except requests.RequestException as e:
        logging.error(f"HTTP hatası: {e}")
        return []


def parse_campground(item):
    try:
        return Campground(**item["attributes"], id=item["id"], type=item["type"], links=item["links"])
    except ValidationError as e:
        logging.warning(f"Doğrulama hatası: {e}")
        return None


def save_to_db(campgrounds):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    insert_query = """
    INSERT INTO campgrounds (
        id, type, name, latitude, longitude, region_name, administrative_area,
        nearest_city_name, accommodation_type_names, bookable, camper_types,
        operator, photo_url, photo_urls, photos_count, rating, reviews_count,
        slug, price_low, price_high, availability_updated_at, detail_url, address
    ) VALUES %s
    ON CONFLICT (id) DO UPDATE SET
        name = EXCLUDED.name,
        latitude = EXCLUDED.latitude,
        longitude = EXCLUDED.longitude,
        region_name = EXCLUDED.region_name,
        rating = EXCLUDED.rating,
        reviews_count = EXCLUDED.reviews_count,
        address = EXCLUDED.address
    """

    values = []
    for c in campgrounds:
        address = get_address_from_coords(c.latitude, c.longitude)
        values.append((
            c.id, c.type, c.name, c.latitude, c.longitude, c.region_name, c.administrative_area,
            c.nearest_city_name, c.accommodation_type_names, c.bookable, c.camper_types,
            c.operator, str(c.photo_url) if c.photo_url else None,
            [str(p) for p in c.photo_urls], c.photos_count, c.rating,
            c.reviews_count, c.slug, c.price_low, c.price_high,
            c.availability_updated_at, str(c.links.self), address
        ))

    try:
        execute_values(cur, insert_query, values)
        conn.commit()
        logging.info(f"{len(values)} kamp alanı kaydedildi/güncellendi.")
    except Exception as e:
        logging.error(f"DB hatası: {e}")
    finally:
        cur.close()
        conn.close()


def main():
    raw_items = get_campgrounds()
    parsed = [parse_campground(item) for item in raw_items]
    valid = [p for p in parsed if p is not None]
    if valid:
        save_to_db(valid)
    else:
        logging.warning("Geçerli veri bulunamadı.")


if __name__ == "__main__":
    main()
