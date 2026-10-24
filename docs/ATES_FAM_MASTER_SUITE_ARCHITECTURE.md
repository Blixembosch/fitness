# 🏛️ ATES FAM Master Suite — Tek Çatı / Portal Mimarisi ve Geçiş Şartnamesi

> **Doküman Türü:** Sistem Mimarisi & Uygulama Şartnamesi (Argon / Antigravity Girdi Şablonu)  
> **Hedef:** Streamlit Community Cloud ücretsiz planında (1 Private App limitiyle) 5 bağımsız modülü tek bir özel çatı altında birleştirmek.  
> **Maliyet:** 0 TL (Ömür boyu sıfır abonelik ücreti)  
> **Gizlilik:** %100 Private (Tüm kaynak kodları ve veriler gizli GitHub deposunda)  
> **Taşınabilirlik:** Bu şartname bağımsız bir ana plandır; ister ATES FAM Fitness, ister ATES FAM Budget altında saklanabilir veya doğrudan yeni `ates-fam-suite` deposuna girdi olarak verilebilir.

---

## 🎯 1. Yönetici Özeti ve Problem Tanımı

### Mevcut Durum (Current State)
* Ailenin kullandığı ve planlanan 5 bağımsız modülü bulunmaktadır:
  1. 🏋️ **Fitness** (Mevcut repo: `Blixembosch/fitness`)
  2. 💰 **Budget** (Mevcut repo: `Blixembosch/budget` — Saf finans, muhasebe & bütçe)
  3. 📚 **Library** (Mevcut repo: `Blixembosch/atlas-library` — Kitap kataloğu & okuma hedefleri)
  4. ✈️ **Flight** (Canlı Uçuş & Radar Takip)
  5. 📔 **Memories** (Aile Anı Defteri & Kilometre Taşları — Bütçeden tamamen ayrılmış bağımsız hatıra albümü)
* Streamlit Community Cloud ücretsiz katmanı **yalnızca 1 adet Private App** barındırmaya izin verir; diğer uygulamaların Public (kod ve verisi dünyaya açık) olması zorunludur.

### Hedef Durum (Target State)
* Tek bir özel GitHub deposu (`Blixembosch/ates-fam-suite`) altında 5 modülü birleştiren **Master Suite (Aile Portalı)** kurulur.
* Streamlit Cloud'a bu **tek private repo** dağıtılır (`1 Private App Slot`).
* 5 modülün tamamı tek bir güvenli, mobil uyumlu URL (`https://ates-fam-suite.streamlit.app`) üzerinden, %100 gizli ve sıfır maliyetle çalışır.

---

## 🏗️ 2. Mimari Yapı ve Dizin Hiyerarşisi

Sistem, projelerin kodlarını ve dokümantasyonlarını birbirine karıştırmadan, modüler ve bağımsız paketler halinde barındıran **Modüler Monorepo** yapısıyla kurgulanır. 

> [!TIP]
> **Ayırt Edilebilir Dokümantasyon (`README_<PROJE>.md` & `ROADMAP_<PROJE>.md`):**  
> IDE sekmelerinde birden fazla `README.md` açıkken hangisinin hangi projeye ait olduğunu karıştırmamak için her modül kendi ismini taşıyan net, ayırt edilebilir dokümanlara sahiptir. Ana dizindeki `README.md` ise yalnızca Suite Portal genel mimarisini açıklar.

