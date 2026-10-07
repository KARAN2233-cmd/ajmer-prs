"""Builds the website into ./site and fills in the Firebase values from GitHub Secrets."""
import os, re, shutil, sys

NAMES = [
    "FIREBASE_API_KEY", "FIREBASE_AUTH_DOMAIN", "FIREBASE_PROJECT_ID", "FIREBASE_STORAGE_BUCKET",
    "FIREBASE_MESSAGING_SENDER_ID", "FIREBASE_APP_ID", "VAPID_KEY", "GAS_URL",
]

values = {n: os.environ.get(n, "").strip() for n in NAMES}
missing = [n for n, v in values.items() if not v]
if missing:
    sys.exit("Missing GitHub Secrets: " + ", ".join(missing))

vapid = values["VAPID_KEY"]
if not re.fullmatch(r"[A-Za-z0-9_-]{80,100}", vapid):
    sys.exit("VAPID_KEY does not look like a Firebase Web Push key (about 87 characters, starts with B, "
             "no spaces or quotes). Re-create the secret. Length found: %d" % len(vapid))

os.makedirs("site", exist_ok=True)

for template, target in [("index.template.html", "index.html"),
                         ("firebase-messaging-sw.template.js", "firebase-messaging-sw.js")]:
    text = open(template, encoding="utf-8").read()
    for n, v in values.items():
        text = text.replace("__" + n + "__", v)
    left = re.findall(r"__[A-Z_]+__", text)
    if left:
        sys.exit(template + " still has placeholders: " + ", ".join(sorted(set(left))))
    open(os.path.join("site", target), "w", encoding="utf-8").write(text)

for f in ["manifest.json", "icon-192.png", "icon-512.png"]:
    if not os.path.exists(f):
        sys.exit("Missing file in the repo root: " + f)
    shutil.copy(f, os.path.join("site", f))

print("Built site/ with", len(values), "values filled in.")
