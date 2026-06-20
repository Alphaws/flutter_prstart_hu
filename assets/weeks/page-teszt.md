# Teszt

Az automatizált tesztek futtatása biztosítja, hogy a kód módosítása során ne rontsuk el a meglévő funkciókat.

## 🛠️ Parancsok:
* **Összes teszt futtatása:**
  ```bash
  flutter test
  ```
  Lefuttatja a `test/` mappában található összes unit és widget tesztet.

* **Tesztlefedettség (Coverage) mérése:**
  ```bash
  flutter test --coverage
  ```
  Létrehoz egy `coverage/lcov.info` fájlt, amely megmutatja, a sorok hány százalékát fedik le tesztek.