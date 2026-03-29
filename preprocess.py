import re
import pandas as pd
pd.set_option('display.max_columns', None)  # Show all columns


def preprocess_data(data):
    
    # Split messages
    messages = re.split(
        r'\n(?=\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s?[ap]m\s-\s)', 
        data
    )

    dates = []
    times = []
    users = []
    texts = []

    pattern = r"(\d{2}/\d{2}/\d{2}),\s(\d{1,2}:\d{2}\s?[ap]m)\s-\s(.+?):\s(.+)"

    for msg in messages:
        msg = msg.strip()

        match = re.match(pattern, msg)

        if match:
            date, time, user, text = match.groups()
        else:
            # system message
            parts = msg.split(" - ", 1)
            if len(parts) == 2:
                date_time, text = parts
                date, time = date_time.split(", ")
                user = "system"
            else:
                continue

        dates.append(date)
        times.append(time)
        users.append(user)
        texts.append(text)

    # Create DataFrame
    df = pd.DataFrame({
        "date": dates,
        "time": times,
        "user": users,
        "message": texts
    })

    # Clean time (handle WhatsApp special space)
    df['time'] = df['time'].str.replace('\u202f', ' ', regex=False)

    # Create datetime directly (NO meridian needed)
    df['datetime'] = pd.to_datetime(
        df['date'] + ' ' + df['time'],
        format='%d/%m/%y %I:%M %p',
        errors='coerce'
    )

    # Drop unnecessary columns
    df.drop(columns=['date', 'time'], inplace=True)

    # Feature extraction
    df['year'] = df['datetime'].dt.year
    df['only_date']=df['datetime'].dt.date
    df['day_name'] = df['datetime'].dt.day_name()
    df['month'] = df['datetime'].dt.month_name()
    df['month_num'] = df['datetime'].dt.month
    df['day'] = df['datetime'].dt.day
    df['minute'] = df['datetime'].dt.minute
    df['hour'] = df['datetime'].dt.hour

    periods = []
    for hour in df['hour']:
        if hour == 23:
            periods.append('23-00')
        elif hour == 0:
            periods.append('00-1')
        else:
            periods.append(f"{hour}-{hour+1}")
    df['period'] = periods

    return df



