import argparse

def add_arguments(parser):
    parser.description = "simple SV language server"

    parser.add_argument(
        "--tcp", action="store_true",
        help="Use TCP server"
    )
    parser.add_argument(
        "--ws", action="store_true",
        help="Use WebSocket server"
    )
    parser.add_argument(
        "--host", default="127.0.0.1",
        help="Bind to this address"
    )
    parser.add_argument(
        "--port", type=int, default=2087,
        help="Bind to this port"
    )
    parser.add_argument(
        "--slangLib", type=str, default="",
        help="The path to the slang compiled libraries"
    )
    parser.add_argument(
        "--slangSource", type=str, default="",
        help="The path to the slang source code"
    )

parser = argparse.ArgumentParser()
add_arguments(parser)
args = parser.parse_args()
