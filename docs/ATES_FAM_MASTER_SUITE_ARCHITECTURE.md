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
│   └── flight_radar/                    # ✈️ Flight Radar (Canlı Uçuş Takip)
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

## 🔒 3. Veri İzolasyonu ve State Güvenliği (Kritik Kurallar)

Birleştirme sürecinde projelerin birbirini bozmaması için şu **3 mimari kural tavizsiz uygulanır**:

### Kural 1: Session State İsim Uzayı (Namespacing)
Streamlit'in global `st.session_state` sözlüğü ortak paylaşıldığı için değişken çakışmalarını önlemek adına her uygulama kendi önekini kullanır:
* Fitness değişkenleri: `st.session_state["fitness_targets"]`, `st.session_state["fitness_page"]`
* Budget değişkenleri: `st.session_state["budget_transactions"]`, `st.session_state["budget_month"]`
* Library değişkenleri: `st.session_state["library_books"]`
* Flight Radar değişkenleri: `st.session_state["radar_aircraft"]`

### Kural 2: Bağımsız Veritabanı ve Çift Katmanlı Kalıcılık
* Her uygulamanın SQLite veritabanı kendi klasöründe (`apps/fitness/data/fitness.db`, `apps/budget/data/budget.db`) izole kalır.
* GitHub bağımsız `data` branch'i senkronizasyonu devam eder.

### Kural 3: Bellek (RAM) Optimizasyonu
* Streamlit Cloud ücretsiz katmanında 1 GB RAM bulunur.
* Kullanıcı menüden hangi uygulamayı seçerse yalnızca o uygulama belleğe çağrılır (`lazy import`). Hafif SQLite mimarisi sayesinde 4 uygulama toplamda ~300 MB RAM tüketir (1 GB sınırının çok altındadır).

---

## 🔐 4. Rol Tabanlı Yetkilendirme & Aile Profil Mimarisi (RBAC)

Kullanıcının kritik gereksinimi: **"Oğlumun Budget ve Fitness sayfalarına erişmesini istemiyorum. Kütüphaneye ve Flight Radar'a erişsin, ancak Kütüphane içinde yönetici işlemleri için şifre koruması olsun."**

Bu gereksinim, Netflix tarzı **Aile Profil Seçimi (Profile Switcher) + İki Kademeli Yetkilendirme (RBAC)** ile çözülür:

### 1. Erişim Matrisi (Authorization Matrix)

| Profil / Kullanıcı | Giriş Yöntemi | 🏋️ Fitness | 💰 Budget | 📚 Atlas Library | ✈️ Flight Radar |
| :--- | :---: | :---: | :---: | :---: | :---: |
| 👑 **Anıl (Admin / Baba)** | 4 Haneli PIN (`****`) | ✅ Tam Erişim | ✅ Tam Erişim | ✅ Yönetici Modu (Kitap Ekle/Sil/Düzenle) | ✅ Tam Erişim |
| 🧒 **Atlas (Junior / Çocuk)** | Şifresiz / Tek Tık | ❌ **Görünmez & Engelli** | ❌ **Görünmez & Engelli** | ✅ Okuyucu Modu (Kitap İnceleme & Arama) | ✅ Tam Erişim |
| 👩 **Eş (Anne / Opsiyonel)** | 4 Haneli PIN | ✅ Menü & Sağlık | ✅ Bütçe İnceleme | ✅ Okuyucu Modu | ✅ Tam Erişim |

### 2. Router Düzeyinde Güvenlik ve URL Manipülasyon Engeli
Atlas profili aktifken:
* Menü çubuğunda `[ 💰 Bütçe ]` ve `[ 🏋️ Fitness ]` butonları arayüzde **kesinlikle render edilmez**.
* Atlas tarayıcı adres satırına elle `?app=budget` veya `?app=fitness` yazsa bile yönlendirici bunu anında yakalar:
  ```python
  ALLOWED_APPS = {
      "atlas": ["library", "flight_radar"],
      "anil": ["fitness", "budget", "library", "flight_radar"],
  }

  current_profile = st.session_state.get("active_profile", "atlas")
  if target_app not in ALLOWED_APPS[current_profile]:
      st.error("⛔ Bu bölüme erişim yetkiniz bulunmamaktadır.")
      st.stop()
  ```

### 3. Kütüphane İçi Yönetici Kilidi (Library Admin Gate)
* Atlas kütüphane uygulamasını açtığında şu anki gibi kitapları listeleyebilir, arayabilir ve okuma durumunu görebilir.
* Ancak kütüphane içindeki **"Kitap Sil", "Yeni Kitap Ekle" veya "Katalog Ayarları"** sekmesine/butonuna tıklandığında:
  * Sistem şık bir modal/popover açar: `"🔒 Bu işlem için Yönetici PIN kodu gereklidir"`.
  * Yalnızca Anıl'ın bildiği 4 haneli PIN girildiğinde işlem onaylanır.

