# Alap branch modell

A Git verziókövető strukturált használata elengedhetetlen a biztonságos kódfejlesztéshez és a csapatmunkához.

## 🌲 Ág Szerkezet (Branches):
* **`main`:** A stabil, éles ág. Csak alaposan letesztelt, kiadásra kész kód kerülhet ide.
* **`dev` / `development`:** A fejlesztési főág. A fejlesztők ide integrálják az elkészült funkciókat.
* **`feature/*`:** Új funkciók fejlesztésére szolgáló ideiglenes ágak (pl. `feature/login-screen`).
* **`fix/*` / `bugfix/*`:** Hibajavító ágak (pl. `fix/empty-list-crash`).

## 🔄 Fejlesztési Folyamat:
1. Hozz létre egy új ágat a dev ágból: `git checkout -b feature/my-feature dev`
2. Kódolj, majd commitolj rendszeresen.
3. Küldd be a kódot és nyiss egy Pull Request-et (PR) a dev ágra a kód felülvizsgálatához (Code Review).