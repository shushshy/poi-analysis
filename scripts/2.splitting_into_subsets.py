import pandas as pd
from sqlalchemy import create_engine


def split_into_subsets(data):
    data_copy = data.copy()
    data_copy = data_copy.drop_duplicates(subset=['business_name', 'business_address'])
    vague_addresses = ['Divisadero St', 'B Hayes St', 'Union St', 'Vicente St', 'Close to Park',
                       'Close to Golden Gate bridge', 'Unnamed ST', '377', 'Golden Gate Park', 'Fort Mason',
                       'Off The Grid-Upper Haight', 'Ocean Ave', 'Public', 'Off The Grid', 'OFF The Grid',
                       'Treasure Island Flea Market', 'Soma Street Food Park', 'Various Farmers Markets',
                       'Treasure Island', 'Approved Private Locations', 'Private & Public', 'Cortland Ave',
                       'Approved Locations', 'Approved Private Locations & Special Events', 'TFF Event Operations',
                       'Private Locations', 'OTG', 'Treasure Fest']

    low_quality_conditions = (
            data_copy['business_name'].isnull() |
            ((data_copy['business_address'].isin(vague_addresses)) &
             (~data_copy['business_latitude'].astype(str).str.startswith('37') |
              ~data_copy['business_longitude'].astype(str).str.startswith('-122')))
    )

    low_quality_data = data_copy[low_quality_conditions]
    print(len(low_quality_data))

    # Remove low quality data and provide dataframe with remaining records (containing medium and high)
    remaining_data = data_copy[~low_quality_conditions]

    dummy_names = ['hidden', 'Hidden', 'Unavailable']
    medium_quality_conditions = (
            remaining_data['business_address'].isin(vague_addresses) |
            ~remaining_data['business_latitude'].astype(str).str.startswith('37') |
            ~remaining_data['business_longitude'].astype(str).str.startswith('-122') |
            (remaining_data['business_postal_code'].astype(str).str.len() != 5) |
            (remaining_data['business_state'].astype(str) == 'IL') |
            remaining_data['business_phone_number'].isnull() |
            ~((remaining_data['business_phone_number'].str.len() == 11) & remaining_data[
                'business_phone_number'].str.startswith('1415')) |
            (remaining_data['business_name'].isin(dummy_names))
    )

    medium_quality_data = remaining_data[medium_quality_conditions]
    print(len(medium_quality_data))

    # What's left is considered high quality data
    high_quality_data = remaining_data[~medium_quality_conditions]
    print(len(high_quality_data))

    write_to_db(low_quality_data, 'low_quality_subset')
    write_to_db(medium_quality_data, 'medium_quality_subset')
    write_to_db(high_quality_data, 'high_quality_subset')


def write_to_db(dataframe, table_name):
    # assuming the database already exists
    server = r'DESKTOP-L8TSC8I\SQLEXPRESS01'
    database = 'POI_subsets'
    conn_str = f'mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
    engine = create_engine(conn_str)
    dataframe.to_sql(name=table_name, con=engine, if_exists='replace', index=False)


if __name__ == '__main__':
    dataset = pd.read_csv('../input_files/DataSF_Restaurant_Inspections.csv')
    split_into_subsets(dataset)
