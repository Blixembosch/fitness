# 🏛️ ATES FAM Master Suite — Tek Çatı / Portal Mimarisi ve Geçiş Şartnamesi

> **Doküman Türü:** Sistem Mimarisi & Uygulama Şartnamesi (Argon / Antigravity Girdi Şablonu)  
> **Hedef:** Streamlit Community Cloud ücretsiz planında (1 Private App limitiyle) 4 bağımsız projeyi tek bir özel çatı altında birleştirmek.  
> **Maliyet:** 0 TL (Ömür boyu sıfır abonelik ücreti)  
> **Gizlilik:** %100 Private (Tüm kaynak kodları ve veriler gizli GitHub deposunda)  
> **Kullanım Amacı:** Argon / Antigravity kotası açıldığında bu dosya doğrudan girdi olarak verilerek adım adım uygulanabilir.

---

## 🎯 1. Yönetici Özeti ve Problem Tanımı

### Mevcut Durum (Current State)
* Kullanıcının 4 ayrı Streamlit projesi bulunmaktadır:
  1. 🏋️ **ATES FAM Fitness** (Mevcut repo: `Blixembosch/fitness`)
  2. 💰 **ATES FAM Budget** (Mevcut repo: `Blixembosch/budget`)
  3. 📚 **Atlas Library** (Mevcut repo: `Blixembosch/atlas-library`)
  4. 📁 **4. Özel Proje**
* Streamlit Community Cloud ücretsiz katmanı **yalnızca 1 adet Private App** barındırmaya izin verir; diğer uygulamaların Public (kod ve verisi dünyaya açık) olması zorunludur.

### Hedef Durum (Target State)
* Tek bir özel GitHub deposu (`Blixembosch/ates-fam-suite`) altında 4 projeyi modüler olarak birleştiren **Master Suite (Aile Portalı)** kurulur.
* Streamlit Cloud'a bu **tek private repo** dağıtılır (`1 Private App Slot`).
* 4 projenin tamamı tek bir güvenli, mobil uyumlu URL (`https://ates-fam-suite.streamlit.app`) üzerinden, %100 gizli ve sıfır maliyetle çalışır.

---

## 🏗️ 2. Mimari Yapı ve Dizin Hiyerarşisi

Sistem, projelerin kodlarını birbirine karıştırmadan, modüler ve bağımsız paketler halinde barındıran **Modüler Monorepo** yapısıyla kurgulanır:

```text
ates-fam-suite/                          # Ana Özel Depo (GitHub: Blixembosch/ates-fam-suite)
├── app.py                               # Master Suite Yönlendirici (Hub / Router)
├── requirements.txt                     # Ortak ve birleştirilmiş bağımlılıklar
├── README.md                            # Suite düzeyinde teknik dokümantasyon
├── ROADMAP.md                           # Suite yol haritası
├── .streamlit/
│   ├── config.toml                      # Ortak karanlık tema ve WCAG AA/AAA CSS
│   └── secrets.toml                     # Birleştirilmiş gizli anahtarlar
├── core/                                # Paylaşılan ortak çekirdek modüller
│   ├── __init__.py
│   ├── auth.py                          # İsteğe bağlı Aile PIN / Parola kilidi
│   ├── layout.py                        # Üst menü, uygulama geçiş çubuğu (App Switcher)
│   └── theme.py                         # Ortak CSS token'ları (--bg, --fg, --accent vb.)
├── apps/                                # Bağımsız Uygulama Modülleri
│   ├── fitness/                         # 🏋️ ATES FAM Fitness
│   │   ├── __init__.py
│   │   ├── main.py                      # Fitness giriş noktası
│   │   ├── lib/                         # fitness lib modülleri (workout, store, meal_planner vb.)
│   │   └── data/                        # fitness.db
│   ├── budget/                          # 💰 ATES FAM Budget
│   │   ├── __init__.py
│   │   ├── main.py                      # Budget giriş noktası
│   │   ├── lib/                         # budget lib modülleri
│   │   └── data/                        # budget.db
│   ├── library/                         # 📚 Atlas Library
│   │   ├── __init__.py
│   │   ├── main.py                      # Library giriş noktası
│   │   ├── lib/
│   │   └── data/                        # library.db
│   └── project4/                        # 📁 4. Proje
│       ├── __init__.py
│       ├── main.py
│       └── lib/
└── tests/                               # Suite Testleri
    ├── test_hub_router.py               # Uygulama geçiş ve yönlendirme testleri
    ├── test_state_isolation.py          # State çakışması izolasyon testleri
    └── ...
```

---

## 🔒 3. Veri İzolasyonu ve State Güvenliği (Kritik Kurallar)

Birleştirme sürecinde projelerin birbirini bozmaması için şu **3 mimari kural tavizsiz uygulanır**:

### Kural 1: Session State İsim Uzayı (Namespacing)
Streamlit'in global `st.session_state` sözlüğü ortak paylaşıldığı için değişken çakışmalarını önlemek adına her uygulama kendi önekini kullanır:
* Fitness değişkenleri: `st.session_state["fitness_targets"]`, `st.session_state["fitness_page"]`
* Budget değişkenleri: `st.session_state["budget_transactions"]`, `st.session_state["budget_month"]`
* Library değişkenleri: `st.session_state["library_books"]`

