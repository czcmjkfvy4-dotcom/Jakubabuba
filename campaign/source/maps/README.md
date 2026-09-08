# Dragon Citadel Campaign Sources

These eight native VCMI maps are included in the 1.5.7 campaign. Rebuild them with `python campaign/build_maps.py --templates campaign/source/native-templates.json` from the repository root. The playable archive is `Content/Maps/Smocza_Cytadela.vcmp`.

Included files:

1. `01-first-foundry.vmap`
2. `02-golem-oath.vmap`
3. `03-titan-halls.vmap`
4. `04-split-grotto.vmap`
5. `05-treasury-of-the-storm.vmap`
6. `06-eternal-storm.vmap`
7. `07-azure-throne.vmap`
8. `08-heart-of-the-end.vmap`

The player starts with the core Dragon Citadel economy and available basic dwellings already built. Creature dwellings above the current chapter are forbidden. Engine tests cover starts, reachability, progression and simulated objectives; roughly 30 minutes per chapter remains a design target, not a measured human-playthrough result.