```text
ates-fam-suite/                          # Ana Özel Depo (GitHub: Blixembosch/ates-fam-suite)
├── app.py                               # Master Suite Yönlendirici (Hub / Router)
├── requirements.txt                     # Ortak ve birleştirilmiş bağımlılıklar
├── README.md                            # Suite düzeyinde teknik dokümantasyon & portal mimarisi
├── ROADMAP.md                           # Suite entegrasyon yol haritası
├── .streamlit/
│   ├── config.toml                      # Ortak karanlık tema ve WCAG AA/AAA CSS
│   └── secrets.toml                     # Birleştirilmiş gizli anahtarlar & 4 ayrı PIN hash'i
├── core/                                # Paylaşılan ortak çekirdek modüller
│   ├── __init__.py
│   ├── auth.py                          # 4 Profilli Netflix tarzı RBAC ve PIN kilidi
│   ├── layout.py                        # Üst menü, dinamik yetkili uygulama geçiş çubuğu (App Switcher)
│   └── theme.py                         # Ortak CSS token'ları (--bg, --fg, --accent vb.)
├── apps/                                # Bağımsız Uygulama Modülleri
│   ├── fitness/                         # 🏋️ Fitness
│   │   ├── README_FITNESS.md            # Fitness klinik mimarisi, GLP-1/MPS ve test matrisi
│   │   ├── ROADMAP_FITNESS.md           # Fitness gelişim aşamaları ve bekçi mekanizmaları
│   │   ├── __init__.py
│   │   ├── main.py                      # Fitness giriş noktası
│   │   ├── lib/                         # workout, store, meal_planner vb.
│   │   └── data/                        # fitness.db
│   ├── budget/                          # 💰 Budget (Saf Finans & Muhasebe)
│   │   ├── README_BUDGET.md             # Bütçe çift taraflı kayıt & finansal analiz mimarisi
│   │   ├── ROADMAP_BUDGET.md            # Bütçe yol haritası
│   │   ├── __init__.py
│   │   ├── main.py                      # Budget giriş noktası
│   │   ├── lib/                         # budget lib modülleri
│   │   └── data/                        # budget.db
│   ├── library/                         # 📚 Library
│   │   ├── README_LIBRARY.md            # Kütüphane kataloglama, yaş filtreleme & sayaç mimarisi
│   │   ├── ROADMAP_LIBRARY.md           # Kütüphane yol haritası & çocuk okuma hedefleri
│   │   ├── __init__.py
│   │   ├── main.py                      # Library giriş noktası
│   │   ├── lib/                         # library lib modülleri
│   │   └── data/                        # library.db
│   ├── flight/                          # ✈️ Flight (Canlı Uçuş & Radar Takip)
│   │   ├── README_FLIGHT.md             # Canlı radar, ADS-B/OpenSky API ve harita mimarisi
│   │   ├── ROADMAP_FLIGHT.md            # Flight yol haritası
│   │   ├── __init__.py
│   │   ├── main.py                      # Flight giriş noktası
│   │   ├── lib/                         # flight lib modülleri
│   │   └── data/                        # flight.db
│   └── memories/                        # 📔 Memories (Aile Anı Defteri & Kilometre Taşları)
│       ├── README_MEMORIES.md           # Anı defteri mimarisi, medya yönetimi ve çocuk okuyucu modu
│       ├── ROADMAP_MEMORIES.md          # Anı defteri yol haritası (Atlas & Alina albümleri)
│       ├── __init__.py
│       ├── main.py                      # Memories giriş noktası
│       ├── lib/                         # memories lib modülleri (timeline, gallery, tags)
│       └── data/                        # memories.db
└── tests/                               # Suite Testleri
    ├── test_hub_router.py               # Uygulama geçiş ve yönlendirme testleri
    ├── test_rbac_auth.py                # Rol tabanlı yetki, PIN ve profil sızdırmazlık testleri
    ├── test_state_isolation.py          # State çakışması izolasyon testleri
    └── ...
```

---

## 🔒 3. Kod, Fonksiyon ve Veri İzolasyon Mimarisi (Kritik Kurallar)

Kullanıcının en kritik sorusu: **"Repoda bunları ayrı branch'ler altında mı tutacağız? Dataların ve fonksiyonların kesinlikle birbiriyle karışmaması gerekiyor."**

### A. Kod ve Fonksiyon İzolasyonu (Neden Ayrı Branch Değil, Ayrı Paket?)
* **Streamlit Cloud Kısıtı:** Streamlit Cloud bir uygulamayı **tek bir git branch'inden** (`main`) çalıştırır; aynı anda birden fazla branch'ten kod çekip tek ekranda birleştiremez.
* **Fonksiyonların Karışmaması Güvencesi (Python Package Isolation):** Kodlar `main` branch'inde yaşar ancak **tamamen izole Python paketleri (`apps/*`)** içine hapsedilir:
  * Fitness fonksiyonları: `apps.fitness.lib.*`
  * Budget fonksiyonları: `apps.budget.lib.*`
  * Library fonksiyonları: `apps.library.lib.*`
  * Flight fonksiyonları: `apps.flight.lib.*`
  * Memories fonksiyonları: `apps.memories.lib.*`
