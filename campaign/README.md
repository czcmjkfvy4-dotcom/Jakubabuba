# Kampania: Smocza Cytadela

Version 1.5.7 includes eight native, self-contained VCMI campaign scenarios. The campaign is in Polish, with prologues, epilogues, 45 timed story messages and repeatable unit information on signposts. Unit statistics and prices are read directly from the mod configuration when building the maps.

The shipped file is `Content/Maps/Smocza_Cytadela.vcmp`. Start it through New Game > Campaign > Custom and select **Smocza Cytadela: Narodziny Ostatniej Burzy**. The individual maps are in `source/maps/`; they do not need to be installed separately. Restart VCMI after updating the mod.

Each chapter has a 36x36 surface map, three neutral enemy armies, three mines and a fixed starting hero/army. Earlier creature tiers remain available and their basic dwellings are prebuilt; higher tiers are forbidden. From chapter 4 a second settlement demonstrates the mutually exclusive Ruby Dragon branch. Chapter 5 requires the Royal Mint, 50000 gold and at least day 8. Chapter 8 begins with the Grail recovered in chapter 7, waits for the first monthly recruit on day 29, and requires a surviving Ultimate or Absolute Dragon. Hero armies reset between scenarios to preserve their authored balance. Losing Billaden loses the chapter.

Engine regressions verify all eight map starts, the seven sequential unlocks, 97 accessible objective locations, nonempty human story events, Grail recruitment restrictions and simulated victory/defeat conditions. The 20-30 minute target per map is a design target, not a timed human-playthrough result. Battle balance and visual composition still benefit from player testing.

## Opis kampanii

W świecie, w którym stare imperia dogasają pod ciężarem własnej pychy, a magia burz rozdziera niebo niczym gniew zapomnianych bogów, pojawia się nowa potęga. **Smocza Cytadela** nie jest zwykłym miastem — to monumentalna twierdza końca czasów, wzniesiona dla tych, którzy nie boją się poświęcić całych skarbców królestw w zamian za absolutną siłę.

Kampania opowiada historię narodzin tej przerażającej potęgi: od pierwszych eksperymentów z runiczną stalą i rubinową magią, przez ujarzmianie pradawnych bestii burzy, aż po przebudzenie smoków, które nie powinny nigdy powrócić na świat. Na drodze gracza staną upadające królestwa, zazdrośni magowie, fanatyczne zakony i armie, które zrobią wszystko, by nie dopuścić do wzniesienia ostatniej smoczej dynastii.

Każdy z ośmiu etapów kampanii prowadzi coraz głębiej w mroczne tajemnice Cytadeli. Zaczynając od walki o przetrwanie i zabezpieczenie pierwszych zasobów, gracz stopniowo odkryje sekrety Rubinowego Golema, potęgę Tytanów Burzy oraz znaczenie Graala — burzowej relikwii, bez której niemożliwe jest przywołanie najstraszliwszych istot tego świata. Dopiero zdobycie tej mocy otworzy drogę do rekrutacji dwóch legendarnych jednostek poziomu 8: **Smoka Ostatecznego** i **Smoka Absolutnego**.

To opowieść o ambicji większej niż rozsądek, o wojnie droższej niż wszystkie wcześniejsze wojny razem wzięte i o potędze, która nie zna kompromisów. Tutaj każde zwycięstwo kosztuje fortunę, ale każda przegrana może kosztować cały świat.

Czy zdołasz wznieść Smoczą Cytadelę ponad chmury, opanować burzę i poprowadzić ostatnie smoki do ostatecznego triumfu?

Czy też zginiesz, próbując ujarzmić siłę, która od początku nie była przeznaczona śmiertelnikom?

**Osiem etapów. Jedna Cytadela. Jedna burza. Jeden kres dla wszystkich, którzy staną ci na drodze.**

## Campaign Goals

- Introduce every Dragon Citadel creature gradually.
- Let the player learn the economy before reaching the level 8 dragon line.
- Use the Royal Dragon Mint as a difficult but real path toward the final dragon economy.
- Keep the town color visually consistent with the established Dragon Citadel palette regardless of player ownership.
- Keep each stage self-contained so development can continue safely in small steps.

## Included Stages

1. `stage-01-first-foundry.md` - Sharpshooters and Elite Sharpshooters.
2. `stage-02-golem-oath.md` - Gold, Diamond and Ruby Golems.
3. `stage-03-titan-halls.md` - Titans and Storm Titans.
4. `stage-04-split-grotto.md` - Faerie, Ruby and Ancient Ruby Dragons.
5. `stage-05-rust-and-storm.md` - Rust Dragons plus Treasury, Dragon Mint and Royal Dragon Mint economy.
6. `stage-06-azure-border.md` - Storm Dragons and Eternal Storm Dragons.
7. `stage-07-mint-of-kings.md` - Azure Dragons and Ancient Azure Dragons.
8. `stage-08-end-of-ages.md` - Grail, Ultimate Dragons and Absolute Dragons.

## Packing

Rebuild all maps and the archive with Python 3.8 or newer:

```powershell
python campaign/build_maps.py --templates campaign/source/native-templates.json
```

The template registry was exported from VCMI 1.7.5 with Dragon Citadel loaded; it contains identifiers and collision masks, not original game artwork. The older PowerShell packer can also repack the existing maps without regenerating them:

```powershell
.\campaign\build-campaign.ps1
```

If any stage map is missing, the script exits with a list of missing files and does not create a campaign package.

## Required Engine Support

Stock VCMI can load the town, creatures, buildings, screenshots and maps. BILLADENC4 is reserved for rules that data-only mods cannot express cleanly:

- exact monthly growth for level 8 dragons
- Ruby Golem round scaling in battle
- creator cheat code support
- future campaign-specific scripted rules
