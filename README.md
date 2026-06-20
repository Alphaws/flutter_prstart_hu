# 📘 flutter.prstart.hu – Flutter Tanulás Alapoktól a Profi Szintig

Ez a projekt a **Flutter mobilfejlesztés profi módon** teljes 24 hetes tananyagot feldolgozó interaktív e-learning weboldal forráskódja. A weboldal a helyi fejlesztői környezetben a [https://flutter.localhost](https://flutter.localhost) címen érhető el.

## 🚀 Fejlesztési környezet indítása

A projekt teljesen konténerizált, és a futtatásához mindössze Dockerre van szükség:

```bash
docker compose up -d --build
```

A weboldal a **Traefik** reverse proxyn keresztül kapja meg a kéréseket lokálisan.

---

## 📁 Projektstruktúra

- **`index.html`**: A weboldal alapváza, amely betölti a Prism.js (kódszínező) és a Marked.js (markdown feldolgozó) könyvtárakat.
- **`style.css`**: Premium Space-dark témájú, reszponzív stíluslap zökkenőmentes görgetéssel, üveg hatásokkal (glassmorphism) és animációkkal.
- **`script.js`**: A kliensoldali JavaScript motor, amely:
  - Lekéri az `assets/tananyag.md` tartalmát.
  - Dinamikusan generál egy interaktív, összecsukható oldalsávot a fejezetekből és leckékből.
  - Kezeli a leckék teljesítettségének jelölését és perzisztens mentését `localStorage`-be.
  - Végrehajtja a valós idejű keresést a teljes tananyagban.
  - Támogatja a sötét/világos mód váltást.
- **`assets/tananyag.md`**: A teljes 24 hetes elméleti és gyakorlati Flutter tananyag.
- **`docker-compose.yml`**: Docker szerviz beállítás és Traefik címkék (labels) a lokális routinghoz.
- **`nginx.conf`**: Nginx konfiguráció az SPA útválasztáshoz és statikus állományok kiszolgálásához.

---

## 🔧 Haladás mentése és keresés
A weboldal automatikusan követi, hol tartasz:
- Minden lecke mellett találsz egy pipát, amit bejelölve elmentheted a haladásodat.
- A fejlécben található keresősávval azonnal szűrheted a leckéket címek vagy tartalom alapján.

---
*Utolsó frissítés: 2026-06-20*
