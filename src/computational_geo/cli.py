from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt

from computational_geo.computations.convex_hull import ConvexHullFinder
from computational_geo.computations.intersection_points import (
    IntersectionFinder,
    Point,
    Segment,
)

console = Console()


def _read_point(label: str) -> Point:
    """
    Wczytujemy wspolrzedne jednego punktu
    """
    x: int = IntPrompt.ask(f"  {label} x")
    y: int = IntPrompt.ask(f"  {label} y")
    return Point(x, y)


def _read_segment(label: str) -> Segment:
    """
    Wczytujemy oba konce odcinka
    """
    console.print(f"[bold]{label}[/bold]")
    return Segment(_read_point("początek"), _read_point("koniec"))


def _run_intersection() -> None:
    """
    Zadanie 1 - punkt przeciecia dwoch odcinkow
    """
    s1: Segment = _read_segment("Odcinek 1")
    s2: Segment = _read_segment("Odcinek 2")

    result: None | Point | Segment = IntersectionFinder.find_intersection(s1, s2)

    if result is None:
        console.print(Panel("NIE — odcinki się nie przecinają.", style="red"))
    elif isinstance(result, Point):
        console.print(
            Panel(
                f"TAK — przecięcie jest punktem.\nWspółrzędne: ({result.X}, {result.Y})",
                style="green",
            )
        )
    else:
        console.print(
            Panel(
                "TAK — przecięcie jest odcinkiem.\n"
                f"Końce: ({result.p1.X}, {result.p1.Y}) → "
                f"({result.p2.X}, {result.p2.Y})",
                style="green",
            )
        )


def _run_hull() -> None:
    """
    Zadanie 2 - otoczka wypukla czterech punktow
    """
    points: list[Point] = [_read_point(f"Punkt {i}") for i in range(1, 5)]

    hull: list[Point] = ConvexHullFinder.find_hull(points)
    kind: str = ConvexHullFinder.classify(hull)
    vertices: str = " → ".join(f"({p.X}, {p.Y})" for p in hull)

    console.print(
        Panel(
            f"Otoczka wypukła to {kind}.\nKolejne wierzchołki: {vertices}",
            style="green",
        )
    )


def main() -> None:
    console.print(Panel("Geometria obliczeniowa", style="bold cyan"))
    console.print("1. Punkt przecięcia dwóch odcinków")
    console.print("2. Otoczka wypukła czterech punktów")

    choice: str = Prompt.ask("Wybierz zadanie", choices=["1", "2"], default="1")

    if choice == "1":
        _run_intersection()
    else:
        _run_hull()
