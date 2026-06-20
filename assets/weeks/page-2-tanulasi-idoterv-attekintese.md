# Tanulási időterv áttekintése

A sikeres Flutter fejlesztővé válás kulcsa a strukturált haladás. A 24 hetes képzést 7 fő szakaszra osztottuk fel, amelyek lépésről lépésre épülnek egymásra. Az alábbiakban részletesen áttekintheted a teljes időtervet.

---

## 📅 A 24 hetes tanmenet részletes felépítése

| Szakasz | Időtartam | Fókuszterület | Főbb technológiák és témák |
| :--- | :---: | :--- | :--- |
| **1. Alapozás** | 1–2. hét | Fejlesztői környezet, Dart programozás | Git, Dart SDK, Variables, Collections, OOP, Null Safety |
| **2. UI és navigáció** | 3–5. hét | Felhasználói felületek és route-ok | Widgets, Column/Row, Navigation, GoRouter, Themes |
| **3. Adat és állapot** | 6–9. hét | API-k, Aszinkronitás, State Management | HTTP/Dio, JSON parsing, Provider, ValueNotifier, Forms |
| **4. Profi app alapok** | 10–14. hét | Architektúra, Perzisztencia, Biztonság | Clean Architecture, GetIt, Isar DB, JWT Auth, Offline-first |
| **5. Tesztelés és minőség** | 15–18. hét | Tesztelés, Hibakezelés, Linter | Unit/Widget/Integration Tests, Crashlytics, Static Analysis |
| **6. Haladó Flutter** | 19–22. hét | Animációk, Native integráció, Performance | Custom Painter, Animations, Platform Channels, Profiling |
| **7. Publikálás** | 23–24. hét | Release build, CI/CD, Google Play / App Store | GitHub Actions, Fastlane, App Bundle signing, Publishing |

---

## 🔍 Az egyes szakaszok részletes bemutatása

### 1. szakasz: Alapozás (1–2. hét)
A cél a stabil alapok lefektetése. Megismerkedünk a fejlesztői környezet beállításával (Android Studio, VS Code, Flutter SDK), valamint a Dart programozási nyelv alapjaival.
* **Főbb témák:** Dart változók, kollekciók (`List`, `Map`, `Set`), funkcionális és objektumorientált programozás (OOP), Null Safety alapelvei, Dart 3 újdonságok (Records, Pattern Matching).
* **Mérföldkő:** Egy konzolos, interaktív számológép és egy kosár-kezelő alkalmazás Dartban.

### 2. szakasz: UI és navigáció (3–5. hét)
A mobilalkalmazások szíve a látvány és a használhatóság. Ebben a szakaszban megtanulunk reszponzív felületeket építeni.
* **Főbb témák:** Alapvető és elrendezés-szabályozó widgetek (`Container`, `Row`, `Column`, `Stack`, `ListView`), reszponzív elrendezések (`LayoutBuilder`, `MediaQuery`), témázás (Light/Dark mode, egyedi színpaletták), navigáció (Navigator 1.0 és a deklaratív `go_router` csomag).
* **Mérföldkő:** Egy összetett, többképernyős recept- és étel-katalógus alkalmazás UI prototípusa.

### 3. szakasz: Adat és állapot (6–9. hét)
Az alkalmazások többsége online adatokból építkezik. Itt kötjük össze a vizuális felületet az adatokkal és a szerverrel.
* **Főbb témák:** Aszinkron programozás (`Future`, `Stream`, `async`/`await`), REST API-k meghívása (`http` és `dio` csomagok), JSON adatok szerializálása modellekké, űrlapok kezelése validációval, valamint az első komolyabb állapotkezelők (`ChangeNotifier`, `Provider`).
* **Mérföldkő:** Egy valós idejű hírolvasó és kereső alkalmazás egy publikus API-ra csatlakoztatva.

### 4. szakasz: Profi alkalmazások alapjai (10–14. hét)
Hogyan építsünk skálázható és biztonságos alkalmazásokat? Ez a szakasz a professzionális szoftverfejlesztés sztenderdjeit mutatja be.
* **Főbb témák:** Rétegelt architektúra (Clean Architecture), függőségek befecskendezése (Dependency Injection - `get_it`), lokális perzisztens adatbázisok (`Isar` vagy `Hive`), JWT alapú autentikációs folyamatok és biztonságos token tárolás (`flutter_secure_storage`), offline-first adatszinkronizáció.
* **Mérföldkő:** Egy teljes értékű, offline is működő, bejelentkezést igénylő teendőkezelő (To-Do) alkalmazás helyi adatbázissal.

### 5. szakasz: Tesztelés és minőségbiztosítás (15–18. hét)
A profi kód egyik legfőbb ismertetője, hogy automatizált tesztek védik a hibáktól.
* **Főbb témák:** Unit tesztek írása az üzleti logikára, Widget tesztek a UI viselkedésére, Integration tesztek a teljes felhasználói folyamatokra, CI/CD pipeline-ok beállítása GitHub Actions-szel.
* **Mérföldkő:** A korábbi projektek lefedése tesztekkel, és egy automatizált ellenőrző pipeline felépítése.

### 6. szakasz: Haladó Flutter fejlesztés (19–22. hét)
A prémium felhasználói élményhez elengedhetetlenek a szép animációk és a hardveres funkciók.
* **Főbb témák:** Implicittel és explicit animációk, egyedi grafikák rajzolása (`CustomPainter`), natív platform funkciók elérése (**Platform Channels** segítségével Androidra és iOS-re), teljesítménydiagnosztika (memory leak és lassulások keresése a DevTools segítségével).
* **Mérföldkő:** Egy animációkkal gazdagított, natív eszközfunkciót (pl. kamera vagy helymeghatározás) használó applikáció.

### 7. szakasz: Publikálás és Záróprojekt (23–24. hét)
Az utolsó fázisban az alkalmazásunkat eljuttatjuk a felhasználókhoz.
* **Főbb témák:** Google Play Console és App Store Connect fiókok beállítása, Android App Bundle (AAB) és iOS IPA fájlok előkészítése, build aláírás (signing keys), kiadási csatornák kezelése (béta és produkciós tesztelés), és a saját, egyedi záróprojekt befejezése.
* **Mérföldkő:** A saját egyedi projekted publikálásra kész állapotban való feltöltése GitHubra és egy tesztcsatornára.

---

> [!NOTE]
> Bár a tananyag 24 hétre van tervezve, a haladási tempó rugalmasan alakítható. A legfontosabb, hogy ne siess előre addig, amíg az adott szakasz mérföldkő-projektjét nem tudod önállóan megvalósítani.
