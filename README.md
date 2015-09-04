# clickpapa-api-pushbullet-example
ClickPapa API example to fetch unread messages and push them via PushBullet to your device as notifications.

You can obtain your ClickPapa API key via your clickpapa.com profile, and the PushBullet API key from your pushbullet.com account.

Install the requirements with pip:

	pip install -r requirements.txt

Then put the script into cron, like this:

	# */5 * * * * python /path/to/this/script/clickpapa-pushbullet-notification.py > /dev/null

