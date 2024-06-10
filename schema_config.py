MODEL_SCHEMA = {
    'author': {
        'primary_key': 'auth_id',
        'initial_column': ['author'],
        'transform': False,
        'all_columns': ['auth_id', 'author']
    },
    'tag': {
        'primary_key': 'tag_id',
        'initial_column': ['tag'],
        'transform': False,
        'all_columns': ['tag_id', 'tag']
    },
    'quote': {
        'primary_key': 'quote_id',
        'initial_column': ['quote', 'author'],
        'merge_frame_locations': [0],
        'transform': True,
        'all_columns': ['quote_id', 'quote', 'auth_id'],
        'merge_keys': ['author']
    },
    'quote_tag': {
        'primary_key': ['quote_id', 'tag_id'],
        'initial_column': ['quote', 'tag'],
        'merge_frame_locations': [2, 1],
        'transform': True,
        'all_columns': ['quote_id', 'tag_id'],
        'merge_keys': ['quote', 'tag']
    }
}