import requests

__all__ = ['download_curated_models']


def download_curated_models(dirpath, chunk_size=10):
    """
    Downloads all curated models from https://www.ebi.ac.uk/biomodels and stores
    them in a specified directory.

    :param dirpath: Path to directory to store curated model files in. The directory
                    will be created if it does not exist.
    :param chunk_size: Number of files to download with each download request.
                    Note that the BioModels search API allows a maximum of 100
                    files with each request.
    """
    # Biomodels API documentation can be found at https://www.ebi.ac.uk/biomodels/docs.

    # With chunk_size = 10, download_curated_models took 783.2160873413086 seconds
    # (13m 3s) to download all curated model SBML files on UW Wifi.

    import zipfile
    import io

    with requests.Session() as s:
        # Query parameters for Biomodels API search endpoint
        params = {
            # This query string yields all manually curated biomodels
            'query': '*:* AND curationstatus:"Manually curated"',
            'format': 'json',
            # Number of models to return in response
            'numResults': chunk_size
        }
        r = s.get('https://www.ebi.ac.uk/biomodels/search', params=params)

        num_models = r.json()['matches']

        # Download all SBML files for curated biomodels in chunks of size chunk_size
        for offset in range(0, num_models + 1, chunk_size):
            print("Downloaded {} models.".format(offset))

            # Number of items to skip before starting to collect the model result set
            params['offset'] = offset

            r = s.get('https://www.ebi.ac.uk/biomodels/search', params=params)
            model_ids = (model_json['id'] for model_json in r.json()['models'])

            r = s.get(
                'https://www.ebi.ac.uk/biomodels/search/download',
                params={'models': ','.join(model_ids)},
                stream=True
            )
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(dirpath)
        print("Finished downloading all {} models.".format(num_models))


def main():
    import os

    # Saves all SBML files in a local directory named "curated"
    dirpath = os.path.join(os.path.dirname(__file__), 'curated')
    download_curated_models(dirpath)


if __name__ == '__main__':
    main()
