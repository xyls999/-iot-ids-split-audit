import importlib.util
from pathlib import Path
import unittest

import numpy as np


MODULE_PATH = Path(__file__).with_name("run_nbaiot_embedding_probe.py")
spec = importlib.util.spec_from_file_location("embedding_probe", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class EmbeddingProbeTests(unittest.TestCase):
    def test_hidden_representation_applies_relu_affine_projection(self):
        x = np.array([[1.0, 2.0], [-1.0, 3.0]])
        weights = np.array([[1.0, -2.0], [0.5, 1.0]])
        bias = np.array([-1.0, 0.5])

        actual = module.hidden_representation(x, weights, bias)

        np.testing.assert_allclose(actual, [[1.0, 0.5], [0.0, 5.5]])


if __name__ == "__main__":
    unittest.main()
