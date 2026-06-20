# 6. nap — Column, Row és Container widgetek

Megtanuljuk a legalapvetőbb elrendezési (layout) widgetek használatát. A Column függőlegesen, a Row vízszintesen helyezi el a gyerekeket. A Container dekorálható, méretezhető, margókkal és paddinggel látható el.

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
Container(
  padding: const EdgeInsets.all(16.0),
  margin: const EdgeInsets.all(8.0),
  decoration: BoxDecoration(
    color: Colors.blue.shade100,
    borderRadius: BorderRadius.circular(12),
  ),
  child: const Column(
    mainAxisSize: MainAxisSize.min,
    children: [
      Text('Főcím', style: TextStyle(fontWeight: FontWeight.bold)),
      Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text('Bal oldal'),
          Text('Jobb oldal'),
        ],
      ),
    ],
  ),
)
```

---

## 🛠️ Napi Gyakorlat
> [!IMPORTANT]
> A programozást nem lehet elméletben megtanulni. A mai gyakorlati feladatod a következő:
>
> **Feladat:** Készíts egy profil kártyát, ahol bal oldalon egy színes ikon látható, tőle jobbra pedig egymás alatt a felhasználó neve és munkaköre.

---

> [!TIP]
> **Profi tipp:** Futtasd rendszeresen a `dart format .` parancsot a terminálból, hogy a kódod elrendezése mindig megfeleljen a Dart hivatalos irányelveinek.