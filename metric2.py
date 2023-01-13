import pandas as pd


# function that calculate the final score

def calcul_utility(difference, original_perc):
    if difference < 0.5 * original_perc:
        return 1 - difference / original_perc
    else:
        return 0


def pourcentage(diff, total):
    diff = diff / total


def main(df_anon, df_original, params, nb_lignes):
    pd.set_option('display.max_rows', None)
    df = pd.read_csv(df_original).copy()
    df_anon = pd.read_csv(df_anon).copy()

    # changing zip code column's type to string

    df['Zip'] = df['Zip'].astype(str)
    df_anon['Zip'] = df_anon['Zip'].astype(str)

    # getting the list of the unique values of zip-code, and it's length

    test = df_anon['Zip'].unique()
    size1 = test.size
    dfGlob = pd.DataFrame()
    count = 0

    # loop to get the count of each person working under a department in a given region
    # (first 2 digit of the zip code)

    for x in range(size1):
        dfGlob["df_dep_orig"] = df.loc[df['Zip'].str[:2] == test.item(x), "Department"].value_counts(
            ascending=True).sort_index(ascending=True)
        dfGlob["df_dep_anonym"] = df_anon.loc[df_anon['Zip'] == test.item(x), "Department"].value_counts(
            ascending=True).sort_index(ascending=True)

        sumOriginal = sum(dfGlob["df_dep_orig"])
        sumAnonym = sum(dfGlob["df_dep_anonym"])

        dfGlob["perc_original"] = dfGlob["df_dep_orig"].apply(lambda x: x / sumOriginal)
        dfGlob["perc_anonym"] = dfGlob["df_dep_anonym"].apply(lambda x: x / sumAnonym)

        dfGlob["diff_perc"] = abs(dfGlob['perc_original'] - dfGlob['perc_anonym'])
        dfGlob['score_region'] = dfGlob.apply(lambda x: calcul_utility(x['diff_perc'], x['perc_original']), axis=1)

        region_score = sum(dfGlob['score_region']) / len(dfGlob)
        count = count + region_score
        dfGlob = pd.DataFrame()

    # calcul du score
    score_final = count / size1
    return score_final


result = str(100*main("anonymous.csv", "venv/DataSet/dataset_2.0.csv"))
print("Score of the utility 2 is "+result[0:5]+" %")
