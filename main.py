

import datetime
import json
import os
import random
from collections import defaultdict

import time_zone_utils as util

# ///////////////////////////////////////////////////////////
# CONFIG
output_path = r"/mnt/c/Users/senor/Obsidian_Syncthing/SV_Personal2/03 Work/0/LS TA Work Stuff/study-session-staging"
courses = {
    'LS171': [
        ('01-08', '11:00'),
        ('01-20', '20:30'),
    ],
    # 'PY109': [
    #     ('12-13', '16:00'),
    # ],
    # 'PY119': [
    #     ('12-15', '19:00'),
    #     ('12-04', '15:00'),
    # ],
    # 'PY129': [
    #     ('12-04', '11:00'),
    #     ('12-18', '20:00'),
    # ],
    # 'PEDAC': [
    #     ('12-08', '20:00'),
    #     ('12-18', '18:30'),
    # ],
}


# ///////////////////////////////////////////////////////////
# CODE


directory = os.path.dirname(__file__)      # Get directory without filename
path = os.path.join(directory, 'messages.json') # Append desired text file filename

with open(path) as file:
    mydict = json.load(file)

def print_by_day(sessions=courses):
    """
    Print sessions grouped by date in ascending date-key order.
    sessions: dict[str, list[tuple[str, str]]] where each value is a list
              of (date_str, time_str) tuples, e.g. ("10-09", "20:00").
    """
    print("SESSIONS BY DAY:")
    days = defaultdict(list)
    for course_code, entries in sessions.items():
        for date, time in entries:
            days[date].append(f"{course_code} at {time}")

    for day in sorted(days):
        print(f"{day} -> {', '.join(days[day])}")
    print()
    

def fuzzy_get(containsKey:str, myDict:dict) -> str:
    """
    Warning: the functionality is slightly counter-inuitive!
    containsKey: string that should contain a key in myDict
    Returns: entry from myDict if the key is a substring of `containsKey`
    EXAMPLE: 
        containsKey = 'PY101 / PY109'
        myDict = {'py109': ..., 'py129': ...}
        returns = the value for key 'py109'
    """
    for key in myDict.keys():
      if key.lower() in containsKey.lower():
          return myDict[key]
    raise ValueError(f"""None of the dict keys were found in `containsKey`:
    dict keys = {myDict.keys()}
    containsKey = {containsKey}
                     """)

def random_greeting() -> str:
    return random.choice(mydict['misc']['greetings']) 


def validate_course(course:str):
    if course == "(no course selected)":
        raise ValueError(f"Looks like you forgot to select a course? {course=}")

