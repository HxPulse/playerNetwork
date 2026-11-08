#%%
import requests
import webbrowser
import time
import sys
import json
from collections import defaultdict
from itertools import combinations
print(sys.executable)
from pyvis.network import Network

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
API_KEY = "cs_5d1fcd28cbfcb2d2f981422cf995282459b5a83f929e17ee"
BASE_URL = "https://api.cellstring.com/games/moco/leaderboard/"
CACHE_FILE = "players.json"
headers = {"X-API-Key": API_KEY}

def get_with_retry(url, headers, max_retries=10):
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 429:
            print(f"Rate limited. Waiting 30s... ({attempt + 1}/{max_retries})")
            time.sleep(30)
            continue

        response.raise_for_status()
        return response.json()

    raise Exception(f"Max retries reached for {url}")

def fetch_data():

    players = defaultdict(lambda: {
        "tag": None,
        "name": None,
        "entries": []
    })

    for rift in rifts:

        slug = rift["slug"]
        period = rift["period"]

        data = get_with_retry(BASE_URL + slug, headers)

        # Ensure slug ends with its period
        if not slug.endswith("-" + period):
            slug = f"{slug}-{period}"

        print(f"Fetching {slug}...")

        # Adapt this if your API wraps results differently.
        rows = data if isinstance(data, list) else (
            data.get("entries", data.get("leaderboard", data.get("data", [])))
        )

        for row in rows:

            tag = row.get("tag")
            name = row.get("name")

            if not tag:
                continue

            score = row.get("score") or {}

            # Prefer valueSeconds, fallback to value
            value = score.get("valueSeconds")
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
    # Save fetched data
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

    connections = defaultdict(int)
    rift_entries = defaultdict(list)

    for tag, player in players.items():
        for entry in player["entries"]:
            rift_entries[entry["slug"]].append({
                "tag": tag,
                "score": entry["score"]
            })

    for slug, entries in rift_entries.items():

        for a, b in combinations(entries, 2):

            if a["tag"] == b["tag"]:
                continue

            if a["score"] == b["score"]:
                pair = tuple(sorted([a["tag"], b["tag"]]))
                connections[pair] += 1

    print(f"Connections: {len(connections)}")

    return connections


# ---------------- GENERATE GRAPH ----------------

def generate_graph(players, connections):
    
    MIN_CONNECTION_WEIGHT = 20
    MIN_MATCHES = 3

    connections = {
        pair: weight
        for pair, weight in connections.items()
        if weight >= MIN_MATCHES
    }

    player_weights = defaultdict(int)

    for (tag1, tag2), weight in connections.items():
        player_weights[tag1] += weight
        player_weights[tag2] += weight

    # Keep only sufficiently connected players
    filtered_players = {
        tag: player
        for tag, player in players.items()
        if player_weights[tag] >= MIN_CONNECTION_WEIGHT
    }

    # Keep only connections between retained players
    filtered_connections = {
        pair: weight
        for pair, weight in connections.items()
        if pair[0] in filtered_players and pair[1] in filtered_players
    }

    players = filtered_players
    connections = filtered_connections
    print(f"Players displayed: {len(players)}")
    print(f"Connections displayed: {len(connections)}")

    net = Network(
        height="100vh", 
        width="100%",
        bgcolor="#111827",
        font_color="white",
        notebook=False,
        cdn_resources="in_line"
    )

    net.repulsion(
        node_distance=900,
        central_gravity=0.05,
        spring_length=250,
        spring_strength=0.01,
        damping=0.09
    )

    for tag, player in players.items():

        degree = sum(
            weight for pair, weight in connections.items()
            if tag in pair
        )

        net.add_node(
            tag,
            label=player["name"] or tag,
            title=f"{player["name"]}\n{tag}\nConnections: {degree}\n",
            size=min(22, 8 + degree * 0.3),
            color="#60A5FA",
            font={
                "size": 100,  
                "face": "arial",
                "bold": True,
                "strokeWidth": 3,
                "strokeColor": "#111827"
            }
        )

    for (tag1, tag2), weight in connections.items():

        net.add_edge(
            tag1,
            tag2,
            value=weight,
            title=f"{weight} matching entries",
            color="#64748b",
            originalColor="#64748b"
        )

    html = net.generate_html()

    with open("highlight.js", "r", encoding="utf-8") as f:
        js = f.read()

    html = html.replace("</body>", f"<script>{js}</script></body>")
    with open("player_network.html", "w", encoding="utf-8") as f:
        f.write(html)
    webbrowser.open("player_network.html")


# ---------------- MAIN ----------------

# Change this to True whenever you want to refresh API data.
FETCH_NEW_DATA = False

if FETCH_NEW_DATA:
    players = fetch_data()
else:
    players = load_data()

connections = build_connections(players)
#generate_graph(players, connections)


def get_top_connected_players(connections, players, limit=20):
    player_connections = defaultdict(int)

    # Sum connection weights for each player
    for (tag1, tag2), weight in connections.items():
        player_connections[tag1] += weight
        player_connections[tag2] += weight

    # Sort players by total connection weight
    ranked = sorted(
        player_connections.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        {
            "name": players[tag]["name"],
            "tag": tag,
            "connections": count
        }
        for tag, count in ranked[:limit]
    ]

def get_top_matching_pairs(connections, players, limit=20):
    ranked = sorted(
        connections.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        {
            "player1": players[tag1]["name"],
            "player2": players[tag2]["name"],
            "tag1": tag1,
            "tag2": tag2,
            "matches": weight
        }
        for (tag1, tag2), weight in ranked[:limit]
    ]

def get_player_top_connections(player_tag, connections, players, limit=15):
    # Find all connections involving this player
    results = []

    for (tag1, tag2), weight in connections.items():
        if tag1 == player_tag:
            other_tag = tag2
        elif tag2 == player_tag:
            other_tag = tag1
        else:
            continue

        results.append({
            "tag": other_tag,
            "name": players[other_tag]["name"],
            "matchings": weight
        })

    # Sort by most matchings
    results.sort(key=lambda x: x["matchings"], reverse=True)
    results = results[:limit]

    for i, player in enumerate(results, 1):
        print(f"{i}. {player['name']} — {player['matchings']} matchings")

    return

top10 = get_player_top_connections("#G8P880G", connections, players)
#%%
