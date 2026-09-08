# BILLADENC4 Engine Patch For VCMI 1.7.5

**IMPORTANT: AFTER INSTALLING THE MOD IN VCMI, RUN `INSTALL BILLADENC4 RUNTIME.CMD` ONCE TO ENABLE ALL ENGINE FEATURES.**

This mod works in stock VCMI 1.7.5, but stock VCMI town JSON cannot express "one final dragon per month" for only one creature line while ignoring Castle, Grail, plague and bonus-week growth modifiers.

For normal players, use the ready runtime package:

`BILLADENC4 Runtime VCMI 1.7.5`

It contains:

- `VCMI_lib.dll`
- `VCMI_server.exe`
- `VCMI_client.exe`
- `Install BILLADENC4 Runtime.cmd`

The installer asks for the VCMI 1.7.5 program folder, creates a backup, and replaces only those three runtime files. VCMI and VCMI Launcher must be closed first.

For source publication and rebuilding, the same runtime is based on:

`BILLADENC4/vcmi-1.7.5-dragon-citadel.patch`

The patch changes:

- town growth for `dcUltimateDragon` and `dcAbsoluteDragon` to one creature per month,
- adventure dwelling growth for the same dragons to one creature per month,
- wandering Ultimate and Absolute Dragon stacks so they do not grow weekly,
- joining checks so only 10% of those dragon stacks can agree to join,
- the `nwcbilladen` cheat code,
- a fixed Dragon Citadel autosave slot that overwrites the previous autosave,
- fitted animated recruitment previews for Ultimate and Absolute Dragons without changing their battle scale.

After applying the patch to VCMI 1.7.5 source, build at least:

- `VCMI_lib.dll`
- `VCMI_server.exe`
- `VCMI_client.exe`

Copy the resulting files into the VCMI program folder used for the BILLADENC4 shortcut, or use the ready runtime package so players do not need to patch or compile anything.

The normal mod ZIP still goes into the regular VCMI mods folder. The engine patch is only needed for the exact monthly growth, Ruby Golem round growth, creator code and fixed Dragon Citadel autosave rules.
