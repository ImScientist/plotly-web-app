from __future__ import annotations

import argparse

from plotly_web_app.content import export_static_content


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the fully static Plotly app assets.")
    parser.add_argument("--size", type=int, default=4000, help="Number of samples per class.")
    parser.add_argument("--seed", type=int, default=15, help="Random seed for synthetic data generation.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = export_static_content(size=args.size, seed=args.seed)
    print(f"Static content written to {output_path}")


if __name__ == "__main__":
    main()

