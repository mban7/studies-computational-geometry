from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    X: float
    Y: float


@dataclass(frozen=True)
class Segment:
    p1: Point
    p2: Point


class IntersectionFinder:
    @staticmethod
    def find_intersection(s1: Segment, s2: Segment) -> None | Point | Segment:
        denom: float = IntersectionFinder._get_denominator(s1, s2)

        if denom != 0:
            num_x, num_y = IntersectionFinder._get_numerators(s1, s2)
            p = Point(num_x / denom, num_y / denom)

            if IntersectionFinder._is_point_on_segments(p, s1, s2):
                return p
            return None

        if IntersectionFinder._are_segments_collinear(s1, s2) and (
            res := IntersectionFinder._find_overlapping_intersections(s1, s2)
        ) is not None:
            return res

        return None
        

    
    @staticmethod
    def _get_denominator(s1: Segment, s2: Segment) -> float:
        """
        Obliczamy mianownik
        """
        equation: float = (
            (s1.p1.X - s1.p2.X)*(s2.p1.Y - s2.p2.Y) - 
            (s1.p1.Y - s1.p2.Y)*(s2.p1.X - s2.p2.X)
        )
        return equation

    @staticmethod
    def _get_numerators(s1: Segment, s2: Segment) -> tuple[float, float]:
        """
        Znajdujemy liczniki X i Y
        """
        base_eq1: float = s1.p1.X * s1.p2.Y - s1.p1.Y * s1.p2.X
        base_eq2: float = s2.p1.X * s2.p2.Y - s2.p1.Y * s2.p2.X

        diff_x1: float = s1.p1.X - s1.p2.X
        diff_y1: float = s1.p1.Y - s1.p2.Y
    
        diff_x2: float = s2.p1.X - s2.p2.X
        diff_y2: float = s2.p1.Y - s2.p2.Y

        num_x: float = base_eq1 * diff_x2 - diff_x1 * base_eq2
        num_y: float = base_eq1 * diff_y2 - diff_y1 * base_eq2
        
        return num_x, num_y

    @staticmethod
    def _is_point_on_segments(p: Point, s1: Segment, s2: Segment) -> bool:
        '''
        Sprawdzamy czy punkt lezy na obu odcinkach
        '''
        on_s1: bool = (
            min(s1.p1.X, s1.p2.X) <= p.X <= max(s1.p1.X, s1.p2.X)
            and min(s1.p1.Y, s1.p2.Y) <= p.Y <= max(s1.p1.Y, s1.p2.Y)
        )
        on_s2: bool = (
            min(s2.p1.X, s2.p2.X) <= p.X <= max(s2.p1.X, s2.p2.X) 
            and min(s2.p1.Y, s2.p2.Y) <= p.Y <= max(s2.p1.Y, s2.p2.Y)
        )
        return on_s1 and on_s2

    @staticmethod
    def _are_segments_collinear(s1: Segment, s2: Segment) -> bool:
        """
        Sprawdzamy czy odcinki leza na tej samej prostej
        """
        equation = (
            (s1.p2.X - s1.p1.X) * (s2.p1.Y - s1.p1.Y) - 
            (s1.p2.Y - s1.p1.Y) * (s2.p1.X - s1.p1.X)
        )
        return abs(equation) < 1e-9

    @staticmethod
    def _find_overlapping_intersections(s1: Segment, s2: Segment) -> None | Point | Segment:
        """
        Sprawdzamy czy odcinki na siebie nachodza
        """
        x_start = max(min(s1.p1.X, s1.p2.X), min(s2.p1.X, s2.p2.X))
        x_end = min(max(s1.p1.X, s1.p2.X), max(s2.p1.X, s2.p2.X))
        y_start = max(min(s1.p1.Y, s1.p2.Y), min(s2.p1.Y, s2.p2.Y))
        y_end = min(max(s1.p1.Y, s1.p2.Y), max(s2.p1.Y, s2.p2.Y))
        
        if x_start > x_end or y_start > y_end:
            return None

        if x_start == x_end and y_start == y_end:
            return Point(x_start, y_start)

        return Segment(Point(x_start, y_start), Point(x_end, y_end))
    