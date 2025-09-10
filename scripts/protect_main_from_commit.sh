#!/usr/bin/env bash
REPO="${1:?owner/repo}"
SHA="$(gh api "repos/$REPO/commits/main" --jq .sha 2>/dev/null || true)"
[ -z "$SHA" ] && { echo "Sin commit en main"; exit 0; }
NAMES="$(gh api "repos/$REPO/commits/$SHA/check-runs" --jq '.check_runs[].name' 2>/dev/null | sed '/^[[:space:]]*$/d' | grep -vi windows | sort -u || true)"
[ -z "$NAMES" ] && { echo "Sin check-runs aún"; exit 0; }
printf '%s\n' "$NAMES" | jq -R -s 'split("\n")|map(select(length>0))' >/tmp/ctx.json
jq -n --argjson ctx "$(cat /tmp/ctx.json)" '{strict:true,contexts:$ctx}' >/tmp/req.json
gh api -X PUT -H "Accept: application/vnd.github+json" \
  "repos/$REPO/branches/main/protection/required_status_checks" \
  --input /tmp/req.json >/dev/null
echo "Checks requeridos:"
printf '%s\n' "$NAMES"
