# 1. szint — Alap

Ezen a szinten azt ellenőrizzük, hogy sikerült-e elsajátítanod a Dart nyelv alapvető szintaxisát és a legegyszerűbb helyi perzisztens tárolást.

## 🎯 Vizsga Feladatok
Készíts egy egyképernyős Flutter alkalmazást, amely:
1. **Név bekérése:** Tartalmaz egy TextField-et, ahol a felhasználó megadhatja a nevét.
2. **Mentés lokálisan:** Egy 'Mentés' gomb megnyomására elmenti ezt a nevet helyben `shared_preferences` segítségével.
3. **Betöltés induláskor:** Az alkalmazás újraindítása után automatikusan beolvassa a mentett nevet és megjeleníti egy üdvözlő kártyán.
4. **Theme váltás:** Tartalmaz egy kapcsolót (Switch) a sötét és világos mód kézi váltásához.

## 🔍 Értékelési Szempontok
* A kód tiszta és mentes a `flutter analyze` figyelmeztetésektől.
* A név mentése és betöltése hibátlanul lefut üres értékek esetén is.
* A sötét mód azonnal érvényesül az egész felületen.