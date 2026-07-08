"""
FIFA World Cup 2026 - Realistic Synthetic Dataset Generator
Generates 4 CSV files:
  data/raw/fifa2026/wc2026_teams.csv    (48 nations)
  data/raw/fifa2026/wc2026_matches.csv  (104 matches)
  data/raw/fifa2026/wc2026_players.csv  (200 players)
  data/raw/fifa2026/wc2026_groups.csv   (48 group standings)
"""

import os, random
import numpy as np
import pandas as pd
from itertools import combinations
from datetime import date, timedelta

random.seed(42)
np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'fifa2026')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────
# 1. TEAM DEFINITIONS  (48 nations)
# ─────────────────────────────────────────────────────────
TEAMS = {
    # Group A
    'United States': {'conf':'CONCACAF','group':'A','rank':15,'elo':1845,'coach':'Mauricio Pochettino','host':True},
    'England':       {'conf':'UEFA',    'group':'A','rank': 3,'elo':2020,'coach':'Gareth Southgate',   'host':False},
    'Panama':        {'conf':'CONCACAF','group':'A','rank':38,'elo':1615,'coach':'Thomas Christiansen','host':False},
    'Tunisia':       {'conf':'CAF',     'group':'A','rank':31,'elo':1680,'coach':'Jalel Kadri',        'host':False},
    # Group B
    'Mexico':        {'conf':'CONCACAF','group':'B','rank':22,'elo':1760,'coach':'Javier Aguirre',     'host':True},
    'Argentina':     {'conf':'CONMEBOL','group':'B','rank': 2,'elo':2080,'coach':'Lionel Scaloni',     'host':False},
    'Ecuador':       {'conf':'CONMEBOL','group':'B','rank':27,'elo':1720,'coach':'Sebastian Beccacece','host':False},
    'Morocco':       {'conf':'CAF',     'group':'B','rank':12,'elo':1880,'coach':'Walid Regragui',     'host':False},
    # Group C
    'Canada':        {'conf':'CONCACAF','group':'C','rank':28,'elo':1710,'coach':'Jesse Marsch',       'host':True},
    'Germany':       {'conf':'UEFA',    'group':'C','rank': 9,'elo':1955,'coach':'Julian Nagelsmann',  'host':False},
    'South Korea':   {'conf':'AFC',     'group':'C','rank':21,'elo':1775,'coach':'Hong Myung-bo',      'host':False},
    'Ivory Coast':   {'conf':'CAF',     'group':'C','rank':33,'elo':1645,'coach':'Emerse Fae',         'host':False},
    # Group D
    'Brazil':        {'conf':'CONMEBOL','group':'D','rank': 4,'elo':2010,'coach':'Fernando Diniz',     'host':False},
    'France':        {'conf':'UEFA',    'group':'D','rank': 1,'elo':2090,'coach':'Didier Deschamps',   'host':False},
    'Japan':         {'conf':'AFC',     'group':'D','rank':19,'elo':1800,'coach':'Hajime Moriyasu',    'host':False},
    'Cameroon':      {'conf':'CAF',     'group':'D','rank':34,'elo':1640,'coach':'Rigobert Song',      'host':False},
    # Group E
    'Spain':         {'conf':'UEFA',    'group':'E','rank': 8,'elo':1960,'coach':'Luis de la Fuente',  'host':False},
    'Portugal':      {'conf':'UEFA',    'group':'E','rank': 6,'elo':1980,'coach':'Roberto Martinez',   'host':False},
    'Australia':     {'conf':'AFC',     'group':'E','rank':30,'elo':1695,'coach':'Tony Popovic',       'host':False},
    'Senegal':       {'conf':'CAF',     'group':'E','rank':20,'elo':1790,'coach':'Aliou Cisse',        'host':False},
    # Group F
    'Netherlands':   {'conf':'UEFA',    'group':'F','rank': 7,'elo':1970,'coach':'Ronald Koeman',      'host':False},
    'Colombia':      {'conf':'CONMEBOL','group':'F','rank':17,'elo':1825,'coach':'Nestor Lorenzo',     'host':False},
    'Iran':          {'conf':'AFC',     'group':'F','rank':26,'elo':1730,'coach':'Amir Ghalenoei',     'host':False},
    'DR Congo':      {'conf':'CAF',     'group':'F','rank':46,'elo':1570,'coach':'Sebastien Desabre',  'host':False},
    # Group G
    'Belgium':       {'conf':'UEFA',    'group':'G','rank': 5,'elo':1995,'coach':'Domenico Tedesco',   'host':False},
    'Italy':         {'conf':'UEFA',    'group':'G','rank':10,'elo':1945,'coach':'Luciano Spalletti',  'host':False},
    'Uruguay':       {'conf':'CONMEBOL','group':'G','rank':14,'elo':1860,'coach':'Marcelo Bielsa',     'host':False},
    'Saudi Arabia':  {'conf':'AFC',     'group':'G','rank':37,'elo':1620,'coach':'Roberto Mancini',    'host':False},
    # Group H
    'Croatia':       {'conf':'UEFA',    'group':'H','rank':11,'elo':1920,'coach':'Zlatko Dalic',       'host':False},
    'Turkey':        {'conf':'UEFA',    'group':'H','rank':24,'elo':1745,'coach':'Vincenzo Montella',  'host':False},
    'Costa Rica':    {'conf':'CONCACAF','group':'H','rank':35,'elo':1630,'coach':'Gustavo Alfaro',     'host':False},
    'South Africa':  {'conf':'CAF',     'group':'H','rank':36,'elo':1625,'coach':'Hugo Broos',         'host':False},
    # Group I
    'Austria':       {'conf':'UEFA',    'group':'I','rank':18,'elo':1815,'coach':'Ralf Rangnick',      'host':False},
    'Switzerland':   {'conf':'UEFA',    'group':'I','rank':16,'elo':1840,'coach':'Murat Yakin',        'host':False},
    'Honduras':      {'conf':'CONCACAF','group':'I','rank':42,'elo':1598,'coach':'Reinaldo Rueda',     'host':False},
    'Egypt':         {'conf':'CAF',     'group':'I','rank':39,'elo':1610,'coach':'Rui Vitoria',        'host':False},
    # Group J
    'Denmark':       {'conf':'UEFA',    'group':'J','rank':13,'elo':1870,'coach':'Kasper Hjulmand',    'host':False},
    'Serbia':        {'conf':'UEFA',    'group':'J','rank':23,'elo':1748,'coach':'Dragan Stojkovic',   'host':False},
    'Nigeria':       {'conf':'CAF',     'group':'J','rank':25,'elo':1738,'coach':'Finidi George',      'host':False},
    'Qatar':         {'conf':'AFC',     'group':'J','rank':40,'elo':1607,'coach':'Marquez Lopez',      'host':False},
    # Group K
    'Scotland':      {'conf':'UEFA',    'group':'K','rank':29,'elo':1705,'coach':'Steve Clarke',       'host':False},
    'Hungary':       {'conf':'UEFA',    'group':'K','rank':32,'elo':1670,'coach':'Marco Rossi',        'host':False},
    'Indonesia':     {'conf':'AFC',     'group':'K','rank':47,'elo':1555,'coach':'Patrick Kluivert',   'host':False},
    'Jordan':        {'conf':'AFC',     'group':'K','rank':44,'elo':1580,'coach':'Hussain Ammouta',    'host':False},
    # Group L
    'New Zealand':   {'conf':'OFC',     'group':'L','rank':45,'elo':1560,'coach':'Darren Bazeley',     'host':False},
    'Uzbekistan':    {'conf':'AFC',     'group':'L','rank':43,'elo':1592,'coach':'Srecko Katanec',     'host':False},
    'Venezuela':     {'conf':'CONMEBOL','group':'L','rank':41,'elo':1600,'coach':'Fernando Batista',   'host':False},
    'Guatemala':     {'conf':'CONCACAF','group':'L','rank':48,'elo':1540,'coach':'Luis Fernando Tena', 'host':False},
}

