import unittest
from pipeline import EnterpriseComplianceEngine

class TestComplianceEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = EnterpriseComplianceEngine()

    def test_food_banned_additive(self):
        res = self.engine.inspect("FOOD", "Sandwich Bread", "Flour, water, yeast, potassium bromate, salt")
        self.assertEqual(res["overall_status"], "PROHIBITED")
        self.assertEqual(res["tier_triggered"], "Tier 1: Statutory Authority Check")
        self.assertTrue(any(c["regulator"] == "FSSAI" for c in res["regulatory_citations"]))

    def test_agriculture_banned_chemical(self):
        res = self.engine.inspect("AGRICULTURE", "Insecticide 35", "Endosulfan technical grade formulation")
        self.assertEqual(res["overall_status"], "PROHIBITED")
        self.assertTrue(any("CIBRC" in c["regulator"] for c in res["regulatory_citations"]))

    def test_cosmetics_banned_heavy_metal(self):
        res = self.engine.inspect("COSMETICS", "Fair Cream", "Water, glycerin, mercury, parfum")
        self.assertEqual(res["overall_status"], "PROHIBITED")
        self.assertTrue(any("CDSCO" in c["regulator"] for c in res["regulatory_citations"]))

    def test_safe_food_cleared(self):
        res = self.engine.inspect("FOOD", "Brown Rice", "Pure whole grain brown rice")
        self.assertEqual(res["overall_status"], "COMPLIANT")
        self.assertIn("model_insights", res)

    def test_safe_cosmetic_cleared(self):
        res = self.engine.inspect("COSMETICS", "Gentle Cleanser", "Aqua, Glycerin, Sodium Chloride")
        self.assertEqual(res["overall_status"], "COMPLIANT")

    def test_e_code_additive_alias_detected(self):
        res = self.engine.inspect("FOOD", "Toast Bread", "Refined flour, yeast, E924, salt")
        self.assertEqual(res["overall_status"], "PROHIBITED")
        self.assertEqual(res["tier_triggered"], "Tier 1: Statutory Authority Check")
        self.assertTrue(any("Potassium Bromate" in c["flagged_ingredient"] for c in res["regulatory_citations"]))

    def test_novel_safe_product_cleared(self):
        res = self.engine.inspect("FOOD", "Almond Sweets", "Pure roasted almonds, raw sugar, cardamom powder")
        self.assertEqual(res["overall_status"], "COMPLIANT")
        self.assertIn("model_insights", res)

    def test_case_and_whitespace_handling(self):
        res = self.engine.inspect("  food  ", "White Bread", "  Wheat Flour, WATER, Yeast, E924A  ")
        self.assertEqual(res["overall_status"], "PROHIBITED")

if __name__ == "__main__":
    unittest.main()