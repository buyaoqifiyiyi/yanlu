"""Framework-free offline integration checks. Run with Python 3.11+."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/skill_snapshot.py"
checks = 0


def call(*args, ok=True):
    global checks
    process = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)
    result = json.loads(process.stdout)
    assert (process.returncode == 0) == ok, (process.returncode, result, process.stderr)
    assert result["ok"] == ok, result
    checks += 1
    return result


with tempfile.TemporaryDirectory(prefix="中文 空格 ", dir=Path(__file__).parent) as temp:
    root = Path(temp)
    source = root / "原技能 source"
    source.mkdir()
    (source / "SKILL.md").write_text("# 测试\n", encoding="utf-8")
    (source / "assets").mkdir()
    (source / "assets/资源 space.bin").write_bytes(bytes(range(256)))
    (source / "empty").mkdir()
    (source / ".git").mkdir()
    (source / ".git/config").write_text("ignore")
    (source / "__pycache__").mkdir()
    (source / "__pycache__/ignored.pyc").write_bytes(b"ignore")
    run = root / "实验 run"
    call("capture", source, run)
    call("verify", run, "--source")
    assert (run / "baseline/assets/资源 space.bin").read_bytes() == bytes(range(256))
    assert (run / "baseline/empty").is_dir()
    assert not (run / "baseline/.git").exists()
    assert not (run / "baseline/__pycache__").exists()
    assert call("diff", run)["changes"] == []
    (run / "candidate/SKILL.md").write_text("changed")
    (run / "candidate/assets/资源 space.bin").unlink()
    (run / "candidate/new.txt").write_text("new")
    assert {row["status"] for row in call("diff", run)["changes"]} == {"added", "modified", "deleted"}
    call("verify", run, "--source")
    assert (source / "SKILL.md").read_text(encoding="utf-8") == "# 测试\n"
    call("capture", source, run, ok=False)
    call("capture", source, source / "nested", ok=False)
    call("capture", source, source, ok=False)
    (source / "SKILL.md").write_text("source changed")
    call("verify", run, "--source", ok=False)
    call("verify", run)
    (source / "SKILL.md").write_text("# 测试\n", encoding="utf-8")
    baseline = run / "baseline/SKILL.md"
    original = baseline.read_bytes()
    baseline.write_bytes(b"tampered")
    call("verify", run, ok=False)
    call("diff", run, ok=False)
    baseline.write_bytes(original)
    baseline.unlink()
    call("verify", run, ok=False)
    baseline.write_bytes(original)
    extra = run / "baseline/unlisted"
    extra.write_text("extra")
    call("verify", run, ok=False)
    extra.unlink()
    manifest = run / "manifest.json"
    saved = manifest.read_text(encoding="utf-8")
    for content in ("{broken", '{"version":1,"version":1}',):
        manifest.write_text(content, encoding="utf-8")
        call("verify", run, ok=False)
    data = json.loads(saved)
    data["files"]["../escape"] = "0" * 64
    manifest.write_text(json.dumps(data), encoding="utf-8")
    call("verify", run, ok=False)
    data["files"].pop("../escape")
    data["files"]["C:/escape"] = "0" * 64
    manifest.write_text(json.dumps(data), encoding="utf-8")
    call("verify", run, ok=False)
    manifest.write_text(saved, encoding="utf-8")
    data = json.loads(saved)
    data["algorithm"] = "md5"
    manifest.write_text(json.dumps(data), encoding="utf-8")
    call("verify", run, ok=False)
    manifest.write_text(saved, encoding="utf-8")
    call("verify", run, "--source")
    spec = importlib.util.spec_from_file_location("snapshot", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    failed = root / "partial"
    try:
        with patch.object(module.shutil, "copy2", side_effect=OSError("injected copy failure")):
            module.capture(source, failed)
        raise AssertionError("Failure injection did not fail")
    except OSError:
        assert (failed / ".incomplete").is_file()
    call("verify", failed, ok=False)
    link = root / "directory link"
    linked = False
    try:
        link.symlink_to(source, target_is_directory=True)
        linked = True
    except OSError:
        if os.name == "nt":
            linked = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(source)], capture_output=True).returncode == 0
    if linked:
        try:
            call("capture", link, root / "linked capture", ok=False)
            call("capture", source, link / "output", ok=False)
            inner_link = source / "linked resource"
            if os.name == "nt":
                assert subprocess.run(["cmd", "/c", "mklink", "/J", str(inner_link), str(root / "partial")], capture_output=True).returncode == 0
            else:
                inner_link.symlink_to(root / "partial", target_is_directory=True)
            try:
                call("capture", source, root / "reject inner link", ok=False)
            finally:
                os.rmdir(inner_link) if os.name == "nt" else inner_link.unlink()
            candidate_link = run / "candidate/link"
            if os.name == "nt":
                assert subprocess.run(["cmd", "/c", "mklink", "/J", str(candidate_link), str(source)], capture_output=True).returncode == 0
            else:
                candidate_link.symlink_to(source, target_is_directory=True)
            try:
                call("diff", run, ok=False)
            finally:
                os.rmdir(candidate_link) if os.name == "nt" else candidate_link.unlink()
        finally:
            os.rmdir(link) if os.name == "nt" else link.unlink()
    call("verify", run, "--source")
    call("nonsense", ok=False)
print(json.dumps({"passed": checks, "links_tested": linked}))
