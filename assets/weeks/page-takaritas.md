# Takarítás

Néha a Flutter cache-e megsérülhet, vagy verzióváltás után beragadhatnak régi build fájlok. Ilyenkor érdemes kitakarítani a projektet.

## 🛠️ Parancsok:
* **Build és cache fájlok törlése:**
  ```bash
  flutter clean
  ```
  Kitörli a `build/` mappát és az ideiglenes Dart cache fájlokat.

* **Függőségek friss letöltése:**
  ```bash
  flutter pub get
  ```
  A takarítás után mindig le kell futtatni, hogy újraépüljön a csomagtár.