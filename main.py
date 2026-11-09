#%%
import requests
import time
import json
import webbrowser
from pathlib import Path
from collections import defaultdict
from itertools import combinations
import os

rifts = [
 {'slug': 'dead-end-s1w1', 'name': 'Dead End', 'period': 's1w1'},
 {'slug': 'heavy-hitting-2p-s1w1', 'name': 'Heavy Hitting 2P', 'period': 's1w1'},
 {'slug': 'double-double-hop-s1w1', 'name': 'Double Double Hop', 'period': 's1w1'},
 {'slug': 'sewer-showdown-s1w1', 'name': 'Sewer Showdown', 'period': 's1w1'},
 {'slug': 'twilight-takedown-s1w1', 'name': 'Twilight Takedown', 'period': 's1w1'},
 {'slug': 'moonlit-ruins-s1w2', 'name': 'Moonlit Ruins', 'period': 's1w2'},
 {'slug': 'royal-guard-s1w2', 'name': 'Royal Guard', 'period': 's1w2'},
 {'slug': 'target-priority-2p-s1w2', 'name': 'Target Priority 2P', 'period': 's1w2'},
 {'slug': 'bug-fight-s1w2', 'name': 'Bug Fight', 'period': 's1w2'},
 {'slug': 'rooftop-rumble-s1w2', 'name': 'Rooftop Rumble', 'period': 's1w2'},
 {'slug': 'grand-librarian-s1w2', 'name': 'Grand Librarian', 'period': 's1w2'},
 {'slug': 'overgrown-tomb-s1w3', 'name': 'Overgrown Tomb', 'period': 's1w3'},
 {'slug': 'noble-courtyard-s1w3', 'name': 'Noble Courtyard', 'period': 's1w3'},
 {'slug': 'crowd-control-2p-s1w3', 'name': 'Crowd Control 2P', 'period': 's1w3'},
 {'slug': 'researchers-on-a-mission-s1w3', 'name': 'Researchers On A Mission', 'period': 's1w3'},
 {'slug': 'everything-all-at-once-s1w3', 'name': 'Everything, All At Once', 'period': 's1w3'},
 {'slug': 'nightmare-clash-s1w3', 'name': 'Nightmare Clash', 'period': 's1w3'},
 {'slug': 'rage-room-s1w4', 'name': 'Rage Room', 'period': 's1w4'},
 {'slug': 'rooftop-rumble-s1w4', 'name': 'Rooftop Rumble', 'period': 's1w4'},
 {'slug': 'no-escape-2p-s1w4', 'name': 'No Escape 2P', 'period': 's1w4'},
 {'slug': 'dragon-cave-s1w4', 'name': 'Dragon Cave', 'period': 's1w4'},
 {'slug': 'hunting-party-s1w4', 'name': 'Hunting Party', 'period': 's1w4'},
 {'slug': 'windy-mountaintop-s1w4', 'name': 'Windy Mountaintop', 'period': 's1w4'},
 {'slug': 'juggle-juggle-s2w1', 'name': 'Juggle Juggle', 'period': 's2w1'},
 {'slug': 'bug-lord-bash-s2w1', 'name': 'Bug Lord Bash', 'period': 's2w1'},
 {'slug': 'double-double-dragon-s2w1', 'name': 'Double Double Dragon', 'period': 's2w1'},
 {'slug': 'rooftop-rumbles-s2w1', 'name': 'Rooftop Rumbles', 'period': 's2w1'},
 {'slug': 'x2-takedown-s2w1', 'name': 'X2 Takedown', 'period': 's2w1'},
 {'slug': 'axe-clash-nightmare-s2w1', 'name': 'Axe Clash Nightmare', 'period': 's2w1'},
 {'slug': 'cave-of-corruption-s2w2', 'name': 'Cave Of Corruption', 'period': 's2w2'},
 {'slug': 'knights-chambers-s2w2', 'name': "Knights' Chambers", 'period': 's2w2'},
 {'slug': 'taking-hits-s2w2', 'name': 'Taking Hits', 'period': 's2w2'},
 {'slug': 'ceremonial-score-s2w2', 'name': 'Ceremonial Score', 'period': 's2w2'},
 {'slug': 'rooftop-garden-s2w2', 'name': 'Rooftop Garden', 'period': 's2w2'},
 {'slug': 'toxic-tangle-s2w2', 'name': 'Toxic Tangle', 'period': 's2w2'},
 {'slug': 'mountaintop-cleanup-s2w3', 'name': 'Mountaintop Cleanup', 'period': 's2w3'},
 {'slug': 'canyon-peril-s2w3', 'name': 'Canyon Peril', 'period': 's2w3'},
 {'slug': 'thick-of-it-s2w3', 'name': 'Thick Of It', 'period': 's2w3'},
 {'slug': 'van-defense-s2w3', 'name': 'Van Defense', 'period': 's2w3'},
 {'slug': 'mass-invasion-s2w3', 'name': 'Mass Invasion', 'period': 's2w3'},
 {'slug': 'deep-george-s2w3', 'name': 'Deep George', 'period': 's2w3'},
 {'slug': 'ramparts-s2w4', 'name': 'Ramparts', 'period': 's2w4'},
 {'slug': 'unhushed-library-s2w4', 'name': 'Unhushed Library', 'period': 's2w4'},
 {'slug': 'sewer-king-s2w4', 'name': 'Sewer King', 'period': 's2w4'},
 {'slug': 'moonlit-ruins2-s2w4', 'name': 'Moonlit Ruins', 'period': 's2w4'},
 {'slug': 'twin-princes-s2w4', 'name': 'Twin Princes', 'period': 's2w4'},
 {'slug': 'throne-room-s2w4', 'name': 'Throne Room', 'period': 's2w4'},
 {'slug': 'build-up-s3w1', 'name': 'Build Up', 'period': 's3w1'},
 {'slug': 'boss-rumble-s3w1', 'name': 'Boss Rumble', 'period': 's3w1'},
 {'slug': 'extra-charge-2p-s3w1', 'name': 'Extra Charge 2P', 'period': 's3w1'},
 {'slug': 'apocalypse-s3w1', 'name': 'Apocalypse', 'period': 's3w1'},
 {'slug': 'monster-magnet-s3w1', 'name': 'Monster Magnet', 'period': 's3w1'},
 {'slug': 'midnight-shakedown-s3w1', 'name': 'Midnight Shakedown', 'period': 's3w1'},
 {'slug': 'shipwreck-harbour-s3w2', 'name': 'Shipwreck Harbour', 'period': 's3w2'},
 {'slug': 'snowclaw-summit-s3w2', 'name': 'Snowclaw Summit', 'period': 's3w2'},
 {'slug': 'herding-cats-s3w2', 'name': 'Herrding Cats', 'period': 's3w2'},
 {'slug': 'ice-fishing-s3w2', 'name': 'Ice Fishing', 'period': 's3w2'},
 {'slug': 'snowdrift-cave-s3w2', 'name': 'Snowdrift Cave', 'period': 's3w2'},
 {'slug': 'purrgatory-s3w2', 'name': 'Purrgatory', 'period': 's3w2'},
 {'slug': 'big-3-s3w3', 'name': 'Big-3', 'period': 's3w3'},
 {'slug': 'dust-pit-s3w3', 'name': 'Dust Pit', 'period': 's3w3'},
 {'slug': 'death-by-a-thousand-cuts-s3w3', 'name': 'Death By A Thousand Cuts', 'period': 's3w3'},
 {'slug': 'bleak-shaft-s3w3', 'name': 'Bleak Shaft', 'period': 's3w3'},
 {'slug': 'score-hunt-s3w3', 'name': 'Score Hunt', 'period': 's3w3'},
 {'slug': 'cave-of-corruption-s3w3', 'name': 'Cave Of Corruption', 'period': 's3w3'},
 {'slug': 'rustwater-harbor-s3w4', 'name': 'Rustwater Harbor', 'period': 's3w4'},
 {'slug': 'market-street-s3w4', 'name': 'Market Street', 'period': 's3w4'},
 {'slug': 'deadeye-district-s3w4', 'name': 'Deadeye District', 'period': 's3w4'},
 {'slug': 'reflexology-s3w4', 'name': 'Reflexolgy', 'period': 's3w4'},
 {'slug': 'garbage-disposal-s3w4', 'name': 'Garbage Disposal', 'period': 's3w4'},
 {'slug': 'back-alley-brawl-s3w4', 'name': 'Back Alley Brawl', 'period': 's3w4'},
 {'slug': 'dead-end-s4w1', 'name': 'Dead End', 'period': 's4w1'},
 {'slug': 'heavy-hitting-2p-s4w1', 'name': 'Heavy Hitting 2P', 'period': 's4w1'},
 {'slug': 'ceremonial-square-s4w1', 'name': 'Ceremonial Square', 'period': 's4w1'},
 {'slug': 'double-double-hop-s4w1', 'name': 'Double Double Hop', 'period': 's4w1'},
 {'slug': 'sewer-showdown-s4w1', 'name': 'Sewer Showdown', 'period': 's4w1'},
 {'slug': 'twilight-takedown-s4w1', 'name': 'Twilight Takedown', 'period': 's4w1'},
 {'slug': 'moonlit-ruins-s4w2', 'name': 'Moonlit Ruins', 'period': 's4w2'},
 {'slug': 'royal-guard-s4w2', 'name': 'Royal Guard', 'period': 's4w2'},
 {'slug': 'target-priority-2p-s4w2', 'name': 'Target Priority 2P', 'period': 's4w2'},
 {'slug': 'bug-fight-s4w2', 'name': 'Bug Fight', 'period': 's4w2'},
 {'slug': 'rooftop-rumble-s4w2', 'name': 'Rooftop Rumble', 'period': 's4w2'},
 {'slug': 'grand-librarian-s4w2', 'name': 'Grand Librarian', 'period': 's4w2'},
 {'slug': 'overgrown-tomb-s4w3', 'name': 'Overgrown Tomb', 'period': 's4w3'},
 {'slug': 'noble-courtyard-s4w3', 'name': 'Noble Courtyard', 'period': 's4w3'},
 {'slug': 'crowd-control-2p-s4w3', 'name': 'Crowd Control 2P', 'period': 's4w3'},
 {'slug': 'researchers-on-a-mission-s4w3', 'name': 'Researchers On A Mission', 'period': 's4w3'},
 {'slug': 'everything-all-at-once-s4w3', 'name': 'Everything, All At Once', 'period': 's4w3'},
 {'slug': 'nightmare-clash-s4w3', 'name': 'Nightmare Clash', 'period': 's4w3'},
 {'slug': 'rage-room-s4w4', 'name': 'Rage Room', 'period': 's4w4'},
 {'slug': 'rooftop-rumble-s4w4', 'name': 'Rooftop Rumble', 'period': 's4w4'},
 {'slug': 'no-escape-2p-s4w4', 'name': 'No Escape 2P', 'period': 's4w4'},
 {'slug': 'dragon-cave-s4w4', 'name': 'Dragon Cave', 'period': 's4w4'},
 {'slug': 'hunting-party-s4w4', 'name': 'Hunting Party', 'period': 's4w4'},
 {'slug': 'windy-mountaintop-s4w4', 'name': 'Windy Mountaintop', 'period': 's4w4'},
 {'slug': 'juggle-juggle-s5w1', 'name': 'Juggle Juggle', 'period': 's5w1'},
 {'slug': 'bug-lord-bash-s5w1', 'name': 'Bug Lord Bash', 'period': 's5w1'},
 {'slug': 'double-double-dragon-s5w1', 'name': 'Double Double Dragon', 'period': 's5w1'},
 {'slug': 'rooftop-rumble-s5w1', 'name': 'Rooftop Rumble', 'period': 's5w1'},
 {'slug': 'x2-takedown-s5w1', 'name': 'X2 Takedown', 'period': 's5w1'},
 {'slug': 'axe-clash-nightmare-s5w1', 'name': 'Axe Clash Nightmare', 'period': 's5w1'},
 {'slug': 'cave-of-corruption-s5w2', 'name': 'Cave Of Corruption', 'period': 's5w2'},
 {'slug': 'knights-chambers-s5w2', 'name': "Knights' Chambers", 'period': 's5w2'},
 {'slug': 'taking-hits-s5w2', 'name': 'Taking Hits', 'period': 's5w2'},
 {'slug': 'ceremonial-score-s5w2', 'name': 'Ceremonial Score', 'period': 's5w2'},
 {'slug': 'rooftop-garden-s5w2', 'name': 'Rooftop Garden', 'period': 's5w2'},
 {'slug': 'toxic-tangle-s5w2', 'name': 'Toxic Tangle', 'period': 's5w2'},
 {'slug': 'mountaintop-cleanup-s5w3', 'name': 'Mountaintop Cleanup', 'period': 's5w3'},
 {'slug': 'canyon-peril-s5w3', 'name': 'Canyon Peril', 'period': 's5w3'},
 {'slug': 'thick-of-it-s5w3', 'name': 'Thick Of It', 'period': 's5w3'},
 {'slug': 'van-defense-s5w3', 'name': 'Van Defense', 'period': 's5w3'},
 {'slug': 'mass-invasion-s5w3', 'name': 'Mass Invasion', 'period': 's5w3'},
 {'slug': 'deep-gorge-s5w3', 'name': 'Deep Gorge', 'period': 's5w3'},
 {'slug': 'ramparts-s5w4', 'name': 'Ramparts', 'period': 's5w4'},
 {'slug': 'unhushed-library-s5w4', 'name': 'Unhushed Library', 'period': 's5w4'},
 {'slug': 'sewer-king-s5w4', 'name': 'Sewer King', 'period': 's5w4'},
 {'slug': 'moonlit-ruins-s5w4', 'name': 'Moonlit Ruins', 'period': 's5w4'},
 {'slug': 'twin-princes-s5w4', 'name': 'Twin Princes', 'period': 's5w4'},
 {'slug': 'throne-room-s5w4', 'name': 'Throne Room', 'period': 's5w4'},
 {'slug': 'build-up-s6w1', 'name': 'Build Up', 'period': 's6w1'},
 {'slug': 'boss-rumble-s6w1', 'name': 'Boss Rumble', 'period': 's6w1'},
 {'slug': 'extra-charge-2p-s6w1', 'name': 'Extra Charge 2P', 'period': 's6w1'},
 {'slug': 'apocalypse-s6w1', 'name': 'Apocalypse', 'period': 's6w1'},
 {'slug': 'monster-magnet-s6w1', 'name': 'Monster Magnet', 'period': 's6w1'},
 {'slug': 'midnight-shakedown', 'name': 'Midnight Shakedown', 'period': 's6w1'},
 {'slug': 'shipwreck-harbour-s6w2', 'name': 'Shipwreck Harbour', 'period': 's6w2'},
 {'slug': 'snowclaw-summit-s6w2', 'name': 'Snowclaw Summit', 'period': 's6w2'},
 {'slug': 'herding-cats-s6w2', 'name': 'Herding Cats', 'period': 's6w2'},
 {'slug': 'ice-fishing-s6w2', 'name': 'Ice Fishing', 'period': 's6w2'},
 {'slug': 'snowdrift-cave-s6w2', 'name': 'Snowdrift Cave', 'period': 's6w2'},
 {'slug': 'purrgatory-s6w2', 'name': 'Purrgatory', 'period': 's6w2'},
 {'slug': 'big-3-s6w3', 'name': 'Big 3', 'period': 's6w3'},
 {'slug': 'dust-pit-s6w3', 'name': 'Dust Pit', 'period': 's6w3'},
 {'slug': 'death-by-a-thousand-cuts-s6w3', 'name': 'Death By A Thousand Cuts', 'period': 's6w3'},
 {'slug': 'bleak-shaft-s6w3', 'name': 'Bleak Shaft', 'period': 's6w3'},
 {'slug': 'score-hunt-s6w3', 'name': 'Score Hunt', 'period': 's6w3'},
 {'slug': 'cave-of-corruption-s6w3', 'name': 'Cave Of Corruption', 'period': 's6w3'},
 {'slug': 'rustwater-harbor-s6w4', 'name': 'Rustwater Harbor', 'period': 's6w4'},
 {'slug': 'market-street-s6w4', 'name': 'Market Street', 'period': 's6w4'},
 {'slug': 'deadeye-district-s6w4', 'name': 'Deadeye District', 'period': 's6w4'},
 {'slug': 'reflexology-s6w4', 'name': 'Reflexology', 'period': 's6w4'},
 {'slug': 'garbage-disposal-s6w4', 'name': 'Garbage Disposal', 'period': 's6w4'},
 {'slug': 'back-alley-brawl-s6w4', 'name': 'Back Alley Brawl', 'period': 's6w4'}]
