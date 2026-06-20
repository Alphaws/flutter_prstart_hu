# 25. nap — Theme alapok és ThemeData

Megtanuljuk az alkalmazás színeit, betűtípusait és formáit globálisan konfigurálni a ThemeData segítségével. Így az egész app arculatát egyetlen helyről vezérelhetjük.

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
MaterialApp(
  theme: ThemeData(
    primarySwatch: Colors.deepPurple,
    scaffoldBackgroundColor: Colors.grey.shade50,
    textTheme: const TextTheme(bodyLarge: TextStyle(fontSize: 18)),
  ),
)
```

---

## 🛠️ Napi Gyakorlat
> [!IMPORTANT]
> A programozást nem lehet elméletben megtanulni. A mai gyakorlati feladatod a következő:
>
> **Feladat:** Definiálj egy saját stílust a gombokra és a beviteli mezőkre globálisan az appod témájában, és figyeld meg a változást az összes képernyőn.

---

> [!TIP]
> **Profi tipp:** Futtasd rendszeresen a `dart format .` parancsot a terminálból, hogy a kódod elrendezése mindig megfeleljen a Dart hivatalos irányelveinek.