* Python'ın modül sistemi gereği, bir paketin içindeki fonksiyon diğer paketi **kesinlikle göremez, üzerine yazamaz veya etkileyemez**. Birbirinden tamamen habersiz, bağımsız 5 ada gibi çalışırlar.
* *(İsteğe Bağlı Git Submodule Opsiyonu):* Eğer kaynak kodların da GitHub'da ayrı depolarda kalması istenirse; bağımsız özel depolar tutulur ve `ates-fam-suite` bu depoları **Git Submodule** olarak `apps/` altına çeker. Böylece kod depoları da %100 ayrı kalır.

### B. Veritabanı ve Veri İzolasyonu (Yerel SQLite)
Her uygulamanın veritabanı dosyası ve SQLite bağlantı havuzu tamamen ayrıdır:
* `apps/fitness/data/fitness.db`
* `apps/budget/data/budget.db`
* `apps/library/data/library.db`
* `apps/flight/data/flight.db`
* `apps/memories/data/memories.db`
Fitness veya Memories uygulaması hiçbir zaman `budget.db` bağlantısını açmaz; tablolar, sütunlar ve kayıtlar %100 izoledir.

### C. GitHub Bulut Kalıcılığı: 5 Bağımsız Veri Branch'i (Data Branches)
Verilerin bulut yedeğinde birbirine karışmaması için **GitHub'da 5 ayrı veri branch'i** kullanılır:
* `data-fitness` branch'i $\rightarrow$ Yalnızca `fitness.sql` dökümünü tutar.
* `data-budget` branch'i $\rightarrow$ Yalnızca `budget.sql` dökümünü tutar.
* `data-library` branch'i $\rightarrow$ Yalnızca `library.sql` dökümünü tutar.
* `data-flight` branch'i $\rightarrow$ Yalnızca `flight.sql` dökümünü tutar.
* `data-memories` branch'i $\rightarrow$ Yalnızca `memories.sql` dökümünü tutar.

Uygulamalar GitHub REST API ile veri kaydederken yalnızca kendi veri branch'ine commit atar. Bütçe verisinin Memories veya Fitness branch'ine gitmesi matematiksel olarak imkansızdır.

### D. Session State İsim Uzayı (Namespacing)
Streamlit'in global `st.session_state` sözlüğü ortak paylaşıldığı için değişken çakışmalarını önlemek adına her uygulama kendi önekini kullanır:
* Fitness değişkenleri: `st.session_state["fitness_targets"]`, `st.session_state["fitness_page"]`
* Budget değişkenleri: `st.session_state["budget_transactions"]`, `st.session_state["budget_month"]`
* Library değişkenleri: `st.session_state["library_books"]`
* Flight değişkenleri: `st.session_state["flight_radar_aircraft"]`
* Memories değişkenleri: `st.session_state["memories_album"]`, `st.session_state["memories_filter_kid"]`

### E. Bellek (RAM) Optimizasyonu
* Streamlit Cloud ücretsiz katmanında 1 GB RAM bulunur.
* Kullanıcı menüden hangi uygulamayı seçerse yalnızca o uygulama belleğe çağrılır (`lazy import`). Hafif SQLite mimarisi sayesinde 5 modül toplamda ~320 MB RAM tüketir (1 GB sınırının çok altındadır).

---

## 🔐 4. Rol Tabanlı Yetkilendirme & Aile Profil Mimarisi (RBAC)

