# 16. nap — Login UI tervezése

Egy modern, esztétikus bejelentkező felületet építünk fel. Használunk lekerekítéseket, árnyékokat, egyedi színpalettát és validálható form mezőket.

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
Form(
  key: _formKey,
  child: Column(
    children: [
      TextFormField(
        validator: (v) => v!.isEmpty ? 'Töltsd ki!' : null,
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
> **Feladat:** Tervezd meg a login képernyő felületét, amely tartalmazzon egy logó helyőrzőt, email és jelszó mezőket, valamint egy 'Bejelentkezés' és 'Elfelejtett jelszó' gombot.

---

> [!TIP]
> **Profi tipp:** Futtasd rendszeresen a `dart format .` parancsot a terminálból, hogy a kódod elrendezése mindig megfeleljen a Dart hivatalos irányelveinek.