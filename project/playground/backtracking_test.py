from BackTracking import BackTracking
import unittest


class TestBackTracking(unittest.TestCase):
    def setUp(self):
        # Initialize a BackTracking object with K value for testing
        self.k_value = 3
        self.bt = BackTracking(self.k_value)

    def test_recursive_backtracking(self):
        # Test Case 1: Simple node tracking assignment
        self.bt.update_node_status(1, ["t2", "t3", "t1"])
        self.bt.update_node_status(2, ["t2", "t1"])
        self.bt.update_node_status(3, ["t2", "t3", "t4"])
        self.bt.update_node_status(4, ["t3", "t4"])
        self.bt.update_node_status(5, ["t3", "t4"])

        assignment = {}
        target_tracker = {}

        # Expected result depends on backtracking behavior.
        expected_assignment = {
            1: ["t2", "t3", "t1"],
            2: ["t2", "t1"],
            3: ["t2", "t3", "t4"],
            4: ["t3", "t4"],
            5: ["t3", "t4"],
        }
        expected_target_tracker = {
            "t2": [1, 2, 3],
            "t3": [1, 4, 5],
            "t4": [4, 5],
            "t1": [1],
        }

        result_assignment, result_target_tracker = self.bt.recursive_backtracking(
            assignment, target_tracker
        )
        print(f"Assignment: {result_assignment}")
        print(f"Target Tracker: {result_target_tracker}")

        # Assert that the assignment matches the expected one
        self.assertEqual(result_assignment, expected_assignment)
        self.assertEqual(result_target_tracker, expected_target_tracker)

    def test_recursive_backtracking_no_solution(self):
        # Test Case 2: A case where no solution is possible
        self.bt.update_node_status(1, [100, 101])
        self.bt.update_node_status(2, [100])
        self.bt.update_node_status(3, [101])
        self.bt.update_node_status(4, [102])

        assignment = {}
        target_tracker = {}

        # No valid assignment should be possible for some configurations
        result = self.bt.recursive_backtracking(assignment, target_tracker)

        # The result should be False indicating no valid assignment was found
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
