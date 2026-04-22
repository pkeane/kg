# knowledge_graph

Personal markdown knowledge graph of ~200–300 years of Western political, social, economic, philosophical, and theological thought. Modeled loosely on the territory of Alan Ryan's *On Politics*, extended into psychology, theology, American literature, civil rights, and contemporary critics. Curated around Peter's `~/VALUES.md`: regulated capitalism, strong public sector, Sermon-on-the-Mount Christianity, affinity with Black American Christianity, anti-racism/sexism, attention to the voiceless, moral complexity ("good and evil intertwined").

## Layout

- `docs/thinkers/` `docs/schools/` `docs/concepts/` `docs/events/` `docs/topics/` — entries, plain markdown with YAML frontmatter
  - **thinkers / schools / concepts / events** are short encyclopedic entries (~50–400 words) with an established structure (intro prose, Key themes / Key ideas, Key works, optional Secondary sources). These are the bulk of the graph.
  - **topics** are longer, exploratory pages organized as **annotated bibliographies**. Use them for areas that are contested, still being excavated, or that cut across multiple thinkers in ways no single entry can carry (e.g. `art-and-political-commitment`, `faith-and-the-modern-world`, `western-marxism`). Format: short orienting intro (2–4 paragraphs) + `## Annotated bibliography` organized by sub-section, with bolded author + italic title + a sentence or two of commentary per item. See `docs/topics/` for examples.
- `docs/_template.md` — frontmatter template
- `scripts/build_site.py` — static site generator (markdown + pyyaml). Renders to `site/`. Wikilinks pointing at non-existent ids render as dashed red — they're intentional TODOs, not bugs.
- `scripts/validate_links.py`, `scripts/list_orphans.py` — link checkers
- `scripts/publish.sh` — rebuild + force-push `site/` subtree to `gh-pages` and push `main`
- `venv/` — python3 venv (PEP 668 requires it on this Mac)

## Frontmatter

```yaml
---
id: kebab-case-matches-filename
type: thinker | school | concept | event | topic
name: Display Name
born: 1900            # or omit
died: 1980            # omit if living
era: 20th century
nationality: ...
tags: [tag1, tag2]
related: [other-id, ...]
influenced_by: [...]
influenced: [...]
---
```

## Conventions

- Entry length: typically 200–400 words for thinkers, less for concepts/events. Two or three substantive paragraphs, then `## Key themes` (or `## Key ideas`) and `## Key works` lists.
- Link generously via `[[id]]` to related docs. When adding a new entry that connects to existing ones, also update *their* `related` / `influenced_by` / `influenced` arrays.
- Forward references are fine — broken `[[links]]` are visible TODOs.
- ids are kebab-case `lastname-firstname` for thinkers (e.g. `du-bois-web`, `forman-james-jr`).
- No emojis. Serious-prose register; the site uses Georgia serif on a cream background.

## "What would [Name] say?" sections

Optional H2 section at the end of a thinker page (after `## Key works` and `## Secondary sources`) that applies the thinker's framework to a specific contemporary question. Use sparingly — only where the thinker's framework genuinely illuminates a modern question that isn't obvious from the core entry. Format:

```markdown
## What would [Name] say?

*Synthesized from the published work, not direct quotation.*

### About [the specific question]

2–3 tight paragraphs...
```

Conventions:
- Always include the italic disclaimer line under the H2 — makes the voice explicit.
- Use hedged framings ("would likely argue," "his work suggests"), never fabricated quotes.
- One H3 per question. A single thinker page can accumulate multiple questions over time.
- Compressed: 2–3 paragraphs per question, not an essay. Link to other KG entries via `[[id]]`.
- These sections are applied/speculative, distinct from the encyclopedic register of the rest of the page — the placement at the end and the disclaimer keep the two genres separate.

## Workflow

```bash
# add/edit entries under docs/
./venv/bin/python scripts/build_site.py     # rebuild site/
./scripts/publish.sh                         # commit, push main, deploy gh-pages
```

**ALWAYS publish.** After any edit to this project — new entry, fix, script change, anything — end with `./scripts/publish.sh`. Don't ask, don't stop at "built cleanly," don't leave it for Peter to run. The whole point of editing is to get changes live at pkeane.github.io/kg/. The only exception is an explicit in-progress/WIP state where Peter has said to hold off.

## Hosting

- Repo: https://github.com/pkeane/kg (public; renamed from `knowledge_graph` in April 2026, GitHub redirects the old URL)
- Pages: https://pkeane.github.io/kg/ (served from `gh-pages` branch root, populated by `git subtree split` of `site/`)
- Default branch: `main`. `site/` is committed (not gitignored) so the subtree split has something to publish.

## Style of summaries

Look at `docs/thinkers/du-bois-web.md`, `thurman-howard.md`, `berry-wendell.md`, `morrison-toni.md` for the established voice — confident, biographical, locates the figure in their tradition, names the central books and the central ideas, willing to make an evaluative claim. Avoid hagiography; avoid dismissiveness; assume an intelligent general reader.
