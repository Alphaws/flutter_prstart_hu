# 6.3 Okosotthon mobil app

Az okosotthon alkalmazás egy modern, valós idejű IoT (Internet of Things) vezérlőfelület. Lehetővé teszi a lakásban található eszközök (lámpák, termosztátok, kamerák) megtekintését és vezérlését.

## 🎯 Fő Funkciók
* **Szobák és Csoportok:** Eszközök csoportosítása helyiségek (Nappali, Konyha stb.) szerint.
* **Valós idejű Kapcsolók:** Eszközök státuszának azonnali módosítása és visszajelzése.
* **Fogyasztási Statisztikák:** Dinamikus grafikonok a ház energia- és vízfelhasználásáról.
* **Biztonsági Kamerák:** IP kamerák RTSP streamjének alacsony késleltetésű megjelenítése.
* **MQTT / WebSocket integráció:** Kétirányú, valós idejű adatkapcsolat az otthoni szerverrel.

## 🏗️ Architektúra és Technológiák
* **Állapotkezelés:** BLoC minta az eseményalapú állapotváltások (pl. lámpa felkapcsolás gombnyomásra) precíz modellezésére.
* **Hálózat:** Native WebSocket és MQTT kliensek integrálása a Flutter eseményfolyamokba (Streams).
* **UI:** CustomPainter az egyedi termosztát szabályozó tárcsa megrajzolásához.