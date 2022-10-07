# 🦏 Bing Bot

<p align="center">
   <img alt="Bing Bot" width="256" height="256" src="assets/bing.jpg" />
</p>

## About

Bing Bot is a GroupMe chatbot for H-Row's mascot, Bing. It responds to different "commands" and sends unprompted messages throughout the day.

Bing Bot is a REST API built with the Python Flask framework, hosted on [pythonanywhere](https://www.pythonanywhere.com).

## System Architecture

There are many components/services that connect to create the Bing Bot we know and love:

- GroupMe bot registered on the owner's GroupMe account
- pythonanywhere Flask web app
- pythonanywhere scheduled task
- "Bing Settings" Google Sheet where settings and nicknames can be changed
- The Google Sheets API enabled from Google Cloud Platform
- OpenWeather API for getting weather data
- Imgflip API for generating memes

## [Help Guide](HELP.md)
