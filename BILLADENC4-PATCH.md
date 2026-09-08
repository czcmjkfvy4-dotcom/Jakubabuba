# VCMI BILLADENC4 Extension

**IMPORTANT: AFTER INSTALLING THE MOD IN VCMI, RUN `INSTALL BILLADENC4 RUNTIME.CMD` ONCE TO ENABLE ALL ENGINE FEATURES.**

`Dragon Citadel: Endgame Rules` is a regular VCMI submod. The town, creatures, buildings, graphics and adventure-map objects load in stock VCMI 1.7.5.

Requested Dragon Citadel rules cannot currently be represented by a data-only VCMI mod:

- one final dragon per month without Castle, Grail, plague or bonus-week multiplication
- an individual joining probability for one creature type
- Ruby Golem battle scaling after every round
- fixed-slot Dragon Citadel autosaves

The BILLADENC4 edition is therefore a small, source-available VCMI 1.7.5 extension. The dragon endgame rules activate with submod ID `dragon-citadel.endgame-rules`; Ruby Golem round growth activates whenever the creature is present in battle.

## Implemented Rules

- Ultimate and Absolute Dragons add exactly one available creature once per month.
- Recruitment uses a shared pool: +1 on day 29, 57, 85 and each later month boundary. Recruitment must already be unlocked by the Grail. Ordinary weeks add zero; buying a dragon or upgrading it does not restart the calendar.
- Plague can still reduce an existing pool, but Week of the Creature cannot multiply level 8 growth.
- Version 1.5.7 fixes the old-date check that prevented monthly town growth. Plague reduces the existing pool before adding the new monthly recruit.
- PNG creature sprites now have a true grayscale effect layer for petrification; original artwork and alpha are preserved.
- The Grail's automatic level-8 dwellings respect scenario restrictions, including the campaign's chapter locks.
- Wandering Ultimate and Absolute Dragon stacks remain at one creature.
- Only positions whose deterministic VCMI map roll falls in the first 10% may agree to join.
- `nwcbilladen` multiplies every current resource by 10, displays `BILLADENC4`, and does not set the standard `PlayerCheated` flag.
- Ruby Golems gain cumulative +2 Attack, +1 Defense and +10 Health after every completed battle round.
- Ultimate and Absolute Dragons use fitted animations in recruitment and creature-information windows without changing their full-size battle animations.
- Before an enemy battle against an owned mine or other independent armed map structure, the defender receives a dialog naming the attacked object.
- Dragon Citadel games save into a fixed autosave slot, overwriting the previous Dragon Citadel autosave.

## Source Patch

The complete patch against VCMI 1.7.5 is stored at:

`BILLADENC4/vcmi-1.7.5-dragon-citadel.patch`

It changes:

- `client/CPlayerInterface.cpp`
- `client/widgets/MiscWidgets.cpp`
- `lib/mapObjects/CGCreature.cpp`
- `lib/mapObjects/CGDwelling.cpp`
- `lib/mapObjects/CGTownInstance.cpp`
- `server/battles/BattleFlowProcessor.cpp`
- `server/processors/NewTurnProcessor.cpp`
- `server/processors/PlayerMessageProcessor.cpp`
- `server/processors/PlayerMessageProcessor.h`

Apply it to the VCMI 1.7.5 source tree and build `VCMI_lib`, `VCMI_server` and `VCMI_client`. The resulting three runtime files belong in the normal VCMI program directory used by the BILLADENC4 shortcut.

Version 1.5.7 also changes `server/CGameHandler.cpp` and the SDL image/effect-layer rendering files. Optional CMake targets `dragon_growth_regression`, `dragon_visual_regression` and `dragon_campaign_regression` test monthly recruitment and save/load, PNG grayscale, campaign graphics, map loading, restrictions, connectivity and objective predicates. Run them in an isolated VCMI data profile with Dragon Citadel and its endgame-rules submod enabled. The campaign regression simulates completed objectives; it is not a human battle-balance or 30-minute timing test.

The patch follows the VCMI project's GPL-2.0-or-later license.