Kullanıcının tanımladığı aile yapısı ve yetki matrisi:
* **Anıl (Admin):** Tüm 5 modüle ve tüm alt sayfalara tam yönetici erişimi.
* **Berna (Eş / Anne):** Library, Flight ve Memories modüllerine tam erişim; Fitness tarafında **"Menü & Sağlık"** (4 Öğünlü Menü, Alışveriş Listesi, Takviye Takibi) odaklı arayüze erişim; Budget tarafında ise yalnızca **"Financial Overview"** (Finansal Genel Bakış) modülüne erişim.
* **Atlas (Junior):** Library (Okuyucu modu), Flight (Canlı takip) ve **Memories modülü altında Atlas'ın Anılarına yalnızca okuyucu (salt okunur / read-only)** olarak erişim. Fitness ve saf finansal Budget modülleri kesinlikle görünmez ve kilitlidir.
* **Alina (Junior — Gelecek Üye):** Henüz doğmadı ancak altyapısı şimdiden hazır! Library (0-3 yaş masalları), Flight (Canlı radar) ve Memories altında Alina'nın Bebeklik Günlüğü'ne salt okunur erişim. Fitness ve Budget kilitlidir.

### 1. Aile Erişim Yetki Matrisi (Family Authorization Matrix)

| Profil / Aile Üyesi | Giriş Yöntemi | 🏋️ Fitness Kapsamı | 💰 Budget Kapsamı | 📚 Library & Yaş Filtresi | ✈️ Flight | 📔 Memories (Anı Defteri) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 👑 **Anıl (Admin / Baba)** | Ayrı Baba PIN (`****`) | ✅ **Tam Erişim** (Tüm Sayfalar) | ✅ **Tam Erişim** (Tüm Hesaplar & İşlemler) | ✅ **Yönetici Modu** (Tüm Yaşlar) | ✅ **Tam Erişim** | ✏️ **Tam Yönetici** (Tüm Aile Albümleri, Ekle/Sil/Düzenle) |
| 👩 **Berna (Eş / Anne)** | Ayrı Anne PIN (`****`) | 🥗 **Menü & Sağlık** (Beslenme & Takviye) | 📊 **Financial Overview** (Yalnızca Genel Bütçe Özeti) | ✅ **Ebeveyn Modu** (Tüm Yaşlar) | ✅ **Tam Erişim** | ✏️ **Tam Yönetici** (Tüm Aile Albümleri, Ekle/Sil/Düzenle) |
| 🧒 **Atlas (Junior / Çocuk)** | Ayrı Atlas PIN (`****`) | ❌ **Görünmez & Engelli** | ❌ **Görünmez & Kilitli** | 📖 **Atlas Yaş Grubu** (Kişisel Kitap & Sayaç) | ✅ **Tam Erişim** | 👁️ **Salt Okunur (Read-Only)** (Yalnızca Atlas Anıları) |
| 👶 **Alina (Junior / Bebek)** | Ayrı Alina PIN (`****`) | ❌ **Görünmez & Engelli** | ❌ **Görünmez & Kilitli** | 📖 **Alina Bebek/Masal** (Kişisel Kitap & Sayaç) | ✅ **Tam Erişim** | 👁️ **Salt Okunur (Read-Only)** (Yalnızca Alina Bebek Günlüğü) |

> [!IMPORTANT]
> **4 Ayrı Bağımsız PIN:** Dört profilin de şifresi birbirinden tamamen bağımsızdır. Atlas kendi PIN'i ile girdiğinde Berna veya Anıl'ın profiline geçemez. Alina için de şimdiden bağımsız PIN alanı rezerve edilmiştir.

