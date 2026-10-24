#!/usr/bin/env python3
"""Offline skill snapshots. JSON stdout; no skill files are executed."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
from datetime import datetime, timezone

IGNORED = {".git", "__pycache__"}


def checked_path(value):
    """Check every existing component before using an absolute lexical path."""
    path = Path(os.path.abspath(value))
    for part in [*reversed(path.parents), path]:
        if os.path.lexists(part):
            info = part.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
                raise ValueError(f"Link/reparse path forbidden: {part}")
    return path


def digest(path):
    checked_path(path)
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def inventory(root):
    root = checked_path(root)
    if not root.is_dir():
        raise ValueError(f"Not a directory: {root}")
    files, directories = {}, []
    for current, dirs, names in os.walk(root, followlinks=False):
        base = Path(current)
        for name in dirs + names:
            checked_path(base / name)
        dirs[:] = sorted(name for name in dirs if name not in IGNORED)
        for name in dirs:
            directories.append((base / name).relative_to(root).as_posix())
        for name in sorted(names):
            path = base / name
            if not stat.S_ISREG(path.lstat().st_mode):
                raise ValueError(f"Non-regular file forbidden: {path}")
            files[path.relative_to(root).as_posix()] = digest(path)
    return dict(sorted(files.items())), sorted(directories)


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate manifest key: {key}")
        result[key] = value
    return result


def relative_name(name):
    if not isinstance(name, str) or not name or "\\" in name or ":" in name or "\0" in name:
        raise ValueError("Unsafe manifest path")
    path = PurePosixPath(name)
    if path.is_absolute() or any(part in {".", "..", ""} for part in name.split("/")):
        raise ValueError(f"Unsafe manifest path: {name}")
    if any(part in IGNORED for part in path.parts[:-1]):
        raise ValueError(f"Ignored directory in manifest: {name}")
    return name


def load_manifest(run):
    run = checked_path(run)
    if not run.is_dir() or os.path.lexists(run / ".incomplete"):
        raise ValueError("Snapshot missing or incomplete")
    manifest_path = checked_path(run / "manifest.json")
    data = json.loads(manifest_path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)
    if not isinstance(data, dict) or type(data.get("version")) is not int or data.get("version") != 1 or data.get("status") != "complete":
        raise ValueError("Invalid manifest version/status")
    if data.get("algorithm") != "sha256" or data.get("ignored_directories") != sorted(IGNORED):
        raise ValueError("Invalid manifest hashing/ignore policy")
    if not isinstance(data.get("created_at"), str):
        raise ValueError("Missing creation time")
    datetime.fromisoformat(data["created_at"])
    source = data.get("source")
    if not isinstance(source, str) or not Path(source).is_absolute():
        raise ValueError("Invalid source path")
    if not isinstance(data.get("files"), dict) or "SKILL.md" not in data["files"]:
        raise ValueError("Invalid manifest files")
    for name, sha in data["files"].items():
        relative_name(name)
        if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{64}", sha):
            raise ValueError("Invalid SHA256")
    dirs = data.get("directories")
    if not isinstance(dirs, list) or any(not isinstance(item, str) for item in dirs):
        raise ValueError("Invalid manifest directories")
    for name in dirs:
        relative_name(name)
    if len(set(dirs)) != len(dirs) or set(dirs) & set(data["files"]):
        raise ValueError("Conflicting manifest paths")
    return run, data


def verify(run, source=False):
    run, data = load_manifest(run)
    expected = (data["files"], data["directories"])
    if inventory(run / "baseline") != expected:
        raise ValueError("Baseline file set, directories or hashes differ from manifest")
    if source and inventory(data["source"]) != expected:
        raise ValueError("Original source differs from manifest")
    return run, data


def capture(source, run):
    source, run = checked_path(source), checked_path(run)
    if run == source or source in run.parents:
        raise ValueError("RUN_DIR must be outside SOURCE")
    if os.path.lexists(run):
        raise ValueError("RUN_DIR already exists; refusing overwrite")
    if not source.is_dir() or not (source / "SKILL.md").is_file():
        raise ValueError("SOURCE must contain SKILL.md")
    files, directories = inventory(source)
    run.mkdir()  # Exclusive creation; an existing directory is never reused.
    marker = run / ".incomplete"
    marker.write_text("Capture started; do not use until complete.\n", encoding="utf-8")
    try:
        for label in ("baseline", "candidate"):
            target = run / label
            target.mkdir()
            for name in directories:
                (target / name).mkdir(parents=True, exist_ok=True)
            for name in files:
                checked_path(source / name)
                checked_path(target / name)
                shutil.copy2(source / name, target / name)
            if inventory(target) != (files, directories):
                raise ValueError(f"{label} copy differs from source snapshot")
        if inventory(source) != (files, directories):
            raise ValueError("Source changed during capture")
        data = {"version": 1, "status": "complete", "source": str(source),
                "created_at": datetime.now(timezone.utc).isoformat(),
                "algorithm": "sha256", "ignored_directories": sorted(IGNORED),
                "files": files, "directories": directories}
        (run / "manifest.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        marker.unlink()
    except Exception as exc:
        marker.write_text(f"Capture incomplete: {exc}\n", encoding="utf-8")
        raise
    return {"ok": True, "command": "capture", "run_dir": str(run), "file_count": len(files)}


def main():
    class JsonParser(argparse.ArgumentParser):
        def error(self, message):
            raise ValueError(message)

    parser = JsonParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    cap = commands.add_parser("capture")
    cap.add_argument("source")
    cap.add_argument("run_dir")
    check = commands.add_parser("verify")
    check.add_argument("run_dir")
    check.add_argument("--source", action="store_true")
    compare = commands.add_parser("diff")
    compare.add_argument("run_dir")
    args = parser.parse_args()
    if args.command == "capture":
        return capture(args.source, args.run_dir)
    run, data = verify(args.run_dir, getattr(args, "source", False))
    result = {"ok": True, "command": args.command, "run_dir": str(run)}
    if args.command == "verify":
        result["source_checked"] = args.source
    else:
        before, after = data["files"], inventory(run / "candidate")[0]
        result["changes"] = [
            {"path": name, "status": "added" if name not in before else "deleted" if name not in after else "modified",
             "baseline_sha256": before.get(name), "candidate_sha256": after.get(name)}
            for name in sorted(before.keys() | after.keys()) if before.get(name) != after.get(name)]
    return result


if __name__ == "__main__":
    try:
        output = main()
    except Exception as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=True))
        sys.exit(1)
    print(json.dumps(output, ensure_ascii=True))
