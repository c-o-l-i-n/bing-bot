# 📖 Bing Bot User Guide

<img src="https://i.groupme.com/422x422.jpeg.87626f4f99aa48e19536cb96a7314851.avatar" align="right" />

Contents

- [About Bing Bot](#-about-bing-bot)
- [How to change Bing's settings](#%EF%B8%8F-how-to-change-bings-settings)
- [How to move Bing to a different chat](#-how-to-move-bing-to-a-different-chat)
- [How to change environment variables in Heroku](#-how-to-change-environment-variables-in-heroku)
- [How to view data from the database](#-how-to-view-data-from-the-database)

## 🦏 About Bing Bot

Bing Bot is a GroupMe chat bot for H-Row's mascot, Bing. It responds to different "commands" and sends unprompted messages throughout the day.

Bing Bot is a REST API built using the Python Flask framework, hosted on Heroku.

There are 4 components that make Bing run:
- This code repository
- A GroupMe bot on the owner's GroupMe account
- A Heroku app (h-row-bing-bot)
- A PostgreSQL database (Heroku Postgres add-on)

When new code is pushed to the "main" branch of this repository, the Heroku app is updated and re-deployed automatically. (Configured in Heroku settings)

## ⚙️ How to change Bing's settings

1. Navigate to [go.osu.edu/bingsettings](https://go.osu.edu/bingsettings) (or https://h-row-bing-bot.herokuapp.com/settings)
2. Type in the password, and click "Submit"
3. Update the features you want to turn on or off
4. Click "Save Settings"

## 📲 How to move Bing to a different chat

To move Bing to a different chat, you must create a new GroupMe bot:

1. Log into [dev.groupme.com](https://dev.groupme.com)
2. Navigate to the [Bots page](https://dev.groupme.com/bots)
3. Click ["Create Bot"](https://dev.groupme.com/bots/new)
4. Fill in the details:
    - Choose the group this bot will live in: ```{ Current H-Row Chat }```
    - Name: ```Bing```
    - Callback URL: ```https://h-row-bing-bot.herokuapp.com/bing```
    - Avatar URL: ```https://i.groupme.com/422x422.jpeg.87626f4f99aa48e19536cb96a7314851```
5. Click "Submit"
6. Copy the Bot ID, and paste it into the ```GROUPME_BOT_ID``` environment variable in Heroku ([details below](#-how-to-change-environment-variables-in-heroku))
7. If this bot belongs to a different GroupMe user than before: Click "Access Token" at the top right corner of the screen, copy it, and paste it into the ```GROUPME_ACCESS_TOKEN``` environment variable in Heroku ([details below](#-how-to-change-environment-variables-in-heroku))

## 🌐 How to change environment variables in Heroku

1. Log into [heroku.com](https://id.heroku.com/)
    - Email address: ```williamsca20+bingheroku@gmail.com```
    - Password: ```{ Email Buddy at the above email adress if you need the password }```
2. Navigate to: h-row-bing-bot > Settings
3. Click "Reveal Config Vars"
4. Click the pencil icon next to the environment variable you want to edit
5. Make the change in the "Value" textbox
6. Click "Save changes"

Verify the environment variables are set correctly:

```bash
# GroupMe bot ID, found at dev.groupme.com/bots
GROUPME_BOT_ID

# Your GroupMe user's access token, found at dev.groupme.com
GROUPME_ACCESS_TOKEN

# File path to alex.jpg
PATH_TO_ALEX

# File path to laugh.png
PATH_TO_LAUGH

# API key for Open Weather Map (openweathermap.org/api)
WEATHER_API_KEY

# Timezone in Heroku for scheduling jobs. Set to America/New_York for US Eastern time
TZ

# Password for the /settings page. It is the serial number on H-Caliber
BING_SETTINGS_PASSWORD
```

## 🗄 How to view data from the database

1. Log into [heroku.com](https://id.heroku.com/)
    - Email address: ```williamsca20+bingheroku@gmail.com```
    - Password: ```{ Email Buddy at the above email adress if you need the password }```
2. Click "Heroku Postgres" (under "Installed add-ons")
3. Click "Dataclips"
4. Click the Dataclip you want to view (either "Show Settings" or "Show GroupMe Users")
5. Refresh the data by clicking "Show new data." If that button is not showing, the data is up to date.
