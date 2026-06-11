import pytest

from computational_geo.computations.intersection_points import (
    IntersectionFinder,
    Point,
    Segment,
)


def seg(x1, y1, x2, y2) -> Segment:
    return Segment(Point(x1, y1), Point(x2, y2))


class TestCrossingSegments:
    def test_returns_point_at_crossing(self):
        # X shape crossing at (1, 1)
        s1 = seg(0, 0, 2, 2)
        s2 = seg(0, 2, 2, 0)
        assert IntersectionFinder.find_intersection(s1, s2) == Point(1, 1)

    def test_touching_at_endpoint(self):
        s1 = seg(0, 0, 1, 1)
        s2 = seg(1, 1, 2, 0)
        assert IntersectionFinder.find_intersection(s1, s2) == Point(1, 1)

    def test_lines_cross_but_segments_do_not(self):
        # Their infinite lines intersect, but the segments are too short.
        s1 = seg(0, 0, 1, 1)
        s2 = seg(3, 0, 4, 1)
        assert IntersectionFinder.find_intersection(s1, s2) is None


class TestParallelSegments:
    def test_parallel_non_collinear(self):
        s1 = seg(0, 0, 2, 0)
        s2 = seg(0, 1, 2, 1)
        assert IntersectionFinder.find_intersection(s1, s2) is None


class TestCollinearSegments:
    def test_overlapping_returns_segment(self):
        s1 = seg(0, 0, 2, 0)
        s2 = seg(1, 0, 3, 0)
        result = IntersectionFinder.find_intersection(s1, s2)
        assert result == Segment(Point(1, 0), Point(2, 0))

    def test_touching_at_single_point_returns_point(self):
        s1 = seg(0, 0, 1, 0)
        s2 = seg(1, 0, 2, 0)
        assert IntersectionFinder.find_intersection(s1, s2) == Point(1, 0)

    def test_collinear_but_disjoint(self):
        s1 = seg(0, 0, 1, 0)
        s2 = seg(2, 0, 3, 0)
        assert IntersectionFinder.find_intersection(s1, s2) is None

    def test_one_contained_in_other(self):
        s1 = seg(0, 0, 4, 0)
        s2 = seg(1, 0, 2, 0)
        assert IntersectionFinder.find_intersection(s1, s2) == Segment(
            Point(1, 0), Point(2, 0)
        )


class TestHelpers:
    def test_denominator_zero_for_parallel(self):
        s1 = seg(0, 0, 2, 0)
        s2 = seg(0, 1, 2, 1)
        assert IntersectionFinder._get_denominator(s1, s2) == 0

    @pytest.mark.parametrize(
        "s1, s2, expected",
        [
            (seg(0, 0, 2, 0), seg(1, 0, 3, 0), True),
            (seg(0, 0, 2, 0), seg(0, 1, 2, 1), False),
        ],
    )
    def test_are_segments_collinear(self, s1, s2, expected):
        assert IntersectionFinder._are_segments_collinear(s1, s2) is expected
