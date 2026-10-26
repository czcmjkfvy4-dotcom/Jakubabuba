# Cała gra w ośmiu językach — stan potwierdzony 26.10.2026

Przygotowano wybór polskiego, angielskiego, niemieckiego, chińskiego uproszczonego, japońskiego, rosyjskiego, hiszpańskiego i francuskiego. W obu lokalnych instalacjach znajdują się pakiety bazowe z katalogu VCMI 1.7. Ustawienie języka w launcherze włącza jeden właściwy pakiet bazowy, słowniki Smoczej Cytadeli i odpowiednie fonty. Napisy launchera również zmieniają język. Angielski korzysta z angielskich danych bazowych użytkownika.

Test natywny: osiem języków PASS; w każdym 1131 wpisów moda oraz osiem map samodzielnych i osiem map wewnątrz kampanii. Dodatkowo sprawdzono dokładne wartości 6415–6453 wpisów podstawowej gry w każdym z siedmiu dodatkowych języków. Dopuszczono wyłącznie nadpisania zgodne ze sprawdzonym drugim słownikiem VCMI. Różne rosyjskie nazwy magazynów pochodzą z tego słownika, nie są brakiem tłumaczenia.

Wykonano osiem zrzutów rzeczywistego interfejsu miasta. Logi tych prób oraz uruchomienie menu obu instalacji nie zawierają ERROR ani WARN. Test wszystkich ośmiu wyborów w oknie launchera przeszedł; wykryty problem przekazywania wartości z listy został naprawiony. Sprawdzono także pobranie pakietu chińskiego do pustej lokalizacji, sumę SHA-256 i rozpakowanie. Pakiety pozostałych języków pobrano i zweryfikowano przed instalacją lokalną.

Pakiet dystrybucyjny pobiera tłumaczenie bazowe bezpośrednio ze wskazanego w katalogu VCMI wydania GitHub po pierwszym wyborze języka. Wymaga wtedy internetu. Nie dołącza oryginalnych archiwów gry. W obecnych dwóch lokalnych instalacjach siedem pakietów jest już dostępnych. Zmiany profili ograniczono do włączenia tłumaczenia obecnego języka, zachowano istniejące wybory i kopie ustawień.

Ograniczenia: nie wykonano oceny każdego zdania przez rodzimych użytkowników ośmiu języków ani pełnego ręcznego przejścia kampanii. Teksty kampanii moda obejmują tłumaczenia maszynowe wymagające redakcji. Japoński pakiet społecznościowy zawiera oznaczony przez autora komponent AI dla map i Chronicles, włączany przez selektor. Nie oznacza to gwarancji pełnego dubbingu ośmiu języków ani tłumaczenia dowolnych obcych modów. Prace nad wyglądem Smoczej Cytadeli są nadal w toku.

Dowody: native-report.json, native-*.json, launcher/report.json, installed-startup/, actual-language-windows/. Galeria: JEZYKI-CALEJ-GRY.html.
