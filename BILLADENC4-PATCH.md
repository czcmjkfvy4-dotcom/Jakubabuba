# VCMI BILLADENC4 Extension

**IMPORTANT: AFTER INSTALLING THE MOD IN VCMI, RUN `INSTALL BILLADENC4 RUNTIME.CMD` ONCE TO ENABLE ALL ENGINE FEATURES.**

`Dragon Citadel: Endgame Rules` is a regular VCMI submod. The town, creatures, buildings, graphics and adventure-map objects load in stock VCMI 1.7.4.

Two requested rules cannot currently be represented by a data-only VCMI mod:

- growth once every 8 weeks instead of once per week
- an individual joining probability for one creature type
- Ruby Golem battle scaling after every round

The BILLADENC4 edition is therefore a small, source-available VCMI 1.7.4 extension. The dragon endgame rules activate with submod ID `dragon-citadel.endgame-rules`; Ruby Golem round growth activates whenever the creature is present in battle.

## Implemented Rules

- Ultimate and Absolute Dragons add exactly one available creature once every 8 weeks.
- Plague can still reduce an existing pool, but Week of the Creature cannot multiply level 8 growth.
- Wandering Ultimate and Absolute Dragon stacks remain at one creature.
- Only positions whose deterministic VCMI map roll falls in the first 10% may agree to join.
- `nwcbilladen` multiplies every current resource by 10, displays `BILLADENC4`, and does not set the standard `PlayerCheated` flag.
- Ruby Golems gain cumulative +2 Attack, +1 Defense and +10 Health after every completed battle round.
- Ultimate and Absolute Dragons use fitted animations in recruitment and creature-information windows without changing their full-size battle animations.

## Source Patch

The complete patch against VCMI 1.7.4 is stored at:

`BILLADENC4/vcmi-1.7.4-dragon-citadel.patch`

It changes:

- `client/widgets/MiscWidgets.cpp`
- `lib/mapObjects/CGCreature.cpp`
- `lib/mapObjects/CGDwelling.cpp`
- `server/battles/BattleFlowProcessor.cpp`
- `server/processors/NewTurnProcessor.cpp`
- `server/processors/PlayerMessageProcessor.cpp`
- `server/processors/PlayerMessageProcessor.h`

Apply it to the VCMI 1.7.4 source tree and build `VCMI_lib`, `VCMI_server` and `VCMI_client`. The resulting three runtime files belong in the normal VCMI program directory used by the BILLADENC4 shortcut.

The patch follows the VCMI project's GPL-2.0-or-later license.
