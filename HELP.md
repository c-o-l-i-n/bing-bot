# 🦏 Bing Bot Help

- [🦏 Bing Bot Help](#-bing-bot-help)
  - [⚙️ How to change Bing's settings](#️-how-to-change-bings-settings)
  - [🙋 How to change the name Bing calls someone](#-how-to-change-the-name-bing-calls-someone)
  - [📲 How to move Bing to a different chat](#-how-to-move-bing-to-a-different-chat)
- [💻 Tech Stuff for Nerds](#-tech-stuff-for-nerds)
  - [🏃 How do I check if Bing is running?](#-how-do-i-check-if-bing-is-running)
  - [🌐 What online accounts are there?](#-what-online-accounts-are-there)
  - [🪵 How do I check the error logs?](#-how-do-i-check-the-error-logs)
  - [☠️ Code Expiration](#️-code-expiration)
  - [⏰ Scheduled Task Sketchiness](#-scheduled-task-sketchiness)
  - [🏔 Environment Variables](#-environment-variables)

## ⚙️ How to change Bing's settings

1. Navigate to the Settings Google Sheet at [go.osu.edu/bingsettings](https://go.osu.edu/bingsettings)
2. Check or uncheck the box next to any setting

## 🙋 How to change the name Bing calls someone

1. Navigate to the Settings Google Sheet at [go.osu.edu/bingsettings](https://go.osu.edu/bingsettings)
2. Go to the `Nicknames` tab
3. Edit the text in the `Nickname` column

## 📲 How to move Bing to a different chat

To move Bing to a different chat, you must create a new GroupMe bot:

1. Log into [dev.groupme.com](https://dev.groupme.com)
2. Navigate to the [Bots page](https://dev.groupme.com/bots)
3. Click ["Create Bot"](https://dev.groupme.com/bots/new)
4. Fill in the details:
   - Choose the group this bot will live in: `(Current H-Row Chat)`
   - Name: `Bing`
   - Callback URL: `https://bingbot.pythonanywhere.com/bing`
   - Avatar URL: `https://i.groupme.com/422x422.jpeg.87626f4f99aa48e19536cb96a7314851`
5. Click "Submit"
6. Copy the Bot ID, and paste it into the `GroupMe Bot ID` field in the `Tech Config` tab of the [Settings Google Sheet](https://go.osu.edu/bingsettings)
7. Click "Access Token" at the top right corner of the screen, copy it, and paste it into the `GroupMe Access Token` field in the `Tech Config` tab of the [Settings Google Sheet](https://go.osu.edu/bingsettings)

# 💻 Tech Stuff for Nerds

## 🏃 How do I check if Bing is running?
Either send a message in the chat "Bing, are you alive?" and see if she responds, or visit the URL of her server: https://bingbot.pythonanywhere.com/

## 🌐 What online accounts are there?

- [Google / Google Cloud Platoform](https://cloud.google.com/)
  - Settings Google Sheet
  - Google Sheets API credentials from GCP
  - Recieves emails
- [pythonanywhere](https://www.pythonanywhere.com/user/bingbot/webapps/#tab_id_bingbot_pythonanywhere_com)
  - Hosts the Python code that runs the web server and scheduled tasks
- [OpenWeather](https://home.openweathermap.org/api_keys)
  - Weather data API
- [Imgflip](https://imgflip.com/api)
  - Meme generator API

The username/email for all accounts is `hrow.bing.bot@gmail.com`

The password for all accounts is (all lowercase) the nickname of the OSUMB, then the serial number on H-Caliber.

## 🪵 How do I check the error logs?

[pythonanywhere](https://www.pythonanywhere.com/user/bingbot/files/var/log) provides a few different log files. Scroll all the way to the bottom for the latest log entries.

- [Error log](https://www.pythonanywhere.com/user/bingbot/files/var/log/bingbot.pythonanywhere.com.error.log)
- [Server log](https://www.pythonanywhere.com/user/bingbot/files/var/log/bingbot.pythonanywhere.com.server.log)
- [Access log](https://www.pythonanywhere.com/user/bingbot/files/var/log/bingbot.pythonanywhere.com.access.log)

## ☠️ Code Expiration

In free pythonanywhere accounts, [scheduled tasks (Bing's unsolicited messages) expire every 4 weeks, and web apps (Bing's command responses) expire every 3 months.](https://blog.pythonanywhere.com/129/)

  pythonanywhere will email Bing a link to keep things running a week before things expire. Bing's email currently forwards to me, Colin, so I'll probably click the link every time. If I don't click the link, there are buttons in the pythonanywhere dashboard that keep things running.

## ⏰ Scheduled Task Sketchiness

Unsolicited messages when using pythonanywhere (and other free hosting tools) are a bit sketchy because free pythonanywhere accounts only let you have 1 daily scheduled task. I tried doing every unsolicited message from a single Python scheduler file, but pythonanywhere only allows schedlued tasks to last up to 2 hours, which won't work if we want to run tasks the whole day.

__The plan:__
- Set up a Flask endpoint to send an unsolicited message when hit
- Hit that endpoint using cron jobs triggered by the free service cron-jobs.org
- Use my 1 daily Python scheduled task to change the cron-job.org cron jobs to random times
- Profit

## 🏔 Environment Variables

These environment variables are require in pythonanywhere for Bing to work properly. They are set within the `.env` file in the project root.

| Key                              | Value                                      | Notes                                      |
| -------------------------------- | ------------------------------------------ | ------------------------------------------ |
| `TZ`                             | `America/New_York`                         | Time zone used for scheduled jobs          |
| `GOOGLE_APPLICATION_CREDENTIALS` | `/home/bingbot/bing-bot/credentials.json`  | Path to Google credentials file            |
| `CREDENTIALS_JSON`               | _(Credentials JSON data generated by GCP)_ | Ask Colin if you need this                 |
| `SPREADSHEET_ID`                 | _(Settings Google Sheet ID from URL)_      | docs.google.com/spreadsheets/d/`ID`/edit |