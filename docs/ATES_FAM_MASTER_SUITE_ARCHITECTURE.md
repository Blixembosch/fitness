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
* **Berna (Eş / Anne):** Library ve Flight'a tam erişim; Fitness tarafında **"Menü & Sağlık"** (4 Öğünlü Menü, Alışveriş Listesi, Takviye Takibi) odaklı arayüze erişim; Budget tarafında ise hassas/ayrıntılı hesaplar gizlenerek yalnızca **"Financial Overview"** (Finansal Genel Bakış) ve **"Atlas'ın Anı Defteri"** (Atlas' Memory Book) modüllerine erişim.
* **Atlas (Junior):** Yalnızca Library (Okuyucu modu) ve Flight (Canlı takip). Fitness ve Budget kesinlikle görünmez ve engelli.
* **Alina (Junior — Gelecek Üye):** Henüz doğmadı ancak profil altyapısı şimdiden hazır! Atlas ile aynı kurallara tabi (Library okuyucu + Flight tam erişim; Fitness ve Budget engelli).

### 1. Aile Erişim Yetki Matrisi (Family Authorization Matrix)

| Profil / Aile Üyesi | Giriş Yöntemi | 🏋️ Fitness Kapsamı | 💰 Budget Kapsamı | 📚 Library & Yaş Filtresi | ✈️ Flight |
| :--- | :---: | :---: | :---: | :---: | :---: |
| 👑 **Anıl (Admin / Baba)** | Ayrı Baba PIN (`****`) | ✅ **Tam Erişim** (Tüm Sayfalar) | ✅ **Tam Erişim** (Tüm Hesaplar, İşlemler, Ayarlar) | ✅ **Yönetici Modu** (Tüm Yaşlar, Ekle/Sil/Düzenle) | ✅ **Tam Erişim** |
| 👩 **Berna (Eş / Anne)** | Ayrı Anne PIN (`****`) | 🥗 **Menü & Sağlık** (Beslenme & Takviye) | 📊 **Kısıtlı Erişim** (Yalnızca Financial Overview & Atlas'ın Anı Defteri) | ✅ **Ebeveyn Modu** (Tüm Yaşlar, Okuma & Düzenleme) | ✅ **Tam Erişim** |
| 🧒 **Atlas (Junior / Çocuk)** | Ayrı Atlas PIN (`****`) | ❌ **Görünmez & Engelli** | ❌ **Görünmez & Engelli** | 📖 **Atlas Yaş Grubu** (Kişisel Okuma Sayacı & Kitapları) | ✅ **Tam Erişim** |
| 👶 **Alina (Junior / Bebek)** | Ayrı Alina PIN (`****`) | ❌ **Görünmez & Engelli** | ❌ **Görünmez & Engelli** | 📖 **Alina Bebek/Okul Öncesi** (Kişisel Okuma Sayacı) | ✅ **Tam Erişim** |

> [!IMPORTANT]
> **4 Ayrı Bağımsız PIN:** Dört profilin de şifresi birbirinden tamamen bağımsızdır. Atlas kendi PIN'i ile girdiğinde Berna veya Anıl'ın profiline geçemez. Alina için de şimdiden bağımsız PIN alanı rezerve edilmiştir.

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

  current_profile = st.session_state.get("active_profile")
  if target_app not in ALLOWED_APPS[current_profile]:
      st.error("⛔ Bu bölüme erişim yetkiniz bulunmamaktadır.")
      st.stop()
  ```

### 3. Kütüphane İçinde Yaşa Göre Kitap Filtreleme & Çocuk Bazlı İstatistik Sayımı
Kütüphane veritabanında her kitap için `age_group` etiketi (`"atlas"`, `"alina"`, `"aile"`) ve okuma kayıtlarında `reader_id` tutulur:
* **Atlas Profili Açıldığında:**
  * Kitap kataloğu otomatik filtrelenir; yalnızca Atlas'ın yaşına uygun macera, bilim ve hikaye kitapları listelenir.
  * İstatistik paneli yalnızca **Atlas'ın okuduğu kitapları, sayfa sayısını ve haftalık okuma hedefini** sayar (`atlas_stats`).
* **Alina Profili Açıldığında:**
  * Kitap kataloğu otomatik filtrelenir; yalnızca 0–3 yaş bebek, masal ve görsel gelişim kitapları listelenir.
  * İstatistik paneli yalnızca **Alina'ya okunan masalları ve Alina'nın kitap sayacını** sayar (`alina_stats`).
* **Ebeveyn Modu (Anıl & Berna):**
  * Tek tıkla `Tümü`, `Atlas` ve `Alina` sekmeleri arasında geçiş yapabilir; her iki çocuğun kütüphane gelişimini ayrı ayrı grafiklerle izleyebilir.
  * Yeni kitap eklerken kitabın hangi çocuğun rafına ait olduğu (`Atlas`, `Alina` veya `Ortak`) seçilir.
  * Kitap silme veya katalog ayarları için Anne/Baba PIN onayı zorunludur.

### 4. Berna İçin Fitness "Menü & Sağlık" Granüler Kapsamı
* Berna profiliyle Fitness açıldığında, antrenman setleri (`setlog`), RPE ve dambıl ağırlık sayfaları arayüzden gizlenir.
* Doğrudan aile beslenme ve sağlık koordinasyonunu sağlayan **"Menü & Sağlık Merkezi"** (4 Öğünlü Akıllı Menü, Günün Beslenmesini Kaydet, 7 Günlük Menü & Alışveriş Listesi ve Takviye Takibi) gösterilir:
  ```python
  if profile == "berna":
      fitness_app.run_nutrition_and_health_mode()
  else:
      fitness_app.run_full_mode()
  ```

### 5. Berna İçin Budget (Bütçe) Kapsamı: Yalnızca "Financial Overview" & "Atlas'ın Anı Defteri"
* Berna profiliyle Bütçe açıldığında, hassas muhasebe/işlem girişleri, hesap detayları ve bütçe yapılandırma ayarları gizlenir.
* Yalnızca aile için gerekli olan iki temel modül arayüze sunulur:
  1. **Financial Overview (Finansal Genel Bakış):** Aylık gelir/gider özeti, tasarruf oranı ve genel aile bütçesi dashboard'u.
  2. **Atlas'ın Anı Defteri (Atlas' Memory Book):** Atlas'ın anı, hatıra ve kilometre taşlarını içeren özel bölüm.
  ```python
  if profile == "berna":
      # Yalnızca Genel Bakış ve Atlas'ın Anı Defteri sekmeleri aktif
      budget_app.run_overview_and_memories_mode()
  else:
      # Tüm finansal detaylar, işlem düzenleme ve hesap yönetimi
      budget_app.run_full_mode()
  ```

### 6. PIN Hashleme & Secrets Güvenliği
Tüm PIN kodları SHA-256 hash formatında `.streamlit/secrets.toml` dosyasında saklanır:
```toml
[auth.pins]
anil_hash  = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3" # Baba PIN
berna_hash = "b59c67bf196a4758191e42f76670cebaeae11200baeae928f734f024f3078ab2" # Anne PIN
atlas_hash = "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92" # Atlas Çocuk PIN
alina_hash = "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a" # Alina Bebek PIN
```

---

## 🎨 5. Kullanıcı Deneyimi ve Yönlendirici (Router) Tasarımı

```python
# app.py (Örnek Master Hub Mantığı)
import streamlit as st
from core import auth, layout, theme

st.set_page_config(page_title="ATES FAM Suite", page_icon="🏛️", layout="wide")
theme.apply_theme()

# 1. Netflix Tarzı Aile Profil Seçimi & Bireysel PIN Girişi
# [👑 Anıl]  [👩 Berna]  [🧒 Atlas]  [👶 Alina]
profile = auth.render_profile_modal()

# 2. Yetkiye Göre Dinamik Menü Çubuğu
# Atlas / Alina -> [📚 Kütüphanem] [✈️ Flight]
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
    if profile == "berna":
        # Berna için yalnızca Financial Overview ve Atlas'ın Anı Defteri modülleri
        budget_app.run_overview_and_memories_mode()
    else:
        budget_app.run_full_mode()
elif selected_app == "library":
    from apps.library import main as library_app
    # Kütüphane profil bazlı kitapları ve kişisel okuma sayaçlarını açar
    library_app.run(profile=profile)
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
3. **Aşama 3 — 4 Profilli Rol Tabanlı Yetkilendirme & Profil Motoru (`core/auth.py`):**
   * Anıl, Berna, Atlas ve Alina için 4 ayrı PIN doğrulama fonksiyonu kodlanır.
   * Atlas ve Alina için Bütçe ve Fitness filtreleme ile Kütüphane içi yaş filtreleme/kişisel sayaç motoru kurulur.
4. **Aşama 4 — Secrets ve Bağımlılıkların Konsolidasyonu:**
   * 4 projenin `requirements.txt` dosyaları tek bir temiz dosyada birleştirilir.
   * `secrets.toml` dosyasına 4 profilin PIN hash'leri, GitHub token'ları ve iCal URL'leri eklenir.
5. **Aşama 5 — Test Güvencesi:**
   * Yetki sızdırmazlık testleri (`test_rbac_auth.py`), profil yaş filtre testleri ve hub testleri koşulur; 100% yeşil test güvencesi sağlanır.
6. **Aşama 6 — Streamlit Cloud Dağıtımı:**
   * `share.streamlit.io` üzerinden `Blixembosch/ates-fam-suite` Private olarak dağıtılır.

---

## 🤖 7. Argon / Antigravity İçin Hazır İstek Komutu (Prompt Template)

Limitleriniz açıldığında aşağıdaki blok metni doğrudan kopyalayarak asistana verebilirsiniz:

```text
Merhaba! Depomuzdaki "docs/ATES_FAM_MASTER_SUITE_ARCHITECTURE.md" dosyasında tüm detayları tanımlanmış olan "ATES FAM Master Suite" mimarisine geçmek istiyorum. 

Öncelikli Aile Yetkilendirme ve Kütüphane Kuralları:
1. Elimdeki 4 projeyi (Fitness, Budget, Library ve Flight) tek bir private Streamlit uygulaması altında birleştirmek.
2. Netflix tarzı 4 aile profili ve Ayrı PIN'li Rol Tabanlı Yetkilendirme (RBAC) kurmak:
   - "Anıl": Kendi PIN'i ile tüm 4 uygulamaya ve tüm modüllere tam yönetici yetkili.
   - "Berna": Kendi PIN'i ile Library ve Flight'a tam erişim; Fitness'ta yalnızca "Menü & Sağlık" (beslenme/takviye) modülüne erişim; Budget tarafında ise yalnızca "Financial Overview" ve "Atlas'ın Anı Defteri" modüllerine erişim.
   - "Atlas": Kendi çocuk PIN'i ile giriş. Sadece Library (Atlas yaş grubuna ait kitaplar & kişisel okuma sayaçları) ve Flight (Canlı radar) görünür olacak. Budget ve Fitness kesinlikle görünmeyecek ve URL manipülasyonuna karşı engellenecek.
   - "Alina": Kendi çocuk PIN'i ile giriş. Sadece Library (Alina 0-3 yaş bebek kitapları & kişisel okuma sayaçları) ve Flight (Canlı radar) görünür olacak. Budget ve Fitness engelli olacak.
   - Library içinde ebeveyn yönetici işlemleri için Anne/Baba PIN'i gerekecek.
3. apps/fitness, apps/budget, apps/library ve apps/flight şeklinde modüler monorepo kurmak.
4. Çift katmanlı SQLite ve GitHub bağımsız Veri Branch'leri (data-fitness, data-budget, data-library, data-flight) ile veri kalıcılığını %100 izole korumak.
5. Şartnamedeki 6 aşamalı geçiş yol haritasını sırasıyla ve testleri kırılmadan hayata geçirmeni rica ediyorum.
```