API_KEY = os.getenv("CELLSTRING_API_KEY")
BASE_URL = "https://api.cellstring.com/games/moco/leaderboard/"
CACHE_FILE = "players.json"
headers = {"X-API-Key": API_KEY}

def get_with_retry(url, headers, max_retries=10):
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 429:
            time.sleep(30)
            continue

        response.raise_for_status()
        return response.json()

    raise Exception(f"Max retries reached for {url}")

def fetch_data():
    # Fetches cellstring API
    players = defaultdict(lambda: {
        "tag": None,
        "name": None,
        "entries": []
    })

    for rift in rifts:

        slug = rift["slug"]
        period = rift["period"]

        data = get_with_retry(BASE_URL + slug, headers)

        if not slug.endswith("-" + period):
            slug = f"{slug}-{period}"

        print(f"Fetching {slug}...")

        rows = data if isinstance(data, list) else (    # Get LB entries
            data.get("entries", data.get("leaderboard", data.get("data", [])))
        )

        for row in rows:

            tag = row.get("tag")
            name = row.get("name")

            if not tag:
                continue

            score = row.get("score") or {}  # if Score Hunt

            # Prefer valueSeconds, fallback to value
            value = score.get("valueSeconds") # If Rift
            if value is None:
                value = score.get("value")

            if value is None:
                continue

            player = players[tag]

            player["tag"] = tag
            player["name"] = name

            player["entries"].append({
                "period": period,
                "slug": slug,
                "rift": rift["name"],
                "score": float(value)
            })

    players = dict(players)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(players, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(players)} players to {CACHE_FILE}")

    return players

