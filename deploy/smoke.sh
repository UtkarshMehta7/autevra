#!/bin/sh
# Exercise a running backend the way a visitor would: model, integration, simulations,
# an optimisation study and a STEP export. Usage: deploy/smoke.sh http://localhost:8000
# EXPECT_ISOLATION=1 also requires that another visitor workspace cannot see the project.
set -eu
base=${1:?usage: smoke.sh <base-url>}
api="$base/api"
# A visitor workspace key: required by a public instance, ignored locally.
ws="X-Autevra-Workspace: smoke$(date +%s)0000000000000000"
json() { python3 -c "import json,sys; print(json.load(sys.stdin)$1)"; }
post() { curl -fsS -X POST -H 'content-type: application/json' -H "$ws" -d "$2" "$api$1"; }
get() { curl -fsS -H "$ws" "$@"; }

curl -fsS "$api/health" >/dev/null
id=$(post /projects '{"name":"smoke"}' | json '["id"]')
get -o /dev/null "$api/projects/$id/model"
get -o /dev/null "$api/projects/$id/integration"
for target in front rear; do
  post "/projects/$id/tests/run" "{\"test_id\":\"quarter_car\",\"target\":\"$target\"}" >/dev/null
done
post "/projects/$id/tests/run" '{"test_id":"longitudinal","target":"vehicle"}' >/dev/null
status=$(post "/projects/$id/optimize" '{"target":"rear","scenarios":["step_25","hump_75"],"budget":40,
  "objectives":[{"metric":"rms_body_acceleration"}],
  "variables":[{"parameter":"rear_damping_bump","lower":900,"upper":1700},
               {"parameter":"rear_spring_rate","lower":17,"upper":31}]}' | json '["status"]')
echo "optimisation study: $status"
get -o "${TMPDIR:-/tmp}/smoke.step" "$api/projects/$id/export.step"
# Another workspace must not see the project.
code=$(curl -s -o /dev/null -w '%{http_code}' -H "X-Autevra-Workspace: someone-else-0000000000" "$api/projects/$id")
if [ "${EXPECT_ISOLATION:-0}" = 1 ]; then [ "$code" = 404 ]; fi  # 200 where isolation is off
echo "another workspace gets $code"
head -c 13 "${TMPDIR:-/tmp}/smoke.step" | grep -q ISO-10303-21
echo "smoke test passed"
