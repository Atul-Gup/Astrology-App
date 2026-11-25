"""One-time download of the JPL ephemeris kernel (the only code here that uses the network).

Run by hand from services/calc/:  python scripts/fetch_ephemeris.py
The service itself never downloads anything.
"""

import hashlib
import sys
import urllib.request
from pathlib import Path

URL = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp"
DEST = Path(__file__).resolve().parent.parent / "data" / "ephemeris" / "de440s.bsp"


def main() -> int:
    if DEST.exists():
        print(f"Already present: {DEST}")
    else:
        DEST.parent.mkdir(parents=True, exist_ok=True)
        tmp = DEST.with_suffix(".part")
        print(f"Downloading {URL}")
        urllib.request.urlretrieve(URL, tmp)
        tmp.rename(DEST)
    digest = hashlib.sha256(DEST.read_bytes()).hexdigest()
    print(f"Saved {DEST} ({DEST.stat().st_size} bytes)")
    print(f"SHA-256: {digest}")
    print("Checksum is printed for your records; it is not verified against a published value.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
