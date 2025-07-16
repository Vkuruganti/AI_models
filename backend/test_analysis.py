import unittest
from analysis import analyze_metrics

class TestAnalysisEngine(unittest.TestCase):
    def test_over_provisioned(self):
        metrics = {
            "pods": [
                {"name": "pod1", "cpu_usage": 0.1, "cpu_limit": 1.0, "mem_usage": 0.2, "mem_limit": 1.0, "qos_class": "Burstable"}
            ]
        }
        recs = analyze_metrics(metrics)
        self.assertTrue(any(r["type"] == "over-provisioned" for r in recs))

    def test_under_provisioned(self):
        metrics = {
            "pods": [
                {"name": "pod2", "cpu_usage": 0.95, "cpu_limit": 1.0, "mem_usage": 0.8, "mem_limit": 1.0, "qos_class": "Burstable"}
            ]
        }
        recs = analyze_metrics(metrics)
        self.assertTrue(any(r["type"] == "under-provisioned" for r in recs))

    def test_spiky_usage(self):
        metrics = {
            "pods": [
                {"name": "pod3", "cpu_usage": 0.8, "cpu_limit": 1.0, "mem_usage": 0.5, "mem_limit": 1.0, "qos_class": "Burstable"},
                {"name": "pod4", "cpu_usage": 0.2, "cpu_limit": 1.0, "mem_usage": 0.5, "mem_limit": 1.0, "qos_class": "Burstable"}
            ]
        }
        recs = analyze_metrics(metrics)
        self.assertTrue(any(r["type"] == "spiky-usage" for r in recs))

    def test_qos_suggestion(self):
        metrics = {
            "pods": [
                {"name": "pod5", "cpu_usage": 0.5, "cpu_limit": 1.0, "mem_usage": 0.5, "mem_limit": 1.0, "qos_class": "BestEffort"}
            ]
        }
        recs = analyze_metrics(metrics)
        self.assertTrue(any(r["type"] == "qos" for r in recs))

    def test_cost_estimation(self):
        metrics = {
            "pods": [
                {"name": "pod6", "cpu_usage": 0.5, "cpu_limit": 2.0, "mem_usage": 1.0, "mem_limit": 4.0, "qos_class": "Burstable"}
            ]
        }
        recs = analyze_metrics(metrics)
        cost_recs = [r for r in recs if r["type"] == "cost"]
        self.assertTrue(cost_recs)
        self.assertIn("Estimated monthly cost: $30.00", cost_recs[0]["suggestion"])

if __name__ == "__main__":
    unittest.main() 