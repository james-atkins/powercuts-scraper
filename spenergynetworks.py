import json
import pathlib
import re

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

DATA_DIR = pathlib.Path("data") / "spenergynetworks"
RETRIES = 3
TIMEOUT = 10  # Website is quite slow so have a high timeout threshold

if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    retry_strategy = Retry(
        total=RETRIES,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    with requests.Session() as session:
        session.mount("https://", adapter)
        r = session.get("https://www.spenergynetworks.co.uk/pages/power_cuts_map.aspx", timeout=TIMEOUT)

        m = re.search("arrPowercutsPostcodes: (?P<data>\[.*\]),", r.text)
        data = json.loads(m["data"])

        for incident in data:
            incident_ref = incident["INCIDENT_REF"]
            print(f"Incident ref: {incident_ref}")

            with open(DATA_DIR / f"{incident_ref}.json", "w", newline="\n", encoding="utf-8") as f:
                json.dump(incident, f, ensure_ascii=False, indent=2)
