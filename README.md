# 🦏 Bing Bot

<img src="https://i.groupme.com/422x422.jpeg.87626f4f99aa48e19536cb96a7314851.avatar" align="right" />

Contents

- [About Bing Bot](#-about-bing-bot)
- [System Architecture](#-system-architecture)
- [How to change Bing's settings](#%EF%B8%8F-how-to-change-bings-settings)
- [How to move Bing to a different chat](#-how-to-move-bing-to-a-different-chat)
- [How to change environment variables in Heroku](#-how-to-change-environment-variables-in-heroku)
- [How to view data from the database](#-how-to-view-data-from-the-database)

## 🤖 About Bing Bot

Bing Bot is a GroupMe chat bot for H-Row's mascot, Bing. It responds to
different "commands" and sends unprompted messages throughout the day.

Bing Bot is a REST API built with the Python Flask framework and PostgreSQL,
hosted on Heroku.

## 🏰 System Architecture

There are 4 components that make Bing run:

- This code repository
- A GroupMe bot on the owner's GroupMe account
- A Heroku app (h-row-bing-bot)
- A PostgreSQL database (Heroku Postgres add-on)

There is arguably a 5th compoonent: [Kaffeine](http://kaffeine.herokuapp.com)
pings the Heroku server every 30 minutes to keep the bot from idling during the
day. Kaffeine observes a "bedtime" between 6am-12pm GMT (1am-7am EST or 2am-8am
EDT) when it does not ping the server
[to keep the Heroko app in the free tier](https://devcenter.heroku.com/articles/free-dyno-hours#quota).

When new code is pushed to the "main" branch of this repository, the Heroku app
is updated and re-deployed automatically. (Configured in Heroku settings)

## ⚙️ How to change Bing's settings

1. Navigate to [go.osu.edu/bingsettings](https://go.osu.edu/bingsettings) (or
   https://h-row-bing-bot.herokuapp.com/settings)
2. Type in the password, and click "Submit"
3. Update the features you want to turn on or off
4. Click "Save Settings"

## 📲 How to move Bing to a different chat

To move Bing to a different chat, you must create a new GroupMe bot:

1. Log into [dev.groupme.com](https://dev.groupme.com)
2. Navigate to the [Bots page](https://dev.groupme.com/bots)
3. Click ["Create Bot"](https://dev.groupme.com/bots/new)
4. Fill in the details:
   - Choose the group this bot will live in: `{ Current H-Row Chat }`
   - Name: `Bing`
   - Callback URL: `https://h-row-bing-bot.herokuapp.com/bing`
   - Avatar URL:
     `https://i.groupme.com/422x422.jpeg.87626f4f99aa48e19536cb96a7314851`
5. Click "Submit"
6. Copy the Bot ID, and paste it into the `GROUPME_BOT_ID` environment variable
   in Heroku ([details below](#-how-to-change-environment-variables-in-heroku))
7. If this bot belongs to a different GroupMe user than before: Click "Access
   Token" at the top right corner of the screen, copy it, and paste it into the
   `GROUPME_ACCESS_TOKEN` environment variable in Heroku
   ([details below](#-how-to-change-environment-variables-in-heroku))

## 🌐 How to change environment variables in Heroku

1. Log into [heroku.com](https://id.heroku.com/)
   - Email address: `williamsca20+bingheroku@gmail.com`
   - Password:
     `{ Email Buddy at the above email adress if you need the password }`
2. Navigate to: h-row-bing-bot > Settings
3. Click "Reveal Config Vars"
4. Click the pencil icon next to the environment variable you want to edit
5. Make the change in the "Value" textbox
6. Click "Save changes"

Verify that all environment variables are set correctly:

| Key                    | Value                                | Notes                                                           |
| ---------------------- | ------------------------------------ | --------------------------------------------------------------- |
| BING_SETTINGS_PASSWORD | _(The serial number on H-Caliber)_   | The password to access the settings panel                       |
| DATABASE_URL           | _(Automatically set by Heroku)_      | **DO NOT EDIT THIS!** It is automatically set by Heroku         |
| GROUPME_ACCESS_TOKEN   | _(Your GroupMe user's access token)_ | Found at [dev.groupme.com](https://dev.groupme.com)             |
| GROUPME_BOT_ID         | _(GroupMe bot ID for your chat)_     | Found at [dev.groupme.com/bots](https://dev.groupme.com/bots)   |
| PATH_TO_ALEX           | /app/src/assets/alex.jpg             | File path to alex.jpg                                           |
| PATH_TO_LAUGH          | /app/src/assets/laugh.png            | File path to laugh.png                                          |
| TZ                     | America/New_York                     | Time zone used for scheduled jobs                               |
| WEATHER_API_KEY        | _(API key for Open Weather Map)_     | If needed, get an API key at openweathermap.org/api             |
| IMGFLIP_API_KEY        | _(API key for ImgFlip)_              | ImgFlip password for account "bing_bot". Used to generate memes |

## 🗄 How to view data from the database

1. Log into [heroku.com](https://id.heroku.com/)
   - Email address: `williamsca20+bingheroku@gmail.com`
   - Password:
     `{ Email Buddy at the above email adress if you need the password }`
2. Click "Heroku Postgres" (under "Installed add-ons")
3. Click "Dataclips"
4. Click the Dataclip you want to view (either "Show Settings" or "Show GroupMe
   Users")
5. Refresh the data by clicking "Show new data." If that button is not showing,
   the data is up to date.
