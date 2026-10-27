# Dragon Citadel 1.5.9 — playable development release

Integral third creature upgrades, optional fourth upgrades, eight campaign chapters and revised town building terraces. Work on the appearance of Dragon Citadel is in progress.

## Installation and eight languages

Use the complete Projects installer from the release assets. Supply your own Heroes III Complete data. Choose Polski, English, Deutsch, 简体中文, 日本語, Русский, Español or Français in Manage-Dragon-Citadel.ps1. The selector changes the game language and activates its base-game translation package as well as the mod translations. On first selection, the required community translation package is downloaded directly from the official VCMI catalog source and checked against a pinned SHA-256. Internet access is needed for this first download; subsequent starts use installed files. English also has a pinned community base-game translation package. Translation packs are not relicensed as Dragon Citadel content.

## Runtime requirement

BILLADENC4, based on VCMI 1.7.5, is required for custom monthly dragon recruitment and Ruby Golem mechanics. Installing the mod with a standard VCMI launcher does not replace its engine. Use the matching complete installer; corresponding engine source is supplied with the installer. Do not mix old client/server/library binaries.

## Verified scope and limitations

The engine resolved 1,131 mod text keys in each of eight languages and 6,415–6,453 base-game text entries in all eight languages, including separately verified VCMI dictionary overrides. All eight standalone campaign maps and their eight embedded campaign counterparts loaded in each language. Actual town screens were captured in all eight languages; see qa-1.5.9/JEZYKI-CALEJ-GRY.html. This is not a full manual campaign playthrough or a native-speaker review of every translation. The mod campaign includes machine-translated draft text. Japanese upstream map/Chronicles translations include an explicitly marked AI-translated optional component enabled by the selector.

Fort, citadel and castle use a shared courtyard anchor and nominal linear scales 1, 1.3 and 1.69. Forty-seven town building states were captured through actual town interfaces. Graphical work remains in progress. Four AI campaign scenarios did not finish within the bounded test; no claim of complete campaign acceptance is made.

## Credits

See TUM-RESOURCE-CREDITS.txt, bundled mod metadata, graphics submod licenses, font licenses and the engine's corresponding-source archive. Heroes III data is imported locally and is not included in the complete installer.


The 1.5.9 language correction translates 344 Polish-source entries individually, checks for Polish leakage, covers all visible Chinese/Japanese codepoints in the inspected catalogs and derives the two final dragon stat/cost lessons from creature data. Ultimate and Absolute Dragons have distinct names in every supported language. This remains a machine translation draft with targeted manual corrections, not a full native-speaker literary review.

The optional fourth-upgrade mode also verifies 52 text entries from its active WoG dependency in each language, completing the German, Spanish and French English fallbacks. Other manually enabled third-party submods remain outside this localization guarantee.
