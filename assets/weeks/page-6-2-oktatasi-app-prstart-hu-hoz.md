# 6.2 Oktatási app prstart.hu-hoz

Ez az alkalmazás a prstart.hu e-learning és LMS platformjához kapcsolódó mobil kliens. Célja, hogy a tanulók bárhol, akár utazás közben, offline is hozzáférjenek a kurzusaikhoz és elvégezhessék a leckéket.

## 🎯 Fő Funkciók
* **Kurzusok és Tantárgyak:** A felvett kurzusok listája, tematikus modulok és leckék fája.
* **Offline Lecke mentés:** Videók és szöveges tananyagok letöltése helyi tárhelyre offline tanuláshoz.
* **Interaktív Kvízek:** Leckék utáni feleletválasztós és párosítós tesztek kitöltése azonnali kiértékeléssel.
* **Fejlődési Statisztikák:** Vizuális statisztika a haladásról, napi célok kitűzése és jelvények (gamifikáció).
* **Gyerekbarát UI:** Letisztult, nagy kontrasztú, modern dizájn mikro-animációkkal.

## 🏗️ Architektúra és Technológiák
* **Navigáció:** GoRouter nested navigation (ShellRoute) a tabos alsó menürendszerhez.
* **UI elemek:** Lottie animációk a sikeres kvízek ünneplésére, Shimmer a betöltési állapotokhoz.
* **Adattárolás:** SQLite/Drift a tanulói eredmények és leckestátuszok helyi vezetésére.