VENUES = [
    ('SoFi Stadium',           'Los Angeles',   'USA'),
    ('MetLife Stadium',        'New York',      'USA'),
    ('AT&T Stadium',           'Dallas',        'USA'),
    ("Levi's Stadium",         'San Francisco', 'USA'),
    ('Mercedes-Benz Stadium',  'Atlanta',       'USA'),
    ('Lumen Field',            'Seattle',       'USA'),
    ('Gillette Stadium',       'Boston',        'USA'),
    ('NRG Stadium',            'Houston',       'USA'),
    ('Hard Rock Stadium',      'Miami',         'USA'),
    ('Arrowhead Stadium',      'Kansas City',   'USA'),
    ('Lincoln Financial Field','Philadelphia',  'USA'),
    ('BMO Field',              'Toronto',       'Canada'),
    ('BC Place',               'Vancouver',     'Canada'),
    ('Estadio Azteca',         'Mexico City',   'Mexico'),
    ('Estadio Akron',          'Guadalajara',   'Mexico'),
    ('Estadio BBVA',           'Monterrey',     'Mexico'),
]

VENUE_CAPS = {
    'MetLife Stadium': 82500, 'SoFi Stadium': 70240, 'AT&T Stadium': 80000,
    "Levi's Stadium": 68500, 'Mercedes-Benz Stadium': 71000, 'Lumen Field': 69000,
    'Gillette Stadium': 65878, 'NRG Stadium': 72220, 'Hard Rock Stadium': 65326,
    'Arrowhead Stadium': 76416, 'Lincoln Financial Field': 69176,
    'BMO Field': 30000, 'BC Place': 54500,
    'Estadio Azteca': 87523, 'Estadio Akron': 49850, 'Estadio BBVA': 51348,
}