### 2. Router Düzeyinde Güvenlik ve URL Manipülasyon Engeli
Atlas veya Alina profili aktifken:
* Menü çubuğunda Fitness ve Bütçe butonları arayüzde **kesinlikle render edilmez**.
* Çocuklar tarayıcı adres satırına elle `?app=fitness` veya `?app=budget` yazsa bile yönlendirici bunu anında yakalar:
  ```python
  ALLOWED_APPS = {
      "atlas": ["library", "flight", "memories"],
      "alina": ["library", "flight", "memories"],
      "berna": ["fitness", "budget", "library", "flight", "memories"],
      "anil": ["fitness", "budget", "library", "flight", "memories"],
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

### 5. Berna İçin Budget (Bütçe) Kapsamı: Yalnızca "Financial Overview"
* Berna profiliyle Bütçe açıldığında, hassas muhasebe/işlem girişleri, hesap detayları ve bütçe yapılandırma ayarları gizlenir.
* Yalnızca aile için gerekli olan temel modül arayüze sunulur:
  * **Financial Overview (Finansal Genel Bakış):** Aylık gelir/gider özeti, tasarruf oranı ve genel aile bütçesi dashboard'u.
  ```python
  if profile == "berna":
      # Yalnızca Genel Finansal Bakış paneli
      budget_app.run_overview_mode()
  else:
      # Tüm finansal detaylar, işlem düzenleme ve hesap yönetimi
      budget_app.run_full_mode()
  ```

### 6. Bağımsız Memories (Aile Anı Defteri) & Çocuk Salt Okunur (Read-Only) Mimarisi
* Memories modülü bütçeden tamamen bağımsız olarak `apps/memories` altında çalışır ve kendi `memories.db` veritabanını kullanır.
* **Ebeveyn Modu (Anıl & Berna):**
  * Hem Atlas'ın hem de Alina'nın anı albümlerine tam erişim.
  * Yeni anı ekleme, fotoğraf yükleme, tarih/kilometre taşı belirleme ve düzenleme yetkisi.
* **Atlas Profili:**
  * Yalnızca kendi anı defterini (`atlas_album`) dijital bir hatıra albümü gibi **salt okunur (read-only)** olarak görüntüler.
  * Ekleme, düzenleme ve silme butonları arayüzden gizlenir.
* **Alina Profili:**
  * Yalnızca kendi bebeklik günlüğünü ve masal hatıralarını (`alina_album`) **salt okunur (read-only)** olarak görüntüler.
  ```python
  # apps/memories/main.py içindeki profil yetkilendirmesi
  def run(profile: str):
      if profile in ["anil", "berna"]:
          render_parent_editor_mode()
      elif profile == "atlas":
          render_kid_album(album_id="atlas", readonly=True)
      elif profile == "alina":
          render_kid_album(album_id="alina", readonly=True)
  ```

### 7. PIN Hashleme & Secrets Güvenliği
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
# Atlas -> [📚 Kütüphanem] [✈️ Flight] [📔 Anı Defterim]
# Alina -> [📚 Masallarım] [✈️ Flight] [📔 Bebeklik Günlüğüm]
# Berna -> [🥗 Menü & Sağlık] [💰 Bütçe (Özet)] [📚 Kütüphane] [✈️ Flight] [📔 Anı Defteri]
# Anıl -> [🏋️ Fitness] [💰 Bütçe] [📚 Kütüphane] [✈️ Flight] [📔 Anı Defteri]
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
        budget_app.run_overview_mode()
    else:
        budget_app.run_full_mode()
elif selected_app == "library":
    from apps.library import main as library_app
    library_app.run(profile=profile)
elif selected_app == "flight":
    from apps.flight import main as flight_app
    flight_app.run()
elif selected_app == "memories" and auth.can_access(profile, "memories"):
    from apps.memories import main as memories_app
    memories_app.run(profile=profile)
```

---

## 🛡️ 6. Kalite Güvencesi, Bekçi Mekanizmaları (Guards) ve Sıfır Riskli Geçiş Protokolü

Yeni monorepo yapısının her aşamasında ve kademeli geçişin her adımında **ATES FAM Kalite Güvencesi ve Bekçi Mekanizması** zorunlu bir güvenlik kapısı (gatekeeper) olarak çalışır.

