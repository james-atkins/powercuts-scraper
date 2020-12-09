import json
import pathlib

import requests

from common import make_session

DATA_DIR = pathlib.Path("data") / "enwl"


def get_faults(session: requests.Session):
    params = {
        "pageSize": 1000,
        "pageNumber": 1,
        "includeCurrent": "true",
        "includeResolved": "true",
        "includeTodaysPlanned": "true",
        "includeFuturePlanned": "true",
        "includeCancelledPlanned": "true"
    }
    r = session.get("https://www.enwl.co.uk/power-outages/search", params=params)
    r.raise_for_status()
    data = r.json()

    total_results = int(data["TotalResults"])
    faults = data["Items"]

    # A very big page size is used so this should not fail...
    assert len(faults) == total_results

    for fault in faults:
        yield fault


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with make_session() as session:
        for fault in get_faults(session):
            fault_number = fault["faultNumber"]
            print(f"Fault number: {fault_number}")

            with open(DATA_DIR / f"{fault_number}.json", "w", newline="\n", encoding="utf-8") as f:
                json.dump(fault, f, ensure_ascii=False, indent=2)