# ─────────────────────────────────────────────────────────
# 2. SIMULATION HELPERS
# ─────────────────────────────────────────────────────────
def simulate_score(t1, t2):
    e1, e2 = TEAMS[t1]['elo'], TEAMS[t2]['elo']
    wp = 1 / (1 + 10 ** (-(e1 - e2) / 400))
    g1 = int(np.random.poisson(max(0.3, 0.5 + 1.2 * wp)))
    g2 = int(np.random.poisson(max(0.3, 0.5 + 1.2 * (1 - wp))))
    return g1, g2

def match_stats(t1, t2, g1, g2, venue):
    e1, e2 = TEAMS[t1]['elo'], TEAMS[t2]['elo']
    diff = e1 - e2
    hp = int(np.clip(50 + diff / 30 + np.random.normal(0, 4), 32, 68))
    ap = 100 - hp
    hs = max(g1, int(np.random.poisson(10 * hp / 100)))
    as_ = max(g2, int(np.random.poisson(10 * ap / 100)))
    cap = VENUE_CAPS.get(venue[0], 65000)
    att = int(cap * np.random.uniform(0.82, 0.99))
    return {
        'HomePossession': hp, 'AwayPossession': ap,
        'HomeShots': hs, 'AwayShots': as_,
        'HomeXG': round(g1 * 0.75 + np.random.exponential(0.3), 2),
        'AwayXG': round(g2 * 0.75 + np.random.exponential(0.3), 2),
        'HomeYellowCards': int(np.random.poisson(1.4)),
        'AwayYellowCards': int(np.random.poisson(1.4)),
        'HomeRedCards': int(np.random.random() < 0.06),
        'AwayRedCards': int(np.random.random() < 0.06),
        'Attendance': att,
    }

# ─────────────────────────────────────────────────────────
# 3. GROUP STAGE  (72 matches)
# ─────────────────────────────────────────────────────────
groups = {}
for team, info in TEAMS.items():
    grp = info['group']
    groups.setdefault(grp, []).append(team)

all_matches = []
match_id = 1
start_date = date(2026, 6, 11)
d = start_date

group_records = {t: {'W':0,'D':0,'L':0,'GF':0,'GA':0} for t in TEAMS}

for grp in sorted(groups):
    members = groups[grp]
    for i, (t1, t2) in enumerate(combinations(members, 2)):
        venue = random.choice(VENUES)
        g1, g2 = simulate_score(t1, t2)
        stats = match_stats(t1, t2, g1, g2, venue)
        winner = t1 if g1 > g2 else (t2 if g2 > g1 else 'Draw')
        all_matches.append({
            'MatchID': match_id, 'Round': 'Group Stage', 'Date': d.strftime('%Y-%m-%d'),
            'Venue': venue[0], 'City': venue[1], 'Country': venue[2],
            'HomeTeam': t1, 'AwayTeam': t2,
            'HomeGoals': g1, 'AwayGoals': g2, 'Winner': winner, **stats
        })
        # Update records
        group_records[t1]['GF'] += g1; group_records[t1]['GA'] += g2
        group_records[t2]['GF'] += g2; group_records[t2]['GA'] += g1
        if g1 > g2:   group_records[t1]['W'] += 1; group_records[t2]['L'] += 1
        elif g2 > g1: group_records[t2]['W'] += 1; group_records[t1]['L'] += 1
        else:         group_records[t1]['D'] += 1; group_records[t2]['D'] += 1
        match_id += 1
        d += timedelta(days=1)

