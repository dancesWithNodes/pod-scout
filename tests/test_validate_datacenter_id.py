import unittest

import pod_scout


class ValidateDatacenterIdTests(unittest.TestCase):
    def setUp(self) -> None:
        self.original_fetch_gpu_row = pod_scout.fetch_gpu_row

    def tearDown(self) -> None:
        pod_scout.fetch_gpu_row = self.original_fetch_gpu_row

    def test_raises_when_lookup_returns_not_found(self) -> None:
        def fake_fetch_gpu_row(*_args, **_kwargs):
            return {"found": False}

        pod_scout.fetch_gpu_row = fake_fetch_gpu_row

        with self.assertRaises(RuntimeError) as context:
            pod_scout.validate_datacenter_id(
                session=object(),
                datacenter_id="DC-1",
                gpu_type_id="GPU-1",
                markets=[("SECURE", True)],
            )

        self.assertIn("DATACENTER_ID 'DC-1' failed validation", str(context.exception))

    def test_passes_when_any_market_returns_found(self) -> None:
        state = {"calls": 0}

        def fake_fetch_gpu_row(*_args, **_kwargs):
            state["calls"] += 1
            if state["calls"] == 1:
                return {"found": False}
            return {"found": True}

        pod_scout.fetch_gpu_row = fake_fetch_gpu_row

        pod_scout.validate_datacenter_id(
            session=object(),
            datacenter_id="DC-1",
            gpu_type_id="GPU-1",
            markets=[("SECURE", True), ("COMMUNITY", False)],
        )

        self.assertEqual(state["calls"], 2)


if __name__ == "__main__":
    unittest.main()
