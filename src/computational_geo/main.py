import sys
from pathlib import Path


def run_web() -> None:
    """
    Uruchamiamy aplikacje Streamlit (web.py)
    """
    from streamlit.web import cli as stcli

    web_path: Path = Path(__file__).parent / "web.py"
    sys.argv = ["streamlit", "run", str(web_path)]
    sys.exit(stcli.main())