# ─────────────────────────────────────────────────────────
# 4. GROUP STANDINGS
# ─────────────────────────────────────────────────────────
standings_rows = []
group_qualifiers = {}  # group -> [1st, 2nd, 3rd]
all_thirds = []        # for best-3rd-place selection

for grp in sorted(groups):
    members = groups[grp]
    table = []
    for t in members:
        r = group_records[t]
        pts = r['W']*3 + r['D']
        gd = r['GF'] - r['GA']
        table.append({'Nation':t,'Played':3,'Won':r['W'],'Drawn':r['D'],'Lost':r['L'],
                      'GF':r['GF'],'GA':r['GA'],'GD':gd,'Points':pts,'Group':grp})
    table.sort(key=lambda x: (-x['Points'], -x['GD'], -x['GF']))
    for pos, row in enumerate(table, 1):
        row['Position'] = pos
        row['Qualified'] = pos <= 2
        standings_rows.append(row)
    group_qualifiers[grp] = [table[0]['Nation'], table[1]['Nation'], table[2]['Nation']]
    all_thirds.append((table[2]['Points'], table[2]['GD'], table[2]['GF'], grp, table[2]['Nation']))

# Best 8 third-place teams qualify
all_thirds.sort(key=lambda x: (-x[0], -x[1], -x[2]))
best_thirds = [x[4] for x in all_thirds[:8]]
for row in standings_rows:
    if row['Position'] == 3 and row['Nation'] in best_thirds:
        row['Qualified'] = True

# ─────────────────────────────────────────────────────────
# 5. KNOCKOUT ROUNDS  (32 matches)
# ─────────────────────────────────────────────────────────
def simulate_ko(t1, t2, venue, rnd):
    global match_id, d
    g1, g2 = simulate_score(t1, t2)
    # Knockout: no draws – extra time if tied
    if g1 == g2:
        if np.random.random() < 0.5:
            g1 += 1
        else:
            g2 += 1
    stats = match_stats(t1, t2, g1, g2, venue)
    winner = t1 if g1 > g2 else t2
    all_matches.append({
        'MatchID': match_id, 'Round': rnd, 'Date': d.strftime('%Y-%m-%d'),
        'Venue': venue[0], 'City': venue[1], 'Country': venue[2],
        'HomeTeam': t1, 'AwayTeam': t2,
        'HomeGoals': g1, 'AwayGoals': g2, 'Winner': winner, **stats
    })
    match_id += 1; d += timedelta(days=2)
    return winner

# Build R32 (Round of 32) participants: 24 + 8 best thirds = 32
r32_teams = []
for grp in sorted(groups):
    r32_teams.append(group_qualifiers[grp][0])
    r32_teams.append(group_qualifiers[grp][1])
r32_teams += best_thirds
random.shuffle(r32_teams)

# Pair them up for R32
r32_winners = []
for i in range(0, 32, 2):
    v = random.choice(VENUES)
    w = simulate_ko(r32_teams[i], r32_teams[i+1], v, 'Round of 32')
    r32_winners.append(w)

# R16
r16_winners = []
for i in range(0, 16, 2):
    v = random.choice(VENUES)
    w = simulate_ko(r32_winners[i], r32_winners[i+1], v, 'Round of 16')
    r16_winners.append(w)

# QF
qf_winners = []
for i in range(0, 8, 2):
    v = random.choice(VENUES)
    w = simulate_ko(r16_winners[i], r16_winners[i+1], v, 'Quarter-Final')
    qf_winners.append(w)

# SF
sf_losers, sf_winners = [], []
for i in range(0, 4, 2):
    t1, t2 = qf_winners[i], qf_winners[i+1]
    v = random.choice(VENUES)
    w = simulate_ko(t1, t2, v, 'Semi-Final')
    sf_winners.append(w)
    sf_losers.append(t1 if w == t2 else t2)

