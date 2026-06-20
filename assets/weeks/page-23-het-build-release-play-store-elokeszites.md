# 23. hét — Build, release, Play Store előkészítés

## Cél
A lecke célja, hogy a tanuló megismerje a Flutter alkalmazások gyártási (Release) buildjének elkészítését Android platformra. Megtanuljuk az alkalmazás csomagnevének megváltoztatását, az egyedi ikonok és indítóképernyő (Splash Screen) beállítását, a biztonságos Keystore aláíró kulcs generálását és integrálását a Gradle build rendszerbe, valamint a kód-összenyomást és kódvédelmet (R8/ProGuard).

---

## Elmélet

### 1. APK vs AAB (Android App Bundle)
Androidra kétféle release build formátumot készíthetünk:
- **APK (Android Package):** Egyetlen kész bináris fájl, amely tartalmazza az összes CPU architektúrához (arm64-v8a, armeabi-v7a, x86_64) tartozó fordított kódot és az összes grafikai erőforrást. Előnye, hogy közvetlenül telepíthető a telefonokra tesztelési céllal.
- **AAB (Android App Bundle):** A Google Play Store modern publikációs formátuma. Nem telepíthető közvetlenül a telefonra. A Play Store-ba való feltöltés után a Google szerverei ebből generálnak egy egyedileg optimalizált, minimális méretű APK-t a letöltő felhasználó telefonjának specifikációi (képernyőfelbontás, CPU típus) alapján. Ezzel a felhasználóknak átlagosan 20-30%-kal kevesebb adatot kell letölteniük.

### 2. Csomagnév (Package Name / Application ID)
A csomagnév az alkalmazás globálisan egyedi azonosítója (pl. `hu.prstart.geonotes`). 
- A Play Store-ban nem létezhet két azonos csomagnevű app.
- A csomagnév határozza meg a telefonon a tárolási könyvtárat és a jogosultságok elszigetelését.
- **Soha** ne hagyd meg az alapértelmezett `com.example.myapp` nevet, mert azt a Google Play Console azonnal elutasítja!

### 3. Keystore Aláírási Rendszer
A Google megköveteli, hogy minden Play Store-ba feltöltött alkalmazás digitálisan alá legyen írva egy fejlesztői kulccsal (Keystore). Ez garantálja, hogy az alkalmazás frissítéseit valóban te készíted, és senki nem tudja felülírni a telefonon lévő appot egy módosított verzióval.
- **upload-keystore.jks:** A lokálisan generált kulcstároló fájl.
- **BIZTONSÁGI SZABÁLY:** A keystore fájlt és annak jelszavait tartalmazó fájlt (`key.properties`) **szigorúan tilos** feltölteni a nyilvános Git repository-ba! Helyette a `.gitignore` fájlba kell tenni őket, és lokálisan kell tárolni.

### 4. Kód-összenyomás és Védelem: R8 és ProGuard
Az **R8** (korábban ProGuard) az Android build folyamat része, amely három kulcsfontosságú feladatot lát el:
1. **Shrinking (Kód-összenyomás):** Eltávolítja a nem használt osztályokat, mezőket és metódusokat az alkalmazásból és a könyvtáraiból, csökkentve az app méretét.
2. **Optimization (Optimalizálás):** Átalakítja és egyszerűsíti a Kotlin/Java bájtkódot a gyorsabb futás érdekében.
3. **Obfuscation (Kód-homályosítás):** Átnevezi az osztályokat és metódusokat értelmezhetetlen rövid karakterekké (pl. `class UserController` -> `class a`). Ez megnehezíti az alkalmazás visszafejtését (Decompilation / Reverse Engineering).

---

## Kódpéldák

### 1. `key.properties` Sablonfájl
Hozd létre az `android/key.properties` fájlt a kulcs adataival (ez a fájl lokális marad):

```properties
storePassword=titkosJelszo123
keyPassword=titkosJelszo123
keyAlias=upload
storeFile=/home/alphaws/Dev/keys/upload-keystore.jks
```

### 2. Gradle Aláírási Konfiguráció (`android/app/build.gradle`)
Módosítsd az `android/app/build.gradle` fájlt, hogy automatikusan beolvassa a `key.properties` fájlt és aláírja a release buildet.

