# Continuing the topic details page work

This file lives in `tmp/` of the synapse-web-monorepo for now but should be moved to
`b2ai-standards-registry/portal-planning-docs/CONTINUATION.md` along with the mock files.

## Where things live

| Thing | Where |
|---|---|
| Topic page implementation (WIP) | `synapse-web-monorepo` on branch `topic-details-page-209`. Last commit: `c25f9a6faf9` "WIP: topic details page" |
| Design mockups | `b2ai-standards-registry/portal-planning-docs/topic-hierarchy-mock.html` |
| DAG reference | `b2ai-standards-registry/portal-planning-docs/topic-dag.md` (open in MarkView for mermaid rendering) |
| Issue tracker | bridge2ai-standards-registry issue #209 |
| Claude memory | `~/.claude/projects/-Users-sgold15-github-repos-b2ai-standards-registry/memory/topic_details_page_design.md` |

## Two repos, one effort

Design discussion happens in **b2ai-standards-registry** (on the `topic-details-page-209` branch).
Implementation happens in **synapse-web-monorepo** (also on a `topic-details-page-209` branch).
They share a branch name but the changes don't cross-pollinate — registry has mockups + planning
docs, monorepo has the actual TypeScript widget.

Keep both checkouts open while working. When you decide a design detail in the registry branch
(by editing the mockup), implement it in the monorepo branch.

## State of the design (as of the last session)

The widget went through several iterations. The current direction is **Part D in the mockup** —
a boxless DAG rendering. Read the in-mock summary at the top of Part D for the rules. Brief
version:

- Every visible topic at its full-DAG indent (longest path from root).
- `└` corner glyphs show parent-child edges; no colored boxes.
- No expand-up toggles; ancestors shown as breadcrumb prefix on rows whose parents are hidden.
- Polyhierarchy topics render under their longest-path parent with `★ also under: <name>` for the secondary parent(s).
- Click any topic name to switch the anchor to that topic.
- Default ordering: topic-ID order with polyhierarchy override (shorter-path parent comes first).
- Optional user toggle: pure alphabetical (at the cost of polyhierarchy topics sometimes putting longer-path parent above shorter-path).

## Open items before implementation

1. **Skip-rail rendering for secondary-parent edges.** The mock has a placeholder
   `↘` glyph; the agreed direction is CSS-drawn rails in a left gutter that connect
   the polyhierarchy topic to its secondary parent visually, crossing any rows in between.
2. **Color in the boxless rendering.** Subtle column-stripe or per-row tinting by depth.
   User wants prettiness; ideally with semantic meaning.
3. **Breadcrumb-in-row behavior.** Initial render shows anchor + immediate parents + immediate
   children. Ancestors of those parents shown as breadcrumb prefix on the parent row.
   Clicking a breadcrumb segment should expand the tree to that level. Mock doesn't have the
   click behavior yet.
4. **Click-to-switch-anchor.** Each topic name needs to navigate to that topic's details page
   (URL change), which re-renders the widget with the clicked topic as the new anchor.

## How to resume

1. Open the mockup: `open b2ai-standards-registry/portal-planning-docs/topic-hierarchy-mock.html`
2. Open the monorepo branch: `cd synapse-web-monorepo && git checkout topic-details-page-209`
3. Look at the current state of `apps/portals/b2ai.standards/src/components/TopicHierarchyWidget.tsx`
   — note that it implements the OLD box-based approach and needs to be rewritten to match Part D.
4. The WIP commit also has changes in `resources.ts`, `hooks/fetchDataUtils.ts`, and `synapseConfigs/topics.ts`.

## Why the planning docs aren't in the monorepo

Visual mockups are useful collaborative artifacts but shouldn't ship in PRs to the monorepo —
they'd clutter diffs and don't belong in production code. The registry repo is the b2ai team's
shared workspace for the standards portal, so it's a natural home for planning docs. The
`portal-planning-docs/` directory there is the convention for this kind of material.
