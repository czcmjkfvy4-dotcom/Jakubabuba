"""Build the eight native VCMI scenarios and their campaign archive.

Templates must come from DragonCampaignRegression --export with the matching mod.
No Heroes III graphics or original game data are embedded in these archives.
"""
import argparse
import copy
import json
import random
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ['wood', 'mercury', 'ore', 'sulfur', 'crystal', 'gems']
RESOURCE_NAMES = dict(zip(RESOURCES + ['gold'], ['drewna', 'rtęci', 'rudy', 'siarki', 'kryształów', 'klejnotów', 'złota']))
TIERS = [
    ['dcSharpshooter', 'dcEnchanter'],
    ['dcGoldGolem', 'dcDiamondGolem', 'dcRubyGolem'],
    ['dcGiant', 'dcTitan'],
    ['dcFirebird', 'dcPhoenix', 'dcFairieDragon', 'dcCrystalDragon'],
    ['dcGoldDragon', 'dcBlackDragon'],
    ['dcStormDragon', 'dcEternalStormDragon'],
    ['dcRustDragon', 'dcAzureDragon'],
    ['dcUltimateDragon', 'dcAbsoluteDragon'],
]
STORIES = [
    ('Iskra Cytadeli',
     'Stare imperium żąda ostatniego podatku od doliny, która nie ma już czego oddać. Billaden gromadzi ocalałych przy niedokończonej Cytadeli. Nie ma smoków. Są kusznicy, kuźnia i decyzja, że następny poborca nie wróci do domu.',
     'Ostrostrzelcy wywodzą się z łowców pilnujących dawnych smoczych szlaków. Ich runiczne kusze zachowują siłę na całym polu bitwy: nie ponoszą kary za odległość ani mury. Elitarni nie tracą też skuteczności w walce wręcz. Cena oznacza lata szkolenia i koszt amunicji, nie liczbę piór przy hełmie.',
     'Zajmij tartak, kopalnię rudy i kopalnię złota. Rozbij trzy posterunki imperium. Rozdział kończy się najwcześniej piątego dnia, po odprawach o jednostkach.',
     'Poborca drwił z miasta bez smoków. Poległ pod pierwszą salwą. Nad odzyskaną doliną wznosi się dym odlewni: następnym razem łucznicy nie będą walczyć sami.'),
    ('Złote Rdzenie',
     'Pod doliną znaleziono matryce armii starszej niż imperium. Odlewnicy potrafią obudzić złoto, ale do jego przemiany potrzebują rudy i rubinowego serca. Królewska piechota maszeruje zniszczyć formy, zanim te nauczą się chodzić.',
     'Złote i Diamentowe Golemy są nieożywione. Redukują obrażenia od zaklęć odpowiednio o 85% i 95%; nie jest to odporność na każdy efekt magiczny. Trzecie ulepszenie, Rubinowy Golem, zaczyna z Atakiem 10, Obroną 10 i 100 PŻ. Po każdej ukończonej rundzie otrzymuje +2 Ataku, +1 Obrony i +10 maksymalnych PŻ. Premia trwa tylko w tej bitwie. Rdzeń rośnie w siłę pod obciążeniem, dlatego kosztuje kryształ i rudę.',
     'Odzyskaj trzy kopalnie, zbuduj Rubinową Odlewnię i pokonaj trzy oddziały interwencyjne. Zostaw miejsce w armii na nowe ulepszenie.',
     'Kamień nie uciekł. Rubinowe serce wytrzymało. Ostatni piechur zobaczył, jak pęknięcia golema zasklepia światło, a z gór odpowiedział odległy grzmot.'),
    ('Przysięga Tytanów',
     'Magowie próbują zamknąć burzę w trzech górniczych rdzeniach. Uwięzieni Tytani słyszą każdy ich obrót. Billaden oferuje im wolność, a nie posłuszeństwo. W zamian prosi, aby stanęli na murach Cytadeli.',
     'Tytan walczy wręcz; ulepszony Tytan Burzy strzela i nie ponosi kary w zwarciu. Obaj są odporni na zaklęcia umysłu. Klejnoty w ich cenie utrzymują energię rdzenia. Golem ma osłonić strzelającego Tytana, a nie konkurować z nim o pierwszy cios.',
     'Odbij trzy kopalnie z rdzeniami, rozbij straże i maga. Zbuduj Wieżę Tytanów Burzy, aby przypieczętować przysięgę.',
     'Magowie zamknęli piorun w krysztale. Tytani rozbili kryształ i niebo odpowiedziało. Teraz trzeba znaleźć istoty, które potrafią żyć w takiej magii.'),
    ('Groty Pękniętej Magii',
     'W jednej grocie magia śmieje się i zmienia kształt; w drugiej krzepnie w rubin. Zakon Czystego Płomienia chce spalić obie. Dwie osady Cytadeli muszą osłonić dwa różne smocze rody.',
     'Czarodziejskie Smoki latają, rzucają zaklęcia i odbijają część wrogiej magii. Rubinowe Smoki poruszają się po ziemi, stawiają opór magii i są odporne na szkołę ognia. Groty wykluczają się w jednym mieście. Druga osada na wschodzie pozwala tutaj poznać obie linie, nie zmieniając zasad moda. Klejnoty karmią magię, kryształy budują rubinowy pancerz.',
     'Ocal oba smocze rody: zbuduj ulepszoną grotę magii w głównej Cytadeli i ulepszoną grotę rubinu we wschodniej osadzie. Odzyskaj kopalnie i rozbij trzy oddziały zakonu.',
     'Zakon chciał jednej barwy ognia. Dwie groty odpowiedziały dwiema różnymi potęgami. Zwycięstwo kosztowało więcej niż cała pierwsza dolina.'),
    ('Skarbnica Burzy',
     'Wojny nie przegrywa się tylko na polu bitwy. Smoki potrzebują metalu i siarki, Tytani klejnotów, a kupcy chcą złota przed dostawą. Królewski poborca odciął trzy szlaki zaopatrzenia. Tym razem Billaden musi pokonać także pusty skarbiec.',
     'Rdzawe Smoki latają, zioną przez dwa pola i używają żrącego ataku. Pradawna odmiana wzmacnia tę rolę. Nie ustawiaj sojusznika za celem smoczego oddechu. Siarka w cenie nie jest ozdobą: armia płaci za paliwo i odtworzenie niszczycielskich wydzielin.',
     'Odzyskaj trzy kopalnie, pokonaj poborcę i jego straże. Zbuduj Królewską Smoczą Mennicę i zachowaj co najmniej 50000 złota. Zwycięstwo jest możliwe od dnia 8, aby Skarbiec zdążył wypłacić pierwsze odsetki.',
     'Poborca szukał skrzyń. Znalazł złoto, które chodzi, lata i pali. Cytadela może finansować następną wojnę; po raz pierwszy cena ostatecznej potęgi przestaje być wyłącznie legendą.'),
    ('Nadciąga Wieczna Burza',
     'Pioruny wracają do gór co noc i nie gasną o świcie. Trzy oddziały królewskiej konnicy odcięły przewodniki energii przy kopalniach. Billaden musi przywrócić przepływ, zanim burza rozerwie Cytadelę od środka.',
     'Smok Burzy i Smok Wiecznej Burzy latają, zioną przez dwa pola i mają odporność na zaklęcia poziomów 1-5. To nie czyni ich odpornymi na miecz lub strzałę. Rtęć utrzymuje przewodniki w ich leżu, a rzadkie surowce płacą za ujarzmienie pogody. Szybkość daje wybór celu, nie obowiązek samotnej szarży.',
     'Przywróć trzy kopalnie-przewodniki, zbuduj Oko Wiecznej Burzy i rozbij trzy oddziały konnicy. Starsze jednostki pozostają dostępne.',
     'Konnica nigdy wcześniej nie przegrała wyścigu. Burza nie ścigała koni. Czekała już na końcu przełęczy.'),
    ('Błękitny Tron',
     'Ostatni sojusz królów ukrył relikwię burzy za Błękitnym Tronem. Pradawne smoki zgadzają się przeprowadzić Billadena, lecz za ich cień trzeba zapłacić więcej niż za koronę. Anielskie straże nie zamierzają oddać relikwii.',
     'Błękitne i Pradawne Błękitne Smoki latają, sieją strach i zioną przez dwa pola. Są odporne na zaklęcia poziomów 1-3, nie na wszelką magię. Ich cena odzwierciedla trwałość i presję na morale przeciwnika. Nie zastępuj nimi gospodarki: kolejny rozdział wystawi rachunek większy niż wszystkie poprzednie.',
     'Odbij trzy źródła surowców, zbuduj sanktuarium Pradawnych Błękitnych Smoków i pokonaj trzy straże Tronu. Relikwia zostanie przewieziona do Cytadeli w zakończeniu rozdziału.',
     'Na tronie nie leżała korona. Leżało serce burzy. Billaden kazał wieźć Graala do Cytadeli, choć Tytani odwrócili wzrok. Ostatnie drzwi powinny pozostać zamknięte.'),
    ('Serce Końca Wieków',
     'Graal zdobyty przy Błękitnym Tronie został osadzony w Cytadeli. Daje 10000 złota i po 10 każdego surowca dziennie, ale nie rozdaje smoków. Pierwsze przebudzenie nastąpi dnia 29, na początku drugiego miesiąca. Do tego czasu trzeba odbić kopalnie i pokonać przednie straże ostatniego sojuszu.',
     'Smok Ostateczny kosztuje 150000 złota i po 150 każdego surowca; Smok Absolutny 220000 i po 200. Wspólna pula rekrutacji rośnie o jedną sztukę miesięcznie. Możesz wybrać jedną odmianę, nie dwie. Smoki nie kontratakują i blokują kontratak celu, ale nadal mogą otrzymywać zwykłe obrażenia. Uderzają wokół siebie i zioną przez dwa pola. Cena płaci za potęgę, nie za nieśmiertelność.',
     'Zajmij trzy kopalnie, pokonaj obie straże oraz ostatnią armię na południowym wschodzie. Zakończ rozdział z co najmniej jednym Smokiem Ostatecznym lub Absolutnym w armii. Rekrutacja od dnia 29; ulepszenia i wcześniejsze poziomy pozostają dostępne.',
     'Niebo pękło, lecz Cytadela stoi. Ostatni smok otworzył oczy, a świat zrozumiał, dlaczego ta wojna kosztowała fortunę. Osiem etapów. Jedna Cytadela. Jedna burza. Teraz ktoś będzie musiał nauczyć się żyć w jej cieniu.'),
]
ECONOMY = 'Smoczy Skarbiec nalicza 10% posiadanego złota co 7 dni. Smocza Mennica daje 4000 złota dziennie, Królewska Mennica 5000 i po 1 każdego surowca. Dochód sprawdzisz w mieście. Nie wydawaj całej rezerwy przed początkiem nowego tygodnia: mniejsza rezerwa oznacza mniejsze odsetki.'


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write_zip(path, files):
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, data in files.items():
            archive.writestr(name, data if isinstance(data, bytes) else json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))


