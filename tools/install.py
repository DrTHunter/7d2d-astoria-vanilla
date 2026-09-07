#!/usr/bin/env python3
"""
Turn a stock Astoria 8K world into DrTHunter's all-vanilla version.

    python tools/install.py

This does the one thing Vortex cannot: patch the map itself. The starter-base
mod is a normal Vortex mod - see vortex/Astoria-Vanilla-POIs.zip.

Nothing is touched until every check passes, and the stock files are copied to
<name>.stock-backup first, so you can always go back.

    --undo          put the stock map back
    --no-vortex     also drop the POI pack straight into Mods\\
                    (only if you are not using Vortex)
"""
import os, sys, json, shutil, zlib, struct, hashlib, argparse, zipfile

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.dirname(HERE)
PATCH  = os.path.join(ROOT, "world-patch")
MODZIP = os.path.join(ROOT, "vortex", "Astoria-Vanilla-POIs.zip")


def md5(path, chunk=1 << 20):
    m = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            m.update(block)
    return m.hexdigest()


def find_game_dir():
    base = os.environ.get("APPDATA")
    if base and os.path.isdir(os.path.join(base, "7DaysToDie")):
        return os.path.join(base, "7DaysToDie")
    for p in (os.path.expanduser("~/.local/share/7DaysToDie"),
              os.path.expanduser("~/Library/Application Support/7DaysToDie")):
        if os.path.isdir(p):
            return p
    return None


def apply_dtm(stock_path, out_path, patch_path):
    blob = zlib.decompress(open(patch_path, "rb").read())
    if blob[:4] != b"D2DT":
        sys.exit("dtm.patch is corrupt (bad magic)")
    ver, count = struct.unpack_from("<II", blob, 4)
    if ver != 1:
        sys.exit(f"dtm.patch is version {ver}; this installer only understands 1")
    body = blob[12:]
    data = bytearray(open(stock_path, "rb").read())
    for i in range(count):
        off = int.from_bytes(body[i * 4:i * 4 + 4], "little")
        val = body[4 * count + i * 2: 4 * count + i * 2 + 2]
        data[off * 2:off * 2 + 2] = val
    open(out_path, "wb").write(data)
    return count


def undo(world, man):
    n = 0
    for name in man["stock"]:
        bak = os.path.join(world, name + ".stock-backup")
        if os.path.exists(bak):
            shutil.move(bak, os.path.join(world, name)); n += 1
            print(f"  restored {name}")
    if not n:
        sys.exit("No .stock-backup files found - nothing to undo.")
    print(f"\nStock map restored ({n} files). Astoria 8K is vanilla again.")
    print("The POI pack is separate - turn it off in Vortex.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game-dir", help=r"e.g. %APPDATA%\7DaysToDie")
    ap.add_argument("--world", default="Astoria 8K")
    ap.add_argument("--undo", action="store_true", help="restore the stock map")
    ap.add_argument("--no-vortex", action="store_true",
                    help="also copy the POI pack into Mods\\ yourself")
    ap.add_argument("--force", action="store_true",
                    help="patch even if the stock files do not match")
    a = ap.parse_args()

    man = json.load(open(os.path.join(PATCH, "manifest.json")))
    game = a.game_dir or find_game_dir()
    if not game:
        sys.exit("Could not find your 7DaysToDie folder. Pass --game-dir.")
    world = os.path.join(game, "GeneratedWorlds", a.world)
    print(f"game folder : {game}")
    print(f"world folder: {world}\n")
    if not os.path.isdir(world):
        sys.exit(f"'{a.world}' is not installed.\n"
                 f"Install the base map first: {man['base_map']}\n"
                 f"It has to end up at {world}")

    if a.undo:
        return undo(world, man)

    print("checking the stock world ...")
    ok = True
    for name, want in man["stock"].items():
        p = os.path.join(world, name)
        if not os.path.exists(p):
            print(f"  MISSING  {name}"); ok = False; continue
        got = md5(p)
        if got == want:                      print(f"  ok       {name}")
        elif got == man["result"][name]:      print(f"  ALREADY PATCHED  {name}")
        else:
            print(f"  MISMATCH {name}\n           expected {want}\n           found    {got}")
            ok = False
    if not ok and not a.force:
        sys.exit("\nThese are not the Astoria files this patch was built against.\n"
                 f"Expected: {man['base_map']}\n"
                 "Install that exact version, or re-run with --force if you know what you are doing.\n"
                 "Nothing has been changed.")

    print("\npatching the map ...")
    for name in man["stock"]:
        src, bak = os.path.join(world, name), os.path.join(world, name + ".stock-backup")
        if os.path.exists(src) and not os.path.exists(bak):
            shutil.copy2(src, bak); print(f"  backed up {name}")
    n = apply_dtm(os.path.join(world, "dtm.raw.stock-backup"),
                  os.path.join(world, "dtm.raw"), os.path.join(PATCH, "dtm.patch"))
    print(f"  dtm.raw         {n} cells re-graded (the walled plots and the roads)")
    for name in ("prefabs.xml", "spawnpoints.xml"):
        shutil.copy2(os.path.join(PATCH, name), os.path.join(world, name))
        print(f"  {name:<15} replaced")
    for junk in ("dtm_processed.raw", "splat3_processed.png", "splat4_processed.png",
                 "splat3_half.png", "splat4_half.png"):
        p = os.path.join(world, junk)
        if os.path.exists(p):
            os.remove(p); print(f"  cleared cache   {junk}")

    print("\nverifying ...")
    bad = [k for k, want in man["result"].items() if md5(os.path.join(world, k)) != want]
    if bad:
        sys.exit(f"FAILED: {bad} do not match. Re-run with --undo to restore the stock map.")
    print("  all three files match the expected checksums")

    if a.no_vortex:
        dst = os.path.join(game, "Mods")
        print(f"\ninstalling the POI pack -> {os.path.join(dst,'Astoria-Vanilla-POIs')}")
        old = os.path.join(dst, "Astoria-Vanilla-POIs")
        if os.path.isdir(old):
            shutil.rmtree(old)
        with zipfile.ZipFile(MODZIP) as z:
            z.extractall(dst)
        print(f"  {len(os.listdir(os.path.join(old,'Prefabs','POIs')))} files")
    else:
        print("\nThe map is done. One thing left, in Vortex:")
        print(f"    drag  {MODZIP}  onto the Vortex window, then click Enable")

    print(f"\n{man['decorations']} POIs, {man['dtm_cells_changed']} terrain cells.")
    print("Start a NEW save on 'Astoria 8K' - an existing save keeps its old chunks.")


if __name__ == "__main__":
    main()
