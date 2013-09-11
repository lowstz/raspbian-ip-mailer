server-ip-mailer
==================

This is a fork from [shenjia/raspbian-ip-mailer](https://github.com/shenjia/raspbian-ip-mailer)

This version can: 

1. Try several times to connect smtp server, because the Wifi may be not ready yet.
2. Print progress infomation while connect, login and sending mail.
3. Install as a service automatically.

Deploy
---------------------
1. Download [deploy.sh](https://github.com/lowstz/server-mailer/raw/master/deploy.sh) and run it.

	```
	wget https://github.com/lowstz/server-ip-mailer/raw/master/deploy.sh
	sudo chmod +x deploy.sh
	./deploy.sh

	```
2. Update your mail account in `/usr/local/bin/server-ip-mailer.py`:

	```
    # Mail account settings
    mail_setting = {
        'mail_user': 'username@gmail.com',
        'mail_password': 'password'
        }

    send_to_list = [
        'username@gmail.com',
        'username2@gmail.com'
        ]
    ```
    
    If you don't use gmail, update those also:
    
    ```
    # smtp server settings
    smtp_setting = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587
        }
	```

3. Reboot and enjoy it!

