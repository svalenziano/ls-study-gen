from datetime import datetime, date, time, timedelta, tzinfo
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

"""
ABOUT THIS MODULE:
Written with the 'help' of AI.  In retrospect, I think it might be possible to 
simply use built-in methods with a few compact helper functions in 
~10 lines of code

"""

try:
    EDT = ZoneInfo("America/New_York")
    PDT = ZoneInfo("America/Los_Angeles")
except ZoneInfoNotFoundError as e:
    print()
    print("ERROR - maybe you need to `pip install tzdata`?")
    print(e, e.__traceback__)
    print()

def parse_date(string: str) -> datetime:
    """
    Parses a date string in 'MM-DD' or 'YYYY-MM-DD' format and returns a datetime object.
    If only 'MM-DD' is provided, uses the current year.
    """
    from datetime import datetime

    string = string.strip()

    try:
        if len(string) == 5 and '-' in string:
            # Format: MM-DD, use current year
            year = datetime.now().year
            return datetime.strptime(f"{year}-{string}", "%Y-%m-%d")
        elif len(string) == 10 and '-' in string:
            # Format: YYYY-MM-DD
            return datetime.strptime(string, "%Y-%m-%d")
        else:
            raise ValueError("Date string must be in 'MM-DD' or 'YYYY-MM-DD")
    except (Exception) as e:
        raise ValueError("Unknown error while parsing date", e)
    
def parse_time(timeStr:str) -> time:
    """
    timeStr:
        Time input format: HH:MM
        Expects: 24h format, EDT Time Zone
    return: time object in the user's timezone
    Raises error if timeStr is in incorrect format
    """
    timeStr = timeStr.strip()
    timezone = datetime.now().astimezone().tzinfo
    try:
        hour, minute = map(int, timeStr.split(":"))
        if not (0 <= hour < 24):
            raise ValueError("Hour must be between 0 and 23 (inclusive)")
        if not (0 <= minute < 60):
            raise ValueError("Minute must be between 0 and 59 (inclusive)")
        return time(hour=hour, minute=minute, tzinfo=timezone)
    except Exception:
        raise ValueError("Time string must be in 'HH:MM' 24h format")

def add_time_to_date(dateObj:datetime, timeObj:time) -> datetime:
    return dateObj.replace(hour=timeObj.hour, minute=timeObj.minute, tzinfo=timeObj.tzinfo)

def create_time_string(date_obj: datetime) -> str:
    """
    Input: datetime object in local
    Return: string eg "5:30 pm Eastern / 2:30 pm Pacific"
    """
    if date_obj.tzinfo == None:
        raise TypeError("date_obj must have timezone.  Aborting")
    
    try:
        eastern = date_obj.astimezone(EDT)
        pacific = date_obj.astimezone(PDT)
    except ZoneInfoNotFoundError as e:
        raise SystemError("")

    eastern_str = f"{format_time(eastern)} Eastern"
    pacific_str = f"{format_time(pacific)} Pacific"

    return f"{eastern_str} / {pacific_str}"



def format_time(dt):
    hour = dt.hour % 12 or 12
    minute = dt.minute
    ampm = "am" if dt.hour < 12 else "pm"
    return f"{hour}:{minute:02d} {ampm}"

def combine_date_and_time(dateStr:str, timeStr:str) -> datetime:
    """
    Input: date string and time string
    Return: datetime object
    """
    return add_time_to_date(parse_date(dateStr), parse_time(timeStr))

def tests():
    def test_parse_date():
        mydate = parse_date('2025-01-10')
        assert mydate.year == 2025
        assert mydate.month == 1
        assert mydate.day == 10
        assert type(mydate) == datetime

        mydate = parse_date('02-23')
        assert mydate.year == datetime.now().year
        assert mydate.month == 2
        assert mydate.day == 23

    def createDateAndAddTime():
        mydate = parse_date('01-23')
        mytime = parse_time('17:30')
        assert mytime.hour == 17
        assert mytime.minute == 30

        mydate = mydate.replace(hour=mytime.hour, minute=mytime.minute)
        assert mydate.hour == 17
        assert mydate.minute == 30
    
    def testaddTimeToDate():
        mydate = parse_date('   12-31')
        mytime = parse_time(' 11:59  ')
        mydate = add_time_to_date(mydate, mytime)
        assert mydate.hour == 11
        assert mydate.minute == 59

    def testMissingTimeZone():
        parse_time("18:05")  # this should not raise error
        # create_time_string(datetime.now())  # this should raise error
    
    def test_create_time_string():
        mydate = combine_date_and_time("01-01", "07:30")
        print(create_time_string(mydate))

    def test_EDT():
        # Create a datetime object for July 1st (during DST)
        edt = ZoneInfo("America/New_York")
        dt = datetime(2025, 7, 1, 12, 0, 0, tzinfo=ZoneInfo("America/New_York"))
        assert edt.utcoffset(dt) == timedelta(hours=-4)
        assert edt.dst(dt) == timedelta(hours=1)
        assert edt.tzname(dt) == "EDT"
        # Check that the datetime object reflects the correct offset
        assert dt.utcoffset() == timedelta(hours=-4)
        assert dt.tzname() == "EDT"


    test_parse_date()
    testMissingTimeZone()
    createDateAndAddTime()
    testaddTimeToDate()
    test_create_time_string()
    test_EDT()

    print("Tests passed!")


if __name__ == "__main__":
    tests()