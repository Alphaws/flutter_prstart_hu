# Lokális adattárolás

Az adatok helyi mentése szükséges beállítások, offline működés és gyorsabb betöltési idők eléréséhez.

## 📦 Ajánlott Csomagok:
* **`shared_preferences`:** Egyszerű kulcs-érték párok tárolása (pl. sötét mód beállítása).
* **`flutter_secure_storage`:** Érzékeny adatok (pl. JWT tokenek) titkosított tárolása az eszköz biztonságos hardverében.
* **`isar` vagy `hive`:** Ultragyors NoSQL objektum-adatbázisok lokális adathalmazok tárolására.
* **`drift` (sqflite wrapper):** Relációs SQL adatbázis Dart nyelven, típusbiztos lekérdezésekkel.

### Döntési táblázat:
| Adat Típusa | Ajánlott Megoldás |
|---|---|
| Beállítások, flag-ek | `shared_preferences` |
| API Tokenek, jelszavak | `flutter_secure_storage` |
| Offline adatok, listák | `isar` vagy `hive` |
| Komplex relációk | `drift` |