### 4. PIN Hashleme & Secrets Güvenliği
* PIN kodları kod içine yazılmaz; `.streamlit/secrets.toml` dosyasında SHA-256 hash olarak saklanır:
  ```toml
  [auth]
  admin_pin_hash = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3" # Örn: '1234'
  ```

---

## 🎨 5. Kullanıcı Deneyimi ve Yönlendirici (Router) Tasarımı

```python
# app.py (Örnek Master Hub Mantığı)
import streamlit as st
from core import auth, layout, theme

st.set_page_config(page_title="ATES FAM Suite", page_icon="🏛️", layout="wide")
theme.apply_theme()

# 1. Profil ve Kimlik Doğrulama
profile = auth.render_profile_bar() # "anil" veya "atlas"

# 2. Yetkiye Göre Dinamik Menü Çubuğu
# Atlas ise sadece [📚 Kütüphane] [✈️ Flight Radar] gösterilir
# Anıl ise [🏋️ Fitness] [💰 Bütçe] [📚 Kütüphane] [✈️ Flight Radar] gösterilir
selected_app = layout.render_app_switcher(profile)

# 3. Güvenli Modüler Yönlendirme
if selected_app == "fitness" and auth.can_access(profile, "fitness"):
    from apps.fitness import main as fitness_app
    fitness_app.run()
elif selected_app == "budget" and auth.can_access(profile, "budget"):
    from apps.budget import main as budget_app
    budget_app.run()
elif selected_app == "library":
    from apps.library import main as library_app
    is_admin = (profile == "anil")
    library_app.run(is_admin=is_admin)
elif selected_app == "flight_radar":
    from apps.flight_radar import main as radar_app
    radar_app.run()
```

---

## 🚀 6. Adım Adım Geçiş Yol Haritası (Implementation Plan)

Argon kotası açıldığında takip edilecek 6 aşamalı uygulama planı:

1. **Aşama 1 — Depo Kurulumu (Scaffolding):**
   * GitHub üzerinde `Blixembosch/ates-fam-suite` adında yeni bir **Private** depo oluşturulur.
   * Temel dizin yapısı (`core/`, `apps/`, `.streamlit/`) açılır.
2. **Aşama 2 — Kodların Taşınması:**
   * `ATES_FAM_Fitness`, `ATES_FAM_Budget`, `Atlas Library` ve `Flight Radar` kodları `apps/` altına modüler olarak kopyalanır.
3. **Aşama 3 — Rol Tabanlı Yetkilendirme & Profil Motoru (`core/auth.py`):**
   * Anıl (Admin PIN) ve Atlas (Junior) profilleri kodlanır.
   * Menüden Bütçe ve Fitness'ın filtrelenmesi ve Kütüphane içi yönetici kilidi kurulur.
4. **Aşama 4 — Secrets ve Bağımlılıkların Konsolidasyonu:**
   * 4 projenin `requirements.txt` dosyaları tek bir temiz dosyada birleştirilir.
   * `secrets.toml` dosyasına admin PIN hash'i, GitHub token'ları ve iCal URL'leri eklenir.
5. **Aşama 5 — Test Güvencesi:**
   * Yetki sızdırmazlık testleri (`test_rbac_auth.py`) ve hub testleri koşulur; 100% yeşil test güvencesi sağlanır.
6. **Aşama 6 — Streamlit Cloud Dağıtımı:**
   * `share.streamlit.io` üzerinden `Blixembosch/ates-fam-suite` Private olarak dağıtılır.

---

## 🤖 7. Argon / Antigravity İçin Hazır İstek Komutu (Prompt Template)

Limitleriniz açıldığında aşağıdaki blok metni doğrudan kopyalayarak asistana verebilirsiniz:

```text
Merhaba! Depomuzdaki "docs/ATES_FAM_MASTER_SUITE_ARCHITECTURE.md" dosyasında tüm detayları tanımlanmış olan "ATES FAM Master Suite" mimarisine geçmek istiyorum. 

Öncelikli Yetkilendirme Kuralları:
1. Elimdeki 4 projeyi (Fitness, Budget, Atlas Library ve Flight Radar) tek bir private Streamlit uygulaması altında birleştirmek.
2. Rol tabanlı yetkilendirme (RBAC) kurmak:
   - "Atlas" profili seçildiğinde Bütçe ve Fitness kesinlikle görünmeyecek ve URL manipülasyonuna karşı engellenecek. Atlas yalnızca Kütüphane ve Flight Radar'a erişebilecek.
   - Kütüphane içinde kitap ekleme/silme işlemleri Admin PIN kodu gerektirecek.
   - "Anıl" profili 4 haneli PIN ile açılarak tüm 4 uygulamaya ve Kütüphane yönetici moduna tam yetkiyle erişecek.
3. apps/fitness, apps/budget, apps/library ve apps/flight_radar şeklinde modüler monorepo kurmak.
4. Çift katmanlı SQLite ve GitHub Data Branch kalıcılığını izole korumak.
5. Şartnamedeki 6 aşamalı geçiş yol haritasını sırasıyla ve testleri kırılmadan hayata geçirmeni rica ediyorum.
```
