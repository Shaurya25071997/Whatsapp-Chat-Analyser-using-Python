import pandas as pd
import re


def preprocess(data):
    # Regular Expression to extract date, time, period, name, and message
    pattern = r"(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2})\s?(AM|PM|am|pm)?\s-\s([^:]+):\s(.*)"
    matches = re.findall(pattern, data)

    message_data = []
    for match in matches:
        date_part = match[0]
        time_part = match[1]
        period = match[2] if match[2] else ''
        user = match[3]
        message = match[4]

        datetime_string = f"{date_part}, {time_part} {period}"

        message_data.append({
            'date_time': datetime_string,
            'user': user,
            'message': message
        })

    # Create the DataFrame
    df = pd.DataFrame(message_data)

    # Convert 'date_time' to datetime object
    df['date_time'] = pd.to_datetime(df['date_time'], format='%m/%d/%y, %I:%M %p', errors='coerce')
    df.rename(columns={'date_time': 'date'}, inplace=True)

    # Add new time columns
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
