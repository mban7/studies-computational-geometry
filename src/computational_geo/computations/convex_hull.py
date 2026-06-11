from computational_geo.computations.intersection_points import Point


class ConvexHullFinder:
    @staticmethod
    def find_hull(points: list[Point]) -> list[Point]:
        unique: list[Point] = ConvexHullFinder._get_unique_sorted(points)

        if len(unique) <= 2:
            return unique

        lower: list[Point] = ConvexHullFinder._build_chain(unique)
        upper: list[Point] = ConvexHullFinder._build_chain(list(reversed(unique)))

        return lower[:-1] + upper[:-1]

    @staticmethod
    def classify(hull: list[Point]) -> str:
        """
        Okreslamy jakim zbiorem jest otoczka
        """
        names: dict[int, str] = {
            1: "punkt",
            2: "odcinek",
            3: "trójkąt",
            4: "czworokąt",
        }
        return names.get(len(hull), "wielokąt")

    @staticmethod
    def _get_unique_sorted(points: list[Point]) -> list[Point]:
        """
        Usuwamy duplikaty i sortujemy punkty po X, potem po Y
        """
        unique = {(p.X, p.Y) for p in points}
        ordered = sorted(unique)
        return [Point(x, y) for x, y in ordered]

    @staticmethod
    def _build_chain(points: list[Point]) -> list[Point]:
        """
        Budujemy jeden lancuch otoczki przechodzac po punktach
        """
        chain: list[Point] = []

        for p in points:
            while len(chain) >= 2 and ConvexHullFinder._cross(chain[-2], chain[-1], p) <= 0:
                chain.pop()
            chain.append(p)

        return chain

    @staticmethod
    def _cross(o: Point, a: Point, b: Point) -> float:
        """
        Iloczyn wektorowy OA x OB, dodatni gdy skret w lewo
        """
        equation: float = (
            (a.X - o.X) * (b.Y - o.Y) -
            (a.Y - o.Y) * (b.X - o.X)
        )
        return equation
