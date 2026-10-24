"""Document and Scope Guards for ATES FAM Fitness.

Following ATES FAM standards (ATES FAM Budget, Atlas Library):
1. Document Guard: Enforces synchronization between codebase, test counts, and documentation (README.md & ROADMAP.md).
2. Scope Guard: Protects invariant architectural rules, GLP-1 Wegovy clinical parameters, meal planner integrity,
   and dual-layer persistence keys against silent regression.
3. Progression-to-Regression Guard: Verifies automated test discovery and ensures all tests are accounted for.
"""
import glob
import importlib
import inspect
import os
import re
from pathlib import Path
from lib import meal_planner, store, program

WORKSPACE_DIR = Path(__file__).resolve().parent.parent


def test_document_guard_readme():
    """Verify README.md exists, is comprehensive, and test count matches the suite."""
    readme_path = WORKSPACE_DIR / "README.md"
    assert readme_path.exists(), "README.md must exist in repository root"
    content = readme_path.read_text(encoding="utf-8")
    assert len(content) >= 3000, "README.md must be comprehensive (>3000 chars)"

    # Core architecture and feature sections must be present
    assert "## Özellikler & Ekranlar" in content
    assert "4 Öğünlü Akıllı Menü" in content
    assert "7 Günlük Menü & Alışveriş Listesi" in content
    assert "Akıllı Besin Bulucu" in content or "Evdeki Ürünler" in content
    assert "Takviye" in content
    assert "Wegovy Koruma Modu" in content
    assert "GitHub Data Branch" in content
    assert "ROADMAP.md" in content

    # Test count must be synchronized to 121
    match = re.search(r"(\d+)\s+otomatik\s+birim", content)
    assert match is not None, "README.md must mention automated test count"
    assert int(match.group(1)) == 121, f"README.md test count ({match.group(1)}) must match total suite count (121)"


def test_document_guard_roadmap():
    """Verify ROADMAP.md exists, contains all milestones, architecture invariants, and future horizons."""
    roadmap_path = WORKSPACE_DIR / "ROADMAP.md"
    assert roadmap_path.exists(), "ROADMAP.md must exist in repository root"
    content = roadmap_path.read_text(encoding="utf-8")
    assert len(content) >= 3000, "ROADMAP.md must be comprehensive (>3000 chars)"

    # Must contain roadmap structure
    assert "Vizyon ve Temel İlkeler" in content
    assert "Sürüm Geçmişi ve Tamamlanan Kilometre Taşları" in content
    assert "V1.0" in content and "V1.1" in content and "V1.2" in content
    assert "V1.3" in content and "V1.4" in content and "V1.5" in content
    assert "Aktif Sprint" in content
    assert "Gelecek Yol Haritası" in content
    assert "Kalite Güvencesi ve Bekçi Mekanizması" in content
    assert "121" in content, "ROADMAP.md must mention 121 automated tests"


def test_scope_guard_invariants():
    """Verify that core architectural invariants, persistence keys, and clinical data structures are intact."""
    # 1. Dual-layer persistence keys
    required_keys = (
        "body",
        "wegovy",
        "weights",
        "workouts",
        "padel",
        "cron_ex",
        "active_kcal",
        "setlog",
        "loadlog",
        "settings",
        "custom_products",
        "supplements_log",
    )
    for k in required_keys:
        assert k in store.PERSIST_KEYS, f"Persistence key '{k}' must not be removed from PERSIST_KEYS"

    # 2. Home product library
    prods = meal_planner.HOME_PRODUCT_LIBRARY
    assert len(prods) >= 20, "HOME_PRODUCT_LIBRARY must contain at least 20 staple products"
    for p in prods:
        assert "name" in p and "portion" in p and "kcal" in p and "protein" in p
        assert p["kcal"] >= 0 and p["protein"] >= 0

    # 3. Clinical supplement protocol
    sups = meal_planner.get_supplement_protocol()
    assert len(sups) == 6, "SUPPLEMENT_PROTOCOL must contain exactly 6 protocol items (core + as-needed)"
    sup_ids = {s["id"] for s in sups}
    assert {"multi", "d3", "soda", "vitc", "bromelain", "magnesium"}.issubset(sup_ids)
    assert len(meal_planner.get_core_supplements()) == 4
    assert len(meal_planner.get_as_needed_supplements()) == 2

    # 4. Meal database integrity
    db = meal_planner.MEAL_DATABASE
    for cat in ("breakfast", "lunch", "snack", "dinner"):
        assert cat in db, f"MEAL_DATABASE missing category '{cat}'"
        assert len(db[cat]) >= 5, f"Category '{cat}' must have at least 5 recipes"

    # 5. Offline staples lookup
    assert len(meal_planner.OFFLINE_STAPLE_FOODS) >= 30, "Must maintain >= 30 offline staple foods"
    somon = meal_planner.lookup_food_macros("somon", grams=150)
    assert somon is not None and somon["protein"] > 25.0


def test_progression_to_regression_auto_expansion():
    """Verify that all test files in tests/ are discovered and total test count equals 121."""
    test_files = sorted(glob.glob(str(WORKSPACE_DIR / "tests" / "test_*.py")))
    assert len(test_files) >= 12, f"Expected at least 12 test files, found {len(test_files)}"

    total_test_functions = 0
    for f in test_files:
        rel = os.path.relpath(f, str(WORKSPACE_DIR))
        mod_name = rel.replace(os.sep, ".").replace(".py", "")
        mod = importlib.import_module(mod_name)
        funcs = [
            fn for name, fn in inspect.getmembers(mod, inspect.isfunction)
            if name.startswith("test_")
        ]
        total_test_functions += len(funcs)

    assert total_test_functions == 121, (
        f"Total test suite count is {total_test_functions}, expected 121. "
        f"When adding new tests, update README.md, ROADMAP.md, and this guard together!"
    )
