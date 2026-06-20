# Build

Az alkalmazás kiadásra (Google Play Áruházba való feltöltésre) való előkészítése és lefordítása.

## 🛠️ Parancsok:
* **Android App Bundle (AAB) készítése (Ajánlott):**
  ```bash
  flutter build appbundle --release
  ```
  Ez a hivatalos formátum a Play Áruházba való feltöltéshez. Kisebb méretet eredményez a felhasználók eszközein.

* **Hagyományos APK build:**
  ```bash
  flutter build apk --release
  ```
  Létrehoz egy telepíthető APK fájlt, amit közvetlenül is átküldhetsz tesztelésre.