# Krytyczny przegląd wersji grywalnej 1.5.8 — 26.10.2026

To raport potwierdzonych wyników, ograniczeń testów i wskazanych ocen graficznych. Nie jest gwarancją wykrycia wszystkich możliwych błędów.

## Testy wykonane ponownie po opublikowaniu kodu 1.5.8

- Walki z pierwszym strażnikiem w ośmiu rozdziałach: 8/8 PASS. Użyto prawdziwych armii i strażników z map, lecz przeniesiono strażnika do bohatera i wyłączono ekrany odprawy oraz warunki końca, aby wymusić walkę i odbiór wyniku. Nie jest to ręczne przejście kampanii. Szczegóły i ewentualne ostrzeżenia są w campaign-attacks/attacks.json.
- Natywne obliczenia 154 jednostek: 154/154 PASS. Sprawdzono obrażenia wręcz, stan obrony, trafienie nieśmiertelne i śmiertelne. Raport jawnie zawiera fullBattleActionProcessorTest=false. Nie przypisuję temu testowi potwierdzenia wszystkich umiejętności i animacji w żywej walce.
- Przed publikacją: czysta instalacja z archiwum, wybór języka i przełączenie trzecie → czwarte z grafiką → trzecie: PASS. Osiem rzeczywistych ekranów językowych: brak ERROR i WARN w ich logach. Obie lokalne instalacje dochodzą do menu.

## Niedociągnięcia i ryzyka

| Priorytet | Ustalenie | Rodzaj i znaczenie |
|---|---|---|
| P1 | Nie potwierdzono pełnego ręcznego przejścia ośmiu rozdziałów wraz z przenoszeniem bohaterów. | Luka odbioru kampanii. Cztery wcześniejsze próby AI nie zakończyły się w ograniczonym czasie. Timeout testu nie jest dowodem awarii, ale nie uprawnia do ogłoszenia całej kampanii ukończoną jakościowo. |
| P1 | Niestandardowe mechaniki wymagają BILLADENC4. | Ograniczenie zgodności. Sam standardowy menedżer modów VCMI nie instaluje tego silnika; dlatego zalecany jest pełny pakiet. Zgłoszenie do katalogu nie oznacza jeszcze dostępności domyślnej dla wszystkich. |
| P2 | Budynki special6: 28×30 px, special5: 32×30 px, special2: 34×34 px, silos: 36×34 px. | Potwierdzona geometria. Moja ocena: mimo dopasowania do tarasów są zbyt mało wyraziste przy ekranie 800×600. Mała sylwetka i podobieństwo do dekoracji utrudniają wyszukiwanie. |
| P2 | Fort, cytadela i zamek wykorzystują zaakceptowane grafiki eksportowane w rosnącej skali; nie wszystkie etapy oferują nową architekturę. | Ocena projektu. Wzrost 30% i stała kotwica są spełnione geometrycznie, lecz różnica form może być mniej satysfakcjonująca niż w oryginalnych zamkach. |
| P2 | Klikalne maski i podłoże sprawdzono geometrycznie, a nie testem użyteczności z graczami. | Luka odbioru. Brak wyjścia dolnego pasa nieprzezroczystych pikseli poza ręcznie wyznaczony wielokąt nie dowodzi naturalnego osadzenia całej bryły w perspektywie. |
| P2 | Tłumaczenia kampanii moda obejmują tekst maszynowy bez pełnej redakcji rodzimych użytkowników języków. | Potwierdzony proces. Technicznie rozwiązane klucze nie gwarantują dobrego stylu dialogów, terminologii i podziału długich tekstów w każdym oknie. |
| P2 | Pierwsze pobranie dużego pakietu językowego jest wykonywane synchronicznie z okna launchera. | Ustalenie z kodu. Okno może czekać na zakończenie operacji bez procentowego postępu. Instalacja pakietu i suma kontrolna działają; brak testu opóźnionej sieci i anulowania w połowie pobierania. |
| P2 | Audyt animacji i matematyki nie zastępuje obejrzenia 154 jednostek ze wszystkimi efektami w pełnej walce. | Luka testowa. Wcześniejsze renderowanie klatek potwierdza dostępność grup animacji; obrona może używać animacji trafienia zastępczego. Nie potwierdzono wzrokowo wszystkich kombinacji kierunku, tła, zaklęć i cieni. |
| P3 | Pakiety chiński, rosyjski, hiszpański i francuski mają mniej historycznych kluczy niż polski. | Różnica danych, nie potwierdzony błąd ekranowy. Braki obejmują nieużywane artefakty; dla trzech języków także core.xtrainfo.0–27. W sprawdzonych źródłach lib/client ta tabela jest rejestrowana, lecz nie ma dalszych odwołań. Nie obniżam z tego powodu wyniku widocznego interfejsu. |

## Co należy uznać za nadal niepotwierdzone

Pełny balans ekonomii, poziom trudności wszystkich dróg zwycięstwa, długie sesje bez awarii, pełny zestaw zapis/wczytanie między rozdziałami, rozgrywka sieciowa, wszystkie rozdzielczości i skale UI oraz pełny dubbing w ośmiu językach. Wykonane próby nie uprawniają do określenia kampanii jako najlepszej ze wszystkich dostępnych.

## Zalecana kolejność dalszych prac

1. Pełne ręczne przejście kampanii z zapisem i wczytywaniem między rozdziałami.
2. Zwiększenie rozpoznawalności małych budowli, bez przesuwania kotwic i bez wychodzenia poza tarasy; kontrola na rzeczywistym ekranie gry.
3. Redakcja językowa kampanii i sprawdzenie długich dialogów oraz podpowiedzi.
4. Nieblokujący przebieg pobierania języka z postępem i anulowaniem.
5. Rozszerzenie rzeczywistych walk o efekty specjalne, wszystkie nowe jednostki i rozgrywkę sieciową.
