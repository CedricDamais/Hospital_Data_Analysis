# write your code here

import pandas as pd
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', 8)


def main():
    # Reading all 3 CSV files
    general_dataset = pd.read_csv('data/general.csv')
    sports_dataset = pd.read_csv('data/sports.csv')
    prenatal_dataset = pd.read_csv('data/prenatal.csv')

    # all the columns name must match the name of general_dataset
    sports_dataset.columns = general_dataset.columns
    prenatal_dataset.columns = general_dataset.columns

    # Merge the data into one
    dataset_ = pd.concat([general_dataset, prenatal_dataset], ignore_index=True, join='inner')
    merged_data_set = pd.concat([dataset_, sports_dataset], ignore_index=True, join='inner')
    merged_data_set.drop(columns=["Unnamed: 0"], axis=1, inplace=True)
    df = merged_data_set

    df.dropna(axis=0, how='all', inplace=True)

    # Normalising the gender into 'f' and 'm'
    def replace_gender(lst: list):
        """
        :param lst: List containing the gender of the DataFrame
        :return: List that normalized the gender column into 'f' and 'm' to facilitate the analysis of the data
        """
        for i in range(len(lst)):
            element = lst[i]
            if element in ['male', 'man']:
                lst[i] = 'm'
            elif element in ['female', 'woman']:
                lst[i] = 'f'
        return lst

    def replace_cols_value(dataframe, colum_name, element):
        dataframe[colum_name].fillna(element, inplace=True)

    # list of 'gender' column value
    lst_1 = df['gender'].to_list()
    df['gender'] = replace_gender(lst_1)
    df['gender'].fillna('f', inplace=True)
    # list of names of columns that we must go throw to remove all the NaN
    lst_remove = ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']
    for col_name in lst_remove:
        replace_cols_value(df, col_name, 0)

    # print(f'Data shape: {df.shape}')
    # print(df.sample(n=20, random_state=30))

    highest_num_of_patient = df.hospital.agg('mode').to_list()[0]

    # Calculating the share of patients in gen hospitals that suffers from stomach-related issues
    # Specify the condition for the other column
    other_column = 'diagnosis'  # Replace with the name of the other column
    condition_value = 'stomach'  # Replace with the desired value in the other column

    # Count the number of certain values in the column based on the condition in the other column
    gen_hspt_stmch_issues = df[df[other_column] == condition_value]['hospital'].value_counts().to_list()[0]
    amount_gen_hspt = (df['hospital'] == 'general').sum()
    share = (gen_hspt_stmch_issues/amount_gen_hspt).round(3)

    # Calculating the share of patients in sport hospitals that suffers from dislocation issues
    sport_hspt_disloc_issues_serie = df[df['diagnosis'] == 'dislocation']['hospital'].value_counts()
    sport_hspt_disloc = tuple((index, value) for index, value in sport_hspt_disloc_issues_serie.items())[0][1]
    amount_sport_hspt = (df['hospital'] == 'sports').sum()
    share_sport = (sport_hspt_disloc/amount_sport_hspt).round(3)

    # Median age in general hospital
    medians_tup = (tuple((index, value) for index, value in (df.groupby(['hospital'])['age']).median().items()))
    sport_median_age = 0
    general_median_age = 0
    
    # Getting each median age from the tuple
    for element in medians_tup:
        if element[0] == 'sports':
            sport_median_age = element[1]
        elif element[0] == 'general':
            general_median_age = element[1]
    diff_sport_general = general_median_age - sport_median_age

    # Getting as a tuple the value counts of the blood test that were taken
    tup_blood_test = (tuple((index, value) for index, value in df.groupby(['blood_test'])['hospital'].value_counts().items()))
    hospital_most_blood_test = ''
    max_blood_test = 0

    # Going through the tuple to take the hospital with the highest amount of blood_test taken
    for el in tup_blood_test:
        if 't' in el[0] and max_blood_test < el[1]:
            max_blood_test = el[1]
            hospital_most_blood_test = el[0][1]

    # Print the answers
    print(f"The hospital with the highest number of patient is: {highest_num_of_patient}\n"
          f"The share of patient that are in general hospitals is of {share}\n"
          f"The share of patient that are in sports hospitals is of {share_sport}\n"
          f"The difference between the median age of patients in sport and general hospital is  {diff_sport_general}\n"
          f"The answer to the 5th question is {hospital_most_blood_test}, {max_blood_test} blood tests")

    # Start plotting Values
    ts = df.plot(y='age', kind='hist', bins=[0, 15, 35, 55, 70, 80])
    ts.plot()
    plt.show()

    ts = df['diagnosis'].value_counts().plot(kind='pie')
    ts.plot()
    plt.show()

    def create_dictionary(tup: tuple):
        """

        :param tup:tuple:
        :return dictionary of the tuple :
        """
        dic = {}
        for el in tup:
            hospital_type = el[0][0]
            if hospital_type not in dic:
                dic[hospital_type] = [el[0][1]]*el[1]
            else:
                dic[hospital_type] += [el[0][1]]*el[1]
        return dic

    ts = tuple((index, value) for (index, value) in df.groupby(['hospital'])['height'].value_counts().items())
    dic_hospitals_height = create_dictionary(ts)

    # List of the different heights in the hospitals
    general_height = dic_hospitals_height['general']
    sports_height = dic_hospitals_height['sports']
    prenatal_height = dic_hospitals_height['prenatal']

    data_list = [general_height, sports_height, prenatal_height]
    fig, axes = plt.subplots()
    plt.violinplot(dataset=data_list)
    plt.show()
    # Print the answers
    print("\n")
    print(f"Judging by the Histogram, the most common age of a patient among all hospitals: 15-35\n"
          f"The most common diagnosis among patients in all hospitals is: pregnancy\n"
          f"There is a big difference between the violin charts because the sport hospital does not use metric system \n")


if __name__ == "__main__":
    main()
