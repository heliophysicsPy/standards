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
        body = f.readlines()
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
    idx = next((i for i, l in enumerate(body)
                if l.startswith("# Copyright")), None)
    if idx is not None:
        doi_lines = [l for l in body[idx:] if " doi " in l]
        for doi_line in doi_lines:
            m = re.search(r"10\.\d{4}(\.\d+)*/[-._;()/:A-Z0-9]+",
                          doi_line, flags=re.IGNORECASE)
            if m:
                phep["DOI"] = m.group(0)
                break
    if "DOI" not in phep:
        warnings.warn(
            f"Found no DOI in {ph}, must fix output by hand.")
        phep["DOI"] = "Unknown"
    pheps.append(phep)
with open("pheps.yml", "wt") as f:
    f.write(yaml.dump(pheps))
