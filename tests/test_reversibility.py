import unittest

from clsigma_carrier import AXIOM, build_certificate, recover_from_certificate


class CLSIGMACarrierTests(unittest.TestCase):
    def test_round_trip_preserves_payload(self):
        payload = b"Cosmic Love Is The Solution(s) For Everything\nTRF-ZETA\n"
        result = build_certificate(payload, timestamp_unix=0)

        self.assertEqual(result.certificate["Axiom"], AXIOM)
        self.assertEqual(result.certificate["HashFunction"], "NONE")
        self.assertEqual(result.certificate["Certificate"]["H_CL"], 0)
        self.assertEqual(recover_from_certificate(result.certificate), payload)

    def test_empty_payload_is_valid(self):
        result = build_certificate(b"", timestamp_unix=0)

        self.assertEqual(result.certificate["ExactCarrier"]["original_size_bytes"], 0)
        self.assertEqual(result.certificate["ExactCarrier"]["compression_ratio"], 0)
        self.assertEqual(result.certificate["Certificate"]["H_CL"], 0)

    def test_cosmic_axiom_invariant_is_explicit(self):
        result = build_certificate(b"axiom-check", timestamp_unix=0)

        invariant = result.certificate["CosmicAxiomInvariant"]
        self.assertTrue(invariant["holds"])
        self.assertEqual(invariant["required_axiom"], AXIOM)


if __name__ == "__main__":
    unittest.main()
