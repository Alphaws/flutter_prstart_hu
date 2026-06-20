# 19. hét — Animációk

## Cél
A lecke célja, hogy elsajátítsd a Flutter animációs motorjának használatát. Megtanulod a különbséget az implicit (automatikus) és explicit (teljes kontrollt biztosító) animációk között, megérted a `AnimationController`, `Tween` és `CurvedAnimation` fogalmát, és képes leszel olyan prémium minőségű, interaktív mobil UI-t készíteni, amely áttűnésekkel, egyedi visszajelzésekkel és sima navigációs átmenetekkel (`Hero`) nyűgözi le a felhasználót.

---

## Elmélet

### Miért fontosak az animációk?
Az animációk nem csupán dekorációs elemek. A jó animációk:
- **Kontextust adnak:** Segítenek a felhasználónak megérteni, honnan jött egy elem és hová tűnt (pl. egy oldalirányú suhintás).
- **Visszajelzést biztosítanak:** A gombok mikro-interakciói jelzik, hogy a rendszer regisztrálta a kattintást.
- **Prémium érzet:** A folyamatos, 60 vagy 120 FPS sebességű, finom fizikai görbéket követő animációk teszik az alkalmazást professzionálissá.

### Animációk típusai Flutterben

#### 1. Implicit animációk (Implicit Animations)
Ezek a legegyszerűbb animációk, ahol a Flutter maga kezeli az átmenetet az állapotok között. Ha megváltoztatunk egy értéket (pl. szélesség, magasság, szín), a Flutter automatikusan kiszámítja a köztes képkockákat.
- **Példák:** `AnimatedContainer`, `AnimatedOpacity`, `AnimatedPadding`, `AnimatedAlign`, `AnimatedPositioned`.
- **Mikor használjuk?** Ha egyszerű, egyirányú átmenetet szeretnénk létrehozni (pl. egy gomb színe pirosról kékre vált kattintáskor) anélkül, hogy bonyolult kontrollereket akarnánk írni.

#### 2. Explicit animációk (Explicit Animations)
Teljes körű ellenőrzést biztosítanak az animáció felett (indítás, leállítás, visszafelé lejátszás, végtelen ismétlés). Ehhez már több komponens összehangolására van szükség:
- **`AnimationController`:** Vezérli az animációt. Megadjuk neki az időtartamot (`Duration`), és ő generálja az értékeket 0.0 és 1.0 között a megadott idő alatt.
- **`TickerProvider` (Mixin):** Szinkronizálja az animációt a telefon kijelzőjének frissítési rátájával (refresh rate). A widget State osztályához hozzá kell adni a `SingleTickerProviderStateMixin` (ha egy kontrollerünk van) vagy a `TickerProviderStateMixin` (ha több) mixint.
- **`Tween` (Between):** Meghatározza a kezdő és végpont közötti tartományt. Mivel az `AnimationController` csak 0.0 és 1.0 között számlál, a `Tween` segítségével ezt lefordíthatjuk más értékekre (pl. `ColorTween` a piros és kék szín között, vagy `Tween<Offset>` koordináták között).
- **`CurvedAnimation`:** Meghatározza az átmenet sebességi görbéjét (pl. `Curves.bounceOut` a rugózó hatáshoz, vagy `Curves.easeIn` a fokozatos gyorsuláshoz).

### A Hero widget
A `Hero` widget segítségével két különálló képernyő azonos elemei között tudunk látványos repülési átmenetet (flight transition) létrehozni. Ha a listában van egy kis termékképünk, és a részletek oldalon egy nagy fejléc képünk, ha mindkettőt egy azonos `tag`-gel rendelkező `Hero` widgetbe csomagoljuk, a Flutter a navigáció során automatikusan megnöveli és átúsztatja a képet az új pozíciójára.

---

## Kódpéldák

Az alábbiakban egy teljes, compilable példát láthatsz egy explicit animációra. Egy kártyát fogunk lerenderelni, ami a képernyő megjelenésekor alulról finoman felúszik és felerősödik az opacitása.

### Explicit animáció kódja (`lib/ui/animated_card.dart`)

