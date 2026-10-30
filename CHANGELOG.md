# Changelog

## Development - 2026-10-28

- Adopt the supplied The Empire Endures pack as the authoritative baseline (30 game files).
- Add an independent Gunnery School controller and faction permissions for Karl Franz.
- Filter both schools' mission-completion conditions by owning faction.
- Preserve Elspeth's progression, save key, victory objectives and Gardens of Morr.
- Verify all baseline payload hashes, decode all packed DB fragments, and pass isolated Lua 5.1 mission-ownership tests.
- In-game UI, recruitment, campaign progression and multiplayer validation remain pending.

- Add Arkhan-style GitHub Actions for DB validation, Lua lint/isolation checks and verified RPFM pack builds, with main-mod artifacts only.

## Fix - 2026-10-29

- Fix startup CTD: three cloned charge-check members incorrectly referenced nonexistent cloned campaign groups. Retain vanilla group IDs and independent member IDs.
- Validate every added schema-declared reference against reviewed native keys and local records; verify native DB bytes match documented rows.
- Add regression tests reproducing all three invalid references.

## Lua cleanup - 2026-10-30

- Resolve all 37 Luacheck warnings in the two Gunnery School scripts: wrap long lines, remove trailing whitespace and unused callback arguments.
- Preserve campaign behavior and keep all lint checks enabled.
