# Projekt

A Flutter projektek indításának és tesztkörnyezetben való futtatásának legalapvetőbb parancsai.

## 🛠️ Parancsok:
* **Projekt generálása:**
  ```bash
  flutter create --org hu.prstart my_app
  ```
  A `--org` paraméter határozza meg a csomagnevet (package name), ami a Play Áruházban egyedi azonosító lesz (pl. `hu.prstart.my_app`).

* **Alkalmazás indítása:**
  ```bash
  flutter run
  ```
  Elindítja az alkalmazást a kiválasztott emulátoron vagy telefonon debug módban, támogatva a Hot Reload funkciót.

* **Futtatás adott eszközön:**
  ```bash
  flutter run -d <device_id>
  ```