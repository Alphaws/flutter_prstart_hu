# 4. szint — Auth

A vizsga fókuszában a felhasználói beléptetés, a tokenek biztonságos tárolása és a védett útvonalak (Protected Routes) kezelése áll.

## 🎯 Vizsga Feladatok
Valósítsd meg az alábbi biztonsági modult:
1. **Bejelentkező oldal:** Email és jelszó mezők validációval, hibaüzenetek megjelenítésével.
2. **Secure Token storage:** Sikeres bejelentkezés után a kapott JWT tokent mentsd el a `flutter_secure_storage` csomaggal.
3. **Protected Route:** Ha van mentett érvényes token, az app induláskor azonnal vigye a felhasználót a védett profil oldalra.
4. **Kijelentkezés:** Törölje a mentett tokent a storage-ból és vigye vissza a felhasználót a bejelentkező felületre.

## 🔍 Értékelési Szempontok
* A token soha nem kerül sima (nem titkosított) Shared Preferences-be.
* A nem hitelesített felhasználók semmilyen trükkel nem érhetik el a védett profil oldalt.