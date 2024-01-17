import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def visualize_completeness():
    column_names = ['business_id', 'business_postal_code', 'business_name', 'violation_id',
                     'risk_category', 'violation_description', 'inspection_score', 'business_longitude',
                     'business_latitude', 'business_location', 'business_phone_number']

    empty_percentages = [0.57, 2.38, 3.31, 24.22, 24.22, 24.22, 26.24, 43.34, 43.34,
                   43.44, 68.36]

    plt.figure(figsize=(15, 10))
    plt.barh(column_names, empty_percentages)
    plt.xlabel('Percentage of missing values')
    plt.title('Percentage of missing values per column')
    plt.grid(axis='x', linestyle='--', alpha=0.6)

    for i, percent in enumerate(empty_percentages):
        plt.text(percent + 2, i, f'{percent:.0f}%', va='center', fontsize=11, color='black')

    plt.yticks(fontsize=13)
    plt.xlim(0, 110)
    plt.tight_layout()
    plt.show()

def plot_high_risk_violations_by_percentage(data):

    
    palette = sns.color_palette("coolwarm", n_colors=len(data))[:8]
    plt.figure(figsize=(14, 8))
    barplot = sns.barplot(
        y='Percentage',
        x='Type of High Risk',
        data=data,
        palette=palette
    )
    plt.xlabel('')
    plt.xticks([])
    for index, value in enumerate(data['Percentage']):
        plt.text(index, value, f'{value:.1f}%', va='bottom', ha='center', color='black', fontweight='bold')
    plt.title('Top 8 High Risk Violations by Percentage', fontsize=20)
    plt.ylabel('Percentage', fontsize=14)
    top_8_risks = [plt.Rectangle((0, 0), 1, 1, color=palette[i]) for i in range(len(data))]
    top_8_labels = data['Type of High Risk'].tolist()
    legend = plt.legend(top_8_risks, top_8_labels, title='Type of High Risk', loc="upper right", fontsize=12,
                        borderaxespad=0)
    plt.gca().add_artist(legend)
    sns.despine(top=True, right=True)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    data = pd.read_csv(('../input_files/DataSF_Restaurant_Inspections.csv'))
    visualize_completeness()

    high_risk_violations = data[data['risk_category'] == 'High Risk']
    high_risk_violations_counts = high_risk_violations['violation_description'].value_counts()
    high_risk_violations_percentages = (high_risk_violations_counts / high_risk_violations_counts.sum()) * 100
    high_risk_data = high_risk_violations_percentages.reset_index().head(8)
    high_risk_data.columns = ['Type of High Risk', 'Percentage']
    high_risk_data = high_risk_data.sort_values(by='Percentage', ascending=False)
    plot_high_risk_violations_by_percentage(high_risk_data)