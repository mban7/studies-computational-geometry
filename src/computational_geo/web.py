import streamlit as st

from computational_geo.computations.convex_hull import ConvexHullFinder
from computational_geo.computations.intersection_points import (
    IntersectionFinder,
    Point,
    Segment,
)

st.set_page_config(page_title="Geometria obliczeniowa")

st.title("Geometria obliczeniowa")

MODE_LABELS: dict[str, str] = {
    "intersection": "Punkt przecięcia",
    "hull": "Otoczka wypukła",
}

mode = st.segmented_control(
    label="Wybierz operację",
    options=list(MODE_LABELS),
    format_func=MODE_LABELS.get,
    default="intersection",
)


def segment_input(label: str, defaults: tuple[int, int, int, int]) -> Segment:
    st.markdown(f"**{label}**")
    c1, c2, c3, c4 = st.columns(4)
    x1: int = c1.number_input("x₁", value=defaults[0], step=1, key=f"{label}_x1")
    y1: int = c2.number_input("y₁", value=defaults[1], step=1, key=f"{label}_y1")
    x2: int = c3.number_input("x₂", value=defaults[2], step=1, key=f"{label}_x2")
    y2: int = c4.number_input("y₂", value=defaults[3], step=1, key=f"{label}_y2")
    return Segment(Point(x1, y1), Point(x2, y2))


def point_input(index: int) -> Point:
    st.markdown(f"**Punkt {index}**")
    c1, c2 = st.columns(2)
    x: int = c1.number_input("x", value=0, step=1, key=f"p{index}_x")
    y: int = c2.number_input("y", value=0, step=1, key=f"p{index}_y")
    return Point(x, y)


if mode == "intersection":
    st.caption("Podaj końce dwóch odcinków.")
    s1: Segment = segment_input("Odcinek 1", (0, 0, 0, 0))
    s2: Segment = segment_input("Odcinek 2", (0, 0, 0, 0))

    if st.button("Oblicz", type="primary", use_container_width=True):
        result: None | Point | Segment = IntersectionFinder.find_intersection(s1, s2)
        if result is None:
            st.error("NIE — odcinki się nie przecinają.")
        elif isinstance(result, Point):
            st.success("TAK — przecięcie jest punktem.")
            st.write(f"Współrzędne: ({result.X}, {result.Y})")
        else:
            st.success("TAK — przecięcie jest odcinkiem.")
            st.write(
                f"Końce: ({result.p1.X}, {result.p1.Y}) → "
                f"({result.p2.X}, {result.p2.Y})"
            )

else:
    st.caption("Podaj cztery punkty.")
    points: list[Point] = [point_input(i) for i in range(1, 5)]

    if st.button("Oblicz", type="primary", use_container_width=True):
        hull: list[Point] = ConvexHullFinder.find_hull(points)
        kind: str = ConvexHullFinder.classify(hull)
        st.success(f"Otoczka wypukła to **{kind}**.")
        st.write(
            "Kolejne wierzchołki: "
            + " → ".join(f"({p.X}, {p.Y})" for p in hull)
        )
