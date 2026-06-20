# 6.4 Raktárkezelő / vonalkódos app

A raktárkezelő mobilapp egy célirányos ipari célszoftver, amely a raktárosok napi munkáját (bevételezés, kiszedés, áthelyezés) támogatja vonalkód- és QR-kód olvasással.

## 🎯 Fő Funkciók
* **Termékkeresés:** Villámgyors keresés cikkszám, név vagy vonalkód alapján.
* **Vonalkód-olvasás:** A kamera képének folyamatos elemzése és a leolvasott kód azonnali feldolgozása.
* **Készletmódosítás:** Mennyiségek korrekciója, sérült termékek leírása közvetlenül a polcok mellett.
* **Offline írási sor (Sync Queue):** Hálózati hiba esetén a beolvasások lokálisan tárolódnak, majd a kapcsolat helyreállásakor szinkronizálódnak.
* **Raktáros Jogosultságok:** Egyszerűsített felület PIN-kódos vagy ujjlenyomatos gyors belépéssel.

## 🏗️ Architektúra és Technológiák
* **Olvasó:** `mobile_scanner` vagy Google ML Kit csomag a gyors kódleolvasáshoz.
* **Helyi adat:** Hive adatbázis a szupergyors íráshoz és az offline tranzakciós sor tárolásához.
* **Tesztelés:** Szigorú egységtesztek a szinkronizációs és konfliktuskezelési logika lefedésére.