# 📖 Bing Bot User Guide

<img src="https://i.groupme.com/422x422.jpeg.87626f4f99aa48e19536cb96a7314851.avatar" align="right" />

Contents

- [About Bing Bot](#-about-bing-bot)
- [How to move Bing to a different chat](https://github.com/c-o-l-i-n/bing-bot/edit/main/README.md#-how-to-move-bing-to-a-different-chat)
- [How to change environment variables in Heroku](#-how-to-change-environment-variables-in-heroku)

## 🦏 About Bing Bot

Bing Bot is a GroupMe chat bot for H-Row's mascot, Bing. It responds to different "commands" and sends unprompted messages throughout the day.

Bing Bot is a REST API built using the Python Flask framework, hosted on Heroku.

There are 3 components that make Bing run:
- This code repository
- The Heroku app (h-row-bing-bot)
- A GroupMe bot on the owner's GroupMe account

When new code is pushed to the "main" branch of this repository, the Heroku app is updated and re-deployed automatically. (Configured in Heroku settings)

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
