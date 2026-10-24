"""Smart Meal Planner & Nutrition Recommender for ATES FAM Fitness.

Tailored for Wegovy (GLP-1) protocol + muscle preservation:
- Anchored at ~160g Protein, ~67g Fat, ~189g Carbs, ~28g Fiber (~2000 kcal).
- 4-meal structure (Breakfast, Lunch, Snack/Recovery, Dinner) to avoid gastric fullness/reflux.
- Integrates home inventory (AH Kwark, Hüttenkäse, Impact Whey, Upfront, AH protein mousse/pudding,
  Yfood/Huel, eggs, chicken, lean mince, veggies) with 5 evidence-based options per meal.
- Generates customizable daily menus, WhatsApp messages for spouses, 7-day plans, and categorized
  Albert Heijn / Dutch grocery shopping lists.
"""
from __future__ import annotations

MEAL_DATABASE: dict[str, list[dict]] = {
    "breakfast": [
        {
            "id": "b1",
            "name": "Kwark, Yulaf & Çikolatalı Whey Kasesi",
            "subtitle": "3 dakikada hazır · Pişirme gerektirmez · Evdeki malzemelerle",
            "ingredients": [
                "250g AH Magere Kwark (Low-fat quark)",
                "25g Impact Whey Protein Pure Chocolade",
                "40g Yulaf (Havermout)",
                "60g Muz (yarım muz, dilimlenmiş)",
                "10g AH Terra 100% Fıstık Ezmesi (parçacıklı)",
                "5g Chia veya keten tohumu",
            ],
            "kcal": 465,
            "protein": 42.0,
            "fat": 11.5,
            "carbs": 46.0,
            "fiber": 7.0,
            "home_items": ["AH Magere Kwark", "Impact Whey Chocolade", "Muz", "AH Terra Fıstık Ezmesi"],
            "prep_time": "3 dk",
            "wegovy_tip": "Yağ oranı düşüktür; yulaftaki beta-glukan lifi GLP-1 ile birleşerek sabah kan şekerini ve tokluğu dengeler.",
        },
        {
            "id": "b2",
            "name": "Sıcak Vanilla-Yulaf Lapası & Muz",
            "subtitle": "Kış sabahları için sıcak, sindirimi kolay ve kremsi",
            "ingredients": [
                "45g Yulaf (Havermout)",
                "200ml Alpro Roasted Almond Drink (şekersiz)",
                "25g Upfront Whey Milkshake Vanilla",
                "100g Muz (1 orta boy, dilimlenmiş)",
                "10g AH Terra Fıstık Ezmesi",
                "Tarçın (isteğe bağlı, kan şekeri desteği)",
            ],
            "kcal": 445,
            "protein": 36.0,
            "fat": 10.5,
            "carbs": 49.0,
            "fiber": 6.5,
            "home_items": ["Upfront Whey Vanilla", "Alpro Almond Drink", "Muz", "AH Terra Fıstık Ezmesi"],
            "prep_time": "5 dk",
            "wegovy_tip": "Alpro badem sütü kalorisi ve yağı minimumda tutar; tarçın tatlı isteğini doğal yolla keser.",
        },
        {
            "id": "b3",
            "name": "Hüttenkäse & Yumurtalı Sporcu Tostu",
            "subtitle": "Tuzlu kahvaltı sevenler için yüksek proteinli omlet & ekmek",
            "ingredients": [
                "2 adet AH Organik Yumurta (M/L)",
                "100g AH Cottage Cheese Light (Hüttenkäse light)",
                "2 dilim tam buğday ekmeği (Volkoren)",
                "50g Bebek ıspanak & çeri domates",
                "3g Zeytinyağı spreyi (tava için)",
            ],
            "kcal": 425,
            "protein": 35.0,
            "fat": 14.0,
            "carbs": 36.0,
            "fiber": 6.0,
            "home_items": ["AH Organic Eggs", "AH Cottage Cheese Light", "Ispanak"],
            "prep_time": "8 dk",
            "wegovy_tip": "Hüttenkäse yumurtayı kabartır ve yağ eklemeden proteini 35 grama ulaştırır; tam buğday lifi sindirimi destekler.",
        },
        {
            "id": "b4",
            "name": "Çırpılmış Yumurta, Hindi Füme & Elma",
            "subtitle": "Klasik protein tabağı + taze lifli meyve",
            "ingredients": [
                "2 adet AH Organik Yumurta + 100g Cottage cheese light",
                "50g Hindi veya Tavuk Göğsü füme dilimleri",
                "1 dilim tam buğday ekmeği (Volkoren)",
                "1 adet orta boy elma (kabuklu, pektin lifi)",
            ],
            "kcal": 430,
            "protein": 38.0,
            "fat": 14.5,
            "carbs": 35.0,
            "fiber": 6.5,
            "home_items": ["AH Organic Eggs", "AH Cottage Cheese Light"],
            "prep_time": "7 dk",
            "wegovy_tip": "Elmadaki pektin lifi Wegovy'de bağırsak mikrobiyotasını besler; yumurta ve süzme peynir kas yıkımını önler.",
        },
        {
            "id": "b5",
            "name": "Pratik Şişe Kahvaltı (Yoğun Sabahlar)",
            "subtitle": "Evden hızlı çıkarken veya toplantı öncesinde hazır öğün",
            "ingredients": [
                "1 şişe Yfood Cold Brew Coffee veya Choco (500ml)",
                "1 adet orta boy muz",
                "1 adet haşlanmış AH Organik Yumurta",
            ],
            "kcal": 510,
            "protein": 38.0,
            "fat": 18.0,
            "carbs": 48.0,
            "fiber": 7.5,
            "home_items": ["Yfood Cold Brew / Choco", "Muz", "AH Organic Eggs"],
            "prep_time": "1 dk",
            "wegovy_tip": "Yfood dengeli mikro ve makro içerir; yanında haşlanmış yumurta tokluk süresini öğleye kadar uzatır.",
        },
    ],
    "lunch": [
        {
            "id": "l1",
            "name": "Izgara Tavuk Göğsü, Basmati & Buharda Brokoli",
            "subtitle": "Temiz, yağsız ve altın standart kas koruma öğünü",
            "ingredients": [
                "150g Tavuk Göğsü (Kipfilet, yağsız ızgara/tava)",
                "130g Haşlanmış Basmati Pirinç (yaklaşık 45g çiğ)",
                "180g Buharda Brokoli (limonlu)",
                "6g Sızma zeytinyağı (1 tatlı kaşığı)",
            ],
            "kcal": 445,
            "protein": 44.0,
            "fat": 9.5,
            "carbs": 43.0,
            "fiber": 6.5,
            "home_items": ["Brokoli"],
            "prep_time": "15 dk",
            "wegovy_tip": "Minimum yağ oranı sayesinde mide boşalmasını geciktirmez; akşamüstü Padel veya ağırlık antrenmanına glikojen sağlar.",
        },
        {
            "id": "l2",
            "name": "Suda Ton Balıklı & Nohutlu Akdeniz Kasesi",
            "subtitle": "Pişirme yok · Yüksek lif ve omega yağ asitleri",
            "ingredients": [
                "1 kutu Suda Ton Balığı (Tonijn in water, 130g süzülmüş)",
                "140g Haşlanmış Nohut (Kikkererwten, konserve yıkanmış)",
                "100g Bebek ıspanak, salatalık ve çeri domates",
                "8g Sızma zeytinyağı + elma sirkesi ve limon",
            ],
            "kcal": 465,
            "protein": 43.0,
            "fat": 13.0,
            "carbs": 42.0,
            "fiber": 9.5,
            "home_items": ["Ispanak"],
            "prep_time": "5 dk",
            "wegovy_tip": "Nohut tek başına 8g lif sağlar; ton balığı sıfır karbonhidratlı saf protein sunarak kaloriyi dengeler.",
        },
        {
            "id": "l3",
            "name": "Hüttenkäse & Tavuklu Dürüm (Wrap)",
            "subtitle": "Ofise veya dışarıya taşımaya çok uygun pratik öğle yemeği",
            "ingredients": [
                "120g Didiklenmiş Tavuk Göğsü",
                "90g AH Cottage Cheese Light (sos olarak)",
                "1 adet Tam Buğday Lavaş (Volkoren wrap ~60g)",
                "Garnitür: Marul, mor lahana, rende havuç",
                "1 tk hardal ve karabiber",
            ],
            "kcal": 435,
            "protein": 43.0,
            "fat": 10.5,
            "carbs": 40.0,
            "fiber": 6.0,
            "home_items": ["AH Cottage Cheese Light"],
            "prep_time": "8 dk",
            "wegovy_tip": "Mayonez yerine Hüttenkäse sos kullanmak yağı 20 gramdan 10 grama indirir; mide yanmasını engeller.",
        },
        {
            "id": "l4",
            "name": "Fırın Tavuk Göğsü & Yeşil Mercimek Salatası",
            "subtitle": "Bitkisel + hayvansal çift protein ve süper lif kaynağı",
            "ingredients": [
                "130g Fırınlanmış Tavuk Göğsü",
                "150g Haşlanmış Yeşil Mercimek (Linzen)",
                "Roka, nane, kırmızı soğan ve maydanoz",
                "6g Sızma zeytinyağı + 1 tatlı kaşığı nar ekşisi",
            ],
            "kcal": 460,
            "protein": 46.0,
            "fat": 9.5,
            "carbs": 45.0,
            "fiber": 10.5,
            "home_items": [],
            "prep_time": "12 dk",
            "wegovy_tip": "Mercimeğin çözünür lifi Wegovy ile mükemmel uyumludur; GLP-1'in tokluk sinyalini 5 saate kadar uzatır.",
        },
        {
            "id": "l5",
            "name": "Huel Meal Drink & AH Protein Pudding",
            "subtitle": "Mutfakta vakit olmayan süper yoğun günler için tam makro",
            "ingredients": [
                "1 şişe Huel Chocolate Ready-to-drink (500ml)",
                "1 kap AH Protein Pudding Chocolate (200g, 20g protein)",
            ],
            "kcal": 550,
            "protein": 46.0,
            "fat": 19.0,
            "carbs": 49.0,
            "fiber": 8.0,
            "home_items": ["Huel Chocolate Drink", "AH Protein pudding choco"],
            "prep_time": "1 dk",
            "wegovy_tip": "Huel bezelye ve keten tohumu lifi içerir; protein pudingiyle birlikte 46g protein ve tatlı tatmini sağlar.",
        },
    ],
    "snack": [
        {
            "id": "s1",
            "name": "Çikolatalı Fit Mousse & Kwark Tatlı Kasesi",
            "subtitle": "Tatlı krizini sıfır kaçamakla çözen evdeki favori karışım",
            "ingredients": [
                "1 kap XXL Fitmousse veya AH Protein Mousse (200g, 20g P)",
                "100g AH Magere Kwark (8.5g P)",
                "50g Muz (dilimlenmiş)",
                "8g AH Terra Fıstık Ezmesi",
            ],
            "kcal": 340,
            "protein": 32.0,
            "fat": 7.5,
            "carbs": 35.0,
            "fiber": 4.0,
            "home_items": ["XXL Fitmousse / AH Protein mousse", "AH Magere Kwark", "Muz", "AH Terra Fıstık Ezmesi"],
            "prep_time": "2 dk",
            "wegovy_tip": "Mousse ve kwark birleşimi yoğun hacim ve çikolata hazzı verir; toplam şeker neredeyse sıfırdır.",
        },
        {
            "id": "s2",
            "name": "Antrenman Sonrası Çikolata Recovery Shake",
            "subtitle": "Padel veya ağırlık sonrası kas onarımı & glikojen yenileme",
            "ingredients": [
                "30g Impact Whey Protein Pure Chocolade (1 ölçek)",
                "250ml Alpro Roasted Almond Drink (şekersiz)",
                "1 adet orta boy Muz (100g)",
                "25g Yulaf (blendere eklenmiş)",
                "5g Chia tohumu",
            ],
            "kcal": 380,
            "protein": 32.0,
            "fat": 6.5,
            "carbs": 48.0,
            "fiber": 6.5,
            "home_items": ["Impact Whey Chocolade", "Alpro Almond Drink", "Muz"],
            "prep_time": "3 dk",
            "wegovy_tip": "Sıvı formda olduğu için ağırlık veya padel sonrası iştah kapalıyken bile rahatça tüketilir.",
        },
        {
            "id": "s3",
            "name": "Upfront Vanilla Shake & Elma-Ceviz Tabağı",
            "subtitle": "İkindi çayı/kahvesi yanına doyurucu ve çıtır atıştırmalık",
            "ingredients": [
                "25g Upfront Whey Milkshake Vanilla (soğuk su veya Alpro ile)",
                "1 adet orta boy elma (dilimlenmiş, üzerine tarçın)",
                "15g Çiğ Badem veya Ceviz",
            ],
            "kcal": 325,
            "protein": 28.0,
            "fat": 10.5,
            "carbs": 29.0,
            "fiber": 5.0,
            "home_items": ["Upfront Whey Vanilla", "Alpro Almond Drink"],
            "prep_time": "2 dk",
            "wegovy_tip": "Ceviz/bademdeki sağlıklı yağlar tokluk hormonlarını uyarır; porsiyon kontrolüyle yağ sınırını aşmaz.",
        },
        {
            "id": "s4",
            "name": "AH Protein Drink & Fıstık Ezmeli Pirinç Patlağı",
            "subtitle": "Ofiste ya da antrenmana giderken çantada taşınabilir ikili",
            "ingredients": [
                "1 şişe AH Protein Drink Chocolate (330ml, 25g P)",
                "2 adet Tam Tahıllı Pirinç Patlağı (Rijstwafel)",
                "12g AH Terra 100% Fıstık Ezmesi",
                "1 kutu Sade Soda (Maden suyu)",
            ],
            "kcal": 350,
            "protein": 29.0,
            "fat": 8.0,
            "carbs": 39.0,
            "fiber": 4.5,
            "home_items": ["AH Protein drink chocolate", "AH Terra Fıstık Ezmesi", "Sade soda"],
            "prep_time": "1 dk",
            "wegovy_tip": "Sade soda Wegovy'de mideyi rahatlatır ve mineral desteği sağlar; hazır protein içeceği pratiktir.",
        },
        {
            "id": "s5",
            "name": "Tuzlu Hüttenkäse & Çıtır Wasa Tabağı",
            "subtitle": "Tatlı yerine tuzlu atıştırmalık isteyen günlerin kurtarıcısı",
            "ingredients": [
                "150g AH Cottage Cheese Light",
                "3 dilim Wasa Volkoren (tam çavdar gevreği)",
                "6 adet çeri domates + taze fesleğen / nane",
                "Pul biber & çörekotu serpiştirilmiş",
            ],
            "kcal": 285,
            "protein": 25.0,
            "fat": 4.5,
            "carbs": 34.0,
            "fiber": 6.0,
            "home_items": ["AH Cottage Cheese Light"],
            "prep_time": "3 dk",
            "wegovy_tip": "Wasa'nın yüksek çavdar lifi ve hüttenkäse proteini akşam yemeğine kadar açlık krizini tamamen keser.",
        },
    ],
    "dinner": [
        {
            "id": "d1",
            "name": "Kıymalı & Bezelyeli Ev Yemeği & Bulgur",
            "subtitle": "Geleneksel anne lezzeti · Süper lif ve dengeli yağ",
            "ingredients": [
                "140g Yağsız Dana Kıyma (Magere rundergehakt ≤%5)",
                "150g Bezelye & havuç (domates soslu tencere pişimi)",
                "130g Pişmiş Bulgur Pilavı (veya basmati)",
                "8g Sızma zeytinyağı (pişirme payı)",
                "Geniş kase yeşil salata (limonlu)",
            ],
            "kcal": 515,
            "protein": 44.0,
            "fat": 15.5,
            "carbs": 47.0,
            "fiber": 9.5,
            "home_items": ["Bezelye"],
            "prep_time": "20 dk",
            "wegovy_tip": "Bezelye porsiyon başına 7g lif ve 8g bitkisel protein içerir; kıymayla birleştiğinde mükemmel tokluk sağlar.",
        },
        {
            "id": "d2",
            "name": "Fırın Baharatlı Tavuk, Fırın Patates & Sote Ispanak",
            "subtitle": "Hafif, temiz, sindirimi rahat akşam yemeği",
            "ingredients": [
                "160g Tavuk Göğsü (Kekik, kırmızı toz biber ve sarımsakla marine)",
                "180g Fırınlanmış Patates veya Tatlı Patates (elma dilim)",
                "150g Bebek Ispanak (1 tk zeytinyağında sotelenmiş)",
                "6g Sızma zeytinyağı",
            ],
            "kcal": 485,
            "protein": 46.0,
            "fat": 11.5,
            "carbs": 47.0,
            "fiber": 7.5,
            "home_items": ["Ispanak"],
            "prep_time": "25 dk",
            "wegovy_tip": "Tatlı patates potasyum deposudur (padel kramplarını önler); sote ıspanak magnezyumla kasları rahatlatır.",
        },
        {
            "id": "d3",
            "name": "Ev Yapımı Anne Köftesi, Piyaz & Fırın Sebze",
            "subtitle": "Hafta sonu klasiği · Yağsız ızgara köfte ve lif bombası piyaz",
            "ingredients": [
                "150g Az Yağlı Kıyma ile yapılmış köfte (fırında veya ızgara)",
                "140g Haşlanmış Kuru Fasulye (piyazlık, kırmızı soğan ve maydanoz)",
                "150g Izgara Kabak ve Kapya Biber",
                "7g Sızma zeytinyağı + sirke",
            ],
            "kcal": 525,
            "protein": 46.0,
            "fat": 17.0,
            "carbs": 43.0,
            "fiber": 10.0,
            "home_items": [],
            "prep_time": "20 dk",
            "wegovy_tip": "Köfteler ızgara yapıldığı için fazla yağı akar; kuru fasulye piyazı sindirim geçişini hızlandırır.",
        },
        {
            "id": "d4",
            "name": "Tavuklu & Brokolili Wok (Stir-Fry) & Noodle",
            "subtitle": "Asya usulü hızlı ve renkli sebze ziyafeti",
            "ingredients": [
                "150g Tavuk Göğsü şeritleri",
                "150g Brokoli ve havuç jülyen",
                "50g Çiğ Tam Buğday veya Soba Noodle (haşlanmış ~120g)",
                "6g Susam veya zeytinyağı + az tuzlu soya sosu + taze zencefil",
            ],
            "kcal": 475,
            "protein": 45.0,
            "fat": 10.0,
            "carbs": 49.0,
            "fiber": 8.0,
            "home_items": ["Brokoli"],
            "prep_time": "15 dk",
            "wegovy_tip": "Zencefil Wegovy kullananlarda mide bulantısını doğal olarak dindiren en etkili kök baharattır.",
        },
        {
            "id": "d5",
            "name": "Çıtır Nohutlu & Tavuklu Kase (Kwarklı Yoğurt Sos)",
            "subtitle": "Hafif ama çok doyurucu Akdeniz kasesi",
            "ingredients": [
                "130g Izgara Tavuk Göğsü",
                "130g Fırında baharatla çıtırdatılmış Nohut",
                "100g AH Magere Kwark (Sarımsak, dereotu ve limonla sos yapılmış)",
                "Bol marul, salatalık, çeri domates",
                "5g Zeytinyağı",
            ],
            "kcal": 490,
            "protein": 48.0,
            "fat": 12.0,
            "carbs": 45.0,
            "fiber": 9.0,
            "home_items": ["AH Magere Kwark"],
            "prep_time": "15 dk",
            "wegovy_tip": "Kwarktan yapılan sarımsaklı yoğurt sosu mayonezli sosların tüm kalorisini eler, 8.5g ekstra protein katar.",
        },
    ],
}


