# The Empire Endures

The supplied The Empire Endures mod, extended with an independent Imperial Gunnery School for Karl Franz (Reikland).

## Status

Development build. Static checks and isolated Lua checks do not replace an in-game campaign test.

## Build and install

Run `python build.py` with Python 3. The output is `dist/the_empire_endures.pack`. Enable this replacement pack instead of the original The Empire Endures pack. Do not enable both copies. Requires the game's Elspeth/DLC25 content. Start a new Karl Franz campaign for validation; existing-save migration has not been verified.

## Scope

The supplied baseline's 30 game files are preserved byte for byte. `baseline.json` records their hashes. RPFM editor metadata is excluded. Added database fragments use `ss_franz_gunnery` filenames. Karl receives separate campaign-group membership, ritual access, pooled resources, salvage-guns options, amethyst recruitment permissions and the school panel. Gardens of Morr and teleportation are excluded.

Elspeth's native script has one ownership guard added to its MissionSucceeded condition so Karl's missions cannot advance her progression. This is the only vanilla script override; mods replacing the same script need review. Karl's controller has independent event names, listener names, progression and save keys. Mission success is filtered by faction. His existing victory conditions are retained. The two factions reuse native ritual/mission definitions, with faction-scoped progress.

`src/` contains native game files, including binary DB fragments. `db_rows.json` documents added rows for review; edit native DB files with RPFM. `tools/packfile.py` provides the deterministic pack builder.

## In-game validation still required

- Start Karl and Elspeth campaigns separately and a simultaneous multiplayer campaign.
- Confirm Karl's school button opens, starts with 250 schematics, and preserves Elector Count features.
- Complete all four mission tiers; verify the other faction's missions and tier rewards do not change.
- Buy upgrades and amethyst units; check independent stocks, limits and artillery charges.
- Earn schematics through Salvage Guns; verify costs and rewards.
- Save/reload each tier and inspect script/game error logs.
- Confirm the original Empire Endures building/recruitment changes remain available.

School income from buildings gated specifically to Wissenland remains as supplied; Karl can acquire schematics through his added salvage option.