```groovy
plugins {
    id "com.android.application"
    id "kotlin-android"
    id "dev.flutter.flutter-gradle-plugin"
}

// 1. key.properties betöltése biztonságosan
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    namespace "hu.prstart.geonotes"
    compileSdk flutter.compileSdkVersion
    ndkVersion flutter.ndkVersion

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = '17'
    }

    sourceSets {
        main.java.srcDirs += 'src/main/kotlin'
    }

    defaultConfig {
        // A Play Store azonosító
        applicationId "hu.prstart.geonotes"
        minSdk flutter.minSdkVersion
        targetSdk flutter.targetSdkVersion
        versionCode flutter.versionCode
        versionName flutter.versionName
    }

    // 2. Aláírási konfigurációk megadása
    signingConfigs {
        release {
            if (keystorePropertiesFile.exists()) {
                storeFile = file(keystoreProperties['storeFile'])
                storePassword = keystoreProperties['storePassword']
                keyAlias = keystoreProperties['keyAlias']
                keyPassword = keystoreProperties['keyPassword']
            }
        }
    }

    buildTypes {
        release {
            // Aláírás hozzárendelése a release buildhez
            signingConfig signingConfigs.release
            
            // R8 kód-összenyomás és optimalizálás bekapcsolása
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}

flutter {
    source '../..'
}
```

### 3. ProGuard konfiguráció (`android/app/proguard-rules.pro`)
Néha az R8 túl agresszíven törölhet olyan osztályokat, amelyeket a Flutter vagy a harmadik féltől származó pluginok reflexióval (Reflection) hívnak meg. A következő szabályok megvédik a Flutter belső működését.

```proguard
# Flutter belső osztályok megőrzése
-keep class io.flutter.app.** { *; }
-keep class io.flutter.plugin.** { *; }
-keep class io.flutter.util.** { *; }
-keep class io.flutter.view.** { *; }
-keep class io.flutter.embedding.** { *; }
-keep class io.flutter.plugins.** { *; }

# Az átadott adatok (modellek) megőrzése, ha json_serializable-t használunk
-keepclassmembers class * {
    @com.google.gson.annotations.SerializedName <fields>;
}

# AndroidX és Google Play Services specifikus megtartások
-dontwarn com.google.android.gms.**
-dontwarn io.flutter.plugins.**
```

### 4. Parancssori Csalólap (Cheatsheet)

#### A) Aláíró kulcs (Keystore) generálása
Futtasd ezt a parancsot a terminálban egy új kulcstároló létrehozásához:
```bash
keytool -genkey -v -keystore ~/upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload
```

#### B) Release build indítása
Takaríts ki minden korábbi ideiglenes build fájlt, majd fordítsd le az alkalmazást:
```bash
# Projekt kitakarítása
flutter clean
flutter pub get

# Android App Bundle (.aab) generálása a Play Store-hoz (Ajánlott)
flutter build appbundle --release

# Android APK (.apk) generálása közvetlen teszteléshez
flutter build apk --release
```

#### C) Visszafejtési napló (Obfuscation mapping) keresése
Ha az elhomályosított kód összeomlik, a konzolon csak ilyen sorokat látunk: `at a.b.c(Unknown Source)`. A visszafejtéshez a Google Play Console-ba fel kell tölteni a build során keletkezett fordítási térképet:
- Elérési út: `build/app/outputs/mapping/release/mapping.txt`

---

## Gyakorlófeladatok & Megoldások

### 1. Feladat: Aláíró kulcs generálása és beállítása
Generálj egy új keystore fájlt `my-release-key.jks` néven a parancssorból, másold be egy biztonságos könyvtárba, és hozd létre a hozzá tartozó `key.properties` konfigurációt az `android` mappában.

#### Megoldás:
1. Parancs futtatása (adj meg jelszót, pl. `AppKey2026`):
   ```bash
   keytool -genkey -v -keystore ~/my-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-alias
   ```
2. Hozz létre egy `keys` mappát pl. a home könyvtárban: `mkdir -p ~/keys` és helyezd át oda a kulcsot: `mv ~/my-release-key.jks ~/keys/`
3. Hozd létre az `android/key.properties` fájlt:
   ```properties
   storePassword=AppKey2026
   keyPassword=AppKey2026
   keyAlias=my-alias
   storeFile=/home/alphaws/keys/my-release-key.jks
   ```

### 2. Feladat: Csomagnév refaktorálás
Módosítsd az alkalmazásod csomagnevét `com.example.myapp`-ról `hu.sajatdomain.appnev` névre.