```dart
import 'package:flutter/material.dart';

class FadeSlideCard extends StatefulWidget {
  final String title;
  final String description;

  const FadeSlideCard({
    super.key,
    required this.title,
    required this.description,
  });

  @override
  State<FadeSlideCard> createState() => _FadeSlideCardState();
}

// 1. SingleTickerProviderStateMixin hozzáadása a kijelző-szinkronizációhoz
class _FadeSlideCardState extends State<FadeSlideCard>
    with SingleTickerProviderStateMixin {
  
  late AnimationController _controller;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;

  @override
  void initState() {
    super.initState();

    // 2. Controller inicializálása 800 ms időtartammal
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    );

    // 3. Görbe hozzáadása az animációhoz
    final CurvedAnimation curvedAnimation = CurvedAnimation(
      parent: _controller,
      curve: Curves.easeOutBack, // Finom túllendülős, rugalmas görbe
    );

    // 4. Tween-ek definiálása
    // Opacitás: 0.0 (teljesen átlátszó) -> 1.0 (teljesen látható)
    _fadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(curvedAnimation);

    // Csúszás: Alulról (y: 0.35 szorzóval lejjebb) -> Eredeti pozíció (0, 0)
    _slideAnimation = Tween<Offset>(
      begin: const Offset(0.0, 0.35),
      end: Offset.zero,
    ).animate(curvedAnimation);

    // 5. Animáció elindítása
    _controller.forward();
  }

  @override
  void dispose() {
    // 6. Nagyon fontos az erőforrások felszabadítása!
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // 7. A Transition widgetek segítségével építjük fel a fát
    return FadeTransition(
      opacity: _fadeAnimation,
      child: SlideTransition(
        position: _slideAnimation,
        child: Card(
          elevation: 6,
          shape: RoundedRectangleBorder(
            border_radius: BorderRadius.circular(16),
          ),
          child: Padding(
            padding: const EdgeInsets.all(20.0),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  widget.title,
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 10),
                Text(
                  widget.description,
                  style: const TextStyle(
                    fontSize: 14,
                    color: Colors.grey,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
```

---

## Gyakorlófeladatok & Megoldások

### 1. feladat: Animált Kártya méretezése (Implicit)
Készíts egy `HoverCard` widgetet. Ha a felhasználó rákattint a kártyára, a kártya magassága változzon meg 150-ről 220-ra, a háttérszíne pedig sötétkékről világoskékre implicit animációval.

#### Megoldás kódja (`lib/ui/hover_card.dart`)
```dart
import 'package:flutter/material.dart';

class HoverCard extends StatefulWidget {
  const HoverCard({super.key});

  @override
  State<HoverCard> createState() => _HoverCardState();
}

class _HoverCardState extends State<HoverCard> {
  bool _isExpanded = false;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        setState(() {
          _isExpanded = !_isExpanded;
        });
      },
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 400),
        curve: Curves.easeInOut,
        width: 200,
        height: _isExpanded ? 220.0 : 150.0,
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: _isExpanded ? Colors.lightBlue : Colors.indigo,
          border_radius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.2),
              blurRadius: 10,
              offset: const Offset(0, 5),
            )
          ],
        ),
        child: Center(
          child: Text(
            _isExpanded ? 'Kiterjesztve!' : 'Kattints rám!',
            style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
          ),
        ),
      ),
    );
  }
}
```

---

### 2. feladat: Hero transition megvalósítása
Hozz létre egy lista nézetet és egy részletező nézetet. A listában szereplő kör alakú profilkép a részletező oldal megnyitásakor repüljön át a képernyő tetejére egy nagy kör alakú képpé.

#### Megoldás kódja (`lib/ui/hero_demo.dart`)
```dart
import 'package:flutter/material.dart';

class HeroListScreen extends StatelessWidget {
  const HeroListScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Felhasználók')),
      body: ListView(
        children: [
          ListTile(
            leading: const Hero(
              tag: 'avatar_user_1',
              child: CircleAvatar(
                backgroundColor: Colors.blue,
                child: Icon(Icons.person, color: Colors.white),
              ),
            ),
            title: const Text('Kovács János'),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const HeroDetailScreen()),
              );
            },
          )
        ],
      ),
    );
  }
}

class HeroDetailScreen extends StatelessWidget {
  const HeroDetailScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Részletek')),
      body: Center(
        child: Column(
          children: [
            const SizedBox(height: 40),
            const Hero(
              tag: 'avatar_user_1',
              child: CircleAvatar(
                radius: 80,
                backgroundColor: Colors.blue,
                child: Icon(Icons.person, size: 80, color: Colors.white),
              ),
            ),
            const SizedBox(height: 20),
            const Text(
              'Kovács János',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            )
          ],
        ),
      ),
    );
  }
}
```