# 3rd place
simulate_ko(sf_losers[0], sf_losers[1], VENUES[0], 'Third Place')

# Final
champion = simulate_ko(sf_winners[0], sf_winners[1], VENUES[1], 'Final')
print(f"\n*** FIFA 2026 Champion: {champion} ***\n")

# ─────────────────────────────────────────────────────────
# 6. PLAYER DATA  (200 players)
# ─────────────────────────────────────────────────────────
STAR_PLAYERS = {
    'France':        [('Kylian Mbappe','FW',25,'PSG'),('Antoine Griezmann','FW',35,'Atletico Madrid'),('Aurelien Tchouameni','MF',24,'Real Madrid'),('Raphael Varane','DF',31,'Como')],
    'Argentina':     [('Lionel Messi','FW',38,'Inter Miami'),('Julian Alvarez','FW',24,'Atletico Madrid'),('Rodrigo De Paul','MF',30,'Atletico Madrid'),('Cristian Romero','DF',26,'Tottenham')],
    'England':       [('Harry Kane','FW',32,'Bayern Munich'),('Jude Bellingham','MF',22,'Real Madrid'),('Phil Foden','MF',26,'Man City'),('Bukayo Saka','FW',22,'Arsenal')],
    'Brazil':        [('Vinicius Jr','FW',25,'Real Madrid'),('Rodrygo','FW',24,'Real Madrid'),('Bruno Guimaraes','MF',26,'Newcastle'),('Marquinhos','DF',30,'PSG')],
    'Portugal':      [('Cristiano Ronaldo','FW',41,'Al Nassr'),('Bernardo Silva','MF',30,'Man City'),('Rafael Leao','FW',25,'AC Milan'),('Ruben Dias','DF',27,'Man City')],
    'Spain':         [('Pedri','MF',23,'Barcelona'),('Lamine Yamal','FW',18,'Barcelona'),('Alvaro Morata','FW',31,'AC Milan'),('Rodri','MF',28,'Man City')],
    'Germany':       [('Florian Wirtz','MF',22,'Bayer Leverkusen'),('Leroy Sane','FW',29,'Bayern Munich'),('Kai Havertz','FW',25,'Arsenal'),('Antonio Rudiger','DF',31,'Real Madrid')],
    'Netherlands':   [('Cody Gakpo','FW',25,'Liverpool'),('Memphis Depay','FW',30,'Atletico Madrid'),('Frenkie de Jong','MF',27,'Barcelona'),('Virgil van Dijk','DF',33,'Liverpool')],
    'Belgium':       [('Romelu Lukaku','FW',31,'Napoli'),('Kevin De Bruyne','MF',33,'Man City'),('Jeremy Doku','FW',22,'Man City'),('Wout Faes','DF',26,'Leicester')],
    'Croatia':       [('Luka Modric','MF',40,'Real Madrid'),('Mateo Kovacic','MF',30,'Man City'),('Ivan Perisic','FW',35,'Hajduk Split'),('Josko Gvardiol','DF',22,'Man City')],
    'Morocco':       [('Achraf Hakimi','DF',25,'PSG'),('Hakim Ziyech','MF',31,'Galatasaray'),('Youssef En-Nesyri','FW',27,'Fenerbahce'),('Romain Saiss','DF',34,'Besiktas')],
    'Uruguay':       [('Darwin Nunez','FW',25,'Liverpool'),('Federico Valverde','MF',26,'Real Madrid'),('Luis Suarez','FW',37,'Nacional'),('Jose Maria Gimenez','DF',29,'Atletico Madrid')],
    'Japan':         [('Takuma Asano','FW',29,'VfL Bochum'),('Kaoru Mitoma','FW',27,'Brighton'),('Wataru Endo','MF',31,'Liverpool'),('Maya Yoshida','DF',36,'Shimizu')],
    'United States': [('Christian Pulisic','MF',25,'AC Milan'),('Gio Reyna','MF',21,'Nottm Forest'),('Tyler Adams','MF',25,'Bournemouth'),('Tim Weah','FW',24,'Juventus')],
    'Colombia':      [('James Rodriguez','MF',33,'Rayo Vallecano'),('Luis Diaz','FW',27,'Liverpool'),('Richard Rios','MF',24,'Palmeiras'),('Davinson Sanchez','DF',27,'Galatasaray')],
    'Senegal':       [('Sadio Mane','FW',32,'Al Nassr'),('Ismaila Sarr','FW',26,'Crystal Palace'),('Pape Gueye','MF',24,'Villarreal'),('Kalidou Koulibaly','DF',33,'Al Hilal')],
    'Denmark':       [('Christian Eriksen','MF',32,'Man Utd'),('Rasmus Hojlund','FW',22,'Man Utd'),('Pierre-Emile Hojbjerg','MF',29,'Atletico Madrid'),('Andreas Christensen','DF',28,'Barcelona')],
    'Switzerland':   [('Xherdan Shaqiri','FW',32,'Chicago Fire'),('Granit Xhaka','MF',31,'Bayer Leverkusen'),('Breel Embolo','FW',27,'Monaco'),('Manuel Akanji','DF',29,'Man City')],
    'Austria':       [('Marcel Sabitzer','MF',30,'Dortmund'),('Christoph Baumgartner','MF',25,'Leipzig'),('Marko Arnautovic','FW',35,'Bologna'),('David Alaba','DF',32,'Real Madrid')],
    'Mexico':        [('Hirving Lozano','FW',28,'PSV'),('Edson Alvarez','MF',26,'West Ham'),('Henry Martin','FW',32,'Club America'),('Cesar Montes','DF',27,'Espanyol')],
    'Serbia':        [('Aleksandar Mitrovic','FW',29,'Al Hilal'),('Dusan Vlahovic','FW',24,'Juventus'),('Filip Kostic','MF',31,'Juventus'),('Nikola Milenkovic','DF',26,'Nottm Forest')],
    'Nigeria':       [('Victor Osimhen','FW',25,'Galatasaray'),('Ademola Lookman','FW',26,'Atalanta'),('Wilfred Ndidi','MF',27,'Leicester'),('William Troost-Ekong','DF',30,'Watford')],
    'Iran':          [('Sardar Azmoun','FW',29,'Fenerbahce'),('Alireza Jahanbakhsh','FW',30,'Feyenoord'),('Ahmad Noorollahi','MF',30,'Persepolis'),('Ehsan Hajsafi','DF',34,'AEK Athens')],
    'South Korea':   [('Son Heung-min','FW',32,'Tottenham'),('Lee Kang-in','MF',23,'PSG'),('Hwang Hee-chan','FW',28,'Wolves'),('Kim Min-jae','DF',28,'Bayern Munich')],
    'Turkey':        [('Arda Guler','MF',20,'Real Madrid'),('Hakan Calhanoglu','MF',30,'Inter Milan'),('Burak Yilmaz','FW',38,'Adana Demirspor'),('Zeki Celik','DF',27,'Roma')],
    'Ecuador':       [('Enner Valencia','FW',34,'Internacional'),('Moises Caicedo','MF',22,'Chelsea'),('Jhegson Mendez','MF',25,'LA Galaxy'),('Felix Torres','DF',26,'Santos Laguna')],
    'Canada':        [('Alphonso Davies','DF',23,'Bayern Munich'),('Jonathan David','FW',24,'Lille'),('Tajon Buchanan','MF',25,'Inter Milan'),('Atiba Hutchinson','MF',41,'Besiktas')],
    'Australia':     [('Mathew Ryan','GK',32,'Real Sociedad'),('Mitchell Duke','FW',33,'Fagiano Okayama'),('Mat Leckie','FW',33,'Melbourne City'),('Aaron Mooy','MF',33,'Celtic')],
    'Saudi Arabia':  [('Saleh Al-Shehri','FW',30,'Al Hilal'),('Salem Al-Dawsari','FW',32,'Al Hilal'),('Sami Al-Najei','MF',29,'Al Qadsiah'),('Ali Al-Bulaihi','DF',33,'Al Hilal')],
    'Ghana':         [('Mohammed Kudus','MF',24,'West Ham'),('Jordan Ayew','FW',32,'Leicester'),('Andre Ayew','FW',34,'Le Havre'),('Alexander Djiku','DF',29,'Fenerbahce')],
    'Scotland':      [('Andrew Robertson','DF',30,'Liverpool'),('Scott McTominay','MF',27,'Napoli'),('Che Adams','FW',28,'Southampton'),('John McGinn','MF',30,'Aston Villa')],
    'Croatia':       [('Luka Modric','MF',40,'Real Madrid'),('Mateo Kovacic','MF',30,'Man City'),('Ivan Perisic','FW',35,'Hajduk Split'),('Josko Gvardiol','DF',22,'Man City')],
    'Venezuela':     [('Salomon Rondon','FW',34,'Pachuca'),('Yangel Herrera','MF',26,'Girona'),('Josef Martinez','FW',30,'Inter Miami'),('Tomas Rincon','MF',36,'Deportivo La Guaira')],
    'Costa Rica':    [('Bryan Ruiz','MF',38,'Saprissa'),('Keylor Navas','GK',37,'Newell\'s Old Boys'),('Joel Campbell','FW',32,'Leon'),('Oscar Duarte','DF',34,'Rayo Vallecano')],
    'Cameroon':      [('Eric Maxim Choupo-Moting','FW',35,'Nantes'),('Andre-Frank Anguissa','MF',28,'Napoli'),('Nicolas Nkoulou','DF',34,'Universitario'),('Jean-Charles Castelletto','DF',28,'Nantes')],
    'Egypt':         [('Mohamed Salah','FW',32,'Liverpool'),('Mostafa Mohamed','FW',26,'Galatasaray'),('Tarek Hamed','MF',33,'Pyramids'),('Ahmed Hegazi','DF',33,'Al Ittihad')],
    'Qatar':         [('Akram Afif','FW',27,'Al Sadd'),('Almoez Ali','FW',28,'Al Duhail'),('Abdelkarim Hassan','MF',30,'Al Sadd'),('Boualem Khoukhi','DF',32,'Al Sadd')],
    'Hungary':       [('Dominik Szoboszlai','MF',23,'Liverpool'),('Roland Sallai','FW',27,'SC Freiburg'),('Adam Nagy','MF',29,'Pisa'),('Attila Fiola','DF',31,'Fehervar')],
    'Ivory Coast':   [('Sebastien Haller','FW',29,'Dortmund'),('Franck Kessie','MF',27,'Al Ahli'),('Nicolas Pepe','FW',29,'Trabzonspor'),('Eric Bailly','DF',30,'Villarreal')],
    'Tunisia':       [('Youssef Msakni','FW',33,'Al Arabi'),('Wahbi Khazri','FW',33,'Montpellier'),('Ellyes Skhiri','MF',28,'Eintracht Frankfurt'),('Bilel Ifa','DF',31,'Al Faisaly')],
    'South Africa':  [('Percy Tau','FW',29,'Al Ahly'),('Bongani Zungu','MF',31,'Amiens'),('Themba Zwane','FW',32,'Mamelodi Sundowns'),('Rushine De Reuck','DF',28,'Mamelodi Sundowns')],
    'Honduras':      [('Alberth Elis','FW',27,'FC Nantes'),('Jorge Alvarez','FW',24,'Lobos BUAP'),('Kervin Arriaga','MF',22,'FC Dallas'),('Maynor Figueroa','DF',40,'Houston Dynamo')],
    'Panama':        [('Rommel Quiñones','FW',28,'Liga MX'),('Adolfo Machado','DF',34,'Houston Dynamo'),('Anibal Godoy','MF',35,'Nashville SC'),('Cesar Yanis','FW',27,'Deportivo Saprissa')],
    'DR Congo':      [('Yannick Bolasie','FW',34,'Metz'),('Cedric Bakambu','FW',33,'OM'),('Chancel Mbemba','DF',30,'OM'),('Jonathan Bolingi','FW',30,'Mazembe')],
    'Jordan':        [('Yazan Al-Naimat','FW',27,'Al Jazeera'),('Ahmad Alaeddin','MF',25,'Al Ahli'),('Baha Faisal','DF',30,'Al Faisaly'),('Moussa Al-Tamari','FW',25,'Montpellier')],
    'Uzbekistan':    [('Eldor Shomurodov','FW',27,'Roma'),('Abbosbek Fayzullayev','MF',22,'CSKA Moscow'),('Sherzod Nasrullayev','MF',25,'Pakhtakor'),('Oston Urunov','MF',25,'Rubin Kazan')],
    'New Zealand':   [('Chris Wood','FW',32,'Nottm Forest'),('Clayton Lewis','MF',28,'Hibernian'),('Tommy Smith','DF',33,'Stoke City'),('Liberato Cacace','DF',24,'Empoli')],
    'Guatemala':     [('Carlos Ruiz','FW',45,'Retired'),('Rudy Cardozo','MF',28,'Municipal'),('Oscar Castellanos','DF',30,'Comunicaciones'),('Julio Marroquin','FW',25,'Herediano')],
    'Indonesia':     [('Marselino Ferdinan','MF',20,'Beveren'),('Rafael Struick','FW',21,'Brisbane Roar'),('Thom Haye','MF',27,'Almere City'),('Jay Idzes','DF',23,'Venezia')],
}

