import pandas as pd
            
def dump_data(csv_path: str, schema: dict, engine):
    """
    Load data from a CSV file, transform it according to the schema, and load it into the database.

    Args:
        csv_path (str): The path to the CSV file containing the data.
        schema (dict): The schema configuration for transforming the data.
        engine (Engine): The SQLAlchemy engine for connecting to the database to load the tables.
    """
    result = prepare_dataframes(csv_path, schema, engine)
    print(result)
        
def prepare_dataframes(csv: str, model_schema: dict, db_connection) -> str:
    """
    Prepare dataframes by transforming data according to the provided schema and load them into the database.

    Args:
        csv (str): The path to the CSV file containing the data.
        model_schema (dict): The schema configuration for transforming the data.
        db_connection (Engine): The SQLAlchemy engine for connecting to the database.

    Returns:
        str: A success message indicating that the data dump was successful.
    """
    df = pd.read_csv(csv)
    transformed_dfs = []
    
    for table_name, config in model_schema.items():
        # grab columns needed for each table (to merge and final columns for non-merge tables)
        spliced_df = df[config['initial_column']].drop_duplicates().reset_index(drop=True)
        # Essentially, if a primary key is not needed column
        if type(config['primary_key']) == str:
            # make primary key column
            final_df = make_id_column(spliced_df, config['primary_key'])
            # append non-merge tables and load them
            if not config['transform']:
                final_df = final_df[config['all_columns']].sort_values(by=config['primary_key'])
                transformed_dfs.append(final_df)
                print(load_table(final_df, table_name, db_connection))
        # If merge tables, grab merge table info and merge keys
        if config['transform']:
            merge_indexes = config['merge_frame_locations']
            merge_keys = config['merge_keys']
            merge_index_keys = list(zip(merge_indexes, merge_keys))
            
            if len(merge_index_keys) > 1:
                final_df = spliced_df
            # merge and load
            for idx, key in merge_index_keys:
                df_to_merge = transformed_dfs[idx]
                join_key = key
                final_df = merge_dataframes(final_df, df_to_merge, join_key)
                
            final_df = final_df[config['all_columns']].sort_values(by=config['primary_key'])
            transformed_dfs.append(final_df)
            print(load_table(final_df, table_name, db_connection))
            
    return f'Data dump success.'

def make_id_column(dataframe, primary_key: str):
    """
    Add a primary key column to the dataframe by using the index.

    Args:
        dataframe (DataFrame): The dataframe to modify.
        primary_key (str): The name of the primary key column to create.

    Returns:
        DataFrame: The modified dataframe with the primary key column.
    """
    dataframe[primary_key] = dataframe.index + 1
    dataframe = rearrange_cols(dataframe, primary_key)
    return dataframe

def rearrange_cols(dataframe, primary_key: str):
    """
    Rearrange the columns of the dataframe so that the primary key column is the first column.

    Args:
        dataframe (DataFrame): The dataframe to rearrange.
        primary_key (str): The name of the primary key column.

    Returns:
        DataFrame: The rearranged dataframe.
    """
    new_order = [primary_key] + [col for col in dataframe.columns if col != primary_key]
    dataframe = dataframe[new_order]
    return dataframe

def merge_dataframes(left_df, right_df, join_key: str):
    """
    Merge two dataframes on the specified join key.

    Args:
        left_df (DataFrame): The left dataframe to merge.
        right_df (DataFrame): The right dataframe to merge.
        join_key (str): The column name to join on.

    Returns:
        DataFrame: The merged dataframe.
    """
    left_df = left_df.merge(right_df, on = join_key)
    return left_df

def load_table(dataframe, table: str, engine) -> str:
    """
    Load the dataframe into the specified database table.

    Args:
        dataframe (DataFrame): The dataframe to load.
        table (str): The name of the table to load the data into.
        engine (Engine): The SQLAlchemy engine for connecting to the database.

    Returns:
        str: A success message indicating that the table was loaded to the database.
    """
    dataframe.to_sql(table, con=engine, index = False, if_exists ='append')
    return f'{table} loaded to database.'