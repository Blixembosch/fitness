# 🗺️ ATES FAM Fitness — Ürün ve Mimari Yol Haritası (Roadmap)

> **Proje:** ATES FAM Fitness  
> **Hedef:** Wegovy (GLP-1) protokolünde kas kütlesini koruma/artırma, yağ yakımı, padel performansı ve metabolik sağlık  
> **Teknoloji:** Python 3.14 · Streamlit · SQLite (`data/fitness.db`) · GitHub Data Branch (`Blixembosch/fitness:data`)  
> **Resmi Başlangıç:** 25 Ekim 2026 (Pazar) · **İlk Wegovy Dozu:** 27 Ekim 2026 (Salı)  
> **Kalite Güvencesi:** 122 Otomatik Test (%100 Yeşil) · Doküman & Kapsam Bekçileri (Guards)

---

## 🎯 1. Vizyon ve Temel İlkeler

ATES FAM Fitness; kilo verme sürecinde kas kaybını (**sarkopeni**) önleyen, GLP-1 reseptör agonistlerinin (Wegovy) mide boşalmasını yavaşlatıcı etkisine uygun sindirim konforu sunan, Google Takvim ile Padel antrenmanlarını dinamik dengeleyen ve Cronometer/Apple Health verilerini birleştiren **akıllı, bütüncül ve estetik bir fitness işletim sistemidir**.

### Mimari & Tavizsiz Prensipler (Non-Negotiables)
1. **GLP-1 Mide Konforu & Kas Koruma:**
   - Günlük kalori açığı (`~2000 kcal`) hedeflenirken protein alımı kilo başına yüksek tutulur (`~160g Protein, ~67g Yağ, ~189g Karbonhidrat, ~28g Lif`).
   - Mide dolgunluğu, reflü ve bulantıyı önlemek için beslenme **4 dengeli öğüne** (Kahvaltı, Öğle, Ara Öğün/Shake, Akşam) bölünür.
