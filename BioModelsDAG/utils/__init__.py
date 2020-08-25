from .download import download_curated_models
from .timeit import timeit
from .get_go_json import get_go_json, go_id_is_valid
from .yield_model_paths import yield_model_paths
from .to_csv import to_csv
from .generators import get_species, get_compartments, get_reactions
from .helpers import extract_annotation_identifiers, extract_model_data, extract_publication_date

from pathlib import Path

PROJECT_ROOT = (Path(__file__) / ".." / ".." / "..").resolve()