def stat_text(creature):
    cost = ', '.join(f'{value} {RESOURCE_NAMES[key]}' for key, value in creature['cost'].items())
    return (f"{creature['name']['singular']}: Atak {creature['attack']}, Obrona {creature['defense']}, "
            f"PŻ {creature['hitPoints']}, obrażenia {creature['damage']['min']}-{creature['damage']['max']}, "
            f"szybkość {creature['speed']}. Koszt 1 sztuki: {cost}.")


def event(day, name, text, resources=None):
    return dict(name=name, message=text, players=['red'], humanAffected=1, computerAffected=0,
                firstOccurrence=day-1, nextOccurrence=0, resources=resources or {})


def build(args):
    templates = load(args.templates)
    creatures = load(ROOT/'Content/config/dragon-citadel/creatures.json')
    faction = load(ROOT/'Content/config/dragon-citadel/faction.json')['dragonCitadel']['town']
    campaign = load(ROOT/'campaign/source/header.json')
    campaign.update(name='Smocza Cytadela: Narodziny Ostatniej Burzy', campaignVersion='1.5.7',
                    description='Osiem krótkich rozdziałów o narodzinach przerażającej, potężnej i kosztownej Cytadeli. Jednostki odblokowywane stopniowo; polska historia i odprawy widoczne w grze.',
                    allowDifficultySelection=False)
    campaign['regions'] = dict(prefix='AR', colorSuffixLength=2, desc=[dict(infix=letter, x=x, y=y)
        for letter, (x, y) in zip('ABCDEFGH', [(135,238),(135,121),(206,155),(105,397),(109,275),(158,188),(200,261),(232,197)])])
    maps = {}
    for chapter in range(1, 9):
        title, intro, lore, objective, ending = STORIES[chapter-1]
        objects = []
        occupied = set()

        def obj(kind, subtype, name, x, y, options=None, anchor=False):
            template = copy.deepcopy(templates[f'{kind}/{subtype}'])
            mask = template['mask']
            if not anchor:
                points = [(col, row) for row, line in enumerate(mask) for col, char in enumerate(line) if char == 'A']
                if points:
                    col, row = points[0]
                    x += len(mask[0])-1-col
                    y += len(mask)-1-row
            for row, line in enumerate(mask):
                for col, char in enumerate(line):
                    if char != 'V':
                        occupied.add((x-len(line)+1+col, y-len(mask)+1+row))
            result = dict(instanceName=name, type=kind, subtype=subtype, x=x, y=y, l=0,
                          template=template, options=options or {})
            objects.append(result)
            return result

        base = ['villageHall','townHall','cityHall','tavern','fort','marketplace','blacksmith','mageGuild1']
        if chapter >= 3: base += ['mageGuild2','mageGuild3']
        if chapter >= 5: base += ['capitol','resourceSilo','special3','special5']
        if chapter >= 7: base += ['citadel','castle','mageGuild4','mageGuild5']
        if chapter == 8: base += ['grail','special6','dwellingLvl8','dwellingUpLvl8']
        base += [f'dwellingLvl{n}' for n in range(1,min(chapter,7)+1)]
        locked = [name for name in faction['buildings'] if (match := re.search(r'Lvl(\d+)$',name)) and int(match[1]) > chapter]
        town_options = dict(owner='red', buildings={'allOf':['dragon-citadel:'+b for b in base],
                                                     'noneOf':['dragon-citadel:'+b for b in locked]})
        obj('town','dragon-citadel:dragonCitadel','citadel',6,7,town_options)
        if chapter >= 4:
            alternate = copy.deepcopy(town_options)
            alternate['buildings']['allOf'].remove('dragon-citadel:dwellingLvl4')
            alternate['buildings']['allOf'].append('dragon-citadel:dwellingUp2Lvl4')
            if chapter == 8:
                for building in ['grail','dwellingLvl8','dwellingUpLvl8']:
                    alternate['buildings']['allOf'].remove('dragon-citadel:'+building)
            obj('town','dragon-citadel:dragonCitadel','ruby_outpost',28,9,alternate)
        armies = [
            [('dcSharpshooter',14)],
            [('dcSharpshooter',14),('dcGoldGolem',8)],
            [('dcEnchanter',16),('dcRubyGolem',8),('dcGiant',3)],
            [('dcEnchanter',18),('dcRubyGolem',8),('dcTitan',3),('dcFirebird',2),('dcFairieDragon',2)],
            [('dcEnchanter',20),('dcRubyGolem',10),('dcTitan',3),('dcPhoenix',2),('dcGoldDragon',3)],
            [('dcEnchanter',22),('dcRubyGolem',10),('dcTitan',4),('dcBlackDragon',3),('dcStormDragon',3)],
            [('dcEnchanter',24),('dcRubyGolem',12),('dcTitan',5),('dcEternalStormDragon',3),('dcRustDragon',3)],
            [('dcEnchanter',24),('dcRubyGolem',12),('dcTitan',5),('dcEternalStormDragon',4),('dcAzureDragon',4)],
        ]
        obj('hero','dragon-citadel:dragonLord','hero_billaden',6,8,
            dict(owner='red', type='dragon-citadel:billaden', experience=0,
                 army=[dict(type='dragon-citadel:'+name, amount=count) for name,count in armies[chapter-1]]))
        mine_positions = [(12,12),(24,16),(29,26)]
        for index, (kind, (x,y)) in enumerate(zip(['sawmill','orePit','goldMine'],mine_positions)):
            obj('mine',kind,f'mine_{index}',x,y,dict(owner='neutral'))
        encounters = [
            [('pikeman',18),('archer',10),('halberdier',25)],
            [('swordsman',12),('mage',8),('crusader',18)],
            [('crusader',18),('monk',12),('mage',25)],
            [('cavalier',10),('mage',25),('champion',15)],
            [('champion',12),('monk',30),('angel',12)],
            [('champion',20),('cavalier',30),('blackDragon',12)],
            [('angel',18),('blackDragon',15),('archangel',16)],
            [('angel',20),('blackDragon',18),('archangel',30)],
        ]
        for i, ((unit, amount), (x,y)) in enumerate(zip(encounters[chapter-1],[(13,11),(22,22),(29,30)])):
            obj('monster',unit,f'enemy_{i}',x,y,dict(character='savage',amount=amount,noGrowing=True,neverFlees=True,
                rewardResources=dict(gold=chapter*2000),rewardMessage=ending if i==2 else 'Odzyskane zapasy wracają do Cytadeli. Dowódca wskazuje następny posterunek na południowym wschodzie.'))
        obj('sign','object','orders',8,9,dict(text=intro+'\n\n'+objective))
        obj('sign','object','final_warning',27,29,dict(text='Ostatnia armia czeka na południowym wschodzie.\n\n'+objective))
        for i, creature_id in enumerate(TIERS[chapter-1]):
            obj('sign','object',f'unit_guide_{i}',9+i*2,6,dict(text=stat_text(creatures[creature_id])+'\n\n'+lore))
        if chapter == 5:
            obj('sign','object','treasury_guide',9,8,dict(text=ECONOMY))
        for i, (x,y) in enumerate([(10,14),(17,18),(25,27)]):
            obj('resource','gold',f'supplies_{i}',x,y,dict(amount=chapter*2000))
        # Landscape obstacles stay outside generous corridors around every playable location.
        playable = [(o['x'],o['y']) for o in objects]
        rng = random.Random(1570+chapter)
        for i in range(90):
            x,y = rng.randrange(3,36),rng.randrange(3,36)
            if any(abs(x-px)<5 and abs(y-py)<4 for px,py in playable): continue
            kind = ['oakTrees','pineTrees','rock','mountain'][(chapter+i)%4]
            template = templates[f'{kind}/object']
            mask=template['mask']
            footprint={(x-len(line)+1+c,y-len(mask)+1+r) for r,line in enumerate(mask) for c,ch in enumerate(line) if ch!='V'}
            if footprint & occupied: continue
            obj(kind,'object',f'landscape_{i}',x,y,anchor=True)

        stats = [stat_text(creatures[c]) for c in TIERS[chapter-1]]
        treasury_lesson = ECONOMY if chapter==5 else 'Każda moneta wydana na nową jednostkę znika z rezerwy na odsetki i kolejne ulepszenia. Nie trzeba rekrutować całego dostępnego przyrostu.'
        budget = [15000,35000,60000,120000,100000,180000,220000,140000][chapter-1]
        resources = {r: (35 if chapter<4 else 100) for r in RESOURCES}
        resources['gold']=budget
        events=[event(1,'Odprawa',intro+'\n\n'+objective,resources),event(2,'Pochodzenie',lore),
                event(3,'Jednostki podstawowe','\n\n'.join(stats[::2])),event(4,'Ulepszenia','\n\n'.join(stats[1::2])),
                event(5,'Cena potęgi',treasury_lesson)]
        if chapter==5: events.append(event(8,'Pierwsze odsetki','Rozpoczął się nowy tydzień. Skarbiec naliczył odsetki od twojej rezerwy. Po zbudowaniu Królewskiej Mennicy zachowaj 50000 złota i dokończ odzyskiwanie kopalni.'))
        if chapter==8:
            events += [event(8,'Rachunek Graala','Graal pracuje codziennie. Ostatnie smoki nie korzystają z tygodniowego przyrostu. Jedna wspólna sztuka pojawi się dnia 29.'),
                       event(15,'Głosy pod miastem','Od dwóch tygodni pod miastem słychać oddech. Sprawdź zapasy: 150 każdego surowca i 150000 złota na Smoka Ostatecznego albo 200 i 220000 na Absolutnego.'),
                       event(22,'Ostatnia pieczęć','Za tydzień nastąpi przebudzenie. Powróć bohaterem do Cytadeli z Graalem, zostaw wolne miejsce w armii i przygotuj się na finał.'),
                       event(29,'Przebudzenie','Pierwszy dzień drugiego miesiąca. Graal udostępnił JEDNEGO ostatniego smoka we wspólnej puli. Wybierz Ostatecznego albo Absolutnego. Każdy może otrzymać obrażenia; żaden nie kontratakuje.')]
        conditions = [['destroy',dict(type='monster',object=f'enemy_{i}',position=[x,y,0])] for i,(x,y) in enumerate([(13,11),(22,22),(29,30)])]
        conditions += [['control',dict(type='mine',object=f'mine_{i}',position=[x,y,0])] for i,(x,y) in enumerate(mine_positions)]
        conditions += [['daysPassed',dict(value=7 if chapter==5 else 4)]]
        # Native BuildingID values are taken from the exported engine building registry.
        required = {2:['dwellingUp2Lvl2'],3:['dwellingUpLvl3'],4:['dwellingUpLvl4','dwellingUp3Lvl4'],5:['special6'],6:['dwellingUpLvl6'],7:['dwellingUpLvl7']}.get(chapter,[])
        ids=templates['buildingIDs']
        for name in required: conditions.append(['haveBuilding',dict(type=ids[name])])
        if chapter==5: conditions.append(['haveResources',dict(type='gold',value=50000)])
        if chapter==8: conditions.append(['anyOf',*[['haveCreatures',dict(type='dragon-citadel:'+unit,value=1)] for unit in TIERS[7]]])
        header=dict(versionMajor=3,versionMinor=0,name=f'{chapter:02d}. {title}',description=intro+'\n\n'+objective,
                    author='Billaden',mapVersion='1.5.7',difficulty='NORMAL',battleOnly=False,
                    mapLevels=dict(surface=dict(height=36,width=36,index=0,layer='core:surface')),
                    allowedHeroes=dict(anyOf=['dragon-citadel:billaden']),
                    players=dict(red=dict(allowedFactions=dict(anyOf=['dragon-citadel:dragonCitadel']),canPlay='PlayerOnly',
                                          mainHero='hero_billaden',mainTown=dict(generateHero=False,x=6,y=7,l=0))),
                    events=events,rumors=[],teams=[],victoryIconIndex=0,defeatIconIndex=0,victoryMessage=objective,
                    defeatMessage='Billaden poległ. Cytadela nie przetrwa bez swego władcy.',
                    triggeredEvents=dict(campaignVictory=dict(condition=['allOf',*conditions],message=ending,description=objective,effect=dict(type='victory',messageToSend='')),
                                         campaignDefeat=dict(condition=['anyOf',['daysWithoutTown',dict(value=7)],['noneOf',['control',dict(type='hero',object='hero_billaden',position=[6,8,0])]]],message='Billaden poległ albo Cytadela upadła. Burza pozostaje nieujarzmiona.',effect=dict(type='defeat',messageToSend=''))))
        terrain=[[f'gr{rng.randrange(49,73)}_' for x in range(36)] for y in range(36)]
        # Preserve the native terrain container structure used by VCMI 1.7.5.
        scenario=campaign['scenarios'][chapter-1]
        name=scenario['map']+'.vmap'
        path=ROOT/'campaign/source'/name
        write_zip(path,{'header.json':header,'objects.json':objects,'surface_terrain.json':terrain})
        maps[name]=path.read_bytes()
        scenario.update(preconditions=list(range(chapter-1)),difficulty=0,color=chapter-1,
                        regionText=f'{chapter}. {title}\n{objective}',prolog=dict(text=intro),epilog=dict(text=ending),
                        heroKeeps=[],keepCreatures=[],startOptions='none',playerColor=0)
        for install in args.install:
            target=Path(install)/'Content/Maps'/f'DC_{chapter:02d}.vmap'
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(path,target)
        print(f'BUILT chapter {chapter}: {len(objects)} objects, {len(events)} story events, {len(locked)} forbidden dwellings',flush=True)
    write_zip(ROOT/'Content/Maps/Smocza_Cytadela.vcmp',{'header.json':campaign,**maps})
    (ROOT/'campaign/source/header.json').write_text(json.dumps(campaign,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for install in args.install:
        shutil.copy2(ROOT/'Content/Maps/Smocza_Cytadela.vcmp',Path(install)/'Content/Maps/Smocza_Cytadela.vcmp')
    print('PACKED and installed native eight-stage campaign',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--templates',required=True)
    parser.add_argument('--install',action='append',default=[])
    build(parser.parse_args())
