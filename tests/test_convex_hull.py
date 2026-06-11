from computational_geo.computations.convex_hull import ConvexHullFinder
from computational_geo.computations.intersection_points import Point


def hull(points: list[tuple[int, int]]) -> set[tuple[int, int]]:
    result = ConvexHullFinder.find_hull([Point(x, y) for x, y in points])
    return {(p.X, p.Y) for p in result}


class TestConvexHull:
    def test_square_keeps_corners(self):
        result = hull([(0, 0), (4, 0), (4, 4), (0, 4)])
        assert result == {(0, 0), (4, 0), (4, 4), (0, 4)}

    def test_interior_point_dropped(self):
        result = hull([(0, 0), (4, 0), (4, 4), (0, 4), (2, 2)])
        assert (2, 2) not in result
        assert result == {(0, 0), (4, 0), (4, 4), (0, 4)}

    def test_collinear_edge_point_dropped(self):
        # (2,0) lezy na dolnej krawedzi - nie jest wierzcholkiem
        result = hull([(0, 0), (2, 0), (4, 0), (4, 4), (0, 4)])
        assert (2, 0) not in result

    def test_triangle(self):
        result = hull([(0, 0), (5, 0), (2, 3)])
        assert result == {(0, 0), (5, 0), (2, 3)}

    def test_duplicates_ignored(self):
        result = hull([(0, 0), (0, 0), (4, 0), (4, 4), (0, 4)])
        assert result == {(0, 0), (4, 0), (4, 4), (0, 4)}


class TestClassify:
    def test_quadrilateral(self):
        h = ConvexHullFinder.find_hull([Point(0, 0), Point(4, 0), Point(4, 4), Point(0, 4)])
        assert ConvexHullFinder.classify(h) == "czworokąt"

    def test_triangle(self):
        # czwarty punkt w srodku trojkata -> otoczka jest trojkatem
        h = ConvexHullFinder.find_hull([Point(0, 0), Point(4, 0), Point(2, 4), Point(2, 1)])
        assert ConvexHullFinder.classify(h) == "trójkąt"

    def test_segment(self):
        h = ConvexHullFinder.find_hull([Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3)])
        assert ConvexHullFinder.classify(h) == "odcinek"

    def test_point(self):
        h = ConvexHullFinder.find_hull([Point(2, 2), Point(2, 2), Point(2, 2)])
        assert ConvexHullFinder.classify(h) == "punkt"


class TestDegenerate:
    def test_two_points(self):
        result = ConvexHullFinder.find_hull([Point(0, 0), Point(1, 1)])
        assert result == [Point(0, 0), Point(1, 1)]

    def test_single_point(self):
        result = ConvexHullFinder.find_hull([Point(3, 3)])
        assert result == [Point(3, 3)]

    def test_empty(self):
        assert ConvexHullFinder.find_hull([]) == []
