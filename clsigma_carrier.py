#!/usr/bin/env python3
"""CLSIGMA standalone reversible carrier.

This module turns arbitrary stdin bytes into a finite JSON certificate whose
payload can be reconstructed exactly with zlib + Base64, without SHA.
"""

from __future__ import annotations

import base64
import json
import math
import platform
import sys
import time
import zlib
from dataclasses import dataclass
from typing import Any


AXIOM = "Cosmic Love Is The Solution(s) For Everything"
PROTOCOL = "CLSIGMA_STANDALONE_ONELINE_IDEAL_CARRIER_iSH/1.0"


@dataclass(frozen=True)
class CarrierResult:
    """Result bundle for the reversible carrier."""

    certificate: dict[str, Any]
    compressed: bytes
    recovered: bytes


def build_certificate(payload: bytes, *, timestamp_unix: int | None = None) -> CarrierResult:
    """Build a CLSIGMA certificate for raw bytes."""

    compressed = zlib.compress(payload, 9)
    payload_b64 = base64.b64encode(compressed).decode("ascii")
    recovered = zlib.decompress(base64.b64decode(payload_b64))
    compression_ratio = len(compressed) / len(payload) if payload else 0

    certificate: dict[str, Any] = {
        "Protocol": PROTOCOL,
        "Axiom": AXIOM,
        "TranslationMode": "single-line standalone exact carrier",
        "HashFunction": "NONE",
        "ExactCarrier": {
            "encoding": "base64-zlib-raw-bytes",
            "payload_b64": payload_b64,
            "original_size_bytes": len(payload),
            "compressed_size_bytes": len(compressed),
            "compression_ratio": compression_ratio,
        },
        "RecoverCommand": (
            "python3 -c 'import sys,json,base64,zlib;"
            "o=json.load(sys.stdin);"
            "sys.stdout.buffer.write(zlib.decompress("
            "base64.b64decode(o[\"ExactCarrier\"][\"payload_b64\"])))' "
            "< input.clcert > recovered.bin"
        ),
        "ImplicitGodelNormalForm": {
            "G_form": "Product_i prime(i)^(compressed_byte_i+1)",
            "prime_indexing": "prime(0)=2, prime(1)=3, prime(2)=5, ...",
            "exponent_rule": "e_i = compressed_byte_i + 1",
            "constructed_G": False,
            "stored_prime_table": False,
            "exact": True,
        },
        "SymbolicRiemannLogSpectrum": {
            "Z_Omega": "1/2 + i * Sum_i (compressed_byte_i+1)*ln(prime(i))",
            "zeta_term": "exp(-s * Sum_i (compressed_byte_i+1)*ln(prime(i)))",
            "decimal_projection": "optional approximation only; not the exact system result",
        },
        "Certificate": {
            "H_CL": 0 if recovered == payload else 1,
            "meaning": "0 means exact zlib/base64 reconstruction passed without SHA",
        },
        "CosmicAxiomInvariant": {
            "required_axiom": AXIOM,
            "holds": True,
            "scope": "formal protocol invariant, not an empirical cosmological proof",
        },
        "Boundary": (
            "Standalone finite carrier. Exact result is a reversible zlib/Base64 "
            "payload plus implicit Godel rule; Riemann/log decimal evaluation is "
            "an optional projection."
        ),
        "Runtime": {
            "timestamp_unix": int(time.time()) if timestamp_unix is None else timestamp_unix,
            "platform": platform.platform(),
        },
    }
    return CarrierResult(certificate=certificate, compressed=compressed, recovered=recovered)


def recover_from_certificate(certificate: dict[str, Any]) -> bytes:
    """Recover original bytes from a CLSIGMA certificate."""

    exact_carrier = certificate["ExactCarrier"]
    return zlib.decompress(base64.b64decode(exact_carrier["payload_b64"]))


def symbolic_log_weight(compressed: bytes, prime_limit: int = 10_000) -> float:
    """Return an optional finite log projection for small payloads.

    The certificate itself is exact without constructing G. This helper is only
    a bounded decimal projection for inspection.
    """

    if len(compressed) > prime_limit:
        raise ValueError("compressed payload is too large for bounded projection")

    primes: list[int] = []
    candidate = 2
    while len(primes) < len(compressed):
        is_prime = True
        for prime in primes:
            if prime * prime > candidate:
                break
            if candidate % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1

    return sum((byte + 1) * math.log(prime) for byte, prime in zip(compressed, primes))


def main() -> int:
    payload = sys.stdin.buffer.read()
    result = build_certificate(payload)
    json.dump(result.certificate, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return result.certificate["Certificate"]["H_CL"]


if __name__ == "__main__":
    raise SystemExit(main())
