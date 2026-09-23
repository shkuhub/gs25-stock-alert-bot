import os

from dotenv import load_dotenv

load_dotenv()

GS25_LAT = float(os.getenv("GS25_LAT", "37.5665"))
GS25_LON = float(os.getenv("GS25_LON", "126.9780"))
GS25_RADIUS = int(os.getenv("GS25_RADIUS", "500"))

# Safe default: 5 minutes.
POLL_SECONDS = int(os.getenv("POLL_SECONDS", "300"))

# 'relay' is the default MVP test path because direct GS25 requests
# currently receive HTTP 403 from the upstream edge in this environment.
GS25_SOURCE = os.getenv("GS25_SOURCE", "relay").lower().strip()

if GS25_SOURCE not in {"relay", "direct"}:
    raise ValueError("GS25_SOURCE must be 'relay' or 'direct'")

# High-frequency polling is an explicit opt-in only.
ALLOW_HIGH_FREQUENCY_POLLING = os.getenv(
    "ALLOW_HIGH_FREQUENCY_POLLING", "false"
).lower() == "true"

if POLL_SECONDS < 60 and not ALLOW_HIGH_FREQUENCY_POLLING:
    raise ValueError(
        "POLL_SECONDS < 60 requires ALLOW_HIGH_FREQUENCY_POLLING=true"
    )

if POLL_SECONDS < 30:
    raise ValueError("POLL_SECONDS cannot be below 30 seconds")

THREADS_ACCESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN", "")
THREADS_USER_ID = os.getenv("THREADS_USER_ID", "")
