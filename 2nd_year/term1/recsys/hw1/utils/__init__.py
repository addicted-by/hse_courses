from pathlib import Path
import subprocess
import sys

def credentials_handler(func):
    def wrapper(*args, **kwargs):
        credentials = Path("~").expanduser() / ".kaggle" / "kaggle.json"

        message = f"""
            Check the credentials. Place kaggle.json in {credentials}
        """
        assert credentials.exists(), message
        print("Credentials approved. Checking dependencies...")
        try:
            import kaggle
        except ImportError:
            print("pip install kaggle")
        res = func(*args, **kwargs)
        return res

    return wrapper


@credentials_handler
def load_file(
    file: str, 
    dataset: str = "marlesson/myanimelist-dataset-animes-profiles-reviews",
    path2save: str = "./data"):
    subprocess.run(
        f"kaggle datasets download {dataset} -f {file} --path {path2save}",
        shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    zipf = Path(path2save) / f"{file}.zip"

    subprocess.run(
        f"unzip {zipf} -d {path2save}", shell=True
    )

    zipf.unlink(missing_ok=True)

    

def load_all_csv():
    load_file("animes.csv")
    load_file("profiles.csv")
    load_file("reviews.csv")