def main():
    print(f"""Writing to: "{output_path}"...""")
    for courseCode in courses:
        for day, time in courses[courseCode]:
            # GET COURSE INFO
            course_dict:dict = fuzzy_get(courseCode, mydict['courses'])
            dt:datetime = util.combine_date_and_time(day, time)
            time:str = util.create_time_string(dt)
            date:str = dt.strftime("%A %B %d, %Y")
            default_summary = f"I will be hosting a study group for students in {course_dict['enrollment']}"

            # BUILD FILEPATH
            filename:str = f"{dt.strftime("%H;%M %a %b %d")} {courseCode}.md"
            fullpath = os.path.join(output_path, filename)  # Example 20;00 Tues Sep 23 LS171
            
            # CHECK FOR EXISTING FILE
            if os.path.exists(fullpath):
                print(f"{filename} -> Skipped because it already exists")
            else:         
                


                # BUILD MESSAGE (based on https://3.basecamp.com/3695031/buckets/24505682/documents/4249499643)
                message = f"""
==forum-url==
              
## TODO
- [ ] [General Forum](https://launchschool.com/forum?tab=Study+Groups) post
	- [ ] Claim, AND Close the post.  Pin if happening soon.
- [ ] [Calendar event](https://launchschool.com/events)
- [ ] Slack post (optional)
- [ ] One day before session
	- [ ] Slots left?  Post reminder in Slack
- [ ] 10-15 mins before
	- [ ] Create slack group and message participants
- [ ] After session
	- [ ] Slack: thanks and [feedback link](https://docs.google.com/forms/d/e/1FAIpQLSfSFQqEZnxjY7Z_pKyIYociBCYApoKSpe1VKW_XCRd5Occlqw/viewform)
	- [ ] Forum post: Unpin and Close
	- [ ] Submit the [Study Session Tracking Form](https://docs.google.com/forms/d/e/1FAIpQLScLVGNxnT2rS4Og_qCg-A673DdlezGELdk0P4AwkTzSWGWHNw/viewform)

## FORUM POST
### TITLE
{course_dict['full_name']} | {date} | {time} 
  

### CONTENT
{random_greeting()}  {course_dict.get('summary', default_summary)}  
  
- **Date:** {date}
- **Time:** {time}
- **Duration:** 1 hour  
- **Activity:** {course_dict['activity']}
- **Platform:** We'll be meeting in **GatherTown** for our study session. If you haven't used Gather before, please read [these instructions](https://launchschool.com/gists/3de2ddcc) and do a test run _before_ our study session. Shortly before, I'll be sending a group message on Slack with instructions for where in Gather to meet.
- **Sign up:**  Study groups are for **currently subscribed students** who are enrolled in {course_dict['enrollment']}.   

To sign up, **comment below with:**
- **(1) Your Slack name**
- **(2) Where you are in the curriculum**
- **(3) How many TA sessions {courseCode} you have already attended**
- **(4) Optional:** any specific goals for the session, or topics you'd like to cover?

There is space for five students.  _Students who have not participated in a study group before will be given priority_.  If it looks like five people are already signed up, but you haven't yet had a chance to attend a study group, please leave your name below anyway.


## CALENDAR POST
### TITLE
{course_dict['full_name']} with Steven

### CONTENT
Think of this as an after-class study group where students can take what they've learned and share in a team-oriented approach. This has proven to be a great way to meet other students and prepare for real-world job interviews and assessments.

**_Requirements:_** Attendance is limited to currently enrolled students who are enrolled in {course_dict['enrollment']}.

Sign-ups and more info: ==forum-url==


## SLACK POST
{random_greeting()}
I just posted a {courseCode} study session to the forum, scheduled for {date} at {time}.  You can sign up [here](https://launchschool.com/forum?tab=Study+Groups), I hope you can join us!  ==forum-url==

## 1 DAY BEFORE
{random_greeting()}
There are still ==a couple of== slots open in the {courseCode} study session for tomorrow at {time}! More info & sign-up here: ==forum-url==

## DAY-OF STUFF

### 'ABOUT TO START'
Hi all, our {courseCode} study session will be starting in a few minutes at {time}, see you in Gathertown!  Look for me in one of the black and gold breakout rooms in the center of the space.

### Session Notes
- See [[TA Study Session Icebreaker]]
- tktk
- tktk
- tktk

### 'THANKS FOR ATTENDING'
{random.choice(mydict['misc']['post-session-thanks'])}  Please remember to keep the questions we studied to yourself, as sharing them may reduce the value of our study sessions for other students.

I'm always looking to improve, so I greatly appreciate any and all feedback you might have.  You can leave anonymous feedback [here](https://docs.google.com/forms/d/e/1FAIpQLSfSFQqEZnxjY7Z_pKyIYociBCYApoKSpe1VKW_XCRd5Occlqw/viewform), or simply DM me. Positive feedback is also helpful :)
"""

                # WRITE MARKDOWN FILES
                try:
                    with open(fullpath, 'x', encoding='utf-8') as f:
                        f.writelines(message)
                except IOError as e:
                    print(f"{e.__class__.__name__}: {e}")

                print(f"{filename} -> Success!")



    

if __name__ == "__main__":
    main()
    print_by_day()