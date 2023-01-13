import pandas as pd


def calcul_utility(diff, avg_salary_original):
    if diff < 0.1 * avg_salary_original:
        score = 1 - diff / avg_salary_original
    else:
        score = 0
    return score


def main(df_anonym, df_original, param, nb_lignes):
    df = df_anonym.copy()
    df_orig = df_original.copy()
    # converting salary to float and replacing '$' and ',' and splitting
    df_salary = pd.DataFrame({'Salary': df['Salary-interval'].copy()})
    df_salary['Min'] = df_salary['Salary'].str.split(',').str[0]
    df_salary['Max'] = df_salary['Salary'].str.split(',').str[1]

    for i in range(len(df_salary)):
        df_salary['Min'][i] = str(df_salary['Min'][i]).replace('[', '').replace('$', '').replace(']', '')
        df_salary['Max'][i] = str(df_salary['Max'][i]).replace('[', '').replace('$', '').replace(']', '')
    df_salary['Min'] = df_salary['Min'].astype(float)
    df_salary['Max'] = df_salary['Max'].astype(float)
    df_salary['Moy'] = (df_salary['Min'] + df_salary['Max']) / 2
    df['Salary'] = df_salary['Moy']

    df_orig_salary = df_orig.Salary.copy()
    for i in range(len(df_orig_salary)):
        df_orig_salary[i] = df_orig_salary[i].replace('$', '', len(df_orig_salary)).replace(',', '',
                                                                                            len(df_orig_salary))

    df_orig_salary = df_orig_salary.astype(float)
    df_orig.Salary = df_orig_salary

    # average salary of each job
    df = df.groupby(by=['Job-Titles'])['Salary'].mean().reset_index().rename(columns={'Salary': 'avg_salary'})
    df_orig = df_orig.groupby(by=['Job-Titles'])['Salary'].mean().reset_index().rename(
        columns={'Salary': 'orig_avg_salary'})

    df_orig['diff'] = abs(df['avg_salary'] - df_orig['orig_avg_salary'])
    df_orig['score'] = df_orig.apply(lambda x: calcul_utility(x['diff'], x['orig_avg_salary']), axis=1)
    score = df_orig['score'].sum()
    nb_lignes = len(df_orig['score'])
    return score / nb_lignes


# test
df_anonym = pd.read_csv("anonymous.csv")
df_original = pd.read_csv("venv/DataSet/dataset_2.0.csv")

result = str(100 * main(df_anonym, df_original))

print("Score of the utility 1 is " + result[0:5] + " %")
