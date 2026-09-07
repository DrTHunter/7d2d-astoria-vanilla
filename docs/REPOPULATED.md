# Astoria 8K — junk/duplicate POI repopulation (2026-09-06)

**1812 POIs replaced** with unique Compopack POIs. `prefabs.xml` still has 13062 decorations —
every replacement reuses the slot it took over, same X/Y/Z, same footprint.

Full per-POI list: `REPOPULATED_pois.csv` (X, Z, why, context, removed, added, tier, size).

## What was replaced

| reason | count | what |
|---|---|---|
| junk | 1416 | Tier-0 `remnant_*`, `rubble_*`, `lot_*`, `*_filler_*` — ruins, rubble and empty lots |
| redundant | 396 | copies **beyond 6** of a vanilla POI; the 6 most spread-out copies of each are kept |

Biggest families cleared: `remnant_downtown_filler` 393, `rubble_downtown_filler` 209,
`lot_industrial` 202, `wilderness_filler` 164, `downtown_filler` 147, `remnant_downtown_strip` 91.

By context: downtown 902, wilderness 383, industrial 319, commercial 106, residential 75, other 27.
By footprint: 25×25 → 1243, 42×42 → 443, 60×60 → 119, 100×100 → 7.

**Kept deliberately:** `downtown_filler_park_*` and `downtown_filler_plaza_*` (53 remain) — that is
intended open space in a downtown block, not junk. 50 junk POIs also remain: the 8×8 and 10×10
wilderness ones, which have no Compopack POI of matching size.

## What went in

820 distinct Compopack POIs, from a pool of **1419 verified-unique** ones.

- **1769 of 1812** have sleeper volumes, so they are lootable and questable. The old rubble had none.
- Difficulty tiers now present: T0 494, T1 644, T2 379, T3 164, T4 66, T5 65.
- Max **4 copies** of any one POI across the whole 8K map (the old map ran to 18 copies of a single filler).
- Same-POI copies are **584 m apart at closest**, median 4221 m, and never twice in the same town
  unless that town had no alternative.

Placement rules used, both verified against this map before anything was written:

- Terrain height is `dtm.raw[Z+4096, X+4096] / 256`.
- `position Y = round(terrain at POI centre) + 1`. `YOffset` is applied by the game, not baked into
  `prefabs.xml` — checked against 1055 wilderness POIs, 100 % within 1.5 m.
- Rotation: `r_new = (r_old − RotationToFaceNorth_old + RotationToFaceNorth_new) mod 4`.
  `(r − RotationToFaceNorth)` was constant across **401/401** repeated tile slots on this map, so
  every replacement faces the street exactly the way the POI it replaced did.

Candidates were restricted to the slot's township context (downtown POIs into downtown blocks, and
so on) and to an **exact footprint match**, so no replacement can overhang its lot.

## Compatibility audit — Compopack on V 3.2.0 (b10)

You asked whether the All-In-One is too old. It is fine as installed; nothing needed patching:

- All **2099** Compopack prefabs parse (`.tts` versions 16–19; the game reads all of them).
- **0 unknown block names** — every block the pack references exists in vanilla V 3.2.0. Nothing
  depends on another mod.
- `biomes.xml`, `rwgmixer.xml`, `spawning.xml` are well-formed and are `<conditional>`-gated
  modlet patches; their xpath targets (`world`, `township`, `district`) all still exist in V 3.2.0.
  They only affect generating *new* worlds — Astoria is pre-generated, so they are not on the path.
- Only 12 name collisions with vanilla, all intentional pack overrides: 5 `part_terrain_greeble_*`
  (identical bytes) and 5 `rwg_tile_oldwest_*` (taller CP versions). **Astoria places zero oldwest
  tiles**, so that override changes nothing here.

### Duplicate check on the 2099

- Byte-identical geometry: **5** Compopack POIs are copies of vanilla POIs — `xcpv_LittleAsia_Park_01_TFP`
  (= `park_01`) and `xcpv_LittleAsia_filler_02/03/04/05_TFP` (= `wilderness_filler_09/13/14/18`).
  All 5 excluded from the pool.
- Near-duplicates (same dimensions + same block array, re-saved under another name): none beyond those 5.
- Duplicates against MPLogue / Voltralux / Zeebark / Svarii / Cog's: **none**.
- Duplicates within the pack itself: only among `Parts` and `RWGTiles`, none among POIs.

Net: **1424 → 1419 genuinely distinct** Compopack POIs.

### One thing fixed

`Mods\AAL-__vortex_tmp_00000001` was a leftover Vortex temp deployment, byte-identical to
`AAJ-Classic All In One …`, including a second copy of `StallionsdensDoorTriggerVolumes.dll`.
Two copies of the same Harmony assembly patch the game twice. Moved to
`%APPDATA%\7DaysToDie\Mods_disabled_by_claude\` — delete it, or move it back if you disagree.

`AAJ-Classic All In One` itself only deploys the door-trigger mod; the POIs from that archive are the
`AAL-Compopack Classic AIO No Traders` folder, which is what was used here.

## Your existing saves

Replacements only appear in chunks the save has not generated yet.

| save | regions generated | replacements already baked into old chunks |
|---|---|---|
| `Astoria 8k` | 100 | 1059 of 1812 |
| `Theft by map` | 10 | 111 of 1812 |

`Theft by map` has only 10 regions (X 1024…3071, Z −3584…−1) and 111 affected POIs. Everything
outside that box is already correct. To pick up the rest inside it, in the F1 console:

    chunkreset 1024 -3584 3071 -1

That rebuilds terrain and POIs in the box and **destroys anything you built there** and resets loot.
Given the starter bases were also rebuilt on this map, a **new save is the cleaner option**.

## Backups

- `prefabs.xml.BEFORE-REPOP` — before this pass (starter bases in, junk still there)
- `prefabs.xml.BEFORE-REBUILD` — before the starter-base rebuild
- `prefabs.xml.ORIGINAL-BACKUP` — untouched original
- `dtm.raw.ORIGINAL-BACKUP`, `spawnpoints.xml.ORIGINAL-BACKUP`

See `MY_PREFABS.md` for the 7 starter bases and the spawn point; they were not touched by this pass
(verified: all 11 of their decorations still present).
