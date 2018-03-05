# Jahus,
# 2018-01-04T23:19Z


import requests
import time
import subprocess


# Variables
url_to_ethosdashboard = "http://xxxxxx.ethosdistro.com/"
url = url_to_ethosdashboard + "?json=yes"
min_perf = {
	"total_hash": 170,
	"alive_gpus": 12,
	"alive_rigs": 2
}
timeout = 60 * 5 # seconds
alert_delay = 60 * 60 * 12 # seconds
telegram_bot_token = "123456789:ABCdefghjklmnpqrstuvwxyz123456_789a"
telegram_bot_request = "https://api.telegram.org/bot"
accounts = {
	"foudre": {
		"number": "5551234567",
		"telegram": "00000000",
		"alarm_time": 0
	},
	"boris": {
		"number": "5559876543",
		"telegram": "000000000",
		"alarm_time": 0
	}
}


# Request data from the server and call check_rig
def main(server):
	try:
		req = requests.get(server)
		if req.status_code != 200:
			print("Server returned error %s" % req.status_code)
		else:
			req_json = req.json()
			check_rig(req_json)
	except:
		print("Error")


# Check performances and alert if anything's wrong
def check_rig(data):
	message = ""
	for perf in min_perf:
		if data[perf] < min_perf[perf]:
			message += "%s = %s < %s\n" % (perf, data[perf], min_perf[perf])
		else:
			print("%s = %s >= %s" % (perf, data[perf], min_perf[perf]))
	if message != "": alert(message)


# Telegram Bot API function for sending messages
def telegram_bot_send_message(chat_id, text, parse_mode=None, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None):
	req_data = {
		"chat_id": chat_id,
		"text": text
	}
	if parse_mode is not None:
		req_data.update([("parse_mode", parse_mode)])
	if disable_web_page_preview is not None:
		req_data.update([("disable_web_page_preview", disable_web_page_preview)])
	if reply_to_message_id is not None:
		req_data.update([("reply_to_message_id", reply_to_message_id)])
	if reply_markup is not None:
		req_data.update([("reply_markup", reply_markup)])
	req = requests.post(url="%s%s%s" % (telegram_bot_request, telegram_bot_token, "/sendMessage"), data=req_data)
	if req.status_code != 200:
		print("** send_message(): Error %s" % req.status_code)
	else:
		req_json = req.json()
	# print(req_json)
	# TODO: Verify if sent message is equal to received message
	#


# Send alert to users, actually supports gammu-smsd (sends SMS messages) and Telegram
def alert(message):
	global numbers
	_message = "ALERT: " + message.replace("\n", " | ")
	print(_message)
	for account in accounts:
		if accounts[account]["alarm_time"] + alert_delay < time.time():
			_command = "gammu-smsd-inject TEXT %s -text \"%s\"" % (accounts[account]["number"], _message)
			print(_command)
			port = subprocess.Popen(
				_command,
				stdout=subprocess.PIPE,
				shell=True
			)
			(output, err) = port.communicate()
			print("output = %s\nerr = %s" % (output, err))
			try:
				telegram_bot_send_message(accounts[account]["telegram"], _message)
			except:
				print("Error: Can't send Telegram message. Contact @Jahus on Telegram.")
			accounts[account]["alarm_time"] = time.time()
		else:
			print("ALERT already sent. Waiting %s seconds." % alert_delay)


# Main script
if __name__ == "__main__":
	while True:
		main(url)
		time.sleep(timeout)