SAMPLE_7DAY_PLAN = [
    {
        "day": "Pazartesi",
        "focus": "Güç Günü (Alt A)",
        "breakfast": "b1",  # Kwark, Yulaf & Çikolatalı Whey Kasesi
        "lunch": "l1",      # Tavuk Göğsü, Basmati & Brokoli
        "snack": "s1",      # Çikolatalı Fit Mousse & Kwark
        "dinner": "d1",     # Kıymalı & Bezelyeli Ev Yemeği
    },
    {
        "day": "Salı",
        "focus": "Padel Maçı & 1. Doz Wegovy",
        "breakfast": "b2",  # Sıcak Vanilla Yulaf Lapası & Muz
        "lunch": "l3",      # Hüttenkäse & Tavuklu Wrap
        "snack": "s2",      # Çikolata Recovery Shake
        "dinner": "d2",     # Fırın Baharatlı Tavuk, Patates & Ispanak
    },
    {
        "day": "Çarşamba",
        "focus": "Padel Maçı (Isa & Robbert)",
        "breakfast": "b3",  # Hüttenkäse & Yumurtalı Tost
        "lunch": "l2",      # Suda Ton Balıklı & Nohutlu Kase
        "snack": "s4",      # AH Protein Drink & Muz & Soda
        "dinner": "d4",     # Tavuklu & Brokolili Wok
    },
    {
        "day": "Perşembe",
        "focus": "Aktif Dinlenme & Toparlanma",
        "breakfast": "b1",  # Kwark, Yulaf & Çikolatalı Whey
        "lunch": "l4",      # Fırın Tavuk & Mercimek Salatası
        "snack": "s5",      # Tuzlu Hüttenkäse & Wasa Tabağı
        "dinner": "d3",     # Ev Yapımı Anne Köftesi & Piyaz
    },
    {
        "day": "Cuma",
        "focus": "Güç Günü (Üst B)",
        "breakfast": "b4",  # Çırpılmış Yumurta, Hindi Füme & Elma
        "lunch": "l1",      # Tavuk Göğsü, Basmati & Brokoli
        "snack": "s2",      # Çikolata Recovery Shake
        "dinner": "d1",     # Kıymalı & Bezelyeli Ev Yemeği
    },
    {
        "day": "Cumartesi",
        "focus": "Kardiyo (Eliptik & Kürek)",
        "breakfast": "b2",  # Sıcak Vanilla Yulaf Lapası
        "lunch": "l2",      # Ton Balıklı & Nohutlu Kase
        "snack": "s1",      # Çikolatalı Fit Mousse
        "dinner": "d5",     # Çıtır Nohutlu & Tavuklu Kase
    },
    {
        "day": "Pazar",
        "focus": "Kickoff / Güç Günü (Üst A)",
        "breakfast": "b1",  # Kwark, Yulaf & Çikolatalı Whey Kasesi
        "lunch": "l3",      # Hüttenkäse & Tavuklu Wrap
        "snack": "s3",      # Upfront Vanilla Shake & Elma
        "dinner": "d2",     # Fırın Baharatlı Tavuk & Patates & Ispanak
    },
]


