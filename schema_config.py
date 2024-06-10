MODEL_SCHEMA = {
    'author': {
        'primary_key': 'auth_id',
        'initial_column': ['author'],
        'dataframe_location': 0,
        'transform': False,
        'all_columns': ['auth_id', 'author']
    },
    'tag': {
        'primary_key': 'tag_id',
        'initial_column': ['tag'],
        'dataframe_location': 1,
        'transform': False,
        'all_columns': ['tag_id', 'tag']
    },
    'quote': {
        'primary_key': 'quote_id',
        'initial_column': ['quote', 'author'],
        'dataframe_location': 2,
        'merge_frame_locations': [0],
        'transform': True,
        'all_columns': ['quote_id', 'quote', 'auth_id'],
        'drop_columns': 'author',
        'merge_keys': ['author']
    },
    'quote_tag': {
        'primary_key': ['quote_id', 'tag_id'],
        'initial_column': ['quote', 'tag'],
        'dataframe_location': 3,
        'merge_frame_locations': [2, 1],
        'transform': True,
        'all_columns': ['quote_id', 'tag_id'],
        'merge_keys': ['quote', 'tag']
    }
}