from matplotlib.figure import Figure

from computational_geo.computations.intersection_points import Point, Segment

_POINT_COLOR = "#2563eb"
_SEGMENT_1_COLOR = "#2563eb"
_SEGMENT_2_COLOR = "#7c3aed"
_RESULT_COLOR = "#dc2626"
_HULL_COLOR = "#16a34a"
_HULL_FILL = "#16a34a22"


def _new_axes() -> tuple[Figure, "object"]:
    """
    Tworzymy figure z jednym, kwadratowym wykresem z siatka
    """
    fig = Figure(figsize=(5, 5), layout="constrained")
    ax = fig.add_subplot(111)
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.axhline(0, color="#94a3b8", linewidth=0.8)
    ax.axvline(0, color="#94a3b8", linewidth=0.8)
    return fig, ax


def _annotate(ax: "object", p: Point, color: str) -> None:
    """
    Podpisujemy punkt jego wspolrzednymi
    """
    ax.annotate(
        f"({p.X:g}, {p.Y:g})",
        (p.X, p.Y),
        textcoords="offset points",
        xytext=(6, 6),
        fontsize=8,
        color=color,
    )


def plot_intersection(
    s1: Segment, s2: Segment, result: None | Point | Segment
) -> Figure:
    """
    Rysujemy dwa odcinki i zaznaczamy wynik ich przeciecia
    """
    fig, ax = _new_axes()

    for seg, color, label in (
        (s1, _SEGMENT_1_COLOR, "Odcinek 1"),
        (s2, _SEGMENT_2_COLOR, "Odcinek 2"),
    ):
        ax.plot(
            [seg.p1.X, seg.p2.X],
            [seg.p1.Y, seg.p2.Y],
            color=color,
            marker="o",
            linewidth=2,
            label=label,
        )

    if isinstance(result, Point):
        ax.plot(
            result.X,
            result.Y,
            marker="*",
            markersize=16,
            color=_RESULT_COLOR,
            linestyle="none",
            label="Przecięcie",
            zorder=5,
        )
        _annotate(ax, result, _RESULT_COLOR)
    elif isinstance(result, Segment):
        ax.plot(
            [result.p1.X, result.p2.X],
            [result.p1.Y, result.p2.Y],
            color=_RESULT_COLOR,
            linewidth=4,
            alpha=0.7,
            label="Część wspólna",
            zorder=5,
        )

    ax.set_title("Przecięcie odcinków")
    ax.legend(loc="best", fontsize=8)
    return fig


def plot_hull(points: list[Point], hull: list[Point]) -> Figure:
    """
    Rysujemy punkty wejsciowe i wypelniona otoczke wypukla
    """
    fig, ax = _new_axes()

    ax.plot(
        [p.X for p in points],
        [p.Y for p in points],
        marker="o",
        markersize=9,
        color=_POINT_COLOR,
        linestyle="none",
        label="Punkty",
        zorder=4,
    )
    for p in points:
        _annotate(ax, p, _POINT_COLOR)

    if len(hull) >= 3:
        closed = hull + [hull[0]]
        ax.fill(
            [p.X for p in closed],
            [p.Y for p in closed],
            color=_HULL_FILL,
            zorder=1,
        )
        ax.plot(
            [p.X for p in closed],
            [p.Y for p in closed],
            color=_HULL_COLOR,
            linewidth=2,
            label="Otoczka",
            zorder=2,
        )
    elif len(hull) == 2:
        ax.plot(
            [hull[0].X, hull[1].X],
            [hull[0].Y, hull[1].Y],
            color=_HULL_COLOR,
            linewidth=2,
            label="Otoczka",
            zorder=2,
        )

    ax.set_title("Otoczka wypukła")
    ax.legend(loc="best", fontsize=8)
    return fig
