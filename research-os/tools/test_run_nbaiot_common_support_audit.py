import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile


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

    def test_read_first_can_select_a_later_row_window(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "sample.zip"
            with zipfile.ZipFile(archive, "w") as zipped:
                zipped.writestr("sample.csv", "a,b\n1,10\n2,20\n3,30\n4,40\n")
            with zipfile.ZipFile(archive) as zipped:
                frame = module.read_first(zipped, "sample.csv", 2, start=1)

        self.assertEqual(frame["a"].tolist(), [2, 3])


if __name__ == "__main__":
    unittest.main()
