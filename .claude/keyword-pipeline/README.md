# Keyword Pipeline

Shared data folder used by the daily-routine orchestrator.

## Files (written fresh each daily run)

| File | Written by | Read by |
|------|-----------|---------|
| `gsc-top-keywords.md` | `gsc-analyzer` | `keyword-expander` |
| `expanded-keywords.md` | `keyword-expander` | `duplicate-checker` |
| `clean-keyword-list.md` | `duplicate-checker` + `trend-scout` | `content-publisher` |
| `strategic-directive.md` | `ceo-agent` | `daily-routine`, `content-publisher`, `keyword-expander` |
| `health-report.md` | `site-health-checker` | `ceo-agent` (next run) |
