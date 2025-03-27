import pandas as pd

data = {
    "student_id": [101,101,101,101,101, 
                   102,102,102,102,103,
                   103,103,103,103,104,  
                   104,104,104,104],
    
    "attendance_date": ["2024-03-01", "2024-03-02", "2024-03-03", "2024-03-04", "2024-03-05",
                        "2024-03-02", "2024-03-03", "2024-03-04", "2024-03-05", "2024-03-05",
                        "2024-03-06", "2024-03-07", "2024-03-08", "2024-03-09", "2024-03-01",
                        "2024-03-02", "2024-03-03", "2024-03-04", "2024-03-05"],
    
    "status": ["Absent", "Absent", "Absent", "Absent", "Present",
               "Absent", "Absent", "Absent", "Absent", "Absent",
               "Absent", "Absent", "Absent", "Absent", "Present",
               "Present", "Absent", "Present", "Present"]
}

df = pd.DataFrame(data)

def absent_streaks(attendance):
    attendance['attendance_date']=pd.to_datetime(attendance['attendance_date'])
    attendance=attendance.sort_values(by=['student_id', 'attendance_date'])
    absent_records=attendance[attendance['status']=='Absent'].copy()
    absent_records['gap']=absent_records.groupby('student_id')['attendance_date'].diff().dt.days.ne(1).cumsum()
    streaks = absent_records.groupby(['student_id', 'gap']).agg(
        absence_start_date=('attendance_date', 'first'),
        absence_end_date=('attendance_date', 'last'),
        total_absent_days=('attendance_date', 'count')
    ).reset_index()
    streaks = streaks[streaks['total_absent_days'] > 3]
    latest_streaks = streaks.loc[streaks.groupby('student_id')['absence_end_date'].idxmax()]
    
    return latest_streaks[['student_id', 'absence_start_date', 'absence_end_date', 'total_absent_days']]

result = absent_streaks(df)
print(result)