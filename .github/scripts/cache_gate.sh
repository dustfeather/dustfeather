#!/usr/bin/env bash
# Per-matrix-cell cache gate for the classify-repo job in classify-owner.yml
# (called per-wave by refresh-badges.yml).
#
# If prior/findings/<owner>__<repo>.json exists AND its head_sha matches the
# current REPO_HEAD_SHA, copy that file forward to findings.json and exit 0
# (signalling cache hit). Otherwise exit 1 (signalling Claude needs to run).
#
# Caller (workflow) uses the exit status to decide whether to invoke `claude`:
#   if .github/scripts/cache_gate.sh; then
#     echo "cache hit"
#   else
#     claude --print ...
#   fi
#
# Required env vars: REPO_OWNER, REPO_NAME, REPO_HEAD_SHA.
# Required on disk: prior/findings/ may or may not exist (cold start is fine).

set -euo pipefail

: "${REPO_OWNER:?REPO_OWNER must be set}"
: "${REPO_NAME:?REPO_NAME must be set}"
: "${REPO_HEAD_SHA:?REPO_HEAD_SHA must be set}"

prior_file="prior/findings/${REPO_OWNER}__${REPO_NAME}.json"

if [ ! -f "$prior_file" ]; then
  echo "cache miss: no prior findings for ${REPO_OWNER}/${REPO_NAME}"
  exit 1
fi

# Compare head_sha. jq exits non-zero if the field is missing; treat that as a miss.
prior_sha=$(jq -r '.head_sha // empty' "$prior_file" 2>/dev/null || true)

if [ -z "$prior_sha" ]; then
  echo "cache miss: prior findings for ${REPO_OWNER}/${REPO_NAME} has no head_sha field"
  exit 1
fi

if [ "$prior_sha" != "$REPO_HEAD_SHA" ]; then
  echo "cache miss: prior head_sha=${prior_sha} != current=${REPO_HEAD_SHA}"
  exit 1
fi

# Schema-version compatibility check. If the prior file's schema_version
# doesn't match the current contract, treat as miss so Claude regenerates.
prior_schema=$(jq -r '.schema_version // empty' "$prior_file" 2>/dev/null || true)
if [ "$prior_schema" != "1" ]; then
  echo "cache miss: prior findings schema_version=${prior_schema} != 1"
  exit 1
fi

cp "$prior_file" findings.json
echo "cache hit: copied ${prior_file} -> findings.json (head_sha=${REPO_HEAD_SHA})"
exit 0
