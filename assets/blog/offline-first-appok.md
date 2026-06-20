# Hogyan építsünk offline-first alkalmazásokat Flutterben?

**Szerző:** PRSTART Blog  
**Dátum:** 2026-06-20  
**Téma:** Haladó architektúra  

---

A mai felhasználók elvárják, hogy egy mobilalkalmazás zökkenőmentesen működjön metrózás közben, repülő üzemmódban vagy instabil térerő mellett is. Az **offline-first** megközelítés lényege, hogy az alkalmazás elsődlegesen a helyi adatbázissal kommunikál, és a háttérben szinkronizál a szerverrel, amikor van internetkapcsolat. Ebben a bejegyzésben bemutatjuk ennek az architektúrának a legfontosabb építőelemeit Flutterben.

---

## 1. Az Offline-First alapelvei

Hagyományos megközelítés:
```
UI ──> API Hívás ──> (Siker: Megjelenítés / Hiba: Hibaüzenet)
```

Offline-first megközelítés:
```
UI ──> Helyi Adatbázis (Azonnali mentés & UI frissítés)
          │
          └──> Háttér Szinkronizáció ──> Éles API Szerver
```

Ez a modell biztosítja, hogy a felhasználói felület **azonnal** reagáljon (optimista UI frissítés), és a hálózati késleltetés ne lassítsa le az interakciót.

---

## 2. A Három Alapvető Építőelem

### A. Lokális Adatbázis (A szilárd alap)
Szükségünk van egy gyors, helyi tárolóra. Flutterben a legnépszerűbbek:
- **SQLite (sqflite):** A klasszikus relációs adatbázis, kiváló komplex lekérdezésekhez.
- **Drift (korábban Moor):** Reaktív SQLite wrapper, típusbiztos Dart lekérdezésekkel.
- **Hive / Isar:** Rendkívül gyors NoSQL kulcs-érték és objektum alapú adatbázisok.

### B. Hálózati Kapcsolat Figyelő (Connectivity Monitor)
Folyamatosan figyelnünk kell, hogy van-e aktív internetkapcsolat. Ehhez a `connectivity_plus` csomagot használjuk:

```dart
import 'package:connectivity_plus/connectivity_plus.dart';

class ConnectivityService {
  final Connectivity _connectivity = Connectivity();

  // Stream, amely figyeli a kapcsolat változását
  Stream<ConnectivityResult> get onConnectivityChanged => 
      _connectivity.onConnectivityChanged.map((results) => results.first);

  Future<bool> isConnected() async {
    final result = await _connectivity.checkConnectivity();
    return result.first != ConnectivityResult.none;
  }
}
```

### C. Szinkronizációs Sor (Sync Queue / Outbox Pattern)
Ha a felhasználó módosít valamit (pl. létrehoz egy új bejegyzést) offline módban, a műveletet elmentjük a helyi adatbázisba, és bejegyezzük a **Sync Queue** (szinkronizációs sor) táblába. 

A szinkronizációs sor rekordja így néz ki:
```sql
CREATE TABLE sync_queue (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  action TEXT,       -- 'CREATE', 'UPDATE', 'DELETE'
  endpoint TEXT,     -- '/api/items'
  payload TEXT,      -- JSON adatok
  timestamp TEXT
);
```

Amikor a `ConnectivityService` jelzi, hogy újra van internetkapcsolat, elindítjuk a **Sync Engine**-t (szinkronizációs motor), ami sorban végrehajtja a sorban álló kéréseket a szerveren, majd törli a sikeresen szinkronizált elemeket.

---

## 3. Konfliktusok Kezelése (Data Conflict Resolution)

Mi történik, ha egy adatot offline módban módosított a felhasználó a telefonon, de közben a szerveren is módosult?
Három elterjedt stratégia létezik:

1. **Client Wins (Az ügyfél nyer):** A telefonon végzett utolsó módosítás felülírja a szerver adatát. Egyszerű, de adatvesztéssel járhat.
2. **Server Wins (A szerver nyer):** A telefon eldobja a helyi módosítást, és frissít a szerver adatára. Bosszantó lehet a felhasználónak.
3. **Merge / Timestamp (Időbélyeg-alapú összefésülés):** A legfrissebb időbélyeggel rendelkező adat győz, vagy a mezőket külön-külön fésüljük össze.

---

## Összegzés

Az offline-first alkalmazások fejlesztése bonyolultabb, mint egy egyszerű API kliens megírása, de a felhasználói élmény szempontjából összehasonlíthatatlanul jobb. A helyi adatbázis (pl. Drift vagy SQLite) és a szinkronizációs sor mintája garantálja, hogy az alkalmazásod soha ne fagyjon le vagy mutasson üres képernyőt térerő hiányában.
