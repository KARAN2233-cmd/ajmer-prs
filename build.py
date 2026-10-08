"""Builds the website into ./site and fills in the Firebase values from GitHub Secrets (or Variables).

Page sources (in the repo root) may be named either way, the script finds them:
  page            : index.template.html | index_template.html | index.html
  service worker  : firebase-messaging-sw.template.js | firebase-messaging-sw_template.js | firebase-messaging-sw.js
The source must contain the __NAME__ placeholders. Real keys must never be typed into it.
"""
import os, re, shutil, sys

NAMES = [
    "FIREBASE_API_KEY", "FIREBASE_AUTH_DOMAIN", "FIREBASE_PROJECT_ID", "FIREBASE_STORAGE_BUCKET",
    "FIREBASE_MESSAGING_SENDER_ID", "FIREBASE_APP_ID", "VAPID_KEY", "GAS_URL",
]

values = {n: os.environ.get(n, "").strip() for n in NAMES}
missing = [n for n, v in values.items() if not v]
if missing:
    sys.exit("Missing or empty GitHub Secrets/Variables: " + ", ".join(missing) +
             "  (names must match exactly, in Settings > Secrets and variables > Actions)")

vapid = values["VAPID_KEY"]
if not re.fullmatch(r"[A-Za-z0-9_-]{80,100}", vapid):
    sys.exit("VAPID_KEY does not look like a Firebase Web Push key (about 87 characters, starts with B, "
             "no spaces or quotes). Re-create the secret. Length found: %d" % len(vapid))

ANY_PLACEHOLDER = re.compile(r"__[A-Z_]+__")


def has_placeholders(text):
    return any("__" + n + "__" in text for n in NAMES)


def find_source(candidates):
    """First existing candidate that really contains our placeholders."""
    found = [c for c in candidates if os.path.exists(c)]
    if not found:
        sys.exit("Missing source file in the repo root. Expected one of: " + ", ".join(candidates)
                 + ". Files found: " + ", ".join(sorted(os.listdir("."))))
    for c in found:
        if has_placeholders(open(c, encoding="utf-8").read()):
            return c
    sys.exit("Found " + ", ".join(found) + " but it has no __NAME__ placeholders "
             "(it looks like an old copy with real keys typed in). Upload the placeholder version again.")


os.makedirs("site", exist_ok=True)

SOURCES = [
    (["index.template.html", "index_template.html", "index.html"], "index.html"),
    (["firebase-messaging-sw.template.js", "firebase-messaging-sw_template.js", "firebase-messaging-sw.js"],
     "firebase-messaging-sw.js"),
]

for candidates, target in SOURCES:
    source = find_source(candidates)
    text = open(source, encoding="utf-8").read()
    for n, v in values.items():
        text = text.replace("__" + n + "__", v)

    left = [n for n in NAMES if "__" + n + "__" in text]       # only OUR placeholders can fail the build
    if left:
        sys.exit(source + " still has placeholders: " + ", ".join(left))

    for i, line in enumerate(text.splitlines(), 1):             # any other __WORD__ is just a warning
        if ANY_PLACEHOLDER.search(line):
            print("Warning: %s:%d has an unknown __TOKEN__ (not filled in): %s" % (source, i, line.strip()))

    open(os.path.join("site", target), "w", encoding="utf-8").write(text)
    print("Built site/%s from %s" % (target, source))

for f in ["manifest.json", "icon-192.png", "icon-512.png"]:
    if not os.path.exists(f):
        sys.exit("Missing file in the repo root: " + f)
    shutil.copy(f, os.path.join("site", f))

print("Done: site/ has", len(os.listdir("site")), "files,", len(values), "values filled in.")
