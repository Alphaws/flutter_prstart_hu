# Csomag hozzáadása

A Flutter projektünkhöz a pub.dev-en található külső csomagokat a pub parancsokkal tudjuk hozzáadni.

## 🛠️ Parancsok:
* **Csomag hozzáadása:**
  ```bash
  flutter pub add dio
  ```
  Ez a parancs automatikusan beírja a legfrissebb kompatibilis verziót a `pubspec.yaml` fájl `dependencies` szekciójába, és le is tölti azt.

* **Függőségek letöltése manuálisan:**
  ```bash
  flutter pub get
  ```
  Használd ezt a parancsot, ha a `pubspec.yaml` fájlt kézzel szerkesztetted vagy frissen húztad le a projektet Git-ről.