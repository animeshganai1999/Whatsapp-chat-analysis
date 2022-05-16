import pandas as pd
import re 

def preprocesses(data):
    pattern = "\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{1,2}\s(?:PM|AM|am|pm)\s\-\s"
    messages = re.split(pattern,data)[1:]
    pattern_date = "\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{1,2}\s(?:PM|AM|am|pm)"
    dates = re.findall(pattern_date,data)
    df = pd.DataFrame({'user_message':messages,'message_date':dates})
    # Convert message_date type
    df = pd.DataFrame({'user_message':messages,'message_date':dates})
    # Convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'])
    df.rename(columns={'message_date':'date'},inplace = True)
    # Separate users and message
    users = []
    messages = []
    have_group_notification = False
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]: # User name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            have_group_notification = True
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'],inplace=True)    
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()
    df['only_date'] = df['date'].dt.date
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour)+'-'+'00')
        elif hour == 0:
            period.append('00'+'-'+str(hour+1))
        else:
            period.append(str(hour)+'-'+str(hour+1))
    df['period'] = period
    return df,have_group_notification