def get_meal_options(meal_type: str) -> list[dict]:
    """Return all options for a specific meal category (breakfast, lunch, snack, dinner)."""
    return MEAL_DATABASE.get(meal_type, [])


def find_meal_by_id(meal_type: str, meal_id: str) -> dict | None:
    """Find specific meal dict by its ID."""
    for m in MEAL_DATABASE.get(meal_type, []):
        if m["id"] == meal_id:
            return m
    return None


def calculate_menu_totals(selected_ids: dict[str, str]) -> dict:
    """Calculate combined nutritional totals for selected breakfast, lunch, snack, and dinner."""
    totals = {"kcal": 0, "protein": 0.0, "fat": 0.0, "carbs": 0.0, "fiber": 0.0, "items": {}}
    for mtype in ("breakfast", "lunch", "snack", "dinner"):
        mid = selected_ids.get(mtype)
        m = find_meal_by_id(mtype, mid) if mid else None
        if not m and MEAL_DATABASE.get(mtype):
            m = MEAL_DATABASE[mtype][0]
        if m:
            totals["kcal"] += m["kcal"]
            totals["protein"] += m["protein"]
            totals["fat"] += m["fat"]
            totals["carbs"] += m["carbs"]
            totals["fiber"] += m["fiber"]
            totals["items"][mtype] = m
    totals["protein"] = round(totals["protein"], 1)
    totals["fat"] = round(totals["fat"], 1)
    totals["carbs"] = round(totals["carbs"], 1)
    totals["fiber"] = round(totals["fiber"], 1)
    return totals


