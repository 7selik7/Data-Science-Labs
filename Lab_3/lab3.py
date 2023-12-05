import pandas as pd
import openpyxl


def parse_table_data(url: str):
    file_path = url
    workbook = openpyxl.load_workbook(file_path)

    sheet = workbook.active

    data = {}
    for row in sheet.iter_rows(min_row=1, values_only=True):
        key = row[0]
        data[key] = list(row[1:-1])
    data['Water_Resistance_Rating'] = [int(val[2:]) for val in data['Water_Resistance_Rating']]

    parsed_weights = {}
    for cell_A, cell_J in zip(sheet['A'][1:], sheet['J'][1:]):
        parsed_weights[cell_A.value] = 1 if cell_J.value == 'max' else -1

    return pd.DataFrame(data), parsed_weights


if __name__ == "__main__":
    df, weights = parse_table_data("input.xlsx")

    for column in df.columns:
        if column not in ['Product']:
            df[column] = df[column] / df[column].max()

    df['Score'] = sum(df[criterion] * weights[criterion] for criterion in weights.keys() if
                      criterion not in ['Product'])

    sorted_df = df.sort_values(by='Score', ascending=False)
    print(sorted_df[['Product', 'Score']])
