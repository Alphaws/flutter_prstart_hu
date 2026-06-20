# Dev dependency

A fejlesztési függőségek olyan eszközök, amelyekre csak a kód írásakor, generálásakor vagy tesztelésekor van szükség, az elkészült éles appba (build) nem kerülnek bele.

## 🛠️ Parancsok:
* **Fejlesztési csomag hozzáadása:**
  ```bash
  flutter pub add --dev build_runner
  ```
  Beírja a csomagot a `pubspec.yaml` fájl `dev_dependencies` szekciójába.

* **Tipikus dev függőségek:**
  * `build_runner` (kódgeneráláshoz)
  * `freezed` és `json_serializable` (modellezéshez)
  * `mocktail` (teszteléshez)