import unittest

from pipeline import check, make_reading


class CheckTests(unittest.TestCase):
    def test_clean_text_passes(self):
        self.assertEqual(check("Focus on one priority today."), [])

    def test_unsafe_claims_flagged(self):
        for bad in ("This will cure your stress.", "A guaranteed windfall.", "You should invest in crypto."):
            self.assertTrue(check(bad), bad)

    def test_length_limit(self):
        self.assertTrue(check("word " * 121))

    def test_empty(self):
        self.assertTrue(check("   "))


class PipelineTests(unittest.TestCase):
    def test_good_draft_skips_refinement(self):
        calls = []
        r = make_reading("Leo", lambda s: "A calm day.", lambda d, i: calls.append(1) or d)
        self.assertEqual((r.needs_human, r.stage2_changed, calls), (False, False, []))

    def test_bad_draft_is_refined(self):
        r = make_reading("Leo", lambda s: "This will cure you.", lambda d, i: "A calm day ahead.")
        self.assertEqual((r.text, r.needs_human, r.stage2_changed), ("A calm day ahead.", False, True))

    def test_refinement_receives_the_issues(self):
        seen = {}
        make_reading("Leo", lambda s: "Guaranteed luck.", lambda d, i: seen.setdefault("i", i) and "Fine.")
        self.assertIn("unsafe", seen["i"][0])

    def test_unfixable_output_goes_to_a_human_not_a_retry_loop(self):
        n = []
        r = make_reading("Leo", lambda s: "Guaranteed.", lambda d, i: n.append(1) or "Still guaranteed.")
        self.assertTrue(r.needs_human)
        self.assertEqual(len(n), 1)


if __name__ == "__main__":
    unittest.main()
