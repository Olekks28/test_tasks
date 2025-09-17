import requests
from collections import deque
from urllib.parse import urlparse, unquote

WIKI_API = "https://en.wikipedia.org/w/api.php"
WIKI_BASE = "https://en.wikipedia.org/wiki/"
HITLER_TITLE = "Adolf Hitler"
MAX_DEPTH = 6
HEADERS = {"User-Agent": "HitlerCrawler/1.0 (example@example.com)"} # Wikipedia API User-Agent (email optional)

def extract_title(url: str) -> str:
    path = urlparse(url).path
    if path.startswith("/wiki/"):
        return unquote(path.split("/wiki/")[1].replace("_", " "))
    return unquote(url.replace("_", " "))

def get_pages(title, prop):
    params = {
        "action": "query",
        "format": "json",
        "titles": title if prop == "links" else None,
        "list": "backlinks" if prop == "backlinks" else None,
        "prop": prop if prop == "links" else None,
        "plnamespace": 0,
        "pllimit": "max",
        "bllimit": "max",
        "bltitle": title if prop == "backlinks" else None
    }
    results = []
    try:
        while True:
            r = requests.get(WIKI_API, params=params, headers=HEADERS, timeout=10)
            r.raise_for_status()
            data = r.json()
            if prop == "links":
                pages = data.get("query", {}).get("pages", {})
                for page in pages.values():
                    results.extend(l.get("title") for l in page.get("links", []))
            else:
                results.extend(b.get("title") for b in data.get("query", {}).get("backlinks", []))
            if "continue" in data:
                params.update(data["continue"])
            else:
                break
    except Exception:
        return []
    return list(dict.fromkeys(filter(None, results)))

def bidirectional_search(start_title):
    if start_title == HITLER_TITLE:
        return [HITLER_TITLE]

    forward_q = deque([(start_title, [start_title])])
    backward_q = deque([(HITLER_TITLE, [HITLER_TITLE])])
    forward_seen = {start_title: [start_title]}
    backward_seen = {HITLER_TITLE: [HITLER_TITLE]}

    for _ in range(MAX_DEPTH):
        if forward_q:
            cur, path = forward_q.popleft()
            for link in get_pages(cur, "links"):
                if link not in forward_seen:
                    new_path = path + [link]
                    forward_seen[link] = new_path
                    forward_q.append((link, new_path))
                    if link in backward_seen:
                        return new_path + backward_seen[link][::-1][1:]

        if backward_q:
            cur, path = backward_q.popleft()
            for link in get_pages(cur, "backlinks"):
                if link not in backward_seen:
                    new_path = path + [link]
                    backward_seen[link] = new_path
                    backward_q.append((link, new_path))
                    if link in forward_seen:
                        return forward_seen[link] + new_path[::-1][1:]
    return None

if __name__ == "__main__":
    start_title = extract_title(input("Enter Wikipedia page URL or English title: ").strip())
    path = bidirectional_search(start_title)
    if path:
        print("\nPath found:\n")
        for t in path:
            print(f"{t} → {WIKI_BASE}{t.replace(' ', '_')}")
    else:
        print("Hitler not found within", MAX_DEPTH, "steps")
