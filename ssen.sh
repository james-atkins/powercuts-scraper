#!/usr/bin/env bash

curl --insecure https://www.ssen.co.uk/Sse_Components/Views/Controls/FormControls/PowerTrackHandler.ashx | jq '.' > data/ssen.json
