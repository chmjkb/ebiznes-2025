### Exercise 1 
[Docker Hub](https://hub.docker.com/r/chmjkb/ebiznes-2025-ex1)

[Kod](https://github.com/chmjkb/ebiznes-2025/tree/main/EX1)

3.0 - Obraz ubuntu z Pythonem w wersji 3.10 - ✅

3.5 - Obraz ubuntu:24.02 z Javą w wersji 8 oraz Kotlinem - ✅

4.0 - Do powyższego należy dodać najnowszego Gradle’a oraz paczkę JDBC - SQLite w ramach projektu na Gradle (build.gradle) - ✅

4.5 - Stworzyć przykład typu HelloWorld oraz uruchomienie aplikacji przez CMD oraz gradle - ✅

5.0 - Dodać konfigurację docker-compose - ✅

### Exercise 2
[Docker Hub](https://hub.docker.com/repository/docker/chmjkb/ebiznes-2025-ex2/general)

[Kod](https://github.com/chmjkb/ebiznes-2025/tree/main/EX2)

3.0 - Należy stworzyć kontroler do Produktów - ✅ - [Commit](https://github.com/chmjkb/ebiznes-2025/commit/48c7d4f2b9d434866b1b5c45d8536f4eea16b879)

3.5 - Do kontrolera należy stworzyć endpointy zgodnie z CRUD - dane
pobierane z listy - ✅ - [Commit](https://github.com/chmjkb/ebiznes-2025/commit/48c7d4f2b9d434866b1b5c45d8536f4eea16b879)

4.0 - Należy stworzyć kontrolery do Kategorii oraz Koszyka + endpointy
zgodnie z CRUD - ✅ - [Commit](https://github.com/chmjkb/ebiznes-2025/commit/1a3c95ce7b5458afeaf8d27b5258da0f2cfbaa5d)

4.5 - Należy aplikację uruchomić na dockerze (stworzyć obraz) oraz dodać
skrypt uruchamiający aplikację via ngrok - ✅ - [Commit](https://github.com/chmjkb/ebiznes-2025/commit/4fc8465492b748d541e165789fb7315d59693104)

5.0 - Należy dodać konfigurację CORS dla dwóch hostów dla metod CRUD - ✅ - [Commit](https://github.com/chmjkb/ebiznes-2025/commit/8d30187d89dc7249c0086dc739ef7c46f2e1d68f)

### Exercise 3

[Kod](https://github.com/chmjkb/ebiznes-2025/tree/main/EX3)

3.0 - Należy stworzyć aplikację kliencką w Kotlinie we frameworku Ktor, która pozwala na przesyłanie wiadomości na platformę Discord - ✅ - [Commit](https://github.com/chmjkb/ebiznes-2025/commit/59bdb930aa8f24476103f82771ce894072cf37d7)

3.5 - Aplikacja jest w stanie odbierać wiadomości użytkowników z platformy Discord skierowane do aplikacji (bota) - ✅ - [Commit](https://github.com/chmjkb/ebiznes-2025/commit/5bdd5759f5afc1c5421b18103c41331d3bfd953a)

4.0 - Zwróci listę kategorii na określone żądanie użytkownika - ❌

4.5 - Zwróci listę produktów wg żądanej kategorii - ❌

5.0 - Aplikacja obsłuży dodatkowo jedną z platform: Slack, Messenger - ❌

### Exercise 4
3.0 - Należy stworzyć aplikację we frameworki echo w j. Go, która będzie miała kontroler Produktów zgodny z CRUD - ✅ - [Commit](https://github.com/chmjkb/ebiznes-2025/commit/37e12440648e7e574ba2f804cc9cb204f2f3bdab)

3.5 - Należy stworzyć model Produktów wykorzystując gorm oraz wykorzystać model do obsługi produktów (CRUD) w kontrolerze (zamiast listy) - ✅ - [Commit](https://github.com/chmjkb/ebiznes-2025/commit/37e12440648e7e574ba2f804cc9cb204f2f3bdab)

4.0 - Należy dodać model Koszyka oraz dodać odpowiedni endpoint - ❌

4.5 - Należy stworzyć model kategorii i dodać relację między kategorią, a produktem - ❌

5.0 - pogrupować zapytania w gorm’owe scope'y - ❌

### Exercise 5
3.0 - W ramach projektu należy stworzyć dwa komponenty: Produkty oraz Płatności. Płatności powinny wysyłać do aplikacji serwerowej dane, a w Produktach powinniśmy pobierać dane o produktach z aplikacji serwerowej - ✅ - [Commit](https://github.com/chmjkb/ebiznes-2025/commit/ff5aa8ccfb9c9c8011d9a5e54b7fcdac916522fb)

3.5 - Należy dodać Koszyk wraz z widokiem; należy wykorzystać routing - ✅ - [Commit](https://github.com/chmjkb/ebiznes-2025/commit/11d8257d069292d1d96e1c357d44ca182b0b8433)

4.0 - Dane pomiędzy wszystkimi komponentami powinny być przesyłane za pomocą React hooks - ✅ - [Commit](https://github.com/chmjkb/ebiznes-2025/commit/11d8257d069292d1d96e1c357d44ca182b0b8433)

4.5 - Należy dodać skrypt uruchamiający aplikację serwerową oraz kliencką na dockerze via docker-compose - ✅ - [Commit](https://github.com/chmjkb/ebiznes-2025/commit/7e0e24cfa12c3070c6fedfe5f39a57ba337d2f0f)

5.0 - Należy wykorzystać axios’a oraz dodać nagłówki pod CORS - ✅ - [Commit](https://github.com/chmjkb/ebiznes-2025/commit/7e0e24cfa12c3070c6fedfe5f39a57ba337d2f0f)

### Exercise 6

Zadanie 6 Testy
Należy stworzyć 20 przypadków testowych w jednym z rozwiązań:

- Cypress JS (JS)
- Selenium (Kotlin, Python, Java, JS, Go, Scala)

Testy mają w sumie zawierać minimum 50 asercji (3.5). Mają również
uruchamiać się na platformie Browserstack (5.0). Proszę pamiętać o
stworzeniu darmowego konta via https://education.github.com/pack.

3.0 Należy stworzyć 20 przypadków testowych w CypressJS lub Selenium
(Kotlin, Python, Java, JS, Go, Scala)
3.5 Należy rozszerzyć testy funkcjonalne, aby zawierały minimum 50
asercji
4.0 Należy stworzyć testy jednostkowe do wybranego wcześniejszego
projektu z minimum 50 asercjami
4.5 Należy dodać testy API, należy pokryć wszystkie endpointy z
minimum jednym scenariuszem negatywnym per endpoint
5.0 Należy uruchomić testy funkcjonalne na Browserstacku