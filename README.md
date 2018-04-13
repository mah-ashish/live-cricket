# live-cricket
Live cricket update notifier for windows-desktop, android and ios

## Installation

#### Clone the repo

    git clone https://github.com/mah-ashish/live-cricket.git

#### Install requirements using pip

    pip install -r requirements.txt

#### For enabling notifications in android or ios

* [Set up a new account](https://ifttt.com/join)
* Install IFTTT mobile app and log in
* [Create a new applet](https://ifttt.com/create)
* Click on the big **this** button
* Search for the “webhooks” service and select the **Receive a web request** trigger
* Name the event **cricket_info**
* Select the big **that** button
* Search for the **notifications** service and select the **Send a notification from the IFTTT app**
* Change the title as required
* Change the message to **{{value1}}** and click on **finish**
* Go to [Documentation](https://ifttt.com/maker_webhooks) page to get your key and paste in **live_cricket.py**
* Run **python live_cricket.py**

#### For Desktop Notifications

* Run **python live_cricket.py --desktop true**
  
#### Notifications for all ongoing tournaments

* The script is written for notifying **IPL 2018** updates. Modify the script for sending notifications for all ongoing tournaments
