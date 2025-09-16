from prettytable import PrettyTable


def display_table(max_rate, min_rate, avg_rate):
    table = PrettyTable()
    table.field_names = ['Показатель', 'Валюта', 'Дата', 'Курс']
    table.add_row(
        [
            'Максимальный курс', max_rate.currency,
            max_rate.date, f"{max_rate.rate:.4f}"
        ]
    )
    table.add_row(
        [
            'Минимальный курс', min_rate.currency,
            min_rate.date, f"{min_rate.rate:.4f}"
         ]
    )
    table.add_row(
        [
            'Средний курс (по всем валютам)', '-',
            '-', f'{avg_rate:.4f}'
        ]
    )
    print(table)
