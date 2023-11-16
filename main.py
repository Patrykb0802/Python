import pandas as pd
import matplotlib.pyplot as plt


class CreditDataAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        self.data = pd.read_csv(self.file_path)

    def remove_duplicates(self):
        self.data = self.data.drop_duplicates()

    def calculate_correlation(self):
        correlation = self.data[['age', 'limit_bal']].corr().iloc[1, 0]
        return correlation

    def add_total_bill_column(self):
        bill_columns = ['bill_amt1', 'bill_amt2', 'bill_amt3', 'bill_amt4', 'bill_amt5', 'bill_amt6']
        self.data['total_bill'] = self.data[bill_columns].sum(axis=1)

    def get_top_oldest_clients(self, n=10):
        top_oldest_clients = self.data.nlargest(n, 'age')

        education_mapping = {
            'education:1': 'graduate school',
            'education:2': 'university',
            'education:3': 'high school',
            'education:4': 'others'
        }

        selected_columns = ['limit_bal', 'age'] + list(education_mapping.keys())
        top_oldest_clients = top_oldest_clients[selected_columns]

        top_oldest_clients = top_oldest_clients.rename(columns=education_mapping)

        return top_oldest_clients

    def plot_histograms_and_scatter(self):

        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))

        axes[0, 0].hist(self.data['limit_bal'], bins=30, color='blue', alpha=0.7)
        axes[0, 0].set_title('Histogram Limitu Kredytu')
        axes[0, 0].set_xlabel('Limit Kredytu')
        axes[0, 0].set_ylabel('Ilość')

        axes[0, 1].hist(self.data['age'], bins=30, color='green', alpha=0.7)
        axes[0, 1].set_title('Histogram Wieku')
        axes[0, 1].set_xlabel('Wiek')
        axes[0, 1].set_ylabel('Ilość')

        axes[1, 0].scatter(self.data['age'], self.data['limit_bal'], color='red', alpha=0.5)
        axes[1, 0].set_title('Zależność Limitu Kredytu od Wieku')
        axes[1, 0].set_xlabel('Wiek')
        axes[1, 0].set_ylabel('Limit Kredytu')

        axes[1, 1].axis('off')

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    analyzer = CreditDataAnalyzer('train.txt')
    analyzer.load_data()
    analyzer.remove_duplicates()
    analyzer.add_total_bill_column()
    correlation = analyzer.calculate_correlation()
    top_oldest_clients = analyzer.get_top_oldest_clients()

    print(f"Korelacja pomiędzy wiekiem a limitem kredytu:\n {correlation}")
    print(analyzer.data.head())
    print(top_oldest_clients)
    plt.table(cellText=top_oldest_clients.values, colLabels=top_oldest_clients.columns, loc='center')
    plt.axis('off')
    plt.show()

    analyzer.plot_histograms_and_scatter()