### A. 4 Katmanlı Bekçi Mekanizması (Guards)
1. **Birim & Fonksiyonel Testler:** Her bir modül (`fitness`, `budget`, `library`, `flight`, `memories`) taşınırken kendi birim testleri ve Streamlit AppTest kontrolleri `tests/` altına aktarılır.
2. **Kapsam Bekçisi (Scope Guard):** `ALLOWED_APPS`, profil PIN doğrulamaları, veritabanı şemaları ve çekirdek fonksiyonların eksiksizliği her commit öncesinde otomatik doğrulanır.
3. **Doküman Bekçisi (Document Guard):** Ana `README.md` ve her modülün kendi `README_<PROJE>.md` / `ROADMAP_<PROJE>.md` dosyalarındaki test sayıları, mimari açıklamalar ve yetki tabloları kodla %100 senkronize olmak zorundadır.
4. **Progression-to-Regression:** Yeni eklenen her modül ve profil testi `run_suite_tests.py` tarafından anında keşfedilir ve kalıcı regresyon testine dönüşür.

### B. Mevcut Repoların Korunması & Sıfır Risk Kuralı (Zero-Risk Parallel Run)
> [!CAUTION]
> **Kırmızı Çizgi (Non-Negotiable Rule) — Erken Silme Kesinlikle Yasaktır:**  
> 1. Yeni `ates-fam-suite` monoreposu Streamlit Cloud üzerinde yayına alınıp, 5 modülün tamamının çalıştığı canlıda kanıtlanmadan ve **kullanıcının (Anıl Ateş) açık yazılı onayı alınmadan**, mevcut hiçbir public repo (`fitness`, `budget`, `atlas-library` vb.) **kesinlikle silinemez, kapatılamaz, içeriği boşaltılamaz veya arşivlenemez!**
> 2. **Paralel Çalışma (Parallel Run):** Yeni portal kurulurken mevcut uygulamalar kesintisiz olarak çalışmaya devam eder. Aile üyeleri yeni portalı deneyip %100 onay verene kadar mevcut repolar güvence altındadır.

---

## 🚀 7. Adım Adım Geçiş Yol Haritası (Implementation Plan)

Argon kotası açıldığında takip edilecek 7 aşamalı kademeli geçiş planı:

1. **Aşama 1 — Depo Kurulumu ve Bekçi Altyapısı (Scaffolding & Guards):**
   * GitHub üzerinde `Blixembosch/ates-fam-suite` adında yeni bir **Private** depo oluşturulur.
   * Temel dizin yapısı (`core/`, `apps/`, `.streamlit/`, `tests/`) ve `run_suite_tests.py` bekçi koşucusu kurulur.
2. **Aşama 2 — Kademeli Modül Taşınması & Test Doğrulaması:**
   * 5 bağımsız modül (**Fitness**, **Budget**, **Library**, **Flight** ve **Memories**) sırasıyla `apps/` altına taşınır.
   * Her modül taşındığında kendi `README_<PROJE>.md`, `ROADMAP_<PROJE>.md` ve test dosyaları eklenir; o modülün testleri %100 yeşil olmadan bir sonraki modüle geçilmez.
3. **Aşama 3 — 4 Profilli Rol Tabanlı Yetkilendirme & Profil Motoru (`core/auth.py`):**
   * Anıl, Berna, Atlas ve Alina için 4 ayrı PIN doğrulama fonksiyonu kodlanır.
   * Çocuk profilleri için Bütçe ve Fitness kesin engelleme; Kütüphane için yaş filtreleme; Memories için albüm bazlı salt okunur (read-only) kuralı kurulur.
   * `test_rbac_auth.py` ile yetki sızdırmazlık testleri koşulur.
4. **Aşama 4 — Secrets ve Bağımlılıkların Konsolidasyonu:**
   * 5 projenin `requirements.txt` dosyaları tek bir temiz dosyada birleştirilir.
   * `secrets.toml` dosyasına 4 profilin PIN hash'leri, GitHub token'ları ve iCal URL'leri eklenir.
5. **Aşama 5 — Suite Düzeyinde Regresyon ve Bekçi Onayı (Suite Guard Gate):**
   * `run_suite_tests.py` çalıştırılır. Tüm birim testler, RBAC sızdırmazlık testleri, Scope Guard ve Document Guard kontrolleri koşulur; **%100 yeşil sonuç** alınır.
