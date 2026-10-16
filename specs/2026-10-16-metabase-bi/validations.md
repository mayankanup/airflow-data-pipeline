# Validations — metabase-bi
Merge gate for `feature/2026-10-16-metabase-bi`. Must all be green.

## Success Checks
1. `docker compose config --services` → includes `metabase`
2. `docker compose up -d metabase` → `http://localhost:3000` setup wizard loads, `docker ps` Up
3. Add Postgres database: host `olap-postgres`, port `5432`, db `olap`, user `metabase_reader` → Save shows `daily_sales_summary` synced
4. New Question → `daily_sales_summary` → `total_revenue` by `date` → chart renders 15 points; values match `python scripts/validate_foundations.py` MATCH
5. RO guard: `metabase_reader` cannot INSERT/DELETE (`permission denied`), can SELECT

## Merge Gate
- [ ] all 5 checks green
- [ ] `plan.md` boxes checked
- [ ] no changes to `specs/mission.md` / `specs/tech-stack.md` scope
- [ ] branch `feature/2026-10-16-metabase-bi` ready to merge