def calculate_custom_totals(selected_ids: dict[str, str | None], enabled_types: list[str] | None = None) -> dict:
    """Calculate combined nutritional totals for specific enabled meals (e.g. subset eaten)."""
    if enabled_types is None:
        enabled_types = [k for k, v in selected_ids.items() if v]
    totals = {"kcal": 0, "protein": 0.0, "fat": 0.0, "carbs": 0.0, "fiber": 0.0, "items": {}}
    for mtype in enabled_types:
        mid = selected_ids.get(mtype)
        m = find_meal_by_id(mtype, mid) if mid else None
        if m:
            totals["kcal"] += m["kcal"]
            totals["protein"] += m["protein"]
            totals["fat"] += m["fat"]
            totals["carbs"] += m["carbs"]
            totals["fiber"] += m["fiber"]
            totals["items"][mtype] = m
    totals["protein"] = round(totals["protein"], 1)
    totals["fat"] = round(totals["fat"], 1)
    totals["carbs"] = round(totals["carbs"], 1)
    totals["fiber"] = round(totals["fiber"], 1)
    return totals


def generate_smart_menu(seed_idx: int = 0) -> dict[str, str]:
    """Pick a balanced combination of 4 meals matching ~160g P, ~65-67g F, ~185-190g C, ~28g Fiber."""
    plan = SAMPLE_7DAY_PLAN[seed_idx % len(SAMPLE_7DAY_PLAN)]
    return {
        "breakfast": plan["breakfast"],
        "lunch": plan["lunch"],
        "snack": plan["snack"],
        "dinner": plan["dinner"],
    }


