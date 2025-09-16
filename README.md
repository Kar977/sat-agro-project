# SatAgro Project

## Instalacja i konfiguracja

1. **Sklonuj repozytorium**
```bash git clone git@github.com:Kar977/sat-agro-project.git ```
2. **Wykonaj migracje do db***
```bash python manage.py migrate```
3. **Pobierz ostrzeżenia meteorologiczne z IMGW**
```python manage.py sync_warning```
4. ***Dodaj dane o powiatach z WFS Geoportalu***
- Wejdź na: Państwowy Rejestr Granic - Jednostki Terytorialne
- Wybierz obiekt: A02_Granice_powiatow
- Zapisz dane dla wybranego powiatu
- Uruchom komendę importu:
  ```python manage.py import_county path/to/file.gml --teryt 'teryt_nbr' --name "County Name"```
5. ***Sprawdź ostrzeżenia dla danej lokalizacji***
  ```Sprawdź ostrzeżenia dla danej lokalizacji```
