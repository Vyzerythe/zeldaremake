# Handoff: continue the fork integration locally (written 2026-10-13)

> **Source primacy.** If this document disagrees with the current source, git history or a
> command's output, the source wins. This is a map, not an authority. Every number marked
> PROVISIONAL was measured once in a cloud container and must be re-derived before you rely on it.

## 0. Resuming

There are two ways to continue on your own machine. Both start from a local clone of
**`Vyzerythe/zeldaremake`** (the fork). A clone of upstream `Leonxlnx/zeldaremake` will not match
the session's repository.

- **A. Fresh session (recommended for the long-running work).** Check out
  `claude/vigilant-lamport-6k3exd`, start `claude` in the clone, and paste the prompt from §16.
  This document and `docs/fork-integration/` carry what the cloud session found.
- **B. Teleport the cloud session.**
  - Command: `claude --teleport session_01BErSdYNdoh31R6c8radHz6`.
  - Requirements: same claude.ai login, a clean working tree, and the branch already pushed
    (it is).
  - What you get: the full prior conversation, but it was already about 340 k tokens, and every
    `/tmp/...scratchpad` path it mentions exists only in the cloud container.
  - Use it if you want to question the earlier analysis. Otherwise start fresh.

Local prerequisites:
- Node ≥ 20 (22.22 was used) and `npm ci`.
- A Chrome or Chromium binary in `CHROME_PATH` for captures.
- Disk: the fork carries every upstream branch, about 5 GB of git objects if you fetch them all
  (PROVISIONAL). Fetch only the branches you need.

## 1. Goal

Turn the experimental integration branch into the fork's working main. Then finish and land the
remaining upstream work on separate feature branches. The owner (you) resolves every issue in
anything that is added.

## 2. Locked decisions (owner-approved 2026-10-13)

These are settled. Re-open one only with evidence (see §4, non-execution outcome).

1. **Working main.** The tip of `claude/vigilant-lamport-6k3exd` becomes the fork's working main.
   The recommended form is to fast-forward the fork's `main` to it, since `main` is an ancestor.
   The alternative is to rename it to a stable branch such as `work` and make that the default
   branch. **Which form is used must be confirmed with the owner before any push to `main`.**
2. **Separate feature branches** off the working main:
   - **`exp-east`** on its own branch. Expected to be "decide, then merge".
   - **`exp-ruins`** on its own branch. Needs real work, and lands after `exp-east`.
   - **Close crowns plus `curtainfar`** on one canopy-detail branch, landed last.
3. **Small items get no combined branch.** The owner judges each one from before/after evidence;
   each accepted one is merged from its own upstream branch.
4. **Merge, never rebase.** The history now contains upstream merge commits. Bring the working
   main into feature branches with merges.
5. **One PR per feature branch into the working main, gated by CI.**

## 3. Read-first floor (read in full before reasoning)

Staleness: all are low-churn, but this session did not re-read them after its last commit.

1. `AGENTS.md` — the collaboration contract and architecture rules: system independence,
   `layout.ts` as the single source of placement, the frozen heightfield interface, `prng`
   determinism, shared wind, audits.
2. `GAUNTLET.md` — the exit criteria, anti-cheat rules and the ledger/rubric locks.
3. `docs/PROMPT_PHASE1.md` — intent: the shot-for-shot target and the art direction.
4. `docs/FORK_INTEGRATION_2026-10-13.md` — what the branch contains, the optional layers and the
   skip list, with upstream verdicts. Written by the session that built the branch; verify its
   claims (§7).

## 4. Success criteria

Each workstream is done when its PR into the working main has:
- typecheck and build green, and every `node --test` file passing;
- source-only anti-cheat green;
- captures of the six hero views (A–F) with no page errors, inside W38 (≤ 700 draws, ≤ 9.0 M
  triangles for the heroes);
- the feature's own look spots and walk routes captured or played (`gauntlet/scripts/playtest.mjs`);
- the owner's sign-off on any look change to a hero frame.

**Allowed non-execution outcome.** A reasoned conclusion, citing evidence from the artifacts, that
a workstream (or the arrangement in §2) is not the highest-yield next step, plus a proposed
alternative.

## 5. Current state (artifacts)