6. **Aşama 6 — Streamlit Cloud Dağıtımı (Paralel Canlı Yayın):**
   * `share.streamlit.io` üzerinden `Blixembosch/ates-fam-suite` Private olarak dağıtılır.
   * Mevcut uygulamalar dokunulmadan arka planda çalışmaya devam eder.
7. **Aşama 7 — Kullanıcı Kabul Testi (UAT) & Açık Onay:**
   * Kullanıcı tüm 5 modülü (Anıl, Berna, Atlas, Alina profilleriyle) mobil ve masaüstünde test eder.
   * **Kullanıcı yazılı "Eski repoları kapatabiliriz" onayı verene kadar eski depolara hiçbir müdahale yapılmaz.**

---

## 🤖 8. Argon / Antigravity İçin Hazır İstek Komutu (Prompt Template)

Limitleriniz açıldığında aşağıdaki blok metni doğrudan kopyalayarak asistana verebilirsiniz:

```text
Merhaba! Depomuzdaki "docs/ATES_FAM_MASTER_SUITE_ARCHITECTURE.md" dosyasında tüm detayları tanımlanmış olan "ATES FAM Master Suite" mimarisine geçmek istiyorum. 

Öncelikli Aile Yetkilendirme, Kütüphane ve Güvenlik Kuralları:
1. Elimdeki modülleri (Fitness, Budget, Library, Flight ve bağımsız Memories) tek bir private Streamlit uygulaması altında birleştirmek.
2. Netflix tarzı 4 aile profili ve Ayrı PIN'li Rol Tabanlı Yetkilendirme (RBAC) kurmak:
   - "Anıl": Kendi PIN'i ile tüm 5 modüle (Fitness, Budget, Library, Flight, Memories) tam yönetici yetkili.
   - "Berna": Kendi PIN'i ile Library, Flight ve Memories'e tam erişim; Fitness'ta yalnızca "Menü & Sağlık" (beslenme/takviye) modülüne erişim; Budget tarafında ise yalnızca "Financial Overview" modülüne erişim.
   - "Atlas": Kendi çocuk PIN'i ile giriş. Sadece Library (Atlas yaş grubuna ait kitaplar & kişisel okuma sayaçları), Flight (Canlı radar) ve Memories (Atlas'ın Anıları - yalnızca okuyucu / read-only) görünür olacak. Bütçe ve Fitness kesinlikle görünmeyecek ve URL manipülasyonuna karşı engellenecek.
   - "Alina": Kendi çocuk PIN'i ile giriş. Sadece Library (Alina 0-3 yaş bebek kitapları & kişisel okuma sayaçları), Flight (Canlı radar) ve Memories (Alina Bebek Günlüğü - yalnızca okuyucu / read-only) görünür olacak. Bütçe ve Fitness engelli olacak.
   - Library ve Memories içinde ebeveyn yönetici işlemleri için Anne/Baba PIN'i gerekecek.
3. apps/fitness, apps/budget, apps/library, apps/flight ve apps/memories şeklinde 5 modüllü monorepo kurmak; her projenin kendi README_<PROJE>.md ve ROADMAP_<PROJE>.md dokümanını ayırt edilebilir isimlerle modül dizininde bağımsız tutmak.
4. Çift katmanlı SQLite ve GitHub bağımsız Veri Branch'leri (data-fitness, data-budget, data-library, data-flight, data-memories) ile veri kalıcılığını %100 izole korumak.
5. KRİTİK KALİTE GÜVENCESİ & BEKÇİ KURALI (GUARDS): Geçişin her aşamasında birim testler, Scope Guard ve Document Guard çalıştırılmalı; %100 yeşil test güvencesi korunmalıdır.
6. KESİN GÜVENLİK KURALI (SIFIR RİSK): Yeni Master Suite canlıda %100 doğrulanıp benden açık yazılı onay almadan mevcut hiçbir public depoyu (fitness, budget, atlas-library vb.) silme, kapatma, içeriğini boşaltma veya arşivleme! Eski sistemler paralel olarak kesintisiz çalışacaktır.
7. Şartnamedeki 7 aşamalı geçiş yol haritasını sırasıyla ve testleri kırılmadan hayata geçirmeni rica ediyorum.
```
