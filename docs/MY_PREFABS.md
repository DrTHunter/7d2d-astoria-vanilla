# Starter bases - Astoria 8K (rebuilt 2026-09-06)

The 13 builds from the first attempt are gone. `prefabs.xml` is back to the state before them
(original map + the 124 mod POIs from the densify pass) and `dtm.raw` is back to the untouched
original terrain, so every old build site is original map again. On top of that, 7 of your
LocalPrefabs are placed in the same general area, on levelled pads, between the 13-tile town at
(1679,-871) and the big 31-tile city at (2654,-646) - hugging the west edge of the big city.

## Names

The seven were renamed on 2026-09-06. The game has no localization for POI names, so whatever the
prefab file is called is what shows in-game on the compass, the map marker and in quest text - the
old working names would have shown as-is. Each new name says it is a starter base and keeps the
identity of the POI it was cut from.

Source POIs were identified by TF-IDF cosine similarity over each build's block-name set against
all 4,128 installed prefabs, so this is what the blocks say, not a guess from the old filename.

| Old name | Cut from | Match | New name |
|---|---|---|---|
| PrisonRightOne | `prison_01` | 0.85 | StarterBase_Prison_Cellblock |
| Best-UFO-Base | `farm_17` | 0.70 | StarterBase_UFO_Farm |
| RangerStationHBbest | `ranger_station_07` | 0.89 | StarterBase_Ranger_Station |
| SuperDuperHousebunkerHB | `house_modern_31` | 0.93 | StarterBase_Bunker_House |
| SuperHouse2BH | `house_modern_18` | 0.94 | StarterBase_Modern_House |
| ayosairHouseUPdated | `Ayesoar_Mansion_by_MPLogue` | 0.83 | StarterBase_Ayesoar_Mansion |
| IdealMajorTowerHB | `hotel_03` | 0.90 | StarterBase_Hotel_Tower |
| CompoundWallSouth/North/West/East | - | - | StarterBase_Compound_Wall_S/N/W/E |

`Best-UFO-Base` scored lowest because it is the most modified: it keeps `farm_17`'s 72 player farm
plots and planted corn, under 132 blocks of 5 m dome that is not in the original farm at all.

The files in `LocalPrefabs` were renamed too (`.tts`, `.xml`, `.blocks.nim`, `.ins`), so a save that
already baked in the old names will not find them - one more reason to start fresh.

## Spawn

`spawnpoints.xml` has one point: **X 2430, Z -800**, the open yard in the middle of StarterBase_Prison_Cellblock.
The original 10 points are in `spawnpoints.xml.ORIGINAL-BACKUP`.

## The builds

Coordinates are the north-west corner of each prefab box (what prefabs.xml uses). Y is the
walkable ground level. "cut/fill" is the average amount the terrain under the box was moved.

| Build | X | Y | Z | size (x by z) | pad | cut/fill | to big city |
|---|---|---|---|---|---|---|---|
| StarterBase_Prison_Cellblock (spawn) | 2374 | 59 | -857 | 113 x 109 | 58 m | 1.1 m | 64 m |
| StarterBase_UFO_Farm | 2429 | 57 | -990 | 69 x 75 | 56 m | 0.7 m | 41 m |
| StarterBase_Ranger_Station | 2426 | 59 | -710 | 70 x 79 | 58 m | 1.1 m | 43 m |
| StarterBase_Hotel_Tower | 2286 | 57 | -736 | 127 x 124 | 56 m | 2.2 m | 155 m |
| **Compound** (wall, 146 x 202) | 2012 | 57 | -586 | 146 x 202 | 56 m | 2.1 m | 192 m |
| - StarterBase_Modern_House | 2029 | 57 | -578 | 111 x 105 | (compound pad) | | |
| - StarterBase_Bunker_House | 2019 | 57 | -467 | 69 x 75 | (compound pad) | | |
| - StarterBase_Ayesoar_Mansion | 2091 | 57 | -457 | 60 x 54 | (compound pad) | | |
| **Plot 2** (wall, 74 x 74) | 2172 | 57 | -524 | 74 x 74 | 56 m | 1.0 m | 14 m east of the compound |
| - StarterBase_Zeebark_Modern_House | 2179 | 57 | -517 | 60 x 60 | (plot 2 pad) | | |

