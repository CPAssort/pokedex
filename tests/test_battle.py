import unittest

from domain.battle import calculate_battle_score, determine_winner


class BattleCalculationTest(unittest.TestCase):
    def test_score_uses_level_and_force(self):
        self.assertEqual(calculate_battle_score(3, 10), 30)

    def test_higher_score_wins(self):
        result = determine_winner(3, 10, 2, 8)
        self.assertEqual(result["winner"], "first")
        self.assertEqual(result["first_score"], 30)
        self.assertEqual(result["second_score"], 16)

    def test_equal_scores_are_a_draw(self):
        result = determine_winner(2, 5, 5, 2)
        self.assertEqual(result["winner"], "draw")
        self.assertEqual(result["first_score"], 10)
        self.assertEqual(result["second_score"], 10)


if __name__ == "__main__":
    unittest.main()
