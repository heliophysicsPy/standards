# Releasing PyHC Enhancement Proposals

This document describes the technical, bits-and-bytes steps necessary
to upload PHEPs once they have been accepted by a vote. It does not
set a standard for PyHC, but documents implementation of a part of
that policy. As such it can be updated in light of new technical
realities without requiring an updated standard.

Unless otherwise noted, these steps can be carried out by the PHEP author, PHEP editors, or PyHC leadership.

## Reserve a DOI on Zenodo
  * Click the "+" sign on Zenodo or go to the [new upload page](https://zenodo.org/uploads/new).
  * At the top of the page, click the "Select a community" button. Search for "heliophysics" and find the "Python in Heliophysics Community" (with our nifty logo); click "Select".
  * Under "Basic information", "Do you already have a DOI for this upload?", click "No". Click the "Get a DOI now!" button that appears after clicking No.
  * Click the "Save draft" button on the right towards the top, we'll come back to this.

Note: Zenodo assigns [two DOIs](https://zenodo.org/help/versioning) on first upload, what we want to have on our citations is the version-specific one. When you reserve a DOI, the version-specific one is shown, but this can be verified by saving the draft record and previewing it. It looks like, in order to keep them connected, future revisions of a PHEP should not be uploaded as new records, but as updated versions of files on the existing record. This process is not entirely clear without going through it, and this document should be updated as we figure it out.

## Final git commit
  * Update the contents of the PHEP as documented in PHEP 1 (Status, current date in Post-History, Revision with date accepted/rejected, updated copyright date, and updated DOI with the DOI reserved above).
  * Add the Resolution header to the PHEP with a link to the minutes of the two votes on the PHEP.
  * Commit and push to the PR.
  * PHEP editors or PyHC leadership merge final commit. History should be maintained, so merge or rebase is fine, squash is not. We have been using merge.

## Creating files and release
  * Create a PDF of the PHEP from the markdown of the latest pushed commit; use pandoc: `pandoc -f commonmark phep-0001.md -V geometry:letterpaper,margin=1in -o phep-0001.pdf`. (This is in the `pandoc` package in Ubuntu and uses `rsvg-convert` from package `librsvg2-bin`.) Pandoc converts via LaTeX, which means if code blocks overflow the line length they will not be wrapped (a problem with a very long `Post-History` header); use RFC-2822 header folding as necessary. If the Markdown source references other files with relative reference, `pandoc` needs to be run in the same directory. Unfortunately pandoc's LaTeX renderer does not handle internal links well, but other renderers have other problems.
  * PHEP editors or PyHC leadership [create a release](https://github.com/heliophysicsPy/standards/releases/new) on GitHub. The release tag is the phep number and revision number, e.g. phep-2-1 for revision 1 of PHEP 2. (Potentially this can be zero-padded). The rendered PDF is the release file.

## Sending to Zenodo

Resume the draft record on Zenodo

### Files
  * Upload the rendered PDF, the Markdown source, and any other sources (e.g. images).

### Basic Information
  * Resource Type "Publication / Standard".
  * Title: PHEP number plus its title, e.g. "PHEP 1: PHEP Purpose and Guidelines".
  * Publication Date: Date when the release was tagged on GitHub.
  * Creators: The author of the PHEP, ideally including their ORCID.
  * Description: Leave blank.
  * Licenses: CC0 (there is no "public domain" option explicitly).

### Recommended Information
  * Contributors: the PHEP editor(s) who managed the process for this PHEP; consider including other major contributors to the discussion.
  * Keywords and subjects: None.
  * Languages: English.
  * Dates
    * Created: same as Created in the PHEP header, i.e. the date the PHEP number was assigned. This will always be the created date of revision 1.
    * Accepted: date of the final vote that accepted the PHEP as Final. This will always be the accepted date of revision 1.
    * Withdrawn: date of a PHEP's withdrawal, a final vote where it was Rejected, or the date of the vote that accepted its replacement.
    * Updated: only for revised PHEPs, date that a revision was merged to `main`.
  * Version: Revision number.
  * Publisher: Leave as Zenodo.

### Funding
Leave blank.

### Alternate Identifiers
Leave blank.

### Related Works
  * Is derived from: Identifier is link to GitHub release e.g. https://github.com/heliophysicsPy/standards/releases/tag/phep-2-12, Scheme URL.
  * Is derived from: Identifier is link to the Markdown source in the tagged commit, e.g. https://github.com/heliophysicsPy/standards/blob/a4b3f558b9ffa712324e63ff6a83325cc69e367f/pheps/phep-0001.md, Scheme URL.
  * For revisions of a single PHEP: Use "Is new version of", scheme DOI, and the Zenodo DOI of the previous revision. On the previous revision, add a new related work of "Is previous version of" and put in the new Zenodo DOI (this field should be updatable after the DOI is minted). Type is Publication/Standard for both.
  * Related works for PHEPs that replace: Use "Obsoletes", scheme DOI, and the Zenodo DOI of any PHEPs that are replaced; similarly update their records to "Is obsoleted by" and the new PHEP's Zenodo DOI. Type is again Publication/Standard.

### References
Leave blank.

### Software
  * Repository URL: https://github.com/heliophysicsPy/standards/ .
  * Programming language: Markdown.
  * Development Status: Active.

### Publishing Information
Leave blank.

### Conference
Leave blank.

### Domain Specific Fields
Leave blank.

### Visibility
Public

### Draft
Save the draft, preview, and publish when ready

## Updating website
Follow these steps to update PHEPs on the PyHC website:
- Clone the website repo: https://github.com/heliophysicsPy/heliophysicsPy.github.io
- Create a new feature branch for your changes
- Clone this [`standards`](https://github.com/heliophysicsPy/heliophysicsPy.github.io) repo where PHEPs are kept
- Run the `phep_to_yaml.py` script to get a new `pheps.yml` file (which will contain entries for every PHEP)
  - If a PHEP has a DOI but no corresponding `DOI` yaml field, manually add it in the format `10.XXXX/YYYYYYYY` (`phep_to_yaml.py` prints a warning when this is needed)
- In the website repo, place your new `pheps.yml` file inside the `_data/` folder (replacing the old one)
- Open a PR to merge your `pheps.yml` changes

## Related PHEPs
The process above should be repeated as necessary to update affected PHEPs. For example, if a PHEP is replaced, a new  revision needs to be uploaded, including which PHEP replaces it (and all the relevant Zenodo records, as noted). If a new revision of a PHEP is uploaded, the metadata on the Zenodo record of the previous revision need to be updated.
