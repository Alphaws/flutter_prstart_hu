# 5. szint — Offline

A vizsga célja egy olyan offline-first alkalmazás létrehozása, amely hálózati kapcsolat nélkül is teljes értékűen használható adatbevitelre.

## 🎯 Vizsga Feladatok
Készíts egy offline jegyzetkezelő alkalmazást:
1. **Helyi Adatbázis:** A jegyzeteket tárold el egy helyi NoSQL vagy SQL adatbázisban (Isar, Hive vagy Drift).
2. **Offline CRUD:** Támogasd a jegyzetek létrehozását, szerkesztését és törlését hálózat nélkül is.
3. **Kapcsolat figyelés:** Figyeld a hálózati kapcsolatot (`connectivity_plus`). Kapcsolat visszatérésekor küldj egy szimulált szinkronizációt a szerverre és jeleníts meg egy sikeres szinkron státuszjelzőt.

## 🔍 Értékelési Szempontok
* Az adatok azonnal mentődnek a helyi adatbázisba, az alkalmazás bezárása után sem vesznek el.
* A szinkronizációs folyamat a háttérben fut le, nem zavarja az épp gépelő felhasználót.