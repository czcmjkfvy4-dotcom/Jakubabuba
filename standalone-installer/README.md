# Dragon Citadel Complete Edition installer

This project builds a separate Windows edition of Dragon Citadel, similar in presentation to a classic Heroes III expansion installation. It contains VCMI 1.7.5, the BILLADENC4 runtime, Dragon Citadel and the bundled `chinese-maps-collection` Maps Collection.

## Player experience

1. Run `Smocza_Cytadela_Complete_Edition_1.5.7_Setup.exe`.
2. On first launch the game automatically finds legal Heroes III Complete / Shadow of Death data in an existing VCMI or GOG installation.
3. If automatic detection fails, one folder picker asks for the legal game directory.
4. The edition uses `%LOCALAPPDATA%\Dragon Citadel\Profile` for its own configuration, saves and logs.
5. Only `core`, `vcmi`, `dragon-citadel` and its required `endgame-rules` module are enabled.

Heroes III HD Edition is not compatible. Copyrighted Heroes III data is never bundled in the installer.

## Building

Run `build-installer.ps1` on Windows with VCMI 1.7.5 and Inno Setup 6 installed. The script stages the open-source engine, replaces the three BILLADENC4 runtime files, adds Dragon Citadel, adds the Maps Collection from `vcmi-map-pack-downloads`, and compiles a single installer executable into `output`.

The generated `staging` and `output` directories are release artifacts and are intentionally excluded from Git.
