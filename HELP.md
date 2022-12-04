# 🦏 Bing Bot Help Guide

- [🦏 Bing Bot Help Guide](#-bing-bot-help-guide)
  - [⚙️ How to turn a command or unsolicited message on or off](#️-how-to-turn-a-command-or-unsolicited-message-on-or-off)
  - [🙋 How to change the name Bing calls someone](#-how-to-change-the-name-bing-calls-someone)
  - [😨 Bing's not working! What do I do??](#-bings-not-working-what-do-i-do)
  - [📸 How to restore Bing's profile picture if it disappears](#-how-to-restore-bings-profile-picture-if-it-disappears)
  - [😳 I got a "Cronjob failed" email. What should I do?](#-i-got-a-cronjob-failed-email-what-should-i-do)
  - [📲 How to move Bing to a new chat](#-how-to-move-bing-to-a-new-chat)
- [💻 Tech Stuff for Nerds](#-tech-stuff-for-nerds)
  - [🌐 What online accounts are there?](#-what-online-accounts-are-there)
  - [🌅 Every 3 Months, Bing Needs Rejuvenated](#-every-3-months-bing-needs-rejuvenated)
  - [🪵 How to check for errors](#-how-to-check-for-errors)
  - [👾 How to update Bing's code](#-how-to-update-bings-code)
    - [Set up your development environment](#set-up-your-development-environment)
    - [Make Code Changes](#make-code-changes)
    - [Commit Code Changes](#commit-code-changes)
    - [Update the code on the server](#update-the-code-on-the-server)
  - [🔐 How to create a new Google credentials.json](#-how-to-create-a-new-google-credentialsjson)
  - [🏔 Environment Variables](#-environment-variables)
  - [🐍 WSGI Configuration](#-wsgi-configuration)

## ⚙️ How to turn a command or unsolicited message on or off

1. Go to the settings Google Sheet at [go.osu.edu/bingsettings](https://go.osu.edu/bingsettings)
2. Check or uncheck the box next to any setting

## 🙋 How to change the name Bing calls someone

1. Go to the settings Google Sheet at [go.osu.edu/bingsettings](https://go.osu.edu/bingsettings)
2. Go to the **Nicknames** tab
3. Edit the text in the **Nickname** column

## 😨 Bing's not working! What do I do??

1. Check if Bing is running by asking "**Bing, are you alive?**" or by visiting [this link](https://bingbot.pythonanywhere.com)
    - If Bing is not running, [log into](#-what-online-accounts-are-there) **pythonanywhere.com**, and [extend Bing's life for 3 more months](#-every-3-months-bing-needs-rejuvenated), [reload the web app](#update-the-code-on-the-server), and try again.
2. Make sure the specific feature is turned on [in the settings Google Sheet](https://go.osu.edu/bingsettings)
3. [Make sure Bing is in the right GroupMe chat and has the correct GroupMe Bot ID and Access Token](#-how-to-move-bing-to-a-new-chat)
4. [Check for errors in pythonanywhere](#-how-to-check-for-errors)
    - If you are getting an error like this, that means an [environment variable](#-environment-variables) is missing. Add it to [the **.env** file](https://www.pythonanywhere.com/user/bingbot/files/home/bingbot/bing-bot/.env?edit), then [reload the web app](#update-the-code-on-the-server)
      ```
        File "/usr/local/lib/python3.9/os.py", line 679, in __getitem__
          raise KeyError(key) from None
      ***************************************************
      If you're seeing an import error and don't know why,
      we have a dedicated help page to help you debug: 
      https://help.pythonanywhere.com/pages/DebuggingImportError/
      ***************************************************
      ```
    - If there is a bug in the code, consider asking a CSE friend to help [update the code](#-how-to-update-bings-code)
5. If Bing said "**my crayon broke :(**" when trying to draw something:
    - Try again. Try again in a day or 2. If it still doesn't work, it likely means the API we use to generate images is no longer running, and we are out of luck :(
6. If Bing said "**i'm not feeling inspired right now. maybe later**" when trying to make a meme:
    - Try again. Try again in a day or 2. If it still doesn't work, it likely means an API or service we use to generate memes is no longer running, and we are out of luck :(
7. This one feature (or multiple features) never works anymore. What gives?
    - Bing relies upon many external services and APIs that are not under our control (especially pythonanywhere.com, the Google Sheets API, cron-job.org, and GroupMe). Any of these companies could choose to stop running their services at any time, and that part of Bing just wouldn't work anymore. All things must come to an end eventually :( It was fun while it lasted.
    - [Relevant Tom Scott video](https://youtu.be/BxV14h0kFs0)

## 📸 How to restore Bing's profile picture if it disappears

For some reason, if you go to the **Edit** page of a GroupMe bot without changing the **Avatar URL**, the profile picture will stop working. To fix it, go back to the **Edit** page for Bing in [dev.groupme.com](https://dev.groupme.com/bots), and set the profile picture URL to `https://i.imgur.com/Kr6ti95.jpg`

## 😳 I got a "Cronjob failed" email. What should I do?

We use **cron-job.org** to run code at a scheduled time, like Bing's unsolicited messages. If you get one of these emails, **you don't have to do anything**. It's just letting you know that the code failed to run.

If you want to investigate why it failed and try to fix it, [check the error logs](#-how-to-check-for-errors).

If there is an error like this when running the cron job **MEME**, just wait a day or 2. it likely means the site **api.allorigins.win** is down.
```
PIL.UnidentifiedImageError: cannot identify image file <_io.BytesIO object at 0x7fbd97939d10>
```

If there is an error like this when running the cron job **ELON**, same thing, just wait a day or 2. If it still doesn't work after a few days, it likely means Forbes changed the format of their website, and this message will no longer work going forward :(
```
AttributeError: 'NoneType' object has no attribute 'text'
```

## 📲 How to move Bing to a new chat

To move Bing to a new chat, you need register a GroupMe bot for that chat:

1. Log into [**dev.groupme.com**](https://dev.groupme.com) using your GroupMe account
2. Click [**Bots**](https://dev.groupme.com/bots)
3. Click [**Create Bot**](https://dev.groupme.com/bots/new)
4. Fill in the details:
   - Choose the group this bot will live in: **(Current H-Row Chat)**
   - Name: `Bing`
   - Callback URL: `https://bingbot.pythonanywhere.com`
   - Avatar URL: `https://i.imgur.com/Kr6ti95.jpg`
5. Click **Submit**
6. Copy the **Bot ID**, and paste it into the **GroupMe Bot ID** field in the **Tech Config** tab of the [settings Google Sheet](https://go.osu.edu/bingsettings)
7. Click **Access Token** at the top right corner of the screen of [**dev.groupme.com**](https://dev.groupme.com), copy it, and paste it into the **GroupMe Access Token** field in the **Tech Config** tab of the [settings Google Sheet](https://go.osu.edu/bingsettings)
8. Have the previous "owner" of Bing log into [**dev.groupme.com**](https://dev.groupme.com) with their GroupMe account and delete the bot from the old chat
9. __Important:__ [Log into](#-what-online-accounts-are-there) Bing's Gmail account and [change the forwarding address](https://support.google.com/mail/answer/10957?hl=en) to your email so you will get alerts once every 3 months [when Bing's code is about to expire](#-every-3-months-bing-needs-rejuvenated), so you can prevent that from happening.

# 💻 Tech Stuff for Nerds

## 🌐 What online accounts are there?

All accounts and services are free. [Just make sure Bing doesn't die every 3 months](#-every-3-months-bing-needs-rejuvenated).

- [Google Drive / Gmail / Google Cloud Platoform](https://cloud.google.com/)
  - Settings Google Sheet
  - Recieves emails
  - Google Sheets API & credentials from GCP
- [pythonanywhere](https://www.pythonanywhere.com/user/bingbot/webapps/#tab_id_bingbot_pythonanywhere_com)
  - Hosts the Python code that runs the web server
- [GitHub](https://github.com/bing-bot)
  - To push code changes, use the **bing-bot** GitHub account. Colin (**c-o-l-i-n**) is the repo owner.
- [cron-job.org](https://cron-job.org)
  - Triggers unsolicited messages throughout the day
- [OpenWeather](https://home.openweathermap.org/api_keys)
  - Weather data API
- [Imgflip](https://imgflip.com/api)
  - Meme generator API
- [Clarifai](https://portal.clarifai.com/settings/authentication)
  - Copmuter vision API
- [Stable Horde](https://stablehorde.net/register)
  - AI image generation API ("Log in with Google," display name: **bing bot**)
- [Open Emoji](https://emoji-api.com/) and [College Football Data](https://collegefootballdata.com/key)
  - Emoji search API and CFB data API
  - There are no password-protected accounts for these sites, but you get a free API key by submitting an email address

The username/email for all accounts is **hrow.bing.bot<span>@</span>gmail.com**

The password for all accounts is **(all lowercase) the nickname of the band, then the serial number on H-Caliber, then an exclamation point**.

## 🌅 Every 3 Months, Bing Needs Rejuvenated

In free pythonanywhere accounts, [web apps are disabled after 3 months unless you click the **Run until 3 months from today** button](https://blog.pythonanywhere.com/129/).

pythonanywhere will email hrow.bing.bot@gmail.com the link to keep things running 1 week before she is brutally murdered.

![Don't let Bing die](assets/extend.jpg)

## 🪵 How to check for errors

[pythonanywhere](https://www.pythonanywhere.com/user/bingbot/files/var/log) provides a few different log files. Scroll all the way to the bottom for the latest log entries:

- [Error log](https://www.pythonanywhere.com/user/bingbot/files/var/log/bingbot.pythonanywhere.com.error.log) (the useful one)
- [Access log](https://www.pythonanywhere.com/user/bingbot/files/var/log/bingbot.pythonanywhere.com.access.log)
- [Server log](https://www.pythonanywhere.com/user/bingbot/files/var/log/bingbot.pythonanywhere.com.server.log)

## 👾 How to update Bing's code

You can technically just change the [code files directly on the server](https://www.pythonanywhere.com/user/bingbot/files/home/bingbot/bing-bot/src), but the "right way" is making the changes in git:

### Set up your development environment
1. (In a terminal on your compter) `git clone https://github.com/c-o-l-i-n/bing-bot.git`
2. `cd bing-bot`
3. [Create a Python virtual environment and install dependencies](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments)
   - `python3 -m venv bing-env`
   - `source bing-env/bin/activate`
   - `pip install -r requirements.txt`
4. `touch credentials.json` to create the Google credientials file, then copy the contents from [the server](https://www.pythonanywhere.com/user/bingbot/files/home/bingbot/bing-bot/credentials.json?edit). 
5. `touch .env` to create the `.env` file, then add all [environment variables](#-environment-variables). Copy the contents from [the server](https://www.pythonanywhere.com/user/bingbot/files/home/bingbot/bing-bot/.env?edit), but these ones need to be different:
   - `PROXY_URL=''`
   - `GOOGLE_APPLICATION_CREDENTIALS='/path/on/your/computer/to/credentials.json'`

### Make Code Changes

6. Make code changes
7. Test the code by running `python src/app.py`
8. If you `pip install` any additional packages, make sure to `pip freeze > requirements.txt` to save them

### Commit Code Changes

8. `git commit` any changes to the `main` branch
9. `git push` the changes
    - When prompted to log into GitHub, use [Bing's GitHub account](#-what-online-accounts-are-there).

### Update the code on the server

10. [Log into pythonanywhere, and open a console.](https://www.pythonanywhere.com/user/bingbot/consoles/)
11. Run the commands:
    - `cd /home/bingbot/bing-bot`
    - `git pull`
    - If you get a an error while pulling, run `git reset --hard origin/main` to force pull
    - If you had to `pip install` additional packages in your changes, run:
      - `workon bing-env`
      - `pip install -r requirements.txt`
12. Go to the [Web](https://www.pythonanywhere.com/user/bingbot/webapps/#tab_id_bingbot_pythonanywhere_com) page
13. Click **Reload bingbot.pythonanywhere.com**

![Reload button](assets/reload.jpg)

If you see this message at the bottom of the [server log](https://www.pythonanywhere.com/user/bingbot/files/var/log/bingbot.pythonanywhere.com.server.log), that means Bing was started successfully.

```
spawned 2 offload threads for uWSGI worker 1
```

If you have no clue what any of that means, ask a CSE major to do it.

## 🔐 How to create a new Google credentials.json

You should be able to use the credentials.json currently on the server forever, but if you accidentally delete this file, you can create a new one from inside Google Cloud Platform.

1. [Click here](https://console.cloud.google.com/iam-admin/serviceaccounts/details/110374235479725686399/keys?authuser=1&project=hrow-bing-bot&supportedpurview=project) to go to the **Keys** page. If the link doesn't work:
   - [Log into](#-what-online-accounts-are-there) the [Google Cloud console](https://console.cloud.google.com), go to **Menu ☰ > IAM & Admin > [Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)**
   - Choose the **Bing Bot** project, if prompted
   - Click **bing-bot-service-account<span>@</span>hrow-bing-bot.iam.gserviceaccount.com**
   - Click the **KEYS** tab

2. It is impossible to re-download an old key, so we have to make a new one. Click **Keys > Add key > Create new key**
3. Select **JSON**, then click **Create**
4. Your new public/private key pair is generated and downloaded to your machine as a new file. This file is the only copy of this key.
5. Click **Close**
6. Log into pythonanywhere.com, and go to the [**credentials.json**](https://www.pythonanywhere.com/user/bingbot/files/home/bingbot/bing-bot/credentials.json?edit) file. If you get a 404 becuase the file was deleted, [create a new one](https://www.pythonanywhere.com/user/bingbot/files/home/bingbot/bing-bot) located at **/home/bingbot/bing-bot/credentials.json**
7. Open the JSON file you downloaded from GCP, copy the contents, and paste it into the file in pythonanywhere
8. Click **Save**
9. [Reload the web app](#update-the-code-on-the-server)

If the layout of GCP has changed and those steps are no loger valid, check the [official instructions from Google](https://developers.google.com/workspace/guides/create-credentials#create_credentials_for_a_service_account).

## 🏔 Environment Variables

These environment variables are require in pythonanywhere for Bing to work properly. They are set within the [`.env` file in the project root](https://www.pythonanywhere.com/user/bingbot/files/home/bingbot/bing-bot/.env?edit). After updating and saving the `.env` file, [reload the web app](#update-the-code-on-the-server) to apply the changes.

| Key                              | Value                                                                         | Notes                                    |
| -------------------------------- | ----------------------------------------------------------------------------- | ---------------------------------------- |
| `PROXY_URL`                      | `http://proxy.server:3128`                                                    | pythoneverywhere proxy server URL        |
| `GOOGLE_APPLICATION_CREDENTIALS` | `/home/bingbot/bing-bot/credentials.json`                                     | Path to Google credentials file          |
| `SPREADSHEET_ID`                 | _([Settings Google Sheet](http://go.osu.edu/bingsettings) ID from URL)_       | docs.google.com/spreadsheets/d/`ID`/edit |
| `OPENWEATHER_API_KEY`            | _([API key from OpenWeather](https://home.openweathermap.org/api_keys))_      | Weather data API                         |
| `IMGFLIP_API_KEY`                | _(Password to [Imgflip](https://imgflip.com) account)_                        | Meme generator API                       |
| `CRON_JOB_ORG_API_KEY`           | _([API key from cron-job.org](https://console.cron-job.org/settings))_        | API to change unsolicited message times  |
| `CLARIFAI_PERSONAL_ACCESS_TOKEN` | _([PAT from Clarifai](https://portal.clarifai.com/settings/authentication))_  | Computer vision API                      |
| `OPEN_EMOJI_API_KEY`             | _([API key from Open Emoji](https://emoji-api.com/))_                         | Emoji search API                         |
| `COLLEGE_FOOTBALL_API_KEY`       | _([API key from College Football Data](https://collegefootballdata.com/key))_ | College football data                    |
| `STABLE_HORDE_API_KEY`           | _([API key from Stable Horde](https://stablehorde.net/register))_             | AI image generation API                  |

## 🐍 WSGI Configuration

Python web apps run on a [WSGI server](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface). There is a configuration file in pythonanywhere located at [/var/www/bingbot_pythonanywhere_com_wsgi.py](https://www.pythonanywhere.com/user/bingbot/files/var/www/bingbot_pythonanywhere_com_wsgi.py?edit). It loads the environment variables from the `.env` file and imports the Flask app.

If something happens to that file, replace it with this, and then [reload the web app](#update-the-code-on-the-server):

```python
# load environment variables from .env file
import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('/home/bingbot/bing-bot/')
load_dotenv(os.path.join(project_folder, '.env'))

# import Flask app
import sys
path = '/home/bingbot/bing-bot/src'
if path not in sys.path:
    sys.path.append(path)
from app import app as application
```
