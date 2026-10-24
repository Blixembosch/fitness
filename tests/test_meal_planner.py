"""Unit tests for lib.meal_planner module."""
from lib import meal_planner as mp


def test_meal_database_completeness():
    for cat in ("breakfast", "lunch", "snack", "dinner"):
        options = mp.get_meal_options(cat)
        assert len(options) >= 5, f"{cat} must have at least 5 options, got {len(options)}"
        for opt in options:
            assert "id" in opt and "name" in opt and "ingredients" in opt
            assert opt["kcal"] > 250
            assert opt["protein"] >= 20.0
            assert opt["fat"] > 0
            assert opt["carbs"] > 0
            assert opt["fiber"] > 0
            assert "wegovy_tip" in opt


def test_sample_7day_plan_validity():
    assert len(mp.SAMPLE_7DAY_PLAN) == 7
    all_b = {m["id"] for m in mp.MEAL_DATABASE["breakfast"]}
    all_l = {m["id"] for m in mp.MEAL_DATABASE["lunch"]}
    all_s = {m["id"] for m in mp.MEAL_DATABASE["snack"]}
    all_d = {m["id"] for m in mp.MEAL_DATABASE["dinner"]}

    for day in mp.SAMPLE_7DAY_PLAN:
        assert day["breakfast"] in all_b
        assert day["lunch"] in all_l
        assert day["snack"] in all_s
        assert day["dinner"] in all_d


def test_calculate_menu_totals():
    sample = {"breakfast": "b1", "lunch": "l1", "snack": "s1", "dinner": "d1"}
    totals = mp.calculate_menu_totals(sample)
    assert 1700 <= totals["kcal"] <= 2100
    assert 150.0 <= totals["protein"] <= 180.0
    assert 40.0 <= totals["fat"] <= 75.0
    assert 160.0 <= totals["carbs"] <= 200.0
    assert totals["fiber"] >= 25.0


def test_smart_menu_generation_hits_targets():
    for i in range(7):
        menu = mp.generate_smart_menu(i)
        totals = mp.calculate_menu_totals(menu)
        assert 150 <= totals["protein"] <= 185
        assert totals["fiber"] >= 24.0


def test_format_whatsapp_daily_plan():
    sample = {"breakfast": "b1", "lunch": "l1", "snack": "s1", "dinner": "d1"}
    msg = mp.format_whatsapp_daily_plan(sample, "Pazar")
    assert "ATES FAM Fitness" in msg
    assert "KAHVALTI" in msg
    assert "ÖĞLE" in msg
    assert "ARA ÖĞÜN" in msg
    assert "AKŞAM" in msg
    assert "Wegovy" in msg


def test_grocery_list_generation():
    groceries = mp.generate_grocery_list()
    assert len(groceries) >= 4
    assert any("Kasap" in k for k in groceries)
    assert any("Süt" in k for k in groceries)
    assert any("Manav" in k for k in groceries)
    assert any("Kuru Gıda" in k for k in groceries)

    msg = mp.format_whatsapp_grocery_list(groceries)
    assert "Alışveriş Listesi" in msg
    assert "Albert Heijn" in msg


def test_calculate_custom_totals():
    # Only breakfast and lunch enabled
    selected = {"breakfast": "b1", "lunch": "l1", "snack": "s1", "dinner": "d1"}
    sub = mp.calculate_custom_totals(selected, enabled_types=["breakfast", "lunch"])
    assert "snack" not in sub["items"]
    assert "dinner" not in sub["items"]
    assert sub["protein"] == round(sub["items"]["breakfast"]["protein"] + sub["items"]["lunch"]["protein"], 1)
    assert sub["kcal"] == sub["items"]["breakfast"]["kcal"] + sub["items"]["lunch"]["kcal"]


def test_home_product_library():
    prods = mp.get_home_products()
    assert len(prods) >= 15
    names = [p["name"] for p in prods]
    assert any("AH Magere Kwark" in n for n in names)
    assert any("Impact Whey" in n for n in names)
    assert any("AH Protein Mousse" in n for n in names)
    assert any("Tavuk Göğsü" in n for n in names)
    for p in prods:
        assert p["kcal"] >= 0
        assert "protein" in p
        assert "fat" in p
        assert "carbs" in p
        assert "fiber" in p


def test_get_home_products_with_custom():
    custom = [
        {
            "name": "AH Zalmfilet",
            "category": "Et & Tavuk & Balık",
            "portion": "100g",
            "kcal": 200,
            "protein": 20.0,
            "fat": 13.0,
            "carbs": 0.0,
            "fiber": 0.0,
            "notes": "Omega-3",
        }
    ]
    all_prods = mp.get_home_products(custom)
    base_len = len(mp.HOME_PRODUCT_LIBRARY)
    assert len(all_prods) == base_len + 1
    assert all_prods[-1]["name"] == "AH Zalmfilet"


