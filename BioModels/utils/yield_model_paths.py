def yield_model_paths():
    from . import PROJECT_ROOT

    for model_path in (PROJECT_ROOT / "BioModels" / "curated").iterdir():
        yield model_path.resolve()
