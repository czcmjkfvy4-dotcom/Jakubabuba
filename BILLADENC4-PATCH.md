# VCMI BILLADENC4 Extension

`Dragon Citadel: Endgame Rules` is a regular VCMI submod. The town, creatures, buildings, graphics and adventure-map objects load in stock VCMI 1.7.4.

Two requested rules cannot currently be represented by a data-only VCMI mod:

- growth once per month instead of once per week
- an individual joining probability for one creature type

The BILLADENC4 edition is therefore a small, source-available VCMI 1.7.4 extension. It remains VCMI and only activates the extra rules when the submod ID `dragon-citadel.endgame-rules` is enabled.

## Implemented Rules

- Ultimate and Absolute Dragons add exactly one available creature at the start of each month.
- Plague can still reduce an existing pool, but Week of the Creature cannot multiply level 8 growth.
- A neutral Sanctuary at the End of Ages is guarded by exactly one Ultimate Dragon.
- Wandering Ultimate and Absolute Dragon stacks remain at one creature.
- Only positions whose deterministic VCMI map roll falls in the first 10% may agree to join.
- `nwcbilladen` multiplies every current resource by 10, displays `BILLADENC4`, and does not set the standard `PlayerCheated` flag.

## Source Patch

The complete patch against VCMI 1.7.4 is stored at:

`BILLADENC4/vcmi-1.7.4-dragon-citadel.patch`

It changes:

- `lib/mapObjects/CGCreature.cpp`
- `lib/mapObjects/CGDwelling.cpp`
- `server/processors/NewTurnProcessor.cpp`
- `server/processors/PlayerMessageProcessor.cpp`
- `server/processors/PlayerMessageProcessor.h`

Apply it to the VCMI 1.7.4 source tree and build `VCMI_lib` plus `VCMI_server`. The resulting `VCMI_lib.dll` and `VCMI_server.exe` belong in the normal VCMI program directory used by the BILLADENC4 shortcut.

The patch follows the VCMI project's GPL-2.0-or-later license.
