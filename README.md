# EthOSWatcher

## Purpose

Watch your EthOS dashboard and receive alerts if your performances are lower than expected.

## Requirements

> requests, subprocess

## Configuration

* `url_to_ethosdashboard`: Set this variable to your own EthOS dashboard URL.
* `min_perf`: In this dictionary, set the minimum hashrate, minimum alive GPU and rigs that you want. Below any of these values, the script will send you an alert.
* `alert_delay`: The minimum delay, in seconds, between two alerts. By default, it is set to 12 hours; this means that if your performances are below you threshold for a long time, you would get 1 alarm each 12 hours.
* `telegram_bot_token`: A *token* for your Telegram bot. You can create a bot by talking in private to [@BotFather](https://t.me/BotFather).
* `accounts`: This dictionary contains, for each of persons you want the bot to notify, a phone number (to use with gammu-sms) and a Telegram UserID (that you can get by sending `/id` in private to [@useridinfobot](https://t.me/useridinfobot).

## Licence

No licence. Use it as you want.