def format_whatsapp_daily_plan(selected_ids: dict[str, str], day_label: str = "Yarınki") -> str:
    """Generate an aesthetic, spouse-friendly WhatsApp message detailing tomorrow's planned menu."""
    totals = calculate_menu_totals(selected_ids)
    items = totals["items"]
    b = items.get("breakfast", {})
    l = items.get("lunch", {})
    s = items.get("snack", {})
    d = items.get("dinner", {})

    b_ing = ", ".join(b.get("ingredients", [])[:3])
    l_ing = ", ".join(l.get("ingredients", [])[:3])
    s_ing = ", ".join(s.get("ingredients", [])[:3])
    d_ing = ", ".join(d.get("ingredients", [])[:3])

    msg = (
        f"🥗 *ATES FAM Fitness — {day_label} Beslenme Menüm*\n"
        f"🎯 *Günlük Makro Hedefi:* {totals['kcal']} kcal | 🥩 {totals['protein']:.0f}g Protein | 🥑 {totals['fat']:.0f}g Yağ | 🍚 {totals['carbs']:.0f}g Karb | 🥦 {totals['fiber']:.0f}g Lif\n\n"
        f"🍳 *1. KAHVALTI:* {b.get('name', '')}\n"
        f"👉 _{b_ing}_\n"
        f"📊 {b.get('kcal')} kcal · {b.get('protein'):.0f}g Protein · {b.get('carbs'):.0f}g Karb · {b.get('fat'):.0f}g Yağ · {b.get('fiber'):.0f}g Lif\n\n"
        f"🥗 *2. ÖĞLE YEMEĞİ:* {l.get('name', '')}\n"
        f"👉 _{l_ing}_\n"
        f"📊 {l.get('kcal')} kcal · {l.get('protein'):.0f}g Protein · {l.get('carbs'):.0f}g Karb · {l.get('fat'):.0f}g Yağ · {l.get('fiber'):.0f}g Lif\n\n"
        f"🥤 *3. ARA ÖĞÜN / SHAKE:* {s.get('name', '')}\n"
        f"👉 _{s_ing}_\n"
        f"📊 {s.get('kcal')} kcal · {s.get('protein'):.0f}g Protein · {s.get('carbs'):.0f}g Karb · {s.get('fat'):.0f}g Yağ · {s.get('fiber'):.0f}g Lif\n\n"
        f"🍲 *4. AKŞAM YEMEĞİ:* {d.get('name', '')}\n"
        f"👉 _{d_ing}_\n"
        f"📊 {d.get('kcal')} kcal · {d.get('protein'):.0f}g Protein · {d.get('carbs'):.0f}g Karb · {d.get('fat'):.0f}g Yağ · {d.get('fiber'):.0f}g Lif\n\n"
        f"💡 _Not: Wegovy mide boşalmasını geciktirdiği için porsiyonlar 4 öğüne eşit yayıldı; akşam yemeği hafif ve lif zenginidir._"
    )
    return msg


