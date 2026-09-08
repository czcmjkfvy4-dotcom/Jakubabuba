# Dragon Citadel 1.5.7

**VCMI LAUNCHER CANNOT INSTALL THE CUSTOM RUNTIME AUTOMATICALLY: ON WINDOWS, USE THE COMPLETE EDITION INSTALLER, OR RUN `INSTALL BILLADENC4 RUNTIME.CMD` ONCE AFTER INSTALLING THE MOD ZIP.**

Dragon Citadel is a terrifying, powerful and exceptionally expensive town for Heroes III on VCMI. Development will continue, with approved updates published on this GitHub repository.

## Downloads

- `Smocza_Cytadela_Complete_Edition_1.5.7_Setup.exe`: Windows x64 installation containing VCMI 1.7.5, the matching BILLADENC4 runtime, the mod, its campaign and a collection containing 1,273 map/campaign files. Uses a separate installation and save profile.
- `Dragon_Citadel_1.5.7.zip`: mod and matching runtime installer for an existing VCMI 1.7.5 installation. Extract the `dragon-citadel` directory into your VCMI Mods directory, enable it, close VCMI, then run the included CMD.
- `INSTALL-1.5.7.txt`: English and Polish instructions.
- `SHA256SUMS.txt`: checksums of the release downloads.

A legal installation of Heroes III Complete or Shadow of Death is required. Original game data is not included. Complete Edition locates existing game data or asks you to select its folder. The Steam HD Edition alone is not sufficient. The supplied custom runtime is for Windows x64 and VCMI 1.7.5; source changes are included, but custom runtime builds for other operating systems have not been tested.

## Fixed and Included

- Final dragons share one recruitment pool with exactly one new creature per month, starting on day 29 after the first four weeks. Grail ownership is required. Weekly multipliers do not create extra final dragons.
- A plague week halves the existing pool before the monthly addition, when due.
- Petrification now greys out truecolor PNG creatures while retaining their transparency.
- Eight native campaign scenarios, Polish prologues and epilogues, 45 timed story events and repeatable unit information. Previous creature tiers remain available; later tiers remain locked. Chapter 5 demonstrates the treasury and mint; chapter 8 introduces Grail recruitment.
- Campaign restrictions also apply to automatic Grail dwellings, preventing early level 8 recruitment.
- Includes the existing town, siege, creature animation, fixed-slot autosave and VCMI 1.7.5 runtime changes accumulated since the previous published source revision.

Start the campaign through **New Game > Campaign > Custom**, then select **Smocza Cytadela: Narodziny Ostatniej Burzy**. Restart the game after updating. New campaign starts are recommended; no compatibility promise is made for saves from older custom engine builds.

## Verification and Limits

Engine regressions passed for 170 daily transitions, 40 weekly/ownership cases and a save/load around day 28. Campaign checks covered all eight starts, seven sequential unlocks, 97 reachable objective locations, restrictions and simulated victory/defeat. The Windows installer completed successfully in a local test. A clean-profile headless startup loaded the tested mods without warnings or errors.

These are automated and installation tests, not eight complete human playthroughs. The intended 20-30 minutes per scenario and final battle balance still need player feedback. Compatibility with every third-party mod or every map in the collection is not established.

The future optional third-form submod is **not included** in this stable release. Its proposed creatures, buildings and abilities must not be mistaken for installed 1.5.7 features.
