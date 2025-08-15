import argparse
from .args import Args

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Coourse Builder")

    for arg in Args:
        parser.add_argument(arg.flag, **arg.kwargs)


    return parser.parse_args()

