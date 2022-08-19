This web app is designed for health/wellness practioners
who want to improve their meditation practice by
tracking their daily meditation sessions

Sit Meditation | Timothy Threet | 2022
sit-meditation.herokuapp.com

Free sign up to access login only features including history of tracked meditations ("Sits"), meditation timer, and trends/ratings.

I designed this app to be as light as possible - while I appreciate apps like Calm and Headspace, I wanted a quick and easy way to set a quick timer to meditate, and then log my daily meditation sessions (how I felt afterwards, areas to work on, etc.).  No guided audio, not a lot of features - something more 'Zen'

API used for quote of the day: www.zenquotes.io

User Flow
A new user would need to sign up (First Name, Last Name, Email, Username and Password) or else the only feature they have access to is the quote of the day.

After signing up (or logging in), the user is again prompted with the quote of the day and a quick button to log a Sit.  There is also a timer function at the top if the user has not meditated yet and would like to do so at that time.

When logging a Sit, the user is prompted for the date, duration, title, body, and rating of the Sit.

After successfully logging a Sit, the user is taken to their history, where they can see previous days meditations and begin to track trends in their meditation habits.

There is also a How To page that teaches someone how to meditate and how to use the Sit Meditation app.

Key Tech Stack (full list available in requirements.txt):
Python==3.10.3
SQLAlchemy==1.4.40
Flask-SQLAlchemy==2.5.1
WTForms==3.0.1