def load_data():

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        players = json.load(f)

    print(f"Loaded {len(players)} players from {CACHE_FILE}")

    return players

def build_connections(players):
# Creates connections between players, 1 rift together = 1 connection
    connections = defaultdict(int)
    rift_entries = defaultdict(list)

    for tag, player in players.items():
        for entry in player["entries"]:
            rift_entries[entry["slug"]].append({
                "tag": tag,
                "score": entry["score"]
            })

    for slug, entries in rift_entries.items():

        for a, b in combinations(entries, 2):   # Has to be same slug, aka rift + period

            if a["tag"] == b["tag"]:
                continue

            if a["score"] == b["score"]:
                pair = tuple(sorted([a["tag"], b["tag"]]))
                connections[pair] += 1

    print(f"Connections: {len(connections)}")

    return connections


# ---------------- GENERATE GRAPH ----------------

def generate_graph(players, connections):

    MIN_MATCHES = 2     # Otherwise graph gets too heavy

    filtered_connections = {
        pair: weight for pair, weight in connections.items()
        if weight >= MIN_MATCHES
    }

    player_weights = defaultdict(int)
    for (tag1, tag2), weight in filtered_connections.items():
        player_weights[tag1] += weight
        player_weights[tag2] += weight

    nodes = [
        {"id": tag, "label": player["name"] or tag}
        for tag, player in players.items()
        if tag in player_weights
    ]

    edges = [
        {
            "from": tag1,
            "to": tag2,
            "value": weight,
            "title": f"{weight} matching entries",
        }
        for (tag1, tag2), weight in filtered_connections.items()
    ]

    with open("graph_data.js", "w", encoding="utf-8") as f:
        f.write("const GRAPH_DATA = ")
        json.dump({"nodes": nodes, "edges": edges}, f, ensure_ascii=False)
        f.write(";\n")

    print(f"Wrote {len(nodes)} nodes and {len(edges)} edges to graph_data.js")
    webbrowser.open(Path("player_network.html").resolve().as_uri())


# ---------------- MAIN ----------------

# True to refresh API data.
FETCH_NEW_DATA = False

if FETCH_NEW_DATA:
    players = fetch_data()
else:
    players = load_data()

connections = build_connections(players)
generate_graph(players, connections)

#%%
