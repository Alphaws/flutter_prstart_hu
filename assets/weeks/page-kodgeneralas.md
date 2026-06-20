# Kódgenerálás

Sok Flutter csomag (pl. freezed, drift, retrofit) kódgenerálást használ a típusbiztos kód automatikus előállításához.

## 🛠️ Parancsok:
* **Egyszeri kódgenerálás:**
  ```bash
  dart run build_runner build --delete-conflicting-outputs
  ```
  Lefuttatja a generálást, és felülírja a korábbi konfliktusos fájlokat.

* **Folyamatos figyelés és generálás:**
  ```bash
  dart run build_runner watch --delete-conflicting-outputs
  ```
  A háttérben futva figyeli a fájlok változását, és mentéskor azonnal újraírja a generált fájlokat.