2. **Çift Katmanlı Veri Kalıcılığı (Dual-Layer Persistence):**
   - Streamlit Cloud geçici container ortamlarında çalıştığından, hiçbir kullanıcı verisi (tartım, antrenman, menü, takviye kayıtları) kod içine yazılmaz.
   - Yerel **SQLite (`data/fitness.db`)** ve GitHub bağımsız **[`data` branch'i](https://github.com/Blixembosch/fitness/tree/data) (`fitness.sql`)** üzerinden çift yönlü otomatik senkronize edilir.
3. **Sıfır Gecikme & Çevrimdışı Öncelikli (Offline-First):**
   - Menü planlayıcı, evdeki 20+ ürünü ve 30+ temel gıdayı yerel kütüphanede (`HOME_PRODUCT_LIBRARY` & `OFFLINE_STAPLE_FOODS`) 0 milisaniyede hesaplar; dış API bağımlılığı olmadan %100 çalışır.
   - Yeni ürünlerde Hollanda **Open Food Facts** veritabanına otomatik bağlanır.
4. **Doküman & Kapsam Bekçileri (Document & Scope Guards):**
   - Kod tabanındaki her yenilik (progression), test paketine bir regresyon testi (regression) olarak otomatik eklenir.
   - Dokümantasyon (`README.md`, `ROADMAP.md`) test sayıları ve kapsam kuralları otomatik bekçiler tarafından denetlenir; doküman kayması engellenir.

---

## 📅 2. Sürüm Geçmişi ve Tamamlanan Kilometre Taşları

### 🟢 V1.0 — Temel Altyapı & Dashboard (Ekim 2026)
- [x] Streamlit çok sayfalı mimari (Ana Sayfa, Plan, Antrenman, Beslenme, İstatistik).
- [x] Cronometer CSV ayrıştırma (dailysummary, biometrics, exercises).
- [x] 52 haftalık GitHub katkı grafiği (heatmap) ve aktivite halkaları.
- [x] WCAG AA/AAA uyumlu karanlık tema, yüksek kontrastlı Emotion/CSS sınıfları.

### 🟢 V1.1 — Wegovy & Dinamik Padel Entegrasyonu (Ekim 2026)
- [x] Wegovy enjeksiyon döngüsü, bölge rotasyonu (sağ/sol karın, uyluk) ve 48 saatlik GI/RPE izleme penceresi.
- [x] Google Takvim (iCal) entegrasyonu: Atlas'ın çocuk antrenmanlarını eleyen, Anıl'ın Padel maçlarını çeken akıllı regex filtresi.
- [x] Padel maçlarına göre dinamik güç antrenmanı kaydırma (Salı-Çarşamba padel senkronu).
- [x] Pazartesi-Pazar döngüsü ve 25 Ekim 2026 resmi program başlangıç filtresi.

### 🟢 V1.2 — 4 Öğünlü Akıllı Menü & Doğrudan Tüketim Kaydı (Ekim 2026)
- [x] Wegovy mide boşalmasına uygun 4 öğünlük (Kahvaltı, Öğle, Ara Öğün, Akşam) planlayıcı.
- [x] Her öğün için 5'er kanıta dayalı tarif (toplam 20 tarif).
- [x] Tek tıkla **"💾 Günün Beslenmesini Uygulamaya Kaydet"**: Cronometer'a tek tek gıda girmeden günlük makroları doğrudan `S["nutrition"]` ve SQLite/GitHub'a kalıcı yazma.
- [x] Akşamdan eşe gönderilebilen kopyalanabilir WhatsApp günlük menü bildirimi.

### 🟢 V1.3 — Evdeki Ürünler & Kalori Kütüphanesi (Ekim 2026)
- [x] Evdeki 20 temel ürünün (AH Kwark, Hüttenkäse, Impact Whey, Upfront, AH Mousse/Pudding, XXL Fitmousse, Yfood, Huel, Alpro, Organik Yumurta vb.) yerel veritabanı (`HOME_PRODUCT_LIBRARY`).
- [x] Beslenme sekmesi altında görsel ürün tablosu ve porsiyon bazlı klinik/pratik kullanım notları.
- [x] Eşit kutucuk yükseklikleri ve yatay flexbox hizalaması.

### 🟢 V1.4 — Akıllı Besin Bulucu & Otomatik Makro Hesaplayıcı (Ekim 2026)
- [x] Arayüzden sadece **Ürün Adı ve Gramaj** girilerek (protein, yağ vb. yazmadan) otomatik değer bulma.
- [x] 30+ temel gıdalık yerel katalog + Hollanda **Open Food Facts** canlı sorgusu.
- [x] Gramaja göre anlık oransal hesaplama (örn. 150g somon -> 1.5x) ve canlı metrik önizlemesi.
- [x] Kütüphanede arama (`🔍 Kütüphanede Ara`) ve kategori filtreleme.
- [x] Eklenen özel ürünleri arayüzden düzenleme (✏️) ve silme (🗑️).

### 🟢 V1.5 — 2 Kademeli Klinik Takviye & Elektrolit Protokolü (Ekim 2026)
- [x] Bilinçli takviye mimarisi: **🟢 Temel Rutin** ve **🟡 Sadece İhtiyaç Halinde** ayrımı:
  - **🟢 Temel Günlük Rutin:**
    - **Sabah (Kahvaltı İle):** Ocean Daily One Multivitamin (1 tb) + Ocean D3 1000 IU Sprey (2 puff / 2000 IU).
    - **Öğleden Sonra / Padel:** Avoya Sert İçim Doğal Maden Suyu (1 şişe 200 ml) veya AH Sade Soda (250–500 ml) — GLP-1 sodyum atılımı (natriürez), tansiyon düşmesi ve kramp önleme.
    - **Gece (Yatmadan):** Orzax Ocean ExtraMag Üçlü Magnezyum (1 tb) — GLP-1 kabızlığını önleme, kas kramplarını engelleme ve derin uyku.
  - **🟡 Sadece İhtiyaç Halinde (Semptomatik):**
    - **Şişkinlik / Ağır Öğün Sonrası:** Orzax Ocean Bromelain 500 mg (1 kap) — ağır et/bakliyat sonrası hazımsızlık veya belirgin ödemde kurtarıcı sindirim enzimi.
    - **Halsizlik / Bağışıklık Riski:** Ocean C Vitamini 1000 mg + Bioflavonoid (1 tb) — kırgınlık başlangıcında destek.
- [x] Her öğün kartında rozet ayrımı (`🟢 Temel` vs `🟡 İhtiyaçta`).
- [x] Günlük interaktif takviye & maden suyu takip kutucukları ve kalıcı kayıt (`supplements_log`).
- [x] **⏰ Sirkadiyen Zamanlama Modülü:** *Nature Communications (2025)* (14.689 katılımcı, $\ge 4$ saat kuralı) ve *Sleep Medicine Reviews (2026)* verileriyle 3 protokol (Hafta İçi Erken Sabah 06:30, Hafta Sonu Gün İçi 11:30, Akşam Padel 18:30). Wegovy mide boşalma gecikmesine uygun aç karnına/sıvı pre-workout stratejisi ve anabolik toparlanma zamanlaması.
- [x] WhatsApp günlük menü çıktısına 2 kademeli protokol ve sirkadiyen zamanlama formatının estetik entegrasyonu.
- [x] 122/122 tam yeşil test paketi ve Doküman/Kapsam Bekçileri (`test_doc_and_scope_guard.py`).

---

## 🚀 3. Aktif Sprint: Kickoff & Uygulama (25 - 31 Ekim 2026)

- [ ] **25 Ekim Pazar (1. Gün):**
  - Sabah başlangıç tartımı ve vücut ölçüleri kaydı.
  - İlk antrenman: **Üst A** (5 dk Eliptik ısınma -> dambıl hareketleri -> 10 dk Su Küreği + 10 dk Eliptik bitirişi).
  - Beslenme: 1. Gün hedefi `~160g P, ~67g Y, ~189g K, ~28g Lif` (Pazar şablonu menüye aktarılıp tüketim kaydedilecek).
- [ ] **26 Ekim Pazartesi (2. Gün):**
  - Aktif dinlenme / toparlanma yürüyüşü + kalori ve protein dengesi.
- [ ] **27 Ekim Salı (3. Gün — Wegovy Başlangıcı):**
  - **İlk Wegovy Dozu: 0.25 mg** (Sol veya sağ karın bölgesi).
  - Salı Padel antrenmanı (19:30).
  - 48 saatlik hidrasyon (≥2.5L su) ve Bromelain/Magnezyum desteğiyle GI yan etki takibi.
- [ ] **28 Ekim Çarşamba (4. Gün):**
  - Çarşamba Padel maçı.
- [ ] **29 Ekim Perşembe (5. Gün):**
  - Güç antrenmanı: **Alt A** (Bacak hipertrofisi ve core).
- [ ] **31 Ekim Cumartesi (7. Gün):**
  - Güç antrenmanı: **Üst B** ve 1. hafta genel değerlendirmesi.

---

## 🔮 4. Gelecek Yol Haritası (Future Horizons — Q4 2026 & 2027)

### Faz 2: Apple Health & Giyilebilir Cihaz Canlı Köprüsü
- [ ] **Doğrudan Webhook / REST Köprüsü:** Cronometer dosya yükleme adımını tamamen arka plana itecek Apple Shortcuts veya yerel webhook köprüsü ile Apple Watch nabız, adım ve uyku verisinin doğrudan aktarımı.
- [ ] **Zone-2 Kardiyo Nabız Takibi:** Kürek ve eliptik kardiyolarında Zone-2 nabız aralığında (115-135 bpm) kalma süresinin dashboard üzerinde görselleştirilmesi.

### Faz 3: Yapay Zeka Destekli Tabak ve Barkod Tanıma
- [ ] **Kamera / Fotoğraftan Tabak Tanıma:** Kullanıcı yemek tabağının fotoğrafını yüklediğinde Gemini / Computer Vision modeli ile tabaktaki besinlerin ve gramajların otomatik tahmin edilip makrolara dökülmesi.
- [ ] **Albert Heijn Barkod Tarayıcı:** Mobil tarayıcı üzerinden ürün barkodunun kamerayla okutularak 100g değerlerinin Open Food Facts üzerinden anında getirilmesi.

### Faz 4: Padel & RPE Performans Analitiği
- [ ] **Padel Maç Yükü Skoru (Match Load):** Kalp atış hızı ve süreye göre Padel maçının antrenman yükünün (TSS) hesaplanıp ertesi günkü bacak toparlanmasına dinamik öneri verilmesi.
- [ ] **Turnuva & Sezon Dağılımı:** Galibiyet/mağlubiyet ve enerji seviyesi korelasyon grafikleri.

### Faz 5: Boylamsal Vücut Kompozisyonu ve Tahminleme Modeli
- [ ] **DEXA & Yağsız Kütle Projeksiyonu:** Kilo kaybının ne kadarının yağdan, ne kadarının kastan gittiğini izleyen doğrulanmış matematiksel koruma endeksi.
- [ ] **Doz Artırım Simülatörü:** Wegovy dozunun 0.25mg -> 0.50mg -> 1.0mg geçişlerinde iştah ve metabolik hız değişim simülasyonu.

---

## 🛡️ 5. Kalite Güvencesi ve Bekçi Mekanizması (Guards — Tamamlandı & Aktif Olarak Çalışıyor)

> [!NOTE]
> Bu bölüm geleceğe yönelik bir planlama değil; projenin her commit ve çalıştırmasında devrede olan **aktif mimari koruma kalkanıdır**.

Proje, regresyonu ve kapsam sapmasını önleyen **4 koruma katmanıyla** çalışır:

1. **Birim & Fonksiyonel Testler (Aktif — 118 Test):** Cronometer ayrıştırma, takvim filtreleme, makro hesaplayıcı, WCAG kontrastı ve tüm Streamlit sayfalarının `AppTest` kontrolü.
2. **Kapsam Bekçisi (`Scope Guard` — Aktif):** `PERSIST_KEYS` (12 kalıcı anahtar), `HOME_PRODUCT_LIBRARY`, 6 parçalı `SUPPLEMENT_PROTOCOL`, 3 parçalı `CIRCADIAN_MEAL_TIMING` ve 20 tarifli `MEAL_DATABASE` gibi çekirdek bileşenlerin eksiksizliğini doğrular.
3. **Doküman Bekçisi (`Document Guard` — Aktif):** `README.md` ve `ROADMAP.md` dosyalarındaki test sayılarının (122), mimari açıklamaların ve entegrasyon bilgilerinin kodla %100 senkronize olduğunu teyit eder.
4. **Progression-to-Regression Otomasyonu (Aktif — Otomatik Genişleyen):** Yazılan her yeni test `run_tests.py` tarafından anında keşfedilir, dinamik olarak sayılır ve bir sonraki güncellemede zorunlu bir regresyon testine dönüşür. Toplam test paketi şu anda **122/122 yeşil** olarak kilitlenmiştir.
