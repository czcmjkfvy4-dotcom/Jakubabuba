# Dragon Citadel for VCMI

**IMPORTANT: AFTER INSTALLING THE MOD IN VCMI, RUN `INSTALL BILLADENC4 RUNTIME.CMD` ONCE TO ENABLE ALL ENGINE FEATURES.**

Dragon Citadel is an original, exceptionally expensive endgame town for Heroes of Might and Magic III running on VCMI.

![Fully developed Dragon Citadel](screenshots/town-screen.png)

Version 1.5.7 fixes the monthly recruitment date check and PNG petrification, and ships all eight campaign scenarios with Polish story events and progressive creature unlocks. The matching VCMI 1.7.5 BILLADENC4 runtime is required for these engine mechanics.

There is no separate level 8 town building. The Grail itself unlocks both final dragons through invisible automatic dwelling entries.

![Town interior before and after the layout cleanup](screenshots/town-screen-decluttered-before-after-1.5.4.png)

## Requirements

- a legal copy of Heroes of Might and Magic III: Complete
- VCMI 1.7.5 with the matching BILLADENC4 runtime for all custom rules. The supplied Windows runtime is built for 1.7.5; later engines need separate compatibility testing.

## Download 1.5.7

[Release and verified downloads](https://github.com/czcmjkfvy4-dotcom/Jakubabuba/releases/tag/v1.5.7)

On Windows x64, the Complete Edition installer installs VCMI 1.7.5, BILLADENC4, Dragon Citadel, its eight-chapter campaign and the map collection together in a separate installation. No additional runtime installation is needed with Complete Edition. You must supply legal Heroes III Complete or Shadow of Death game data; these are not included. The mod ZIP is for an existing VCMI installation and still requires the runtime step below.

The optional third-form expansion is under development and is not part of 1.5.7. See [release notes](RELEASE-1.5.7.md) for fixes and testing limitations.

## Installation

1. Copy the `dragon-citadel` folder to `Documents\My Games\vcmi\Mods`.
2. Start VCMI Launcher.
3. Enable `Dragon Citadel`.
4. Close VCMI and VCMI Launcher.
5. Double-click `INSTALL BILLADENC4 RUNTIME.CMD` inside the installed mod folder and approve the Windows administrator prompt.

The bundled installer automatically detects a standard VCMI installation, creates a backup and enables the exact monthly level 8 growth rule, Ruby Golem round growth, the `nwcbilladen` code, fixed-slot Dragon Citadel autosaves and fitted level 8 recruitment animations. Players do not need to compile VCMI or apply a patch manually.

The mod can also be added as a custom VCMI Launcher repository:

`https://raw.githubusercontent.com/czcmjkfvy4-dotcom/Jakubabuba/main/repository.json`

## Version 1.5.6

Every adventure-map stage of the town remains in the original Dragon Citadel stone, turquoise and gold palette. Village, Fort, Citadel, Castle and Capitol never inherit the owning player's color, including when VCMI interface scaling is enabled.

The Grail appears as an animated storm cloud over the city, with black-crimson and white-violet lightning. It provides an additional 10,000 gold and 10 of every resource per day. Building it is the only way to unlock level 8 recruitment.

Dragon Citadel now has a dedicated siege scene and dragon-shaped tower shooters instead of Dungeon scenery and Titans.

![Dragon Citadel siege and dragon tower shooters](screenshots/dragon-citadel-siege-1.5.5.png)

## Level 8: The Final Dragons

The original town-selection portraits were color-corrected without changing their buildings or composition. Village and Fort thumbnails now retain the same artwork while presenting stronger blue and gold tones, clearer contrast and sharper silhouettes at VCMI's native 58x64 and 48x32 sizes.

![Town-selection portraits before and after](screenshots/town-selection-icons-before-after-1.5.4.png)

Ultimate and Absolute Dragon movement uses separate PNG images for takeoff, a six-frame wing-flapping flight loop and landing. The battle animation no longer moves a single static creature icon across the battlefield.

Both creatures also have four-frame directional attack and damage animations. The Ultimate Dragon gathers, breathes and disperses animated black fire with a dark crimson core. Its Absolute upgrade uses animated white-violet Voidfire with a black center and fading arcane particles. The same sequences are connected to regular attacks and VCMI's special dragon-breath groups.

Their large and small portraits now show the complete creature. The matching BILLADENC4 client uses dedicated fitted animation frames in recruitment and creature-information windows, while the original full-size animation remains unchanged in battle.

![Fitted animated level 8 recruitment previews](screenshots/level8-recruitment-preview-1.5.4.png)

Version 1.5.0 added two entirely original level 8 creatures. Version 1.5.5 moves their recruitment entirely into the Grail and removes the separate town structures.

![Ultimate Dragon and Absolute Dragon](screenshots/level8-dragons.jpg)

| Creature | Attack | Defense | Damage | Health | Speed | Recruitment |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ultimate Dragon | 100 | 100 | 220-320 | 10,000 | 20 | 150,000 gold + 150 of every resource |
| Absolute Dragon | 150 | 150 | 320-480 | 15,000 | 30 | 220,000 gold + 200 of every resource |

Both final dragons can now take damage from normal attacks and damaging magic. They still fly, breathe through two hexes, attack all adjacent enemies, block enemy retaliation and regenerate. As a balance tradeoff, Ultimate and Absolute Dragons cannot retaliate when attacked.

No additional sanctuary construction cost is charged. After the Grail is built, the player only pays the recruitment prices shown above.

## Ruby Golems And The Royal Mint

The golem line now has a finished third upgrade: Ruby Golem, with its own ruby battle animation, map animation and portraits. It starts at 10 Attack, 10 Defense, 10-10 Damage and 100 Health. With the BILLADENC4 runtime it gains +2 Attack, +1 Defense and +10 Health after every completed battle round; the bonuses accumulate until the battle ends.

![Ruby Golem animation and portrait preview](screenshots/ruby-golem-complete-preview.png)

Dragon Mint still provides 4,000 gold per day. Its upgrade, Royal Dragon Mint, provides 5,000 gold and 1 unit of every resource per day, giving the player a difficult but real route toward the final dragon economy.

Wandering dragons use a custom 128x128 map animation and always begin in a stack of one. They do not provide an alternative recruitment source.

## VCMI And The Endgame Rules Submod

The public town and its `Dragon Citadel: Endgame Rules` submod load normally through VCMI 1.7.5. BILLADENC4 is a modified VCMI 1.7.5 runtime, not a separate game. Stock VCMI data cannot express a separate monthly growth rule for only one town creature line, so the exact "one final dragon per month" rule requires the BILLADENC4 engine patch included with this mod.

When the submod is enabled in VCMI with the matching BILLADENC4 runtime, it enforces the exact endgame rules:

- one Ultimate or Absolute Dragon appears once per month
- wandering level 8 stacks remain at one creature
- only 10% of wandering level 8 positions are eligible to join
- Ruby Golems cumulatively gain +2 Attack, +1 Defense and +10 Health after every completed battle round

The source changes are documented in [BILLADENC4-PATCH.md](BILLADENC4-PATCH.md).

## Optional Creator Tools Submod

`Dragon Citadel: Creator Tools` is included as a normal VCMI submod and is disabled by default. With it enabled and the matching BILLADENC4 runtime:

1. Press `Tab` during a single-player game.
2. Enter `nwcbilladen`.
3. Press `Enter`.

The code multiplies every currently owned resource by 10, up to the VCMI resource cap. It displays `BILLADENC4`, does not set the standard Cheater flag and does not disable score recording.

The desktop package also includes `Dragon Citadel Trainer.cmd`, a small button-based helper for sending common VCMI cheat codes to the active game window.

## Campaign Foundation

The native eight-scenario campaign is installed as `Content/Maps/Smocza_Cytadela.vcmp`. Open New Game > Campaign > Custom and select **Smocza Cytadela: Narodziny Ostatniej Burzy**. It includes Polish prologues, epilogues, 45 in-game story messages, current unit statistics and costs, and progressive recruitment restrictions. Chapter 5 demonstrates the Treasury and Royal Mint; chapter 8 requires a Grail-recruited final dragon. See `campaign/README.md` for build instructions and the limits of automated testing.

## Ongoing Development

Dragon Citadel will continue to be developed and updated on GitHub. Public players can use the VCMI repository link once the updated `main` branch contains the current files and screenshots.

## Balance

- level 1 and 2 prices are based on comparable Heroes III creatures
- Titans have reduced early-game statistics, growth of 1 and expensive dwellings
- level 5-7 dragons remain limited to 1 creature per week after building a Castle
- the level 8 line requires an endgame treasury and hundreds of every rare resource

## Information

- Author: Billaden
- Mod creator: Billaden - Jakubabuba
- Version: 1.5.7
- Languages: English by default, full Polish support
- Type: new VCMI town

## Polski

### Smocza Cytadela

Smocza Cytadela to autorskie, wyjątkowo drogie miasto końcowej fazy gry do Heroes III uruchamianego przez VCMI.

Wersja 1.5.7 naprawia datę miesięcznego przyrostu ostatnich smoków i wygląd skamienienia jednostek PNG. Zawiera osiem map kampanii z polskimi historiami, 45 wydarzeniami w grze i stopniowym odblokowywaniem jednostek. Kampanię uruchom przez Nowa gra > Kampania > Własne. Wybierz „Smocza Cytadela: Narodziny Ostatniej Burzy”.

Graal daje dodatkowo 10 000 złota i po 10 każdego surowca dziennie oraz bezpośrednio odblokowuje rekrutację poziomu 8. Nie ma osobnego budynku dla Smoka Ostatecznego. Smok Ostateczny kosztuje 150 000 złota oraz po 150 każdego surowca. Smok Absolutny kosztuje 220 000 złota oraz po 200 każdego surowca.

Z runtime BILLADENC4 jedna jednostka poziomu 8 pojawia się raz na miesiąc. Ten sam runtime uruchamia przyrost Rubinowego Golema o +2 Ataku, +1 Obrony i +10 Zdrowia po każdej zakończonej rundzie bitwy oraz nadpisywany autosave Smoczej Cytadeli co turę.

Projekt fanowski, niekomercyjny i niepowiązany z Ubisoft Entertainment ani właścicielami marki Heroes of Might and Magic.