Everything else in LocalPrefabs (Farm1, IncredibleTower, RangerStationBasicHB, RogueNerds,
ShootingRangeHQ, SrDrogasHouse, Tower1, Parts/...) is not placed.

## Ground level / underground

Your prefab .xml files had no `YOffset`, so the game was standing each prefab's *bottom* layer on the
ground - the whole underground stack ended up in the air. Each .xml now has the YOffset that puts its
real ground floor on the pad (the number is the count of terrain layers under the ground floor in
the .tts):

| Prefab | YOffset |
|---|---|
| StarterBase_Prison_Cellblock | -8 |
| StarterBase_UFO_Farm | -3 |
| StarterBase_Ranger_Station | -4 |
| StarterBase_Bunker_House | -19 (bunker) |
| StarterBase_Modern_House | -18 (bunker) |
| StarterBase_Ayesoar_Mansion | -12 |
| StarterBase_Hotel_Tower | -4 |

The originals of those seven .xml files are in `..\..\LocalPrefabs.backup-2026-09-06\`.

## Zombies

None of the seven prefabs has any sleeper volumes (`SleeperVolume*` properties) and none contains
spawner blocks, so nothing spawns inside them - there was nothing to remove. What can still reach
you is the normal biome spawn walking in, and blood moon / screamer hordes. A land claim block
stops the biome spawns inside the claim (`giveself keystoneBlock` in the F1 console, or the creative
menu). Straight from the game: LCBs prevent sleeper and biome respawns but allow blood moon and
screamer spawns.

## The compound (rebuilt 2026-09-06)

146 x 202 m, X 2012..2157, Z -586..-385, pad 56 m. Grown from the first 140 x 193 and re-spaced,
then the wall rebuilt a second time to match the Modern House's own front wall.

### Why this size

East and north are boxed in - `cabin_16` sits 6 m off the east side and `xcpv_Trailer_01_ZZTong`
7 m off the north - so the only room is west and south. South is free; **west runs into the gully**,
so every metre of width costs embankment. Measured over the whole region, growing wider than 146
doubles the earthwork for very little gain:

| box | X clearance | Z clearance | west embankment over 8 m |
|---|---|---|---|
| 140 x 193 (old) | 2.3 m | 3.0 m | 29 m, max 14.1 m |
| **146 x 202 (built)** | **4.3 m** | **6.0 m** | **31 m, max 14.2 m** |
| 152 x 202 | 6.3 m | 6.0 m | 59 m, max 17.5 m |
| 158 x 202 | 8.3 m | 6.0 m | 69 m, max 18.4 m |

There is no better site: a search of the whole 1700 x 1800 m region for a clear box this size
turned up exactly two, and the other one is a lake bed at 3 m elevation.

### Layout (interior X 2013..2156, Z -585..-386)

| House | position | size | to W wall | to E wall | to S wall | to N wall |
|---|---|---|---|---|---|---|
| StarterBase_Modern_House | 2029, -578 | 111 x 105 | 16 m | 17 m | 7 m | - |
| StarterBase_Bunker_House | 2019, -467 | 69 x 75 | 6 m | - | - | 7 m |
| StarterBase_Ayesoar_Mansion | 2091, -457 | 60 x 54 | - | 6 m | - | 18 m |

Minimum clearance to any wall is now **6 m** (was 2 m), minimum along Z **7 m** (was 3 m). The
Modern House takes the south half; the other two share the north with a 3 m lane between them and
a 6 m east-west lane separating the two bands.

### The wall

Rebuilt again on 2026-09-06 to copy **the front wall of StarterBase_Modern_House** block for block -
the brick-pillared estate wall, not the concrete rampart it replaced. Four strips, **1 m thick**,
`YOffset -3` (three buried footing courses):

| Prefab | position | size |
|---|---|---|
| StarterBase_Compound_Wall_S | 2012, -586 | 146 x 8 x 1 |
| StarterBase_Compound_Wall_N | 2012, -385 | 146 x 8 x 1 |
| StarterBase_Compound_Wall_W | 2012, -585 | 1 x 8 x 200 |
| StarterBase_Compound_Wall_E | 2157, -585 | 1 x 8 x 200 |

Bay pattern, straight off the donor: **brick pillars every 6 m**, five courses
(`brickShapes:cube` x3, `cubeBaseboard4Sided`, `concreteShapes:pillar100Cap`), and between them a
four-course panel - `brickShapes:cubeHalfCentered` base, a `corrugatedMetalShapes:windowCentered`
dark metal panel, then two courses of `ironBarsCentered`. 5 m tall at the pillars, 4 m at the panels.

The "centered" plane blocks are direction-sensitive: measured across the donor, a run along Z uses
rotation 1 or 3 and a run along X uses 0 or 2, so the north and south strips carry different
rotations from the east and west ones.

**Five working gates**, each a `steelGarageDoor5x3Black` (a 5x3 multiblock, so it opens) centred in a
5 m opening with a brick pillar either side and the railing course carried across the top:

| gate | position |
|---|---|
| east 1 | Z -530, opposite the Modern House |
| east 2 | Z -430 |
| north | X 2100 |
| south | X 2085 |
| west | Z -464 |

Gate rotation follows the same axis law: 5-wide along Z needs rotation 1 or 3, along X 0 or 2,
measured across every `steelGarageDoor5x3Black` and `rollUpGate5x3White` in the game's own prefabs.

**This is a decorative estate wall, not a fortification.** It is 1 m thick with iron railings on top,
where the previous version was a 2 m rampart 6 m high with a walkway. It looks like the house it
came from, which is what was asked for, but it will not hold a horde. The walkway is gone with it.

Losing that metre of thickness gave the yard back: minimum clearance to a wall is now **6 m**.

## Roads

Eight thin asphalt prefabs, one course of `terrAsphalt` with clear air above (`YOffset -1`), exactly
how the Modern House lays its own driveway.

| Prefab | position | size | what it is |
|---|---|---|---|
| StarterBase_Road_Ring_W | 2013, -585 | 5 x 200 | ring road, west leg |
| StarterBase_Road_Ring_E | 2152, -585 | 5 x 200 | ring road, east leg |
| StarterBase_Road_Ring_S | 2018, -585 | 134 x 5 | ring road, south leg |
| StarterBase_Road_Ring_N | 2018, -390 | 134 x 5 | ring road, north leg |
| StarterBase_Road_Lane | 2018, -473 | 134 x 5 | cross lane between the house bands |
| StarterBase_Road_Link | 2088, -467 | 3 x 64 | footpath between Bunker House and the mansion |
| StarterBase_Road_Out_A | 2158, -533 | 104 x 7 | east from the east gate |
| StarterBase_Road_Out_B | 2259, -558 | 7 x 25 | south to the existing road |

The ring runs right around the inside of the wall, so **all five gates open straight onto it** and it
passes the front of every house. The cross lane fills the 6 m gap between the Modern House and the
two northern houses.

The way out was chosen by searching every L-shaped route from each gate to a pixel of the existing
road network in `splat3.png`, scored on how much the ground would have to move. The first route
tried - south from the east gate at X 2193 - crossed a gully and needed **17.8 m of fill**. The one
built runs east along Z -530 then south at X 2259 and needs **4.9 m at worst, 1.45 m on average**,
joining the road at about (2262, -545). Both legs are graded flat at 56 m with a 14 m blend.

## Plot 2 - the Zeebark modern house

`Modern_House_Zeebark` from the Zeebark POI pack, added 2026-09-06 as an eighth starter base. It is
60 x 60, so **nothing that size was left inside the compound** - the interior is 144 x 200 and the
three houses already take 82 % of it once the ring road is in.

Extending the compound to swallow it does not work either. Measured against the original terrain:

| compound box | mean cut/fill | wall standing on >8 m of fill |
|---|---|---|
| 146 x 202 (as built) | 2.05 m | 31 m |
| 146 x 225 (Z -610) | 2.13 m | 81 m |
| 146 x 255 (Z -640) | 2.94 m | 157 m |
| 146 x 268 (Z -653, the first depth that actually fits the house) | - | blocked by an existing POI |

And a single box cannot hold both plots, because `cabin_16` sits between them at X 2160..2201.

So it has **its own walled plot**, 74 x 74 at X 2172..2245, Z -524..-451, 14 m east of the compound.
That site is better ground than the compound itself: mean cut/fill **1.0 m**, max fill 3.8 m, and
**no** stretch of its wall stands on more than 8 m of fill. The house sits centred with 6 m clear on
every side.

Same estate wall, same pattern, two gates: **south** onto the road out (a 2 m spur joins
`StarterBase_Road_Out_A`), and **west** facing the compound. To make that west gate lead somewhere,
`StarterBase_Compound_Wall_E` was rebuilt with a **third gate at Z -487**, and
`StarterBase_Road_Link2` paves the 14 m between them - so you can drive compound -> plot 2 directly.
Plot 2 has its own ring road inside the wall.

### What was changed in the prefab

`StarterBase_Zeebark_Modern_House` is a copy in `LocalPrefabs`; the pack's own file is untouched.
The `.tts` is **byte-identical** to the original, so the building itself is exactly as Zeebark built
it. Only the `.xml` metadata changed, to match the other starter bases:

| property | pack original | starter-base copy |
|---|---|---|
| `SleeperVolumeStart` etc. | **31 volumes**, all `GroupZomBadassOnly` | removed |
| `TriggerVolume*` | 3 volumes | removed |
| `DifficultyTier` | 5 | 0 |
| `QuestTags` | `clear, infested` | removed |
| `POIMarker*` | spawns `part_driveway_rural_08` | removed (it would have landed on the new wall) |
| `YOffset` | -17 | -17 (unchanged) |

That is 20 properties stripped. Left as it shipped it would have been the most dangerous building on
the map - a Tier 5 infested POI with 31 badass sleeper volumes - sitting in the group you asked to be
zombie-free. **If you would rather keep the fight, say so and I will restore its sleeper volumes.**

## If you keep an existing save

A save that has already generated this area keeps the old chunks. Either start a new game (everything
is generated fresh), or in the F1 console run

    chunkreset 1920 -1424 2528 -352

That box covers all 13 old build sites and all 7 new ones. WARNING: it rebuilds the terrain and
POIs in that box - anything you built there and every loot container in it is gone. Your bedroll /
claim block should be outside the box first.

`dtm_processed.raw` was deleted; the game rebuilds it on the next load.

## Backups

- `prefabs.xml.BEFORE-REBUILD`, `spawnpoints.xml.BEFORE-REBUILD` - the state with the 13 old builds
- `prefabs.xml.BEFORE-MYPREFABS` - original map + densify POIs (what the new prefabs.xml is built on)
- `prefabs.xml.BEFORE-DENSIFY`, `prefabs.xml.ORIGINAL-BACKUP`
- `dtm.raw.ORIGINAL-BACKUP` - the untouched terrain (the new dtm.raw is this plus the 5 pads)
- `spawnpoints.xml.ORIGINAL-BACKUP` - the original 10 spawn points
- `map_info.xml.ORIGINAL-BACKUP`
- `..\..\LocalPrefabs.backup-2026-09-06\` - the seven prefab .xml files before YOffset was added
