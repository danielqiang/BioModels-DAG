def yield_model_paths():
    from pathlib import Path

    for model_path in Path("../curated").iterdir():
        yield model_path.resolve()
