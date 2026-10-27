# Smocza Cytadela 1.5.9 — grywalne wydanie rozwojowe

Prace nad wyglądem Smoczej Cytadeli są w toku. Wydanie nie ma certyfikacji pełnego ręcznego przejścia kampanii ani pełnej korekty językowej.

## Instalacja

Rozpakuj archiwum i uruchom Windows PowerShell w jego katalogu:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Install-Dragon-Citadel.ps1 -DataSource "C:\Moje gry\Heroes III\Data" -Language polish
```

Podaj katalog Data własnej instalacji Heroes III Complete / Shadow of Death albo VCMI. Oryginalne dane gry nie są dołączone. Instalator sprawdza sumy SHA-256 i importuje dane lokalnie. Domyślna lokalizacja: %LOCALAPPDATA%\Programs\Dragon Citadel Projects; osobny profil: podkatalog Profile. Parametry -Destination oraz -NoShortcut zmieniają lokalizację i pomijają skrót. Zmieniane pliki przy aktualizacji trafiają do .backups.

## Osiem języków całej gry i moda

Dostępne są Polski, English, Deutsch, 简体中文, 日本語, Русский, Español i Français. Wybierz język w dołączonym launcherze, następnie zapisz ustawienia albo uruchom grę. Teksty launchera zmieniają się wraz z wyborem. Parametr -Language akceptuje polish, english, german, chinese, japanese, russian, spanish, french; wartość Keep zachowuje ustawienie i jest dostępna w wierszu poleceń.

Przy pierwszym wyborze każdego języka, także angielskiego, pobierany jest odpowiedni pakiet tłumaczenia podstawowej gry bezpośrednio z wydania wskazanego w oficjalnym katalogu VCMI 1.7. Wymagany jest internet. Sprawdzana jest przypięta suma SHA-256; kolejne uruchomienia korzystają z zainstalowanych plików. Angielski również ma osobny pakiet tłumaczeń bazowych. Przełączaj język tym launcherem, aby jednocześnie włączyć poprawny pakiet bazowy i fonty.

Tłumaczenia społecznościowe zachowują autorstwo i warunki źródeł. Japoński pakiet zawiera oznaczony przez autora komponent AI dla map i Chronicles. Teksty kampanii Smoczej Cytadeli obejmują tłumaczenie maszynowe z poprawkami. Nie deklarujemy pełnego dubbingu ośmiu języków ani tłumaczenia dowolnych dodatkowych modów.

## Ulepszenia i silnik

Trzecie formy są integralną częścią moda. Czwarte formy oraz dodatkowe krajobrazy bitew są opcjonalnymi submodami i domyślnie są wyłączone. Można użyć -Fourth oraz -Graphics podczas instalacji lub odpowiednich opcji launchera. Wygląd drugiej i trzeciej formy łucznika Cytadeli jest zamieniony zgodnie ze zmianą projektu.

Pakiet zawiera pasujący silnik BILLADENC4 oparty na VCMI 1.7.5. Jest on wymagany do niestandardowej rekrutacji miesięcznej smoków i mechanik Rubinowego Golema. Sam standardowy menedżer modów VCMI nie wymienia silnika. Nie mieszaj klienta, serwera i biblioteki ze starszych wydań.

## Grafika i dowody testów

47 stanów budynków Cytadeli używa stałych kotwic rodzin. Fort → cytadela → zamek: skale 1 / 1,30 / 1,69. Zachowano tło i jasność; maski i dolne pasy podstaw sprawdzono względem wyznaczonych tarasów. Nie jest to gwarancja końcowej jakości artystycznej. Testy tekstów, map, ekranów i czystej instalacji mają ograniczony zakres; pełny raport oraz rzeczywiste zrzuty są w repozytorium, katalog qa-1.5.9.

## Licencje i źródła

BILLADENC4-corresponding-source.zip zawiera odpowiadające źródła silnika. Informacje o autorach i licencjach zachowano w payload/licenses i metadanych submodów. H3Landscape: MIT; materiały TUM: oznaczenia i autorzy w TUM-RESOURCE-CREDITS.txt; Noto: OFL. Ten pakiet nie stanowi potwierdzenia praw do sprzedaży materiałów osób trzecich.
