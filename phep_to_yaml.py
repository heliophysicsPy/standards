#!/usr/bin/env python3

import email
import glob
import os.path
import re
import warnings

import yaml


phep_src = glob.glob(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'pheps', 'phep-*.md'))
pheps = []  # fully parsed
for ph in phep_src:
    if not re.match(r"^phep-\d+\.md$", os.path.basename(ph)):
        continue
    with open(ph, "rt") as f:
        if f.readline().rstrip() != "```":
            warnings.warn(f"{ph} preamble has no opening code fence, skipping.")
            continue
        headers = []
        for l in f:
            if l.rstrip() == "```":
                break
            headers.append(l)
        else:
            warnings.warn(f"{ph} preamble has no closing code fence, skipping.")
            continue
    phep = dict(email.message_from_string("".join(headers)))
    required = (
        "PHEP", "Title", "Author", "Discussions-To", "Revision", "Status",
        "Type", "Content-Type", "Created", "Post-History",
    )
    missing = [k for k in required if k not in phep]
    if missing:
        warnings.warn(f"{ph} missing headers {', '.join(missing)}, skipping.")
        continue
    optional = ("Requires", "Replaces", "Replaced-By", "Resolution", )
    bad = [k for k in phep if k not in required + optional]
    if bad:
        warnings.warn(
            f"{ph} has unexpected headers {', '.join(bad)}, skipping.")
        continue
    for k in ('PHEP', 'Revision'):
        phep[k] = int(phep[k])
    phep["Filename"] = os.path.basename(ph)
    pheps.append(phep)
with open("pheps.yml", "wt") as f:
    f.write(yaml.dump(pheps))