Staleness: all of these were accurate at authoring (branch tip after this doc's commit). Re-verify
each.

| Artifact | What it is |
| --- | --- |
| `claude/vigilant-lamport-6k3exd` | The working-main candidate. First parent is the old `main` (`67b801db`). It has 7 merge commits plus 2 doc commits on top. |
| ↳ `15d77292` | `main` merged with `cursor/squad2-matswap-682b` (`90db14d7`). That line is the trunk `cursor/kokiri-world-phase1-f65e` plus 221 squad2 commits. Main-only fixes are ported in: Link tilt `4cf09bc5`, head-snap and body `7ac5fa5a`, pool admission `e7fa0811`, `broll.mjs`, `tiers.test.mjs`. |
| ↳ merges | `be3ae2dd` nearbox · `f23332a9` paving-far · `55da528f` gate-audit · `6bdb82cb` idle-arms · `3fefc188` squad5-ravine · `e004e1d2` exp-south2 |
| Verification at `cdf0d4ee` | tsc clean, build green, 338/338 tests, anti-cheat (source) 101 checks. Renders of A/C/F only: A 547 draws / 8.55 M, C 471 / 7.55 M, F 487 / 7.48 M; 12/12 capture checks. All PROVISIONAL. **B, D and E were not rendered. Walk routes were not run.** |
| `docs/fork-integration/branch_unique.py` | For each file a branch changed, reports whether its version is already in, superseded in, or new to a target ref (blob history, merges included). Use it instead of commit counts. |
| `docs/fork-integration/ref-resolution-*.remerge.diff` | `git show --remerge-diff` of trial merges: east onto trunk+south2, and ruins onto trunk+south2+east. **Stale base:** they predate squad2, nearbox, paving, gate-audit, idle-arms and ravine audio. Use them as a reference for how each conflict was resolved, never as a patch to apply. |
| `origin/<upstream branch names>` | The fork mirrors every upstream branch at the identical commit, except `monitor`. Upstream had no Zelda commits after 2026-10-01 (PROVISIONAL). |

## 6. Widen: surfaces per workstream

Read the surfaces for your workstream in full **before concluding**. Then enumerate any further
surfaces your approach touches, read those too, and list everything you read.

**W0, working main and CI**
- `.github/workflows/gauntlet.yml`: the triggers and `timeout-minutes`.
- `.github/workflows/monitor.yml`.
- The fork's Actions settings, which are unknown and unchecked.

**W1, `exp-east`** (`origin/agent/fable-cursor-exp-east`)
- On that branch:
  - `art/environment/exp-east-2026-09-23/README.md`
  - `src/world/structures/east.ts`
  - `src/world/structures/index.ts`
- `.agents/reviews/fable-5-rubric50-exp-east.md`
- `docs/RUBRIC_50_STRUCTURES.md`
- The crown-rule change it makes in `src/world/trees/` (commit `162f1a6e`).
- `expansionCull` in `src/world/terrain/heightfield.ts`. **That file holds the frozen
  interface**, so check that a signature change to this helper stays outside the frozen
  `Terrain`/`TerrainMask` types.

**W2, `exp-ruins`** (`origin/agent/fable-cursor-exp-ruins`)
- `art/environment/exp-ruins-2026-09-24/README.md` (the author's own rubric) and
  `art/environment/round54-ruins-review/`
- `.agents/reviews/fable-5-rubric50-exp-ruins.md`
- `src/world/ruins/`
- `src/world/vegetation/expansion.ts`
- `src/world/vegetation/carpet.test.mjs`: the expansion-cull bound
- `origin/agent/fable-4-trees-merge3` (`e09a2c29`): an upstream east × ruins merge that
  typechecked and tested green; a reference for unifying the cull flag.

**W3, canopy detail**
- On `main` / the working main: `art/environment/astra-distance-pool/README.md`.
- Commits `1d5f1280`, `e7fa0811`, `9afd1b14`, `31d1de8c` (on `origin/agent/astra-distance-pool-sept23`;
  `e7fa0811`'s pool fix is already ported).
- The close crowns as integrated are in the old main's files at `67b801db`:
  `src/world/trees/{distant,index,nearCanopy}.ts` and `lodPool.test.mjs`. Main adopted them by
  copying files, so those commits are not ancestors of the working main.
- `src/world/trees/{index,distant,lodPool,lodFade,nearCanopy}.ts`
- `origin/agent/fable-4-curtainfar` (`9baa882f`): the `curtainfar` knob in `trees/index.ts`.
- `art/environment/squad2-2026-09-23/INDEX.md`
- `.agents/INBOX.md`: fable-4's 2026-09-26 03:15 thread on where the trees' triangles go.

**W4, small items**, each on its own `origin/` branch:
- `agent/fable-2-dmoss` (`5f37580e`)
- `agent/fable-3-seated-skirt` (`edac4238`)
- `agent/fable-2-ravine-rock` (`503f2b4c` is the only non-redundant commit; see §9)
- `cursor/squad2-consolidate-682b` (evidence only)
- The held sign: `src/world/character/sign.ts`, `signPose.ts`, and
  `public/textures/sign/readers-note.jpg`.

## 7. Required verification (before designing)

Run these and record the output. Every expected value is PROVISIONAL.

1. `git fetch origin && git log --oneline --first-parent -10 origin/claude/vigilant-lamport-6k3exd`.
   Expect the merges in §5.
2. `npm ci && npm run typecheck && npm run build`, then
   `node --test $(git ls-files 'src/**/*.test.mjs' 'gauntlet/**/*.test.mjs' 'site/**/*.test.mjs')`.
   Expect 338 passing.
3. `npm run capture -- --out gauntlet/out/base --settle 4` with all six views; do B, D and E
   especially. Expect no `[pageerror]`, and every hero ≤ 700 draws / 9.0 M.
4. For each candidate:
   `git merge-tree --write-tree --name-only HEAD origin/<branch>`. Expected conflicting files at
   authoring:
   - **exp-east (8):** `playtest.mjs`, `audio/index.ts`, `audio/surfaces.test.mjs`, `layout.ts`,
     `structures/index.ts`, `structures/lantern.ts`, `terrain/heightfield.ts`, `trees/index.ts`
   - **exp-ruins (5):** `audio/index.ts`, `audio/surfaces.test.mjs`, `structures/index.ts`,
     `terrain/heightfield.ts`, `trees/index.ts`
   - **seated-skirt:** `.agents` logs only
   - **ravine-rock:** `rocks/index.ts`
   - **consolidate:** one README
   - **dmoss, curtainfar:** clean
5. With `gh` (it was blocked in the cloud session), check the open/closed state of upstream PRs
   #190, #196, #198, #200–#214 on `Leonxlnx/zeldaremake`. The cloud session inferred "open" only
   from surviving merge refs.

## 8. Handoff self-test (falsifiable claims about this doc)

1. `git merge-base --is-ancestor origin/main origin/claude/vigilant-lamport-6k3exd` exits 0.
2. `git grep -n "leg.stance && leg.tiltAngle > 1e-5" origin/claude/vigilant-lamport-6k3exd -- src/world/character/glbLink.ts`
   matches, and the same grep on `origin/cursor/kokiri-world-phase1-f65e` does not.
3. `git grep -n "export const RAVINE_DRAW_M = 26" origin/claude/vigilant-lamport-6k3exd -- src/world/rocks/index.ts`
   matches. It came from gate-audit, which is why ravine-rock's own 26 m gate is redundant.
4. `.github/workflows/gauntlet.yml` contains `branches: ['**']` under `push` and
   `timeout-minutes: 45`.
5. `expansionCull` takes `(x, z, lift)` on the working main, `(…, east = true)` on exp-east, and
   `(…, withRuins = true)` on exp-ruins.

## 9. Open questions inside each workstream

None has a pre-selected answer. Resolve each through investigation; "other: justify" is always
allowed.

**W0, working main**
- Fast-forward `main`, or use a `work` default branch? The owner must confirm.
- CI policy:
  - keep push-triggered gauntlets on every branch (costly, ~45 min, upstream runs timed out), or
  - limit `push` to the working main and run PRs in full, or
  - other.

**W1, east**
- The top-edge crown change in A/B/E/F (0.5–1.2 % of pixels, PROVISIONAL) is a look call for the
  owner.
- Order relative to ruins: east-first was proposed because east has no outstanding code work.
  Verify that against the branch state.

**W2, ruins**
- How to unify the `expansionCull` flag with east. Upstream's template in `e09a2c29` used one
  `all` flag.
- What "done" means for the author's below-3 rubric checks (#44 camera, #46 budget).
- Whether raising the `carpet.test` cull bound is a fix or a mask.

**W3, canopy**
- The port strategy: re-implement `1d5f1280` against today's `distant.ts`/`index.ts`, or adapt
  the trunk's own floor cards and veils.
- Whether `curtainfar` must cast shadows before it is enabled.

**W4, small items**
- Each item is a look call.
- seated-skirt has an author-offered alternative (hem −0.14).
- ravine-rock's shelf change only shows from the bridge deck (play mode), not in a hero view.

### Contested finding: what the close crowns cost

- **Source 1.** On the working main, `art/environment/astra-distance-pool/README.md` says all six
  A–F views keep zero close slots: unchanged draws and triangles, with four pixels differing by
  one value. The crowns add about 0.88–0.97 M triangles in the play frames where they engage.
- **Source 2.** A sub-agent of this session, citing fable-4's thread in `.agents/INBOX.md`,
  reported "+0.9 M triangles with only ~0.14 M headroom at camera A".

These may describe different frames: a play-mode frame versus hero A. Verification path: capture
hero A and the README's w19 pose, with and without the port, and read the audit's triangle counts.
**Fresh session's call. Don't inherit this session's reading.**

## 10. Session failure modes (calibration from the authoring session)

- **Commit counts were meaningless here.** `main` was an orphan line synced by copying files.
  "3,300 commits ahead" carried no information; compare blobs instead.
- **`git log --raw` skips merge commits.** The first version of the analysis tool reported file
  versions created by merges as "unique". Fixed with `--diff-merges=separate`; the fixed version
  is in `docs/fork-integration/`.
- **The session first assumed the fork lacked the upstream branches.** It mirrored all of them.
  Check `git ls-remote origin` before planning any fetch.
- **Sub-agent test counts disagreed with direct runs** (28/30 vs 30/30 on one file). Re-run tests
  yourself; don't quote agent counts.
- **SwiftShader captures were slow and fragile.** On 4 cores a view took about 2–4 minutes plus a
  2–3 minute load, and one view crashed Chrome under CPU contention. Don't run captures in
  parallel with heavy jobs.
- **Deleting a worktree under a running background job** produced a spurious failure exit. The
  capture had completed.

## 11. Anti-patterns (do not)

- Rebase or force-push branches that contain upstream merge commits.
- Take a reviewer verdict from upstream logs as current without checking the commits made after it.
- Merge look-changing work without hero captures and the owner's sign-off.
- Merge the unrelated projects that live in the same repo:
  - `cursor/vista-*` (Minecraft)
  - `cursor/lego-star-wars-*`, `cursor/lsw-*`
  - `cursor/spiderverse-*`
  - `cursor/spaceship-interior-*`
- Merge the deploy/capture orphans: `monitor`, `play-head`, `captures/*`.
- Bring in the astra Blender sources: about 4.8 GB, superseded, rights unresolved.

## 12. Project invariants (regardless of permissions)

- Every pushed commit keeps `npm run typecheck && npm run build` green.
- Randomness in world code comes only from `prng`.
- The `Terrain`/`TerrainMask` interfaces in `heightfield.ts` are frozen.
- `layout.ts` changes need a reference reason and a log entry.
- `gauntlet/rubric.json` is hash-locked.
- `gauntlet/ledger.json` is append-only and never hand-edited.
- No Nintendo assets, no reference-video frames as scenery, and CC0/original textures credited in
  `public/textures/CREDITS.md`.
- Never edit another agent's `.agents/*.md` log. Upstream logs that arrive through merges are kept
  as merged.

## 13. Permission layer

| Action | Allowed | Ask the owner first | Forbidden |
| --- | --- | --- | --- |
| Create local branches, merges, test runs, captures | ✓ | | |
| Push feature branches to the fork | | ✓ (names) | |
| Push to `main`, or change the default branch | | ✓ | |
| Open PRs on the fork | | ✓ | |
| Change hero-frame look (crowns, skirt, moss, shelves, haze) | | ✓ (owner's call) | |
| Edit `rubric.json` / `ledger.json` by hand; rewrite history; force-push | | | ✓ |
| Anything on upstream `Leonxlnx/zeldaremake` (comments, PRs) | | ✓ | |

## 14. Unresolved questions for the owner

- **Remove the held sign?** In play mode, T makes Link hold up a sign whose face is upstream
  owner's screenshot of an X "Readers added context" note.
- **Link model rights.** The model is Rodin/Hyper3D trial output, and Nintendo character rights
  are a separate question. See `art/characters/link/ASSET_LICENSE_REVIEW.md`. `package.json`
  says `"license": "MIT"`, which that review advises against applying to these assets.
- **The `stairs1-base` look spot renders near-black** (the follow camera sits inside a close
  occluder). Fix it as part of W0, or in its own branch?

## 15. Appendix: provenance (traceability only; not operational)

- Cloud session: `session_01BErSdYNdoh31R6c8radHz6`, 2026-10-13.
- Analysis covered 342 upstream branches and 214 PR refs, using four parallel sub-agent sweeps:
  main-unique work, trunk features, and recent and older side branches.
- Their conclusions are folded into `docs/FORK_INTEGRATION_2026-10-13.md`.

## 16. Starting prompt for the fresh local session

```
Read docs/HANDOFF_2026-10-13_fork-integration.md in full (on branch claude/vigilant-lamport-6k3exd).

Read its read-first floor (AGENTS.md, GAUNTLET.md, docs/PROMPT_PHASE1.md,
docs/FORK_INTEGRATION_2026-10-13.md) in full before reasoning. Complete the "Required
verification" (§7) and "Handoff self-test" (§8) sections against the actual repository and
report the results. Then report your orientation — current state · floor docs read · further
surfaces you derived and read · the workstream and lever you propose to start with · which
document your rationale comes from — before proposing or editing anything.

The arrangement in §2 is owner-approved; propose how to execute it, starting with W0 (working
main + CI), and present that plan for my approval before pushing anything.

Do not assume: numbers in the handoff are current / sub-agent findings were validated / the
remerge diffs apply to today's tree / upstream reviewer verdicts cover commits made after them /
upstream PR states are known / the handoff's ordering is correct.

If your investigation concludes that part of the §2 arrangement is not the right next step, say
so with cited evidence and propose the alternative that better serves the goal.
```
