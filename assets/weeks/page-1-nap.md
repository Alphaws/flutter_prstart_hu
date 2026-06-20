# 1. nap — Flutter telepítés és környezet beállítása

A mai nap célja a Flutter fejlesztői környezet teljes körű beállítása. Telepítjük a Flutter SDK-t, beállítjuk a környezeti változókat (PATH), és ellenőrizzük a rendszert a flutter doctor segítségével. Ezt követően konfiguráljuk a VS Code vagy Android Studio szerkesztőket a Dart és Flutter pluginekkel, majd elindítunk egy emulátort vagy fizikai eszközt.

---

## 📖 Elméleti Háttér és Koncepció
A mai napon a legfontosabb cél a témakör gyakorlati megvalósítása és elméleti tisztázása. A mobilfejlesztésben elengedhetetlen a tiszta szintaxis, a hatékony memóriakezelés és a platform-specifikus minták betartása.

### Kulcsfontosságú szempontok:
* **Strukturáltság:** Mindig válaszd szét a felületeket a logikától.
* **Tiszta kód:** Dart nyelven törekedj a deklaratív és könnyen olvasható elnevezésekre.
* **Hibamegelőzés:** Használj statikus elemzőket és kövesd a Flutter linter ajánlásait.

---

## 💻 Mintakód
Az alábbi kód bemutatja a mai nap legfőbb technológiai fókuszát. Másold be a projektedbe, és vizsgáld meg a működését!

```dart
# Telepítés ellenőrzése
flutter doctor -v

# Elérhető eszközök listázása
flutter devices
```

---

## 🛠️ Napi Gyakorlat
> [!IMPORTANT]
> A programozást nem lehet elméletben megtanulni. A mai gyakorlati feladatod a következő:
>
> **Feladat:** Futtasd le sikeresen a `flutter doctor` parancsot. Javíts ki minden hibát (Android toolchain licenc, VS Code kiterjesztés stb.), amíg minden lényeges pont zöld nem lesz.

---

> [!TIP]
> **Profi tipp:** Futtasd rendszeresen a `dart format .` parancsot a terminálból, hogy a kódod elrendezése mindig megfeleljen a Dart hivatalos irányelveinek.