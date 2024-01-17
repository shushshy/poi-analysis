import pandas as pd


def check_percentage_empty_columns(data):
    missing_data = data.isnull().sum().sort_values()
    missing_percentage = (missing_data / len(data)) * 100
    formatted_percentage = missing_percentage.apply(lambda x: f'{x:.2f}%')
    print('Percentage of empty values for each column')
    print(formatted_percentage)

def check_frequent_values(data):
    columns_list = [  'business_city', 'business_state', 'inspection_score',
                      'inspection_type', 'violation_description', 'risk_category']
    for column in columns_list:
        value_counts = data[column].value_counts()
        value_counts = value_counts.sort_index(ascending=True)
        number_unique_values = len(value_counts)
        print(f'Number of unique values in column {column}: {number_unique_values}')


        percentage_values = (value_counts / len(data)) * 100
        print(f'Percentage of each value in column {column}:')
        for value, percentage in percentage_values.items():
            print('{}: {:.2f}%'.format(value, percentage))
        print("\n")

def top_7_values(data):
    # at first used this function to get top 7 for inspection columns, nut it was useful for dummy values as well
    columns_of_interest = ['business_id', 'business_name', 'business_address', 'business_city', 'business_state',
                           'business_postal_code', 'business_latitude', 'business_longitude', 'business_location',
                           'business_phone_number', 'inspection_id', 'inspection_date', 'inspection_score',
                           'inspection_type', 'violation_id', 'violation_description', 'risk_category']

    for column in columns_of_interest:
        total_records = len(data)
        top_values_percentage = (data[column].value_counts() / total_records * 100).head(7)
        print(f'Top 7 values for {column} (as percentages):')
        print(top_values_percentage)
        print("\n")

def check_unique_POIs(data):

    unique_names = data['business_name'].nunique()
    unique_addresses = data['business_address'].nunique()
    print(f'Unique business names: {unique_names}, unique business addresses: {unique_addresses}')

    unique_poi = data.drop_duplicates(subset=['business_name', 'business_address'])
    print(f'Number of unique POIs: {len(unique_poi)}')

def zipcode_check(data):
    data['business_postal_code'] = data['business_postal_code'].astype(str)
    different_than_5_digit = data[data['business_postal_code'].astype(str).str.len() != 5]
    different_than_5_digit = different_than_5_digit[['business_name', 'business_address', 'business_city', 'business_state',
                           'business_postal_code']].drop_duplicates(subset=['business_postal_code'])
    print(different_than_5_digit)

def find_unstandardized_phone(data):
    data = data.dropna(subset='business_phone_number')
    data['business_phone_number'] = data['business_phone_number'].astype(str)
    not_standard_phones = data[~((data['business_phone_number'].str.len() == 11) & data['business_phone_number'].str.startswith('1415'))]



if __name__ == '__main__':
    data = pd.read_csv(('../input_files/DataSF_Restaurant_Inspections.csv'))
    check_percentage_empty_columns(data)
    check_frequent_values(data)
    top_7_values(data)
    check_unique_POIs(data)
    zipcode_check(data)
    find_unstandardized_phone(data)


