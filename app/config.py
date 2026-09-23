import os

from dotenv import load_dotenv

load_dotenv()

GS25_LAT = float(os.getenv("GS25_LAT", "37.5665"))
GS25_LON = float(os.getenv("GS25_LON", "126.9780"))
GS25_RADIUS = int(os.getenv("GS25_RADIUS", "500"))
POLL_SECONDS = max(30, int(os.getenv("POLL_SECONDS", "60")))

THREADS_ACCESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN", "")
THREADS_USER_ID = os.getenv("THREADS_USER_ID", "")
