import json
import pathlib

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

DATA_DIR = pathlib.Path("data") / "ssen"
RETRIES = 3
TIMEOUT = 5

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

        r = session.get("https://www.ssen.co.uk/Sse_Components/Views/Controls/FormControls/PowerTrackHandler.ashx", verify=False)

        data = r.json()

        for fault in data["Faults"]:
            fault_ref = fault["Reference"]
            print(fault_ref)

            with open(DATA_DIR / f"{fault_ref}.json", "w", newline="\n", encoding="utf-8") as f:
                json.dump(fault, f, ensure_ascii=False, indent=2)
