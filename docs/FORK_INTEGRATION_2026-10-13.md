# Fork integration of upstream branches (2026-10-13)

This records what the fork (`Vyzerythe/zeldaremake`) took from upstream (`Leonxlnx/zeldaremake`),
what it left out, and why. The analysis covered all 342 upstream branches and 214 pull-request
refs. The GitHub API was not available for the upstream repo, so any pull request that still has
a merge ref is treated as probably open.

## The situation

- The fork already mirrors every upstream branch at the same commit. The only exception is the
  `monitor` deploy branch, which is behind by heartbeat commits. Upstream `main` (`67b801db`,
  2026-09-23) has not moved since. Upstream's last Zelda commit is 2026-10-01.
- The "thousands of commits ahead of main" counts are misleading. `main` is an orphan line
  (root `1e4379c4`) that was built by copying files over from the real development branch,
  `cursor/kokiri-world-phase1-f65e` (PR #2, called "the trunk" below). The two share only the
  initial commit `7f4c30ec`, so commit counts mean nothing. Every comparison here was done on
  file contents (blobs).
- Comparing main's 2,731 files against the trunk:
  - 2,066 are identical.
  - 90 are older copies of trunk files that the trunk has since improved.
  - 559 exist only on main: Link production art and evidence, astra evidence, checkpoint docs.
  - 18 carry main-only edits; these are the real conflicts.
- The main checkpoint deliberately held back several trunk systems:
  - camera collision and near-fade
  - mid-canopy and understory
  - squad atmosphere
  - visible NPCs
  - Link model and gait

  Its stated reason was "need their separate reviews". The trunk later reviewed or fixed each
  one. The owner's own 09-25 cinematic used the trunk world plus main's repaired Link, which is
  the shape of this integration.

## What this branch contains (first-parent order)

| Commit | Source | Status upstream |
| --- | --- | --- |
| `15d77292` | **`main` merged with `cursor/squad2-matswap-682b` `90db14d7`**: the trunk `1232f1d3` plus 221 squad2 performance commits (PR #210 / #213) | Trunk: reviewed merges through 09-26. squad2 after 09-26: author-measured only. Its three pixel-moving changes each have a one-line switch: `TREE_LOD_DITHER` (`trees/lodFade.ts`), `TREE_ONE_MATERIAL_FAR` and `forceSinglePass` (`trees/distant.ts`). |
| ↳ ported from main | Link planted-boot tilt support `4cf09bc5`, plus the head-snap fix, play-mode body and Navi anchor `7ac5fa5a` (from `agent/opus-cinematic-sept24`) | Missing from every upstream line. The trunk's play mode turns the head 0.804 rad in one frame. |
| ↳ ported from main | LOD pool admission recheck `e7fa0811`, plus 3 tests | Missing upstream. Without it the pool can exceed its byte cap: 120 B resident in a 100 B pool. |
| ↳ ported from main | `broll.mjs` exact frame timing `7f645fe9`; merged-pebble test `664f3418`; Windows test-path fix; `capture_play_motion.mjs` | main-only |
| ↳ kept from main | All 559 main-only files; main's `.gitattributes` | main-only |
| ↳ added | `art/characters/link/ASSET_LICENSE_REVIEW.md` from `88ad6ebf` (open PR #8); opus `check-body` motion regression check | Neither line had them |
| `be3ae2dd` | `agent/fable-4-nearbox` (PR #201) | fable-5: PASS, pixel-identical, −126…−198 K triangles |
| `f23332a9` | `agent/fable-2-paving-far` (PR #208) | fable-5: PASS on `b3f677a0` and `666ca29f`; the 40 m tip was not re-reviewed |
| `55da528f` | `agent/fable-2-gate-audit` (PR #196) | Author-measured pixel-identical |
| `6bdb82cb` | `agent/fable-3-idle-arms` (PR #190) | Author-measured pixel-identical |
| `3fefc188` | `cursor/squad5-ravine-5535` (PR #207, includes PR #203) | Audio lane, measured with tests, not independently reviewed |
| `e004e1d2` | `agent/fable-cursor-exp-south2` | fable-5: merge-ready on `5e5ef0b0`; three later commits not re-read |

Verification on the final tree:
- `tsc --noEmit` clean and `vite build` green.
- 338/338 `node --test` across 64 files.
- Source-only anti-cheat green: 101 checks.
- Headless render (SwiftShader, settle 4), no page errors:

  | View | Draws | Triangles |
  | --- | --- | --- |
  | A | 547 | 8.55 M |
  | C | 471 | 7.55 M |
  | F | 487 | 7.48 M |

  The W38 cap is 700 draws and 9 M triangles. main's A renders 484 draws / 8.76 M.

Visible differences from main at A:
- The Kokiri kids are visible again; main hid them.
- The hero flight is worn stone again (upstream `f5015962`, from the owner's reference).
- The haze is lighter and hazier in the distance (squad atmosphere).

## Optional layers (left out, each needs a decision)

| Branch | What it adds | Why it is not included |
| --- | --- | --- |
| `agent/fable-cursor-exp-east` `dd29609b` | Walkable Kokiri lane on the east plateau: shop, tall house, lookout | fable-5 says it is "merge-ready once the owner has called" a top-edge crown change in hero frames A/B/E/F (0.5–1.2 % of pixels). The owner never made that call. |
| `agent/fable-cursor-exp-ruins` `d86a1767` | Waterfall ruins: a new `src/world/ruins/` system | Reviewer scored 176/200; the author's own read is "158/200, NOT READY" (camera and budget). Combining it with east needs the `expansionCull` flag unified, and `carpet.test` bound raised to about 8000. |
| `agent/fable-3-seated-skirt` `edac4238` | Seated girl's skirt | Changes sealed frames B/E (+0.0004); the author asked the owner to accept it. |
| `agent/fable-4-curtainfar` `9baa882f` | Far rung for authored curtains | Inert by default; the shadow twin has to cast before it is turned on. |
| `agent/fable-2-ravine-rock` `02586843` | Bigger, paler ravine shelves; 26 m draw limit | Marked "PROPOSED" and never reviewed. |
| `agent/fable-2-dmoss` `5f37580e` | Near-bare shot-D boulder | fable-4 called it "IMPROVED", but the author left it as "your call". |
| main close crowns `1d5f1280` | Real-leaf geometry on the 8 nearest distant crowns | About 0.9 M extra triangles against roughly 0.14 M of headroom at A. Expect 11–13 hand-resolved conflicts in `trees/`. |
| `cursor/squad2-consolidate-682b` `e20ce87d` | squad2 evidence, 66 files | Evidence only. |
| `agent/opus-cinematic-b-sept25` `8c3f03e3` | Verified cinematic recorder and audio pipeline | Tooling, plus 85 MB of media. |

## Skipped (superseded, failed or unrelated)

- **Older side branches:** 45 of the 49 that predate 2026-09-24 are superseded. Their content
  reached the trunk or main, or they were scratch, evidence or notes. That includes the
  procedural-Link astra line, which was replaced by the GLB Link. The astra Blender sources
  (about 4.8 GB) stay reachable on `agent/astra-local-blender`; `SOURCE.md` provenance links
  point at its commit `bef8e85`.
- **Withdrawn or failed:**
  - `fable-3-wave-palm`: "measured FAIL … do not merge"
  - `fable-4-eastroots`: "withdrawn"
  - `fable-2-ruins-cliffbeds`: "negative result"
  - `fable-2-form` / `form-2`
  - `fable-2-riser-shade`
  - `squad2-woodgain` (PR #214): "must not be merged"
- **Inert or superseded:**
  - `squad2-lodfade4` (PR #198)
  - `squad2-gatetests` (matswap has the superset)
  - `fable-3-lane7-r2`
  - the `fable-4-trees-merge*` scratch merges
  - `squad5-merge-check`
- **Not this project:**
  - `cursor/vista-extreme-distance-mod-75da` (a Minecraft mod)
  - `cursor/lego-star-wars-rots-opening-ed32`, `cursor/lsw-venator-one-of-one-dced`,
    `cursor/lsw-wip-site-ed32`
  - `cursor/spiderverse-ant-short-f2ea`
  - `cursor/spaceship-interior-fc25`
- **Deploy or capture orphans:** `monitor`, `play-head`, `captures/astra-*`.

## Known open points inherited from upstream

- The `stairs1-base` look spot renders near-black. An occluder sits 0.375 m from the lens and the
  follow camera does not push out of it.
- The north and south expansions landed with open reviewer rubric findings: south scored about
  146/200 against a 170 bar.
- The follow camera's turn acceleration p95 rose 1.6–1.7× with the grove ring camera; upstream
  marked this "the owner's call".
- Pressing T in play mode makes Link hold up a sign. Its texture is the upstream owner's
  screenshot of an X "Readers added context" note (`public/textures/sign/readers-note.jpg`). It is
  owner-specific and can be removed.
- CI: upstream gauntlet runs hit `timeout-minutes: 45` and end "cancelled".
- Rights: the Link body is Rodin/Hyper3D trial output, and Nintendo character rights are separate.
  See `art/characters/link/ASSET_LICENSE_REVIEW.md`. This exposure is the same on main and on the
  trunk.
