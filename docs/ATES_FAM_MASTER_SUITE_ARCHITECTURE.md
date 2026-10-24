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
│   └── atlas_flight/                    # ✈️ Atlas Flight (Canlı Uçuş & Radar Takip)
│       ├── __init__.py
│       ├── main.py
│       └── lib/
└── tests/                               # Suite Testleri
    ├── test_hub_router.py               # Uygulama geçiş ve yönlendirme testleri
    ├── test_rbac_auth.py                # Rol tabanlı yetki ve profil testleri
    ├── test_state_isolation.py          # State çakışması izolasyon testleri
    └── ...
```

---

## 🔒 3. Kod, Fonksiyon ve Veri İzolasyon Mimarisi (Kritik Kurallar)

Kullanıcının en kritik sorusu: **"Repoda bunları ayrı branch'ler altında mı tutacağız? Dataların ve fonksiyonların kesinlikle birbiriyle karışmaması gerekiyor."**

### A. Kod ve Fonksiyon İzolasyonu (Neden Ayrı Branch Değil, Ayrı Paket?)
* **Streamlit Cloud Kısıtı:** Streamlit Cloud bir uygulamayı **tek bir git branch'inden** (`main`) çalıştırır; aynı anda 4 farklı branch'ten kod çekip tek ekranda birleştiremez.
* **Fonksiyonların Karışmaması Güvencesi (Python Package Isolation):** Kodlar `main` branch'inde yaşar ancak **tamamen izole Python paketleri (`apps/*`)** içine hapsedilir:
  * Fitness fonksiyonları: `apps.fitness.lib.*`
  * Budget fonksiyonları: `apps.budget.lib.*`
  * Atlas Library fonksiyonları: `apps.library.lib.*`
  * Atlas Flight fonksiyonları: `apps.atlas_flight.lib.*`
* Python'ın modül sistemi gereği, bir paketin içindeki fonksiyon diğer paketi **kesinlikle göremez, üzerine yazamaz veya etkileyemez**. Birbirinden tamamen habersiz, bağımsız 4 ada gibi çalışırlar.
* *(İsteğe Bağlı Git Submodule Opsiyonu):* Eğer kaynak kodların da GitHub'da 4 ayrı repoda kalması istenirse; 4 bağımsız özel repo tutulur ve `ates-fam-suite` bu 4 depoyu **Git Submodule** olarak `apps/` altına çeker. Böylece kod depoları da %100 ayrı kalır.

### B. Veritabanı ve Veri İzolasyonu (Yerel SQLite)
Her uygulamanın veritabanı dosyası ve SQLite bağlantı havuzu tamamen ayrıdır:
* `apps/fitness/data/fitness.db`
* `apps/budget/data/budget.db`
* `apps/library/data/library.db`
* `apps/atlas_flight/data/atlas_flight.db`
Fitness uygulaması hiçbir zaman `budget.db` bağlantısını açmaz; tablolar, sütunlar ve kayıtlar %100 izoledir.

### C. GitHub Bulut Kalıcılığı: 4 Bağımsız Veri Branch'i (Data Branches)
Verilerin bulut yedeğinde birbirine karışmaması için **GitHub'da 4 ayrı veri branch'i** kullanılır:
* `data-fitness` branch'i $\rightarrow$ Yalnızca `fitness.sql` dökümünü tutar.
* `data-budget` branch'i $\rightarrow$ Yalnızca `budget.sql` dökümünü tutar.
* `data-library` branch'i $\rightarrow$ Yalnızca `library.sql` dökümünü tutar.
* `data-flight` branch'i $\rightarrow$ Yalnızca `atlas_flight.sql` dökümünü tutar.

Uygulamalar GitHub REST API ile veri kaydederken yalnızca kendi veri branch'ine commit atar. Bütçe verisinin Fitness branch'ine gitmesi matematiksel olarak imkansızdır.

### D. Session State İsim Uzayı (Namespacing)
Streamlit'in global `st.session_state` sözlüğü ortak paylaşıldığı için değişken çakışmalarını önlemek adına her uygulama kendi önekini kullanır:
* Fitness değişkenleri: `st.session_state["fitness_targets"]`, `st.session_state["fitness_page"]`
* Budget değişkenleri: `st.session_state["budget_transactions"]`, `st.session_state["budget_month"]`
* Library değişkenleri: `st.session_state["library_books"]`
* Flight değişkenleri: `st.session_state["flight_radar_aircraft"]`

### E. Bellek (RAM) Optimizasyonu
* Streamlit Cloud ücretsiz katmanında 1 GB RAM bulunur.
* Kullanıcı menüden hangi uygulamayı seçerse yalnızca o uygulama belleğe çağrılır (`lazy import`). Hafif SQLite mimarisi sayesinde 4 uygulama toplamda ~300 MB RAM tüketir (1 GB sınırının çok altındadır).

---

## 🔐 4. Rol Tabanlı Yetkilendirme & Aile Profil Mimarisi (RBAC)

Kullanıcının tanımladığı aile yapısı ve yetki matrisi:
* **Anıl (Admin):** Tüm 4 projeye ve tüm alt sayfalara tam yönetici erişimi.
* **Berna (Eş / Anne):** Library ve Flight'a tam erişim; Fitness tarafında **"Menü & Sağlık"** (4 Öğünlü Menü, Alışveriş Listesi, Takviye Takibi) odaklı arayüze erişim; Budget erişimi.
* **Atlas (Junior):** Yalnızca Library (Okuyucu modu) ve Flight (Canlı takip). Fitness ve Budget kesinlikle görünmez ve engelli.
* **Alina (Junior — Gelecek Üye):** Henüz doğmadı ancak profil altyapısı şimdiden hazır! Atlas ile aynı kurallara tabi (Library okuyucu + Flight tam erişim; Fitness ve Budget engelli).

### 1. Aile Erişim Yetki Matrisi (Family Authorization Matrix)

| Profil / Aile Üyesi | Giriş Yöntemi | 🏋️ Fitness Kapsamı | 💰 Budget | 📚 Library | ✈️ Flight |
| :--- | :---: | :---: | :---: | :---: | :---: |
| 👑 **Anıl (Admin / Baba)** | 4 Haneli PIN (`****`) | ✅ **Tam Erişim** (Tüm Sayfalar) | ✅ **Tam Erişim** | ✅ **Yönetici Modu** (Ekle/Sil/Düzenle) | ✅ **Tam Erişim** |
| 👩 **Berna (Eş / Anne)** | 4 Haneli PIN (`****`) | 🥗 **Menü & Sağlık** (Beslenme & Takviye) | ✅ **Tam Erişim** | ✅ **Tam Erişim** (Okuma & Düzenleme) | ✅ **Tam Erişim** |
| 🧒 **Atlas (Junior / Çocuk)** | Şifresiz / Tek Tık | ❌ **Görünmez & Engelli** | ❌ **Görünmez & Engelli** | 📖 **Okuyucu Modu** (Arama & İnceleme) | ✅ **Tam Erişim** |
| 👶 **Alina (Junior / Bebek)** | Şifresiz / Tek Tık | ❌ **Görünmez & Engelli** | ❌ **Görünmez & Engelli** | 📖 **Okuyucu Modu** (Arama & İnceleme) | ✅ **Tam Erişim** |

### 2. Router Düzeyinde Güvenlik ve URL Manipülasyon Engeli
Atlas veya Alina profili aktifken:
* Menü çubuğunda `[ 💰 Bütçe ]` ve `[ 🏋️ Fitness ]` butonları arayüzde **kesinlikle render edilmez**.
* Çocuklar tarayıcı adres satırına elle `?app=budget` veya `?app=fitness` yazsa bile yönlendirici bunu anında yakalar:
  ```python
  ALLOWED_APPS = {
      "atlas": ["library", "flight"],
      "alina": ["library", "flight"],
      "berna": ["fitness", "budget", "library", "flight"],
      "anil": ["fitness", "budget", "library", "flight"],
  }

  current_profile = st.session_state.get("active_profile", "atlas")
  if target_app not in ALLOWED_APPS[current_profile]:
      st.error("⛔ Bu bölüme erişim yetkiniz bulunmamaktadır.")
      st.stop()
  ```

### 3. Berna İçin Fitness "Menü & Sağlık" Granüler Kapsamı
* Berna profiliyle Fitness açıldığında, antrenman setleri (`setlog`), RPE ve dambıl ağırlık sayfaları arayüzden gizlenir.
* Doğrudan aile beslenme ve sağlık koordinasyonunu sağlayan **"Menü & Sağlık Merkezi"** (4 Öğünlü Akıllı Menü, Günün Beslenmesini Kaydet, 7 Günlük Menü & Alışveriş Listesi ve Takviye Takibi) gösterilir:
  ```python
  if profile == "berna":
      # Yalnızca Menü, Beslenme ve Sağlık sekmelerini render et
      fitness_app.run_nutrition_and_health_mode()
  else:
      fitness_app.run_full_mode()
  ```

### 4. Kütüphane İçi Yönetici Kilidi (Library Admin Gate)
* Atlas veya Alina kütüphaneyi açtığında kitapları inceler, arama yapar ve okuma listelerine bakar.
* İçeride **"Kitap Sil"**, **"Yeni Kitap Ekle"** veya **"Katalog Ayarları"** butonlarına tıklandığında:
  * Sistem şık bir modal açar: `"🔒 Bu işlem için Ebeveyn PIN kodu gereklidir."`
  * Yalnızca Anıl veya Berna'nın PIN'i girildiğinde işlem gerçekleşir.

---

## 🎨 5. Kullanıcı Deneyimi ve Yönlendirici (Router) Tasarımı

```python
# app.py (Örnek Master Hub Mantığı)
import streamlit as st
from core import auth, layout, theme

st.set_page_config(page_title="ATES FAM Suite", page_icon="🏛️", layout="wide")
theme.apply_theme()

# 1. Netflix Tarzı Aile Profil Seçimi (Anıl, Berna, Atlas, Alina)
profile = auth.render_profile_selector()

# 2. Yetkiye Göre Dinamik Menü Çubuğu
# Atlas / Alina -> [📚 Kütüphane] [✈️ Flight]
# Berna -> [🥗 Menü & Sağlık] [💰 Bütçe] [📚 Kütüphane] [✈️ Flight]
# Anıl -> [🏋️ Fitness] [💰 Bütçe] [📚 Kütüphane] [✈️ Flight]
selected_app = layout.render_app_switcher(profile)

# 3. Güvenli Modüler Yönlendirme
if selected_app == "fitness" and auth.can_access(profile, "fitness"):
    from apps.fitness import main as fitness_app
    if profile == "berna":
        fitness_app.run_nutrition_health_mode()
    else:
        fitness_app.run_full_mode()
elif selected_app == "budget" and auth.can_access(profile, "budget"):
    from apps.budget import main as budget_app
    budget_app.run()
elif selected_app == "library":
    from apps.library import main as library_app
    is_admin = (profile in ["anil", "berna"])
    library_app.run(is_admin=is_admin)
elif selected_app == "flight":
    from apps.flight import main as flight_app
    flight_app.run()
```

---

## 🚀 6. Adım Adım Geçiş Yol Haritası (Implementation Plan)

Argon kotası açıldığında takip edilecek 6 aşamalı uygulama planı:

1. **Aşama 1 — Depo Kurulumu (Scaffolding):**
   * GitHub üzerinde `Blixembosch/ates-fam-suite` adında yeni bir **Private** depo oluşturulur.
   * Temel dizin yapısı (`core/`, `apps/`, `.streamlit/`) açılır.
2. **Aşama 2 — Kodların Taşınması:**
   * `ATES_FAM_Fitness`, `ATES_FAM_Budget`, `Atlas Library` ve `Flight` kodları `apps/` altına modüler olarak kopyalanır (`apps/fitness`, `apps/budget`, `apps/library`, `apps/flight`).
3. **Aşama 3 — Rol Tabanlı Yetkilendirme & Profil Motoru (`core/auth.py`):**
   * Anıl (Admin PIN), Berna (Menü & Sağlık PIN), Atlas (Junior) ve Alina (Junior) profilleri kodlanır.
   * Çocuklar için Bütçe ve Fitness filtreleme ile Kütüphane içi ebeveyn kilidi kurulur.
4. **Aşama 4 — Secrets ve Bağımlılıkların Konsolidasyonu:**
   * 4 projenin `requirements.txt` dosyaları tek bir temiz dosyada birleştirilir.
   * `secrets.toml` dosyasına PIN hash'leri, GitHub token'ları ve iCal URL'leri eklenir.
5. **Aşama 5 — Test Güvencesi:**
   * Yetki sızdırmazlık testleri (`test_rbac_auth.py`) ve hub testleri koşulur; 100% yeşil test güvencesi sağlanır.
6. **Aşama 6 — Streamlit Cloud Dağıtımı:**
   * `share.streamlit.io` üzerinden `Blixembosch/ates-fam-suite` Private olarak dağıtılır.

---

## 🤖 7. Argon / Antigravity İçin Hazır İstek Komutu (Prompt Template)

Limitleriniz açıldığında aşağıdaki blok metni doğrudan kopyalayarak asistana verebilirsiniz:

```text
Merhaba! Depomuzdaki "docs/ATES_FAM_MASTER_SUITE_ARCHITECTURE.md" dosyasında tüm detayları tanımlanmış olan "ATES FAM Master Suite" mimarisine geçmek istiyorum. 

Öncelikli Aile Yetkilendirme Kuralları:
1. Elimdeki 4 projeyi (Fitness, Budget, Library ve Flight) tek bir private Streamlit uygulaması altında birleştirmek.
2. Netflix tarzı 4 aile profili ve Rol Tabanlı Yetkilendirme (RBAC) kurmak:
   - "Anıl (Admin)": 4 haneli PIN ile tüm 4 uygulamaya ve tüm modüllere tam yetkili.
   - "Berna": 4 haneli PIN ile Library ve Flight'a tam erişim; Fitness'ta yalnızca "Menü & Sağlık" modülüne erişim; Budget erişimi.
   - "Atlas" ve "Alina" (Çocuklar): Şifresiz tek tık giriş. Sadece Library (Okuyucu) ve Flight (Canlı takip) görünür olacak. Budget ve Fitness kesinlikle görünmeyecek ve URL manipülasyonuna karşı engellenecek.
   - Library içinde kitap silme/ekleme işlemleri ebeveyn PIN kodu gerektirecek.
3. apps/fitness, apps/budget, apps/library ve apps/flight şeklinde modüler monorepo kurmak.
4. Çift katmanlı SQLite ve GitHub bağımsız Veri Branch'leri (data-fitness, data-budget, data-library, data-flight) ile veri kalıcılığını %100 izole korumak.
5. Şartnamedeki 6 aşamalı geçiş yol haritasını sırasıyla ve testleri kırılmadan hayata geçirmeni rica ediyorum.
```
