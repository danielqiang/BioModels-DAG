from .download import download_curated_models
from .timeit import timeit
from .get_go_json import get_go_json, go_id_is_valid
from .yield_model_paths import yield_model_paths
from .to_csv import to_csv
from .generators import get_species, get_compartments, get_reactions

from pathlib import Path

PROJECT_ROOT = (Path(__file__) / ".." / ".." / "..").resolve()
