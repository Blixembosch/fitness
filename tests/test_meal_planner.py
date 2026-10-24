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
        assert p["kcal"] > 0
        assert "protein" in p
        assert "fat" in p
        assert "carbs" in p
        assert "fiber" in p


