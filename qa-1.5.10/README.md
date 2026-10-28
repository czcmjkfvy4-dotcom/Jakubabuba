# 1.5.10 editorial candidate — verification

Scope: sixteen distinct hero biographies in each of eight languages (128 entries), corrected English source fallbacks and documentation. Hero skills, specialty definitions, armies and other gameplay fields were compared unchanged before installation. No map, battle, creature balance or building art change is included.

- Native VCMI resolver: all eight language runs passed, comparing 1,131 mod text keys per language and loading the eight maps and their eight campaign counterparts.
- Chinese/Japanese font coverage: no missing inspected glyphs.
- Content audit: no detected Polish leakage in foreign dictionaries or critical numeric drift.
- Local installation: both player installations and the private campaign runtime received the candidate with backups; 94 save files compared unchanged.

The root version is 1.5.10 to distinguish this candidate from the immutable 1.5.9 release. No 1.5.10 complete installer or public release is claimed here. This is not native-speaker literary review, a building redraw or a complete campaign playthrough.

Evidence: native-report.json, native-<language>.json, full-game-cjk-font-coverage.json, content-audit.json, preparation-report.json and installation-report.json.

To reproduce the scope comparison without game data, run `python tools/verify_editorial_scope.py --base v1.5.9`. The native resolver test source is included under `source/` for inspection; the recorded runs used the matching local BILLADENC4 build. Source include paths have been made relative to the engine test/game directory. No portable build or native-speaker review is claimed.

Both local player installations initialized the menu with zero ERROR and zero WARN after deployment; see installed-startup.json.
