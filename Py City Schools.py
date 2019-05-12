import pandas as pd
import numpy as np

school_data_file = "Resources/schools_complete.csv"
student_data_file = "Resources/students_complete.csv"

school_data = pd.read_csv(school_data_file)
student_data = pd.read_csv(student_data_file)

school_data_total= pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])

school_data_total.head()


total_schools = len(school_data_total ['school_name'].unique())
total_students = school_data_total['student_name'].count()
total_budget = sum(school_data_total['budget'].unique())
average_math = school_data_total['math_score'].mean()
average_reading = school_data_total['reading_score'].mean()

overall_passing = (average_math + average_reading)/2
passing_math = (school_data_complete[school_data_complete['math_score']>=70]['student_name'].count()/total_student)*100
passing_reading = (school_data_complete[school_data_complete['reading_score']>=70]['student_name'].count()/total_student)*100


district = {
    'Total Schools':total_schools,
    'Total Students':'{:,}'.format(total_students),
    'Total Budget':'${:,.2f}'.format(total_budget),
    'Average Math Score':average_math,
    'Average Reading Score':average_reading,
    '% Passing Math':passing_math,
    '% Passing Reading':passing_reading,
    '% Overall Passing Score':[overall_passing],  
}

district_summary = pd.DataFrame(district)
district_summary


all_schools = school_data_complete.groupby(['school_name'])
school_type = all_schools['type'].first()
total_students = all_schools.size()
total_budget = all_schools['budget'].first()
total_budget_per_student = total_budget/total_students
average_math_score = all_schools['math_score'].mean()
average_reading_score = all_schools['reading_score'].mean()
grouped_passing_math = school_data_complete[school_data_complete['math_score']>=70].groupby(['school_name']).size()
percent_passing_math = (grouped_passing_math/total_student)*100
grouped_passing_reading = school_data_complete[school_data_complete['reading_score']>=70].groupby(['school_name']).size()
percent_passing_reading = (grouped_passing_reading/total_student)*100
percent_overall_passing = (percent_passing_math + percent_passing_reading)/2

school={
    'School Type': school_type,
    'Total Students':total_students,
    'Total School Budget': total_budget,
    'Total Budget per Student': total_budget_per_student,
    'Average Math Score': average_math_score,
    'Average Reading Score': average_reading_score,
    '% Passing Math': percent_passing_math,
    '% Passing Reading': percent_passing_reading,
    '% Overall Passing Rate': percent_overall_passing,
}
school_summary = pd.DataFrame(school)
displayed_school_summary = school_summary.copy()

displayed_school_summary['Total Budget per Student'] = displayed_school_summary['Total Budget per Student'].map('${:,.2f}'.format)
displayed_school_summary['Total School Budget'] = displayed_school_summary['Total School Budget'].map('${:,.2f}'.format)
displayed_school_summary.index.name = None


bottom_performing_schools = displayed_school_summary.sort_values(by='% Overall Passing Rate')
bottom_performing_schools.head()



school_avg_math_9th = school_data_complete[school_data_complete['grade']=='9th'].groupby('school_name')['math_score'].mean()
school_avg_math_10th = school_data_complete[school_data_complete['grade']=='10th'].groupby('school_name')['math_score'].mean()
school_avg_math_11th = school_data_complete[school_data_complete['grade']=='11th'].groupby('school_name')['math_score'].mean()
school_avg_math_12th = school_data_complete[school_data_complete['grade']=='12th'].groupby('school_name')['math_score'].mean()

grade_math_score={
    '9th':school_avg_math_9th,
    '10th':school_avg_math_10th,
    '11th':school_avg_math_11th,
    '12th':school_avg_math_12th,
    }

math_score_by_grade = pd.DataFrame(grade_math_score)
math_score_by_grade.index.name = None
math_score_by_grade.head(20)




school_avg_reading_9th = school_data_complete[school_data_complete['grade']=='9th'].groupby('school_name')['reading_score'].mean()
school_avg_reading_10th = school_data_complete[school_data_complete['grade']=='10th'].groupby('school_name')['reading_score'].mean()
school_avg_reading_11th = school_data_complete[school_data_complete['grade']=='11th'].groupby('school_name')['reading_score'].mean()
school_avg_reading_12th = school_data_complete[school_data_complete['grade']=='12th'].groupby('school_name')['reading_score'].mean()

grade_reading_score={
    '9th':school_avg_reading_9th,
    '10th':school_avg_reading_10th,
    '11th':school_avg_reading_11th,
    '12th':school_avg_reading_12th,
    }

reading_score_by_grade = pd.DataFrame(grade_reading_score)
reading_score_by_grade.index.name = None
reading_score_by_grade.head(20)

# Sample bins. Feel free to create your own bins.
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]

scores_spending = school_summary.loc[:,['Average Math Score',
                                  'Average Reading Score','% Passing Math',
                                  '% Passing Reading','% Overall Passing Rate',]]

scores_spending['Spending Ranges (Per Student)']= pd.cut(school_summary['Total Budget per Student'],spending_bins,labels=group_names)

scores_spending = scores_spending.groupby('Spending Ranges (Per Student)').mean()
scores_spending.head()


size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]




scores_size = school_summary.loc[:,['Average Math Score',
                                  'Average Reading Score','% Passing Math',
                                  '% Passing Reading','% Overall Passing Rate',]]

scores_size['Total Students']= pd.cut(school_summary['Total Students'],size_bins,labels=group_names)

scores_size = scores_size.groupby('Total Students').mean()
scores_size.head()


scores_type = school_summary[['School Type','Average Math Score',
                                  'Average Reading Score','% Passing Math',
                                  '% Passing Reading','% Overall Passing Rate',]]

scores_type = scores_type.groupby('School Type').mean()
scores_type.head()