# Gather team goals from matches for realistic player stat distribution
team_goals = {t: 0 for t in TEAMS}
team_matches_played = {t: 0 for t in TEAMS}
for m in all_matches:
    team_goals[m['HomeTeam']] += m['HomeGoals']
    team_goals[m['AwayTeam']] += m['AwayGoals']
    team_matches_played[m['HomeTeam']] += 1
    team_matches_played[m['AwayTeam']] += 1

player_rows = []
pid = 1
for nation, players in STAR_PLAYERS.items():
    total_g = team_goals.get(nation, 3)
    played = team_matches_played.get(nation, 3)
    for name, pos, age, club in players:
        mins = int(played * np.random.uniform(60, 90))
        if pos == 'FW':
            g = int(np.random.binomial(max(total_g, 1), 0.35))
            a = int(np.random.binomial(max(total_g, 1), 0.18))
        elif pos == 'MF':
            g = int(np.random.binomial(max(total_g, 1), 0.12))
            a = int(np.random.binomial(max(total_g, 1), 0.25))
        else:
            g = int(np.random.binomial(max(total_g, 1), 0.05))
            a = int(np.random.binomial(max(total_g, 1), 0.08))
        shots = max(g, int(np.random.poisson(3 if pos == 'FW' else 1)))
        passes = int(np.random.normal(35 if pos == 'MF' else 20, 8))
        rating = round(np.clip(np.random.normal(7.0, 0.5) + g * 0.15 + a * 0.1, 5.5, 9.5), 1)
        player_rows.append({
            'PlayerID': pid, 'Name': name, 'Nation': nation, 'Position': pos,
            'Age': age, 'Club': club, 'Goals': g, 'Assists': a, 'Minutes': mins,
            'Shots': shots, 'ShotsOnTarget': max(g, int(shots * np.random.uniform(0.3, 0.6))),
            'Passes': max(1, passes), 'KeyPasses': int(np.random.poisson(a + 1)),
            'Dribbles': int(np.random.poisson(2 if pos in ('FW','MF') else 0)),
            'YellowCards': int(np.random.poisson(0.8)),
            'RedCards': int(np.random.random() < 0.04),
            'Rating': rating,
        })
        pid += 1

# ─────────────────────────────────────────────────────────
# 7. SAVE ALL CSVs
# ─────────────────────────────────────────────────────────
# Teams CSV
teams_rows = [{'TeamID': i+1, 'Nation': n, 'Confederation': v['conf'],
               'Group': v['group'], 'FIFA_Rank': v['rank'], 'ELO_Rating': v['elo'],
               'Coach': v['coach'], 'Host': v['host']}
              for i, (n, v) in enumerate(TEAMS.items())]
pd.DataFrame(teams_rows).to_csv(os.path.join(OUTPUT_DIR, 'wc2026_teams.csv'), index=False)

# Matches CSV
pd.DataFrame(all_matches).to_csv(os.path.join(OUTPUT_DIR, 'wc2026_matches.csv'), index=False)

# Players CSV
pd.DataFrame(player_rows).to_csv(os.path.join(OUTPUT_DIR, 'wc2026_players.csv'), index=False)

# Groups CSV
pd.DataFrame(standings_rows).to_csv(os.path.join(OUTPUT_DIR, 'wc2026_groups.csv'), index=False)

# Summary
print(f"[OK] wc2026_teams.csv   -> {len(teams_rows)} teams")
print(f"[OK] wc2026_matches.csv -> {len(all_matches)} matches")
print(f"[OK] wc2026_players.csv -> {len(player_rows)} players")
print(f"[OK] wc2026_groups.csv  -> {len(standings_rows)} group rows")
print(f"\nData saved to: {OUTPUT_DIR}")

