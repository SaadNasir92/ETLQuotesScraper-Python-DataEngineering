import pandas as pd
            
def dump_data(csv_path, schema, engine):
        result = prepare_dataframes(csv_path, schema, engine)
        print(result)
        
def prepare_dataframes(csv, model_schema, db_connection):
    df = pd.read_csv(csv)
    transformed_dfs = []
    
    for table_name, config in model_schema.items():
        
        spliced_df = df[config['initial_column']].drop_duplicates().reset_index(drop=True)
        if type(config['primary_key']) == str:
            final_df = make_id_column(spliced_df, config['primary_key'])
            if not config['transform']:
                final_df = final_df[config['all_columns']].sort_values(by=config['primary_key'])
                transformed_dfs.append(final_df)
                print(load_table(final_df, table_name, db_connection))

        if config['transform']:
            merge_indexes = config['merge_frame_locations']
            merge_keys = config['merge_keys']
            merge_index_keys = list(zip(merge_indexes, merge_keys))
            
            if len(merge_index_keys) > 1:
                final_df = spliced_df

            for idx, key in merge_index_keys:
                df_to_merge = transformed_dfs[idx]
                join_key = key
                final_df = merge_dataframes(final_df, df_to_merge, join_key)
                
            final_df = final_df[config['all_columns']].sort_values(by=config['primary_key'])
            transformed_dfs.append(final_df)
            print(load_table(final_df, table_name, db_connection))
            
    return f'Data dump success.'

def make_id_column(dataframe, primary_key):
    dataframe[primary_key] = dataframe.index + 1
    dataframe = rearrange_cols(dataframe, primary_key)
    return dataframe

def rearrange_cols(dataframe, primary_key):
    new_order = [primary_key] + [col for col in dataframe.columns if col != primary_key]
    dataframe = dataframe[new_order]
    return dataframe

def merge_dataframes(left_df, right_df, join_key):
    left_df = left_df.merge(right_df, on = join_key)
    return left_df

def load_table(dataframe, table, engine):
    dataframe.to_sql(table, con=engine, index = False, if_exists ='append')
    return f'{table} loaded to database.'