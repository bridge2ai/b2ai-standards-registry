---
name: cfde-dcc-curation
description: >
  Curate standards, tools, and organizations from one NIH Common Fund Data Ecosystem
  (CFDE) Data Coordinating Center (DCC) into this registry. Use when asked to work a
  child issue of the CFDE curation epic (#524), to "curate Kids First / MoTrPAC / 4DN /
  SPARC / HuBMAP / GTEx" or any other DCC listed at https://cfde.cloud/info/dcc, or to
  run "the next CFDE batch". Covers research, id assignment, entry authoring,
  annotation of existing entries, validation, regeneration, and the commit.
---

# CFDE DCC curation

One DCC per issue. One issue per branch. Batches are fine. The first batch for a DCC
adds the organization and the resources named in the issue. Later batches extend.

Work on the issue's own branch, cut from `origin/main`:

```bash
git fetch origin && git checkout -b issue-<N>-<dcc> origin/main
```

## 1. Read the issue and the DCC

The child issue lists candidates under "Already in the registry" and "Candidates to add
or verify". Treat both lists as hypotheses. Verify each one against the DCC's own pages
before writing anything. Sources that have paid off:

- The DCC portal and its help center or docs site. Look for a "data process",
  "data dictionary", "data model", "file formats", or "data access" page.
- The DCC GitHub organization. `gh api "search/repositories?q=<term>+org:<org>"` finds
  model, schema, ETL, and API repositories. `gh api repos/<org>/<repo>/readme --jq
  .content | base64 -d` reads a README without a browser.
- The CFDE DCC page https://cfde.cloud/info/dcc for the one-line program description.
- Crossref for every citation: `curl -s https://api.crossref.org/works/<doi>`. Never
  write a reference from memory. This has caught wrong author lists before.
- ROR (`https://api.ror.org/v2/organizations?query=...`) and Wikidata
  (`wbsearchentities`) for organization identifiers. Check the hit is the right body.
  A name match is not enough. ROR returned a Japanese nonprofit for "Kids First".

Write down what each source actually says. The entry text must be traceable to it.

## 2. Decide what to add and what to annotate

Check names first. Abbreviations collide.

```bash
grep -n -i -E "^  name: (foo|bar)$" src/data/DataStandardOrTool.yaml
```

Look up an id by exact name:

```bash
awk -v want="NAME" '/^- id: /{id=$3} $0=="  name: "want{print want" => "id}' src/data/DataStandardOrTool.yaml
```

Rules of thumb:

- If a resource exists, annotate it. Do not add a second entry.
- If an abbreviation exists for a different thing (MAF, SPARC), add the new entry under
  a disambiguated name and say in `purpose_detail` that the two are unrelated.
- Formats a DCC merely consumes (FASTQ, BAM, VCF) get an annotation, not new text.
- Cross-DCC infrastructure that surfaces while curating (dbGaP, Gen3, RefMet, RRID)
  belongs in the batch where it first came up. Do not defer it to a separate issue.
- One entry per platform, service, or model. Do not split a portal into its UI and API
  unless the API has its own published data model.

## 3. Assign ids

```bash
grep -oE "^- id: B2AI_STANDARD:[0-9]+" src/data/DataStandardOrTool.yaml | sed 's/.*://' | sort -n | tail -1
grep -oE "^  - id: B2AI_ORG:[0-9]+" src/data/Organization.yaml | sed 's/.*://' | sort -n | tail -1
```

Next id is max plus one. Ids are never reused. Assign the organization id first so the
standard entries can point at it.

## 4. Organization entry

Append to `src/data/Organization.yaml` (4-space indent inside `organizations:`):

```yaml
  - id: B2AI_ORG:NNN
    category: B2AI_ORG:Organization
    contributor_github_name: caufieldjh
    contributor_name: Harry Caufield
    contributor_orcid: "ORCID:0000-0001-5705-7831"
    description: <full program name>
    name: <short name, e.g. Kids First DRC, MoTrPAC, 4DN, NIH SPARC>
    subclass_of:
    - B2AI_ORG:68
    url: <program url>
```

`B2AI_ORG:68` is NIH Common Fund. Add `ror_id: ror:xxxxxxx` and `wikidata_id:
wikidata:Qnnn` only when the identifier is for the program itself, not its host
institution. A host institution that is itself a responsible organization for some
tool gets its own entry (CTDS is `B2AI_ORG:129`).

## 5. Standard or tool entries

Append to `src/data/DataStandardOrTool.yaml` (2-space indent, top-level `- id:`).
Field order matches the rest of the file:

```yaml
- id: B2AI_STANDARD:NNNN
  category: B2AI_STANDARD:<SoftwareOrTool|BiomedicalStandard|DataStandard|OntologyOrVocabulary|Registry|...>
  collection:
  - <tag>
  concerns_data_topic:
  - B2AI_TOPIC:NN
  contribution_date: 'YYYY-MM-DD'
  contributor_github_name: caufieldjh
  contributor_name: Harry Caufield
  contributor_orcid: ORCID:0000-0001-5705-7831
  description: <one-line expansion of the name>
  formal_specification: <spec or code repository url, if one exists>
  has_relevant_organization:
  - B2AI_ORG:<dcc>          # the DCC uses or contributes to it
  is_open: true
  name: <short name>
  purpose_detail: <one paragraph, see below>
  related_to:
  - B2AI_STANDARD:NNN
  requires_registration: false
  responsible_organization:
  - B2AI_ORG:<owner>        # the DCC or body that publishes and maintains it
  url: <landing page>
  publication:
    ref_url: https://doi.org/...
    ref_title: ...
    ref_authors:
    - Surname AB
    ref_publication_year: NNNN
    ref_journal: ...
```

Conventions:

- `responsible_organization` is the publisher. `has_relevant_organization` is a user
  or contributor. A DCC-built resource gets the DCC as responsible. A resource the DCC
  merely uses gets the DCC as relevant.
- `is_open` is about the resource, not the data behind it. dbGaP is open and requires
  registration.
- Do not set `used_in_bridge2ai: true` for CFDE membership alone. A Grand Challenge
  must demonstrably use the thing.
- `collection` tags live in `src/schema/standards_datastandardortool_schema.yaml` under
  `StandardsCollectionTag`. Common picks: `fileformat`, `datamodel`, `dataregistry`,
  `cloudplatform`, `cloudservice`, `toolkit`, `codesystem`, plus the maturity tags
  `implementation_maturity_pilot|production` and `standards_process_maturity_draft|
  development|final`.
- `concerns_data_topic` ids are in `src/data/DataTopic.yaml`. Pick four to eight.
- `purpose_detail` is a plain YAML scalar wrapped at about 88 columns with 4-space
  continuation. It must not contain `: ` or ` #`. Say what the thing is, what it
  holds or produces, who runs it, how access works, and how it connects to the other
  entries in the batch. Name versions and dates when the source gives them. Say when
  a repository calls itself experimental or has gone quiet.
- `publication` only from a Crossref-verified record. When there is no paper, keep
  the block with an empty placeholder, exactly as the rest of the file does:

  ```yaml
    publication:
      ref_url: ''
  ```

  Every standards entry must carry a `publication` key. The TSV serializer
  (`json_flattener`) indexes `obj['publication']` on every row and raises
  `KeyError: 'publication'` on the first entry without one.

## 6. Annotate existing entries

For every existing entry the DCC uses, add the DCC org id to
`has_relevant_organization`. Create the key before `name:` if it is absent. Do not
touch `purpose_detail` of an existing entry unless it is wrong. Also annotate C2M2
(`B2AI_STANDARD:63`) when the DCC has a C2M2 submission process.

The script pattern from the Kids First batch does this safely: split the file on
`^- id: `, find the target block, append `  - B2AI_ORG:NNN` after the last list item
of `has_relevant_organization`, and skip blocks that already carry the id.

## 7. Validate and regenerate

```bash
make -f project.Makefile validate
make -f project.Makefile sanitize-data
```

`validate` must print `No issues found` for every file. `sanitize-data` normalizes
typographic Unicode in the YAML.

`make -f project.Makefile all-data` is the intended way to rebuild
`project/data/*.json` and `project/data/*.tsv`, and as of 2026-09-02 it fails from the
repository root with linkml 1.11.1 (schema imports resolve against the working
directory, so `standards_manifest_schema.yaml` is not found). It also deletes
`project/data/` before it fails. If that happens, `git checkout -- project/data` and
run the converter from the schema directory instead:

```bash
cd src/schema
for pair in DataStandardOrTool:DataStandardOrToolContainer Organization:OrganizationContainer; do
  f=${pair%%:*}; c=${pair#*:}
  for fmt in json tsv; do
    PYTHONHASHSEED=281 poetry run linkml-convert -s standards_schema_all.yaml -C $c -t $fmt \
      -o ../../project/data/$f.$fmt ../data/$f.yaml
  done
done
cd ../..
make -f project.Makefile src/all_ids.tsv
```

`PYTHONHASHSEED=281` matters. The TSV serializer (`json_flattener`) orders the
`has_application_*` columns by set iteration, which follows Python's hash seed.
Seed 281 reproduces the column order already committed on `main`, so the TSV diff
shows changed rows only. Without it the whole file reorders and the review diff is
unreadable. If the header on `main` ever changes, find the new seed by simulating
`set().update(keys)` over the first entry's `has_application` keys for seeds 0 to
20000 and comparing to the committed header.

Add the other five file:container pairs from `project.Makefile` if their YAML
changed. "Prefix case mismatch" warnings are noise. Commit the regenerated files with
the YAML. Check every new `url` and `formal_specification` returns 200 with
`curl -s -o /dev/null -w '%{http_code}' -L`. If a live API endpoint does not answer,
point `url` at the code repository and say so in the issue comment.

The repository has a `custom-yaml-formatter` pre-commit hook that sorts keys and
re-indents. It is not installed in `.git/hooks` and the files on `main` do not pass
its `--check`. Do not run `scripts/format_yaml.py` on the data files. Match the
existing layout by hand: 2-space keys, list items at the same indent as their key,
`- id:` at column 0 for standards and `  - id:` for organizations.

## 8. Commit and report

One commit per batch. Message shape:

```
Add <DCC> organization and first batch of <DCC> entries

Refs #<issue>.

<one paragraph on what the batch covers and what it verified>

- B2AI_ORG:NNN <name>
- B2AI_STANDARD:NNNN <name>, <one clause>
...
Annotated with B2AI_ORG:NNN: <list of existing ids>.
```

Then comment on the issue with the same list, what was left out and why, and what
the next batch should cover. Tick the checkbox on the epic (#524) only when the DCC
issue closes.

## Files touched per batch

- `src/data/Organization.yaml`
- `src/data/DataStandardOrTool.yaml`
- `project/data/Organization.{json,tsv}`
- `project/data/DataStandardOrTool.{json,tsv}`
- `src/all_ids.tsv`
