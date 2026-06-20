# 6.1 Sephir ERP mobil app

A Sephir ERP mobil companion alkalmazása egy professzionális, éles piaci igényekre szabott üzleti alkalmazás. Célja, hogy a kkv-k munkatársai a raktárban vagy a terepen is elérjék az ERP rendszer legfontosabb adatait.

## 🎯 Fő Funkciók
* **Workspace választás:** Támogatja a több telephelyes vagy több céges struktúrák közötti egyszerű váltást.
* **Termék- és Partnerlista:** Gyors keresés, szűrés, kategóriák és valós idejű készletinformációk.
* **Rendelés felvitel:** Új értékesítési rendelések összeállítása és beküldése közvetlenül a vevőnél.
* **Raktárkezelés és Vonalkódolvasás:** Beépített kamera vagy hardveres olvasó segítségével történő leltározás és árukiadás.
* **Offline-first működés:** Hálózati kapcsolat hiányában is rögzíthetők a bizonylatok, amelyek a kapcsolat visszatérésekor automatikusan szinkronizálódnak.

## 🏗️ Architektúra és Technológiák
* **Állapotkezelés:** Riverpod az aszinkron adatok és a kosár állapotának menedzselésére.
* **Helyi Adatbázis:** Isar az offline adatok gyors és relációs tárolására.
* **Hálózat:** Dio interceptorokkal a JWT tokenek automatikus frissítésére és a kérések naplózására.