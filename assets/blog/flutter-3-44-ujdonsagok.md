# Mi újság a Flutter 3.44-ben? Impeller Androidon, SwiftPM és a UI leválasztása

**Szerző:** PRSTART Blog  
**Dátum:** 2026-06-20  
**Téma:** Flutter Kiadási Újdonságok  

---

A Google kiadta a **Flutter 3.44**-es verzióját (és a hozzá kapcsolódó **Dart 3.12**-es SDK-t), amely a keretrendszer történetének egyik legjelentősebb infrastrukturális mérföldköve. Ez a frissítés radikálisan átalakítja azt, ahogyan az alkalmazásainkat építjük, rendereljük és hogyan kezeljük a csomagokat iOS-en.

Nézzük meg részletesen a legfontosabb újdonságokat és azt, hogy mit jelentenek ezek a napi fejlesztés során!

---

## 1. Az Impeller az alapértelmezett renderelő motor Androidon

Az iOS után a Flutter csapata elérte azt a szintet, hogy az **Impeller** grafikus motort éles, alapértelmezett állapotúvá tegye **Android** platformon is.

### Miért hatalmas dolog ez?
Korábban a Flutter a Skia motort használta, amely futás közben (az első futáskor) fordította le a grafikus shadereket. Ez a telefonokon mikroszaggatásokat (úgynevezett "shader compilation jank"-et) okozott az animációk első indításakor.
Az Impeller ezzel szemben:
*   Előre lefordítja a shadereket (ahead-of-time compile) a build fázisban.
*   Konzisztens, stabil 60 FPS / 120 FPS renderelést biztosít az első pillanattól kezdve.
*   Kisebb memória-lábnyommal dolgozik és hatékonyabban használja a modern GPU API-kat (Vulkan és Metal).

Androidon a Flutter 3.44-től kezdve a régebbi Skia motor már csak fallback opcióként érhető el, a fejlesztőknek nem szükséges külön flaget megadniuk az Impeller használatához.

---

## 2. Viszlát CocoaPods! Érkezik a Swift Package Manager (SwiftPM)

Az Apple platformokra (iOS, macOS) való fejlesztés során a Flutter hosszú évekig a Ruby-alapú CocoaPods csomaggyűjtőt használta a natív pluginek kezelésére. Ez a fejlesztőknek rengeteg fejfájást okozott: Ruby verzióütközések, összetett és sérülékeny `Podfile` konfigurációk, valamint lassú build idők.

A Flutter 3.44-ben a **Swift Package Manager (SwiftPM)** vált az alapértelmezett natív függőségkezelővé az új iOS és macOS projekteknél!

### A SwiftPM előnyei:
*   Nincs szükség Ruby és CocoaPods telepítésére a gazdagépen.
*   Az Xcode natívan támogatja, így a build folyamat sokkal tisztább és stabilabb.
*   Gyorsabb tiszta build idők a hatékonyabb párhuzamos fordításnak köszönhetően.
*   Egyszerűbb konfiguráció közvetlenül az Xcode `.xcodeproj` struktúrán belül.

---

## 3. UI leválasztása a keretrendszerről (Framework Decoupling)

Egy meglepő, de stratégiailag rendkívül fontos változás a **Framework Decoupling** (keretrendszer-leválasztás) elindítása. 
Eddig a Material és Cupertino widget készletek szorosan be voltak építve magába a Flutter SDK-ba. Ha egy Material 3 widgeten javítottak a Google mérnökei, ahhoz a fejlesztőnek le kellett frissítenie a teljes Flutter SDK-t.

A 3.44-es verziótól kezdve a Google elkezdte leválasztani a vizuális komponenseket különálló, pub.dev csomagokká:
*   A jövőben a Material UI elemek a `material_ui` csomagban, a Cupertino (Apple stílusú) elemek pedig a `cupertino_ui` csomagban kapnak helyet.
*   **Mit jelent ez?** Az alap SDK magja (Engine, Rendering, Gestures) kisebb és gyorsabb lesz. A dizájnrendszerek (Material, Cupertino) pedig az SDK kiadási ciklusától függetlenül, sokkal gyorsabban és rugalmasabban fejlődhetnek.

---

## 4. Dart 3.12 és Web optimalizációk

A kiadással együtt érkező **Dart 3.12** főként a motorháztető alatti optimalizációkra fókuszál:
*   **Webes betöltési idő csökkentése:** A CanvasKit WebAssembly modul méretét és a betöltési inicializációt optimalizálták. A webes appok kezdőoldala így érezhetően gyorsabban jelenik meg.
*   **AI fejlesztőtámogatás:** A Dart compiler és az elemző eszközök új API-kat kaptak, amelyek segítik a kódgeneráló és mesterséges intelligenciával támogatott fejlesztőeszközök pontosabb működését.

---

## Összegzés

A Flutter 3.44 nem csupán új widgeteket hozott, hanem a platform stabilitását és jövőbeli karbantarthatóságát helyezte a középpontba. Az Impeller Android default és a SwiftPM bevezetése azonnali teljesítmény- és kényelmi javulást jelent minden fejlesztő számára.

> [!IMPORTANT]
> Ha új projektet indítasz, a Flutter 3.44 már alapból a SwiftPM függőségkezelést fogja használni. Meglévő projekteknél javasolt a migration guide átolvasása a zökkenőmentes átállás érdekében.
