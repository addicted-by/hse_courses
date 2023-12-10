import os
import re
import ast
import argparse
import numpy as np
import pandas as pd

REVIEWS_FILE = 'reviews.csv'
PROFILES_FILE = 'profiles.csv'
ANIMES_FILE = 'animes.csv'

USERID = 'user_id'
ANIMEID = 'anime_id'


def combine_path(data_dir, file_name):
    return os.path.join(data_dir, file_name)


def process_data(data_dir):
    '''Deduplicates and cleans up data from:
    https://www.kaggle.com/datasets/marlesson/myanimelist-dataset-animes-profiles-reviews
    '''
    animes = process_anime_data(data_dir)
    animes.to_csv(combine_path(data_dir, ANIMES_FILE.replace('.csv', '.gz')), index=False)
    known_anime = animes[ANIMEID].values
    
    profiles = process_profiles_data(data_dir, known_anime)
    profiles.to_csv(combine_path(data_dir, PROFILES_FILE.replace('.csv', '.gz')), index=False)
    known_users = profiles[USERID].values
    
    reviews = process_reviews_data(data_dir, known_users, known_anime)
    reviews.to_csv(combine_path(data_dir, REVIEWS_FILE.replace('.csv', '.gz')), index=False)    


def process_anime_data(data_dir):
    animes = (
        pd.read_csv(combine_path(data_dir, ANIMES_FILE))
        .rename(columns={'uid': ANIMEID})
        # deduplicating entries that are only different by the count of members
        .sort_values('members').drop_duplicates(subset=[ANIMEID], keep='last')
        .assign(
            # makes genres a string for convenient tokenization
            genre = lambda x: x['genre'].apply(lambda x: ', '.join(ast.literal_eval(x))),
            # make sure synopsis is a string (use `na_filter=False` in `pd.read_csv`)
            synopsis = lambda x: x['synopsis'].fillna(''),
            # avoid NaNs in integer type
            episodes = lambda x: x['episodes'].fillna(-1).astype(int),
            # avoid NaNs in ratings
            score = lambda x: x['score'].fillna(0.)
        )
        .sort_values(ANIMEID)
    )
    return animes


def process_profiles_data(data_dir, allowed_anime):
    def filter_favorites(fav_str: str):
        favs = np.fromiter(ast.literal_eval(fav_str), int)
        return np.intersect1d(allowed_anime, favs).tolist()
    
    profiles = (
        pd.read_csv(combine_path(data_dir, PROFILES_FILE))
        .rename(columns={'profile': USERID})
        # remove user id duplicates
        .drop_duplicates(subset=[USERID], keep='first')
        # convert text into list of id's, and only allow known items
        .assign(favorites_anime=lambda x: x['favorites_anime'].apply(filter_favorites))
        # only take users with favorites data
        .loc[lambda x: x['favorites_anime'].apply(len) > 0]
    )
    return profiles


def process_reviews_data(data_dir, allowed_users, allowed_anime):
    def extract_review_text(text):
        # cleanup multiple blank lines
        clean_str = re.sub(r'\n+\s+', '\n', text).strip()
        # capture text after the ratings section
        after_ratings = re.split('Enjoyment\s+\n\d+', clean_str, maxsplit=1)[-1].strip()
        # remove the `Helpful` section
        return after_ratings.rsplit('Helpful', maxsplit=1)[0]

    reviews = (
        pd.read_csv(combine_path(data_dir, REVIEWS_FILE))
        .rename(columns={'profile': USERID, 'anime_uid': ANIMEID})
        # remove anime id duplicates
        .drop_duplicates(subset=[USERID, ANIMEID], keep='first')
        # onle take users that have favorites data - we'll run evaluation on them
        .query(f'{USERID} in @allowed_users and {ANIMEID} in @allowed_anime')        
        .assign(text = lambda x: x['text'].apply(extract_review_text))
    )
    return reviews


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', default='./', type=str)
    data_dir = parser.parse_args().data_dir
    process_data(data_dir)
        
