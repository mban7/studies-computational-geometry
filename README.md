# Geometria obliczeniowa

Dwa zadania: punkt przecięcia dwóch odcinków oraz otoczka wypukła czterech punktów.

## Jak uruchomić

**Krok 1: Zainstaluj `uv`** (jeśli nie masz)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Krok 2: Odpal w katalogu głównym projektu**

CLI (terminal):

```bash
uv run computational-geo
```

Aplikacja web (Streamlit):

```bash
uv run computational-geo-web
```

`uv` sam zainstaluje zależności przy pierwszym uruchomieniu.

## Testy

```bash
uv run pytest
```