#### Megoldás:
Bár kézzel is átírhatjuk az `AndroidManifest.xml`, `build.gradle` és a Kotlin osztályok mappaszerkezetét, a leggyorsabb és legbiztonságosabb módszer a `change_app_package_name` dev dependency használata.
1. Add hozzá a `pubspec.yaml`-hez:
   ```yaml
   dev_dependencies:
     change_app_package_name: ^1.1.0
   ```
2. Futtasd a parancsot a terminálban:
   ```bash
   flutter pub run change_app_package_name:main hu.sajatdomain.appnev
   ```
Ez a csomag automatikusan elvégzi az összes szükséges cserét a forrásfájlokban.

### 3. Feladat: Alkalmazás ikon beállítása (`flutter_launcher_icons`)
Konfiguráld a `flutter_launcher_icons` csomagot a `pubspec.yaml`-ben úgy, hogy az alkalmazás ikonja az `assets/images/app_logo.png` kép alapján generálódjon le mind Androidra, mind iOS-re.

#### Megoldás:
1. Add hozzá a csomagokat a `pubspec.yaml`-hez:
   ```yaml
   dev_dependencies:
     flutter_launcher_icons: ^0.13.1

   flutter_launcher_icons:
     android: "launcher_icon"
     ios: true
     image_path: "assets/images/app_logo.png"
     adaptive_icon_background: "#0F172A"
     adaptive_icon_foreground: "assets/images/app_logo_foreground.png"
   ```
2. Futtasd az ikon generáló parancsot:
   ```bash
   flutter pub run flutter_launcher_icons
   ```

### 4. Feladat: Verziószám növelése build script nélkül
Növeld meg az alkalmazás verzióját `1.0.0`-ról `1.1.0`-ra úgy, hogy a belső build szám (version code) 1-ről 5-re változzon. Demonstráld ezt a `pubspec.yaml`-ben és a build parancsban is.

#### Megoldás:
**A) A `pubspec.yaml` fájlban módosítjuk a `version` sort:**
```yaml
# A formátum: verzióNév+verzióKód (versionName+versionCode)
version: 1.1.0+5
```

**B) Vagy felülbíráljuk a build parancs futtatásakor paraméterekkel:**
```bash
flutter build appbundle --release --build-name=1.1.0 --build-number=5
```

### 5. Feladat: Print hívások letiltása release buildben
Írj egy Dart segédfüggvényt `logDebug` néven, amely csak debug módban ír üzenetet a konzolra, release módban viszont teljesen némán viselkedik, megvédve a szenzitív adatokat a naplófájlok kiolvasásától.

#### Megoldás:
```dart
import 'package:flutter/foundation.dart';

/// Biztonságos debug naplózás. Release módban nem fut le.
void logDebug(String message) {
  // A kReleaseMode egy beépített Flutter konstans, 
  // amit a compiler optimalizál release módban
  if (!kReleaseMode) {
    // Csak fejlesztői környezetben printel
    print('[DEBUG] ${DateTime.now()}: $message');
  }
}
```

---

## Heti Mini Projekt: Release Candidate Konfigurálás

### Leírás és Lépések
A heti feladat egy meglévő Flutter projektünk teljes release konfigurációjának elkészítése a gyakorlatban.
Hajtsd végre az alábbi lépéseket:
1. Hozz létre egy új kulcsot a `keytool` segítségével.
2. Hozd létre az `android/key.properties` fájlt.
3. Konfiguráld az `android/app/build.gradle` aláírási szekcióját.
4. Add hozzá az `android/app/proguard-rules.pro` fájlt a kódvédelemhez.
5. Futtasd a `flutter build appbundle --release` parancsot és ellenőrizd az elkészült `.aab` fájlt a `build/app/outputs/bundle/release/` mappában.

---

## Heti Ellenőrző Kérdések

### 1. Kérdés: Miért nem szabad a Keystore fájlokat és a `key.properties`-t becommitolni a verziókezelőbe (Git)? Mi a helyes eljárás csapatmunka vagy CI/CD esetén?
**Válasz:**
Ha a keystore kulcs és annak jelszavai felkerülnek a Git-re (különösen egy publikus repóba), bárki letöltheti azokat, visszafejtheti az aláírást, és készíthet egy kártékony verziót az alkalmazásodból, amit a korábbi felhasználók telefonja frissítésként elfogadna.
**Helyes eljárás:**
- A `.gitignore` fájlba fel kell venni a `*.jks` és `key.properties` sorokat.
- Csapatmunka esetén a kulcsokat és jelszavakat egy biztonságos jelszókezelőben (pl. 1Password, Bitwarden) osztjuk meg a fejlesztők között.
- CI/CD pipeline-ok (pl. GitHub Actions) esetén a keystore fájlt Base64 formátumban kódoljuk, és titkosított változóként (GitHub Secrets) tároljuk. A build folyamat során a CI futtató környezet a Secret-ből állítja vissza ideiglenesen a fájlt a build idejére, majd megsemmisíti azt.