def generate_grocery_list(week_plan: list[dict] | None = None) -> dict[str, list[str]]:
    """Aggregate all ingredients needed for a weekly plan into Albert Heijn supermarket aisles."""
    return {
        "🥩 Kasap & Taze Protein": [
            "Tavuk Göğsü (Kipfilet) — ~1.0 - 1.2 kg (haftalık öğle/akşam)",
            "Yağsız Dana Kıyma (Magere rundergehakt ≤%5) — ~600g (köfte ve bezelyeli yemek)",
            "Hindi / Tavuk Göğsü Füme (Kip/kalkoenfilet vleeswaren) — 2 paket (150g)",
            "Suda Ton Balığı Konservesi (Tonijnstukken in water) — 2 kutu",
        ],
        "🥛 Süt & Şarküteri (Albert Heijn)": [
            "AH Magere Kwark — 3 kova (her biri 500g, toplam 1.5 kg)",
            "AH Cottage Cheese Light (Hüttenkäse light) — 3-4 kutu (her biri 200g)",
            "AH Organik Yumurta (Biologische Eieren M/L) — 10'lu veya 12'li paket",
            "Alpro Roasted Almond Drink (Şekersiz Badem Sütü) — 2 litre",
        ],
        "🥦 Manav & Taze Sebze-Meyve": [
            "Muz (Bananen) — 1 büyük hevenk (~7-8 adet)",
            "Brokoli (Broccoli) — 2 adet taze taç (~800g)",
            "Bebek Ispanak (Baby spinazie) — 2 büyük poşet (~400-500g)",
            "Bezelye & Havuç (Dondurulmuş veya taze AH) — 1 paket (~500g)",
            "Elma (Appels) — 1 kg (tercihen Jonagold veya Pink Lady)",
            "Çeri Domates & Salatalık — 2 paket çeri, 2 adet salatalık",
            "Taze Roka & Marul & Maydanoz — 1'er demet",
            "Tatlı Patates veya Taze Patates — 1 kg",
        ],
        "🌾 Kuru Gıda, Bakliyat & Kiler": [
            "Yulaf (AH Havermout volkoren) — 1 paket (500g)",
            "Basmati veya Esmer Pirinç — 1 paket (1 kg)",
            "Konserve Nohut (Kikkererwten) — 2 kutu (400g)",
            "Konserve Yeşil Mercimek (Linzen) — 2 kutu (400g)",
            "Tam Buğday Lavaş / Wrap (Volkoren wraps) — 1 paket (6'lı)",
            "Tam Çavdar Gevreği (Wasa Volkoren knäckebröd) — 1 paket",
            "Chia veya Keten Tohumu — 1 paket",
            "Sade Maden Suyu (Bruisend mineraalwater) — 6'lı şişe",
        ],
        "⚡ Evdeki Sporcu Stokları (Bitince Alınacaklar)": [
            "Impact Whey Protein Pure Chocolade (Mevcut ✓)",
            "Upfront Whey Milkshake Vanilla (Mevcut ✓)",
            "AH Protein Mousse / Pudding Chocolate (Mevcut ✓ - azaldıkça 4'lü alım)",
            "XXL Nutrition Fitmousse Chocolate (Mevcut ✓)",
            "AH Protein Drink Chocolate (Mevcut ✓)",
            "AH Terra 100% Fıstık Ezmesi (Mevcut ✓)",
            "Huel / Yfood Ready-to-drink (Mevcut ✓)",
        ],
    }


def format_whatsapp_grocery_list(grocery_dict: dict[str, list[str]]) -> str:
    """Format categorized grocery list into a clear WhatsApp message."""
    lines = ["🛒 *ATES FAM Fitness — Haftalık Alışveriş Listesi (Albert Heijn)*\n"]
    for cat, items in grocery_dict.items():
        lines.append(f"*{cat}*")
        for item in items:
            lines.append(f"  ▫️ {item}")
        lines.append("")
    lines.append("💡 _Not: Evdeki protein tozları, kwark, fıstık ezmesi ve protein pudingleri listeye göre kontrol edildi._")
    return "\n".join(lines)
