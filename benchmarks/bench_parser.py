"""
Benchmarks for the lazyenv parser.

Run with:
    python benchmarks/bench_parser.py

Or with hyperfine for CLI benchmarks:
    hyperfine 'lazyenv --list .' 'lazyenv --list examples/'
"""

from __future__ import annotations

import time
import tempfile
from pathlib import Path

from lazyenv.parser import parse_file, parse_directory


def generate_env_file(path: Path, n_keys: int = 100) -> None:
    """Generate a synthetic .env file with n_keys entries."""
    lines = ["# Synthetic benchmark file\n"]
    for i in range(n_keys):
        if i % 10 == 0:
            lines.append(f"\n# Section {i // 10}\n")
        kind = i % 4
        if kind == 0:
            lines.append(f'KEY_{i}=plain_value_{i}\n')
        elif kind == 1:
            lines.append(f'SECRET_{i}=super_secret_password_{i}\n')
        elif kind == 2:
            lines.append(f'KEY_{i}="quoted value with spaces {i}"\n')
        else:
            lines.append(f'KEY_{i}=value_{i} # inline comment\n')
    path.write_text("".join(lines))


def bench(label: str, fn, iterations: int = 1000) -> None:
    # Warmup
    for _ in range(10):
        fn()
    start = time.perf_counter()
    for _ in range(iterations):
        fn()
    elapsed = time.perf_counter() - start
    per_call_us = (elapsed / iterations) * 1_000_000
    print(f"  {label:<40} {per_call_us:8.1f} µs/call  ({iterations} iterations)")


def main() -> None:
    print("lazyenv parser benchmarks\n" + "=" * 50)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        # Small file (10 keys)
        small = tmp_path / ".env.small"
        generate_env_file(small, 10)

        # Medium file (100 keys)
        medium = tmp_path / ".env.medium"
        generate_env_file(medium, 100)

        # Large file (1000 keys)
        large = tmp_path / ".env.large"
        generate_env_file(large, 1000)

        # Nested directory with 20 env files
        for i in range(20):
            d = tmp_path / f"service_{i}"
            d.mkdir()
            generate_env_file(d / ".env", 50)

        print("\nparse_file:")
        bench("10-key file", lambda: parse_file(small))
        bench("100-key file", lambda: parse_file(medium))
        bench("1000-key file", lambda: parse_file(large), iterations=200)

        print("\nparse_directory:")
        bench("20 services × 50 keys", lambda: parse_directory(tmp_path), iterations=100)

        print("\ndiff_files:")
        from lazyenv.diff import diff_files
        env_left = parse_file(medium)
        env_right = parse_file(medium)
        bench("diff 100-key files (identical)", lambda: diff_files(env_left, env_right))

    print("\nAll benchmarks complete.")


if __name__ == "__main__":
    main()