### 2. Kérdés: Mi a különbség a `versionCode` és a `versionName` között a `pubspec.yaml` `version` mezőjében?
**Válasz:**
A `version: 1.2.3+4` formátumban:
- **`versionName` (a plusz jel előtti rész, pl. `1.2.3`):** Ez a felhasználók számára látható verziószám az áruházban és a telefon beállításaiban. Bármilyen formátumú String lehet (pl. `1.0.0-beta`), de a szemantikus verziózás (Major.Minor.Patch) az iparági sztenderd.
- **`versionCode` (a plusz jel utáni rész, pl. `4`):** Ez egy pozitív egész szám (Integer), amelyet a Google Play Store belsőleg használ az alkalmazásverziók sorrendjének meghatározására. Minden új feltöltésnél ennek a számnak szigorúan nagyobbnak kell lennie, mint az előző verzióé (pl. ha a legutóbbi app code-ja 4 volt, az újé legalább 5 kell legyen), különben az áruház visszautasítja a feltöltést.

### 3. Kérdés: Miért omlik össze néha az alkalmazás Release módban, miközben Debug módban tökéletesen működött? Hogyan deríthető ki a hiba oka?
**Válasz:**
A debug és release build közötti legfőbb eltérés az **R8/ProGuard kód-összenyomás és optimalizálás**. Debug módban nincs optimalizálás. Release módban az R8 letörölheti azokat a Kotlin/Java osztályokat, amelyeket a Dart kód reflexióval hív meg, vagy eltorzíthatja a JSON parsoláshoz használt DTO modellek nevét.
**Hiba felderítése:**
1. Futtassuk az alkalmazást lokálisan release módban egy csatlakoztatott eszközön: `flutter run --release`.
2. Figyeljük a konzolt a `flutter logs` segítségével.
3. Keressük meg az összeomlás helyét. Ha pl. `PlatformException` vagy `TypeError` van, akkor valószínűleg a ProGuard törölt egy fontos osztályt. Ekkor a `proguard-rules.pro` fájlban a `-keep` szabállyal meg kell tiltani az adott osztály elhomályosítását.

### 4. Kérdés: Mi az a „Staged Rollout” (szakaszos közzététel) a Google Play Console-ban, és miért hasznos?
**Válasz:**
A szakaszos közzététel lehetővé teszi, hogy az új alkalmazásfrissítést ne a teljes felhasználói bázis kapja meg egyszerre, hanem kezdetben csak egy meghatározott százalék (pl. a felhasználók 5%-a, majd 20%-a, 50%-a, végül 100%-a).
Ez rendkívül hasznos a kockázatok csökkentésére. Ha az új verzióban maradt egy kritikus hiba, ami összeomlást okoz bizonyos telefonokon, az csak a felhasználók egy kis részét érinti. A hibát a crash logokból észlelve leállíthatjuk a kiadást (Halt Rollout), javíthatjuk a hibát, és feltölthetünk egy javított verziót anélkül, hogy a teljes felhasználói bázis bosszankodna.

### 5. Kérdés: Miért kötelező a Privacy Policy (Adatvédelmi nyilatkozat) megléte az alkalmazás publikálásakor?
**Válasz:**
A Google Play és az Apple App Store, valamint a jogszabályok (GDPR, CCPA) kötelezővé teszik az adatvédelmi nyilatkozatot minden olyan alkalmazásnál, amely bármilyen felhasználói adatot kezel (ideértve a helyadatokat, kamerát, eszközazonosítókat, IP címeket vagy analitikai cookie-kat). A nyilatkozatnak világosan le kell írnia:
- Milyen adatokat gyűjt az app.
- Hogyan tárolja és dolgozza fel azokat.
- Továbbítja-e harmadik félnek (pl. Firebase, Google Analytics).
- Hogyan kérheti a felhasználó az adatai törlését.
A nyilatkozatot egy nyilvánosan elérhető weboldalon (URL) kell tárolni, és be kell linkelni a Play Console-ban a beküldés előtt.
