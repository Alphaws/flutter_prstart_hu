# 3. szint — API

Ez a szint azt méri fel, hogyan tudsz összekötni egy mobilalkalmazást egy távoli REST API backenddel, és hogyan kezeled az aszinkron folyamatokat.

## 🎯 Vizsga Feladatok
Készíts egy alkalmazást, amely:
1. **Adatok lekérése:** Adatokat kér le egy szabadon választható publikus JSON API-ból (pl. JSONPlaceholder vagy saját backend).
2. **Három állapot kezelése:**
   * **Loading:** Amíg az adat töltődik, egy Shimmer vagy CircularProgressIndicator látható.
   * **Success:** Sikeres lekéréskor a lista elemei szépen megjelennek egy kártyás listában.
   * **Error:** Hálózati hiba vagy rossz válasz esetén egy hibaüzenet és egy 'Újrapróbálás' (Retry) gomb látható.
3. **Frissítés:** Swipe-to-refresh (RefreshIndicator) támogatása a lista frissítésére.

## 🔍 Értékelési Szempontok
* Az API kérés aszinkron (`async/await`) módon fut le és nem blokkolja az UI szálat.
* A hálózati hibák (pl. offline állapot) nem okoznak app-összeomlást.