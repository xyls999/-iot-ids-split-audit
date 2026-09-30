import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).with_name("run_nbaiot_common_support_audit.py")
spec = importlib.util.spec_from_file_location("common_support_audit", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CommonSupportAuditTests(unittest.TestCase):
    def test_coverage_report_returns_sorted_common_labels_and_missing_cells(self):
        report = module.coverage_report(
            {
                1: {"benign", "gafgyt.combo", "gafgyt.junk"},
                2: {"benign", "gafgyt.combo"},
                3: {"benign", "gafgyt.combo", "gafgyt.junk"},
            }
        )

        self.assertEqual(report["common_labels"], ["benign", "gafgyt.combo"])
        self.assertEqual(report["missing_by_device"], {"2": ["gafgyt.junk"]})

    def test_device_holdout_gap_is_random_metric_minus_held_out_metric(self):
        self.assertAlmostEqual(module.device_holdout_gap(0.91, 0.76), 0.15)

    def test_per_label_f1_uses_declared_label_names(self):
        scores = module.per_label_f1(
            [0, 0, 1, 1], [0, 1, 1, 1], ["benign", "attack"]
        )

        self.assertAlmostEqual(scores["benign"], 2 / 3)
        self.assertAlmostEqual(scores["attack"], 0.8)


if __name__ == "__main__":
    unittest.main()
