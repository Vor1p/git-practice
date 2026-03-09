from datetime import date, timedelta, datetime

# Subtract five days from current date
today = date.today()
five_days = timedelta(days=5)

new_date = today - five_days
print(new_date)

# Print yesterday, today, tomorrow
today = date.today()
one_day = timedelta(days=1)

yesterday = today - one_day
tomorrow = today + one_day

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

# Drop microseconds from datetime
now = datetime.now()
print("Before:", now)

no_microseconds = now.replace(microsecond=0)
print("After:", no_microseconds)

# Calculate two date difference in seconds
date1 = datetime(2026, 2, 25, 10, 0, 0)
date2 = datetime(2026, 2, 25, 12, 30, 0)

difference = date2 - date1
seconds = difference.total_seconds()

print(seconds)