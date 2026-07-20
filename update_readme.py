import urllib.request
import json
import re
import sys

url = "https://dev.to/api/articles?username=aniket_misra_e47d1564ab7b&per_page=3"

try:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        articles = json.loads(r.read().decode())
except Exception as e:
    print(f"fetch failed: {e}", file=sys.stderr)
    sys.exit(1)

if not articles:
    print("no articles returned", file=sys.stderr)
    sys.exit(1)

lines = ["<!-- BLOG-POST-LIST:START -->"]
for a in articles:
    date = a["published_at"][:10]
    title = a["title"].replace("[", "(").replace("]", ")")  # escape markdown
    lines.append(f"- [{title}]({a['url']}) — `{date}`")
lines.append("<!-- BLOG-POST-LIST:END -->")
new_block = "\n".join(lines)

print("fetched posts:")
print(new_block)

try:
    with open("README.md", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("README.md not found", file=sys.stderr)
    sys.exit(1)

if "<!-- BLOG-POST-LIST:START -->" not in content:
    print("markers not found in README.md", file=sys.stderr)
    sys.exit(1)

updated = re.sub(
    r"<!-- BLOG-POST-LIST:START -->.*?<!-- BLOG-POST-LIST:END -->",
    new_block,
    content,
    flags=re.DOTALL,
)

with open("README.md", "w") as f:
    f.write(updated)

print("README.md updated successfully")