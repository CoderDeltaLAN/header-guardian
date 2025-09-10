#!/usr/bin/env bash
REPO="${1:?owner/repo}"
for id in $(gh run list --repo "$REPO" --limit 200 \
  --json databaseId,conclusion \
  --jq '.[]|select(.conclusion=="failure" or .conclusion=="cancelled")|.databaseId'); do
  gh api -X DELETE "repos/$REPO/actions/runs/$id" >/dev/null || true
done
echo "Historial limpio para $REPO"