def test_lookup_food_macros():
    # 1. 100g lookup
    res_100 = mp.lookup_food_macros("somon", grams=100)
    assert res_100 is not None
    assert "Somon" in res_100["name"]
    assert res_100["kcal"] == 208
    assert res_100["protein"] == 20.5

    # 2. 150g scaled lookup
    res_150 = mp.lookup_food_macros("somon", grams=150)
    assert res_150 is not None
    assert res_150["kcal"] == int(round(208 * 1.5))
    assert res_150["protein"] == round(20.5 * 1.5, 1)

    # 3. Skyr and tavuk
    res_skyr = mp.lookup_food_macros("skyr", grams=200)
    assert res_skyr is not None
    assert res_skyr["protein"] == round(11.0 * 2.0, 1)

    res_tavuk = mp.lookup_food_macros("tavuk göğsü", grams=120)
    assert res_tavuk is not None
    assert res_tavuk["protein"] == round(23.0 * 1.2, 1)

    # 4. Empty/whitespace
    assert mp.lookup_food_macros("") is None
    assert mp.lookup_food_macros("   ") is None


def test_supplement_protocol():
    sups = mp.get_supplement_protocol()
    assert len(sups) == 6
    ids = [s["id"] for s in sups]
    assert "multi" in ids
    assert "d3" in ids
    assert "soda" in ids
    assert "vitc" in ids
    assert "bromelain" in ids
    assert "magnesium" in ids

    # Check meal mapping
    b_sups = mp.get_meal_supplements("breakfast")
    assert len(b_sups) == 2  # multi + d3

    snack_sups = mp.get_meal_supplements("snack")
    assert len(snack_sups) == 1  # soda

    l_sups = mp.get_meal_supplements("lunch")
    assert len(l_sups) == 2  # vitc + bromelain

    d_sups = mp.get_meal_supplements("dinner")
    assert len(d_sups) == 1  # magnesium

    # WhatsApp plan includes tiered supplement block
    sample = {"breakfast": "b1", "lunch": "l1", "snack": "s1", "dinner": "d1"}
    msg = mp.format_whatsapp_daily_plan(sample, "Pazar")
    assert "GÜNLÜK TAKVİYE & ELEKTROLİT PROTOKOLÜ" in msg
    assert "TEMEL GÜNLÜK RUTİN" in msg
    assert "SADECE İHTİYAÇ HALİNDE" in msg
    assert "Multivitamin" in msg
    assert "D3 Sprey" in msg
    assert "Avoya" in msg or "Soda" in msg
    assert "ExtraMag" in msg
    assert "Bromelain" in msg


def test_supplement_tiers_and_mineral_water():
    """Verify tier separation between daily core routine and symptomatic items, plus mineral water lookup."""
    core = mp.get_core_supplements()
    assert len(core) == 4
    core_ids = {s["id"] for s in core}
    assert core_ids == {"multi", "d3", "soda", "magnesium"}

    as_needed = mp.get_as_needed_supplements()
    assert len(as_needed) == 2
    as_needed_ids = {s["id"] for s in as_needed}
    assert as_needed_ids == {"bromelain", "vitc"}

    # Check that Avoya and AH Soda are findable via offline staples and home product catalog
    avoya = mp.lookup_food_macros("avoya", grams=200)
    assert avoya is not None
    assert "Avoya" in avoya["name"]
    assert avoya["kcal"] == 0

    soda = mp.lookup_food_macros("soda", grams=250)
    assert soda is not None
    assert "Soda" in soda["name"] or "Bronwater" in soda["name"]

    prods = mp.get_home_products()
    p_names = [p["name"] for p in prods]
    assert any("Avoya" in n for n in p_names)
    assert any("Soda" in n for n in p_names)


def test_circadian_meal_timing_protocols():
    """Verify evidence-based circadian meal and workout timing protocols (Nature 2025 & Sleep Med Rev 2026)."""
    # 1. Weekday morning workout protocol
    wd = mp.get_circadian_meal_timing("weekday")
    assert "06:30" in wd["workout_time"]
    assert "Wegovy" in wd["pre_workout"] or "katı gıda" in wd["pre_workout"]
    assert len(wd["schedule"]) == 4
    roles = {item["meal"]: item["role"] for item in wd["schedule"]}
    assert "Post-Workout" in roles["breakfast"]
    assert "22:45" in wd["sleep_time"]

    # 2. Weekend daytime workout protocol
    we = mp.get_circadian_meal_timing("weekend")
    assert "11:30" in we["workout_time"]
    we_roles = {item["meal"]: item["role"] for item in we["schedule"]}
    assert "Pre-Workout" in we_roles["breakfast"]
    assert "Post-Workout" in we_roles["lunch"]

    # 3. Padel evening protocol (>= 3-4 hours sleep buffer)
    pd = mp.get_circadian_meal_timing("padel_evening")
    assert "Padel" in pd["workout_time"]
    assert "23:45" in pd["sleep_time"]

    # 4. WhatsApp export includes circadian headers & badges
    sample = {"breakfast": "b1", "lunch": "l1", "snack": "s1", "dinner": "d1"}
    msg_wd = mp.format_whatsapp_daily_plan(sample, "Pazartesi", timing_mode="weekday")
    assert "SPOR & SİRKADİYEN ZAMANLAMA" in msg_wd
    assert "06:30 – 07:45" in msg_wd
    assert "Post-Workout Anabolik Pencere" in msg_wd

    msg_we = mp.format_whatsapp_daily_plan(sample, "Cumartesi", timing_mode="weekend")
    assert "SPOR & SİRKADİYEN ZAMANLAMA" in msg_we
    assert "Gün İçi Spor" in msg_we
    assert "Pre-Workout Yakıt" in msg_we
    assert "Post-Workout Anabolik" in msg_we