### Kural 2: Bağımsız Veritabanı ve Çift Katmanlı Kalıcılık
* Her uygulamanın SQLite veritabanı kendi klasöründe (`apps/fitness/data/fitness.db`, `apps/budget/data/budget.db`) izole kalır.
* GitHub bağımsız `data` branch'i senkronizasyonu (`Blixembosch/fitness:data`, `Blixembosch/budget:data` veya tek bir `ates-fam-suite:data` branch'i) devam eder.

### Kural 3: Bellek (RAM) Optimizasyonu
* Streamlit Cloud ücretsiz katmanında 1 GB RAM bulunur.
* Uygulamalar aynı anda bellekte ağır yük tutmaz; kullanıcı menüden **Fitness** seçtiğinde yalnızca Fitness modülleri çalışır, **Budget** seçtiğinde Budget modülleri aktifleşir. Hafif SQLite mimarisi sayesinde 4 uygulama toplamda ~300 MB RAM tüketir (1 GB sınırının çok altındadır).

---

## 🎨 4. Kullanıcı Deneyimi ve Yönlendirici (Router) Tasarımı

`app.py` ana giriş noktası aşağıdaki şık, mobil uyumlu ve modern gezinme çubuğunu içerir:

```python
# app.py (Örnek Master Hub Mantığı)
import streamlit as st
from core import layout, theme

st.set_page_config(page_title="ATES FAM Suite", page_icon="🏛️", layout="wide")
theme.apply_theme()

selected_app = layout.render_app_switcher()

if selected_app == "fitness":
    from apps.fitness import main as fitness_app
    fitness_app.run()
elif selected_app == "budget":
    from apps.budget import main as budget_app
    budget_app.run()
elif selected_app == "library":
    from apps.library import main as library_app
    library_app.run()
elif selected_app == "project4":
    from apps.project4 import main as p4_app
    p4_app.run()
```

### Görsel Arayüz (App Switcher)
Ekranın en üstünde veya sol menüde tek tıkla geçiş sağlayan ergonomik butonlar yer alır:
`[ 🏋️ Fitness ]` &nbsp; `[ 💰 Bütçe ]` &nbsp; `[ 📚 Atlas Kütüphane ]` &nbsp; `[ 📁 4. Proje ]`

---

## 🚀 5. Adım Adım Geçiş Yol Haritası (Implementation Plan)

Argon kotası açıldığında takip edilecek 6 aşamalı uygulama planı:

1. **Aşama 1 — Depo Kurulumu (Scaffolding):**
   * GitHub üzerinde `Blixembosch/ates-fam-suite` adında yeni bir **Private** depo oluşturulur.
   * Temel dizin yapısı (`core/`, `apps/`, `.streamlit/`) açılır.
2. **Aşama 2 — Kodların Taşınması:**
   * `ATES_FAM_Fitness` deposundaki tüm kodlar (`app.py` -> `main.py`, `lib/` -> `apps/fitness/lib/`) taşınır.
   * `ATES_FAM_Budget` ve `Atlas Library` depoları aynı şekilde `apps/` altına kopyalanır.
3. **Aşama 3 — Yönlendirici ve State İzolasyonu:**
   * `core/layout.py` ve `app.py` Master Router kodlanır.
   * State çakışmaları temizlenir.
4. **Aşama 4 — Secrets ve Bağımlılıkların Konsolidasyonu:**
   * 4 projenin `requirements.txt` dosyaları tek bir temiz dosyada birleştirilir (versiyon çakışmaları çözülür).
   * Streamlit `secrets.toml` dosyasına tüm token ve URL'ler eklenir.
5. **Aşama 5 — Test Güvencesi:**
   * Hub yönlendiricisi ve uygulama içi işlevler için testler koşulur; 100% yeşil test güvencesi sağlanır.
6. **Aşama 6 — Streamlit Cloud Dağıtımı:**
   * `share.streamlit.io` üzerinden `Blixembosch/ates-fam-suite` Private olarak dağıtılır.
   * Eski public Streamlit linkleri kapatılır.

---

## 🤖 6. Argon / Antigravity İçin Hazır İstek Komutu (Prompt Template)

Limitleriniz açıldığında aşağıdaki blok metni doğrudan kopyalayarak asistana verebilirsiniz:

```text
Merhaba! "docs/ATES_FAM_MASTER_SUITE_ARCHITECTURE.md" dosyasında tüm detayları tanımlanmış olan "ATES FAM Master Suite" projesine geçmek istiyorum. 

Hedefim:
1. Elimdeki 4 projeyi (ATES FAM Fitness, ATES FAM Budget, Atlas Library ve 4. Proje) bu mimari şartnameye uygun olarak tek bir private Streamlit uygulaması altında birleştirmek.
2. apps/fitness, apps/budget, apps/library ve apps/project4 şeklinde modüler monorepo yapısı kurmak.
3. app.py içinde şık bir App Switcher yönlendiricisi oluşturmak.
4. Çift katmanlı SQLite ve GitHub Data Branch kalıcılığını her uygulama için izole korumak.
5. Dokümandaki 6 aşamalı geçiş yol haritasını sırasıyla ve testleri kırılmadan hayata geçirmeni rica ediyorum.
```
