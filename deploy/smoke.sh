#!/bin/sh
# Exercise a running backend the way a visitor would: model, integration, simulations,
# an optimisation study and a STEP export. Usage: deploy/smoke.sh http://localhost:8000
set -eu
base=${1:?usage: smoke.sh <base-url>}
api="$base/api"
json() { python3 -c "import json,sys; print(json.load(sys.stdin)$1)"; }
post() { curl -fsS -X POST -H 'content-type: application/json' -d "$2" "$api$1"; }

curl -fsS "$api/health" >/dev/null
id=$(post /projects '{"name":"smoke"}' | json '["id"]')
curl -fsS -o /dev/null "$api/projects/$id/model"
curl -fsS -o /dev/null "$api/projects/$id/integration"
for target in front rear; do
  post "/projects/$id/tests/run" "{\"test_id\":\"quarter_car\",\"target\":\"$target\"}" >/dev/null
done
post "/projects/$id/tests/run" '{"test_id":"longitudinal","target":"vehicle"}' >/dev/null
status=$(post "/projects/$id/optimize" '{"target":"rear","scenarios":["step_25","hump_75"],"budget":40,
  "objectives":[{"metric":"rms_body_acceleration"}],
  "variables":[{"parameter":"rear_damping_bump","lower":900,"upper":1700},
               {"parameter":"rear_spring_rate","lower":17,"upper":31}]}' | json '["status"]')
echo "optimisation study: $status"
curl -fsS -o "${TMPDIR:-/tmp}/smoke.step" "$api/projects/$id/export.step"
head -c 13 "${TMPDIR:-/tmp}/smoke.step" | grep -q ISO-10303-21
echo "smoke test passed"