---

## Heti Mini Projekt: Animált Recept App

A heti mini projekt egy látványos receptgyűjtő alkalmazás (`AnimatedRecipeApp`), amely bemutatja az implicit, explicit és Hero animációk együttes használatát.
Funkciók:
1. **Beúszó recept lista:** Az app indulásakor a receptek kártyái egyenként, eltolva (staggered animation) úsznak be a képernyő aljáról.
2. **Hero kép-repülés:** Egy recept kártyájára kattintva a recept képe egy látványos Hero animációval repül át a részletező képernyő tetejére.
3. **Implicit kedvenc gomb:** A részletező oldalon lévő szív gombra kattintva a szív megnő, majd visszaáll az eredeti méretére implicit méretváltoztatással (`AnimatedScale`).

### Recept App Kódja (`lib/recipe_app.dart`)

```dart
import 'package:flutter/material.dart';

class Recipe {
  final String id;
  final String title;
  final String imageUrl;
  final List<String> ingredients;

  Recipe({
    required this.id,
    required this.title,
    required this.imageUrl,
    required this.ingredients,
  });
}

class AnimatedRecipeApp extends StatelessWidget {
  const AnimatedRecipeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData.dark(),
      home: const RecipeListScreen(),
    );
  }
}

class RecipeListScreen extends StatefulWidget {
  const RecipeListScreen({super.key});

  @override
  State<RecipeListScreen> createState() => _RecipeListScreenState();
}

class _RecipeListScreenState extends State<RecipeListScreen>
    with SingleTickerProviderStateMixin {
  
  late AnimationController _listController;
  final List<Recipe> _recipes = [
    Recipe(
      id: 'r1',
      title: 'Olasz Spagetti',
      imageUrl: 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8',
      ingredients: ['Tészta', 'Paradicsomszósz', 'Darált hús', 'Bazsalikom', 'Parmezán'],
    ),
    Recipe(
      id: 'r2',
      title: 'Amerikai palacsinta',
      imageUrl: 'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445',
      ingredients: ['Liszt', 'Tej', 'Tojás', 'Cukor', 'Juharszirup'],
    ),
  ];

  @override
  void initState() {
    super.initState();
    _listController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1000),
    );
    _listController.forward();
  }

  @override
  void dispose() {
    _listController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Prémium Receptek')),
      body: ListView.builder(
        itemCount: _recipes.length,
        itemBuilder: (context, index) {
          // Elcsúsztatott (staggered) animáció számolása
          final double start = index * 0.25;
          final double end = start + 0.5;

          final Animation<double> cardAnimation = Tween<double>(
            begin: 0.0,
            end: 1.0,
          ).animate(
            CurvedAnimation(
              parent: _listController,
              curve: Interval(start, end, curve: Curves.easeOut),
            ),
          );

          final Animation<Offset> slideAnimation = Tween<Offset>(
            begin: const Offset(0.0, 0.5),
            end: Offset.zero,
          ).animate(
            CurvedAnimation(
              parent: _listController,
              curve: Interval(start, end, curve: Curves.easeOutBack),
            ),
          );

          final recipe = _recipes[index];

          return AnimatedBuilder(
            animation: _listController,
            builder: (context, child) {
              return Opacity(
                opacity: cardAnimation.value,
                child: SlideTransition(
                  position: slideAnimation,
                  child: child,
                ),
              );
            },
            child: GestureDetector(
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => RecipeDetailScreen(recipe: recipe),
                  ),
                );
              },
              child: Card(
                margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                clipBehavior: Clip.antiAlias,
                shape: RoundedRectangleBorder(
                  border_radius: BorderRadius.circular(16),
                ),
                child: Column(
                  children: [
                    Hero(
                      tag: 'recipe_img_${recipe.id}',
                      child: Container(
                        height: 180,
                        color: Colors.grey.shade800,
                        child: const Center(
                          child: Icon(Icons.restaurant_menu, size: 64, color: Colors.white),
                        ),
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            recipe.title,
                            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                          ),
                          const Icon(Icons.arrow_forward_ios, size: 16),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}

class RecipeDetailScreen extends StatefulWidget {
  final Recipe recipe;

  const RecipeDetailScreen({super.key, required this.recipe});

  @override
  State<RecipeDetailScreen> createState() => _RecipeDetailScreenState();
}

class _RecipeDetailScreenState extends State<RecipeDetailScreen> {
  bool _isFavorite = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.recipe.title)),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Hero(
              tag: 'recipe_img_${widget.recipe.id}',
              child: Container(
                height: 250,
                color: Colors.grey.shade700,
                child: const Center(
                  child: Icon(Icons.restaurant_menu, size: 120, color: Colors.white),
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(20.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    widget.recipe.title,
                    style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  GestureDetector(
                    onTap: () {
                      setState(() {
                        _isFavorite = !_isFavorite;
                      });
                    },
                    child: AnimatedScale(
                      scale: _isFavorite ? 1.4 : 1.0,
                      duration: const Duration(milliseconds: 200),
                      curve: Curves.bounceOut,
                      child: Icon(
                        _isFavorite ? Icons.favorite : Icons.favorite_border,
                        color: _isFavorite ? Colors.red : Colors.grey,
                        size: 32,
                      ),
                    ),
                  )
                ],
              ),
            ),
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 20.0),
              child: Text(
                'Hozzávalók:',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
            ),
            const SizedBox(height: 10),
            ...widget.recipe.ingredients.map(
              (ing) => Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20.0, vertical: 4),
                child: Row(
                  children: [
                    const Icon(Icons.check_circle_outline, color: Colors.green, size: 18),
                    const SizedBox(width: 10),
                    Text(ing, style: const TextStyle(fontSize: 16)),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## Heti Ellenőrző Kérdések

### 1. Mikor használjunk implicit animációt explicit helyett?
Implicit animációt használunk, ha az átmenet egyszerű állapotalapú változás (pl. gombnyomásra megnövő méret, elhalványuló szöveg) és nem igényel komplex vezérlést (mint az ismétlés, szüneteltetés vagy más animációk láncolása). Az implicit animációk nem igényelnek mixineket és `dispose()` hívásokat, így a kód sokkal rövidebb és egyszerűbb marad.

### 2. Mire való a SingleTickerProviderStateMixin és miért kell meghívni a controller dispose() metódusát?
- A `SingleTickerProviderStateMixin` szolgáltatja a "Tick" (órajelforrás) jelet az `AnimationController` számára. Minden kijelző frissítéskor (pl. 60Hz-en másodpercenként 60-szor) küld egy jelet a kontrollernek, hogy számítsa ki a következő animációs értéket.
- A `dispose()` meghívása kötelező, mert ha a kontroller megmarad a memóriában a widget törlése után, a ticker továbbra is folyamatosan küldené a jeleket, ami komoly memóriaszivárgáshoz (memory leak) és felesleges processzorterheléshez vezet.

### 3. Hogyan optimalizálhatjuk az explicit animációkat a teljesítmény növelése érdekében?
- Kerüljük a `setState` hívásokat a ticker minden lépésénél, mert az újraépíti az egész widgetet.
- Használjuk az `AnimatedBuilder`-t vagy a `RepaintBoundary` widgetet. Az `AnimatedBuilder` segítségével csak az animáció által közvetlenül érintett al-widgeteket építjük újra, míg a `RepaintBoundary` elszigeteli a renderelést, így az animált rész nem kényszeríti rá az alatta lévő statikus rétegeket a felesleges újrarajzolásra.

### 4. Mi a különbség a Tween és a CurvedAnimation között?
- A `Tween` a bemeneti és kimeneti értékek tartományát határozza meg (pl. 0 foktól 180 fokig terjedő forgatás, vagy feketétől sárgáig terjedő színátmenet).
- A `CurvedAnimation` az animáció sebességváltozását (dinamikáját) írja le az idő múlásával. Ezzel érhető el, hogy az animáció ne egyenletes sebességgel fusson, hanem gyorsuljon, lassuljon vagy rugózzon a fizikai törvényeknek megfelelően.

### 5. Hogyan lehet az animációkat teljesen kikapcsolni a tesztek futása alatt?
A Flutter tesztelési keretrendszere alapértelmezetten virtuális időt használ. Widget tesztekben a teszt lefutása alatt az animációk automatikusan leegyszerűsödnek vagy azonnal a végállapotukra ugranak (nem kell kivárnunk a valódi másodperceket). Integrációs tesztekben a `timeDilation` változó 1.0-án hagyható, vagy a teszt binding segítségével kikapcsolhatóak a vizuális átmenetek, hogy a tesztek stabilabbak és gyorsabbak legyenek.
