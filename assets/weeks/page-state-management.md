# State management

Az állapotkezelés határozza meg, hogyan áramlik az adat az alkalmazásodban, és mikor épülnek újra a felhasználói felület elemei.

## 📦 Ajánlott Csomagok:
1. **`flutter_riverpod` (Modern / Ajánlott):** Tiszta, típusbiztos, nem függ a BuildContext-től, kiválóan tesztelhető és támogatja a Dependency Injection-t.
2. **`flutter_bloc` / `bloc` (Enterprise):** Esemény-vezérelt (Event-State) architektúra, szigorúan strukturált, nagy csapatok számára ideális.
3. **`provider` (Egyszerűbb appokhoz):** A klasszikus állapotkezelő, jó a ChangeNotifier alapú mintákhoz.

### Riverpod Példa:
```dart
// Állapot definiálása
final counterProvider = StateProvider<int>((ref) => 0);

// Widgetben használat
class CounterWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    return ElevatedButton(
      onPressed: () => ref.read(counterProvider.notifier).state++,
      child: Text('Számláló: $count'),
    );
  }
}
```