#!/usr/bin/env python3
"""Open every link in the Markdown files at the top of this repository.

Writes maintenance/link-check.md with the date and the result. When every
link answers, it also sets the month in the README sentence "Every link
below was opened and checked in <month> <year>".

It only reads pages and writes files in this repository. It opens no
issues, posts no comments and sends nothing to anyone. It always exits 0
when the check itself ran, so a dead link never produces a failure mail;
the log file is the record.

Python standard library only. Run: python scripts/check_links.py [--no-write]
"""
import datetime
import glob
import os
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "maintenance", "link-check.md")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
# Sites that often refuse machines while the page is fine for a person.
BLOCKED_CODES = {401, 403, 429, 999}
SENTENCE = re.compile(r"(Every link below was opened and checked in )([A-Z][a-z]+ \d{4})")


def links_in(path):
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)  # examples in inline code are not links
    found = re.findall(r"\]\(\s*<?([^)\s>]+)>?[^)]*\)", text)
    found += re.findall(r"<(https?://[^>\s]+)>", text)
    return found


def fetch(url):
    """Return (status, note). status is an int, or 0 when no answer came."""
    last = ""
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.status, ""
        except urllib.error.HTTPError as err:
            if err.code in BLOCKED_CODES or err.code < 500:
                return err.code, ""
            last = "HTTP %d" % err.code
        except Exception as err:  # timeouts, DNS, TLS
            last = type(err).__name__
        time.sleep(5 * (attempt + 1))
    return 0, last


def main():
    write = "--no-write" not in sys.argv
    files = sorted(glob.glob(os.path.join(ROOT, "*.md")))
    web, local = {}, []
    for path in files:
        name = os.path.basename(path)
        for link in links_in(path):
            if link.startswith(("http://", "https://")):
                web.setdefault(link.split("#")[0], set()).add(name)
            elif link.startswith(("#", "mailto:")):
                continue
            else:
                target = os.path.join(ROOT, link.split("#")[0])
                if not os.path.exists(target):
                    local.append((link, name))

    dead, unsure = [], []
    for url in sorted(web):
        status, note = fetch(url)
        where = ", ".join(sorted(web[url]))
        if 200 <= status < 400:
            continue
        if status in BLOCKED_CODES:
            unsure.append((url, "answered %d to the machine" % status, where))
        else:
            dead.append((url, ("answered %d" % status) if status else "no answer (%s)" % note, where))
        print("PROBLEM", status, url)

    today = datetime.datetime.now(datetime.timezone.utc).date()
    out = ["# Link check", "",
           "Last run: %s (UTC)." % today.isoformat(), "",
           "Scope: every web link and every link to a file in the Markdown files at the top of this repository "
           "(%s). A machine opened each one with a browser-like request. "
           "This is a link review, not an installation or runtime test of the projects."
           % ", ".join(os.path.basename(f) for f in files), "",
           "- Web links opened: %d" % len(web),
           "- Answered normally: %d" % (len(web) - len(dead) - len(unsure)),
           "- Dead or not answering: %d" % len(dead),
           "- Refused the machine, needs a look by a person: %d" % len(unsure),
           "- Links to files in this repository that do not exist: %d" % len(local), ""]
    for title, rows in (("Dead or not answering", dead), ("Refused the machine", unsure)):
        if rows:
            out += ["## " + title, ""] + ["- <%s> %s (in %s)" % r for r in rows] + [""]
    if local:
        out += ["## Missing files", ""] + ["- `%s` (in %s)" % r for r in local] + [""]
    report = "\n".join(out)
    print(report)

    if write:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(report)
        if not dead and not unsure and not local:
            readme = os.path.join(ROOT, "README.md")
            text = open(readme, encoding="utf-8").read()
            month = today.strftime("%B %Y")
            new = SENTENCE.sub(lambda m: m.group(1) + month, text, count=1)
            if new != text:
                with open(readme, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(new)
    return 0


if __name__ == "__main__":
    sys.exit(main())
