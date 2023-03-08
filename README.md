# Aurora notifier telegram bot

Auroras are amazing, but the optimal weather conditions to see them are not met quite often. I was dissapointed so many times when I saw high [kp](https://www.swpc.noaa.gov/products/planetary-k-index) index prediction, prepared all the photo equipment and then it was cloudy. Likely, there is a [meteoblue](https://www.meteoblue.com/en/weather/outdoorsports/seeing) service for cloud prediction. This repo combines the best from both worlds, offering telegram bot which can automatically run in github pipeline `for free` and notify the forecast for both clouds and kp index.

## Technicalities
> Current setup works for Tartu but can be adjusted simply to work at any location.

### Inside the script
* If you need wish to change location you should to go to [meteoblue](https://www.meteoblue.com/en/weather/outdoorsports/seeing/) astronomy seeing service and search for your location, and then copy that link to the `LINK_METEOBLUE` variable in [main.py](main.py).

* To get the correct logic `TIMEZONE` variable in [main.py](main.py) should be updated with the correct timezone.

* You should also change `kp_threshold` to the level which makes it possible to see aurora in your region. If there is nothing to notify about, notification will not be send.

### Set up telegram notifications

To get automatic notifications every day you will need to add couple of things in github when you [fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this repo:
1) You should put telegram bot token to the github actions secret and call it `BOT_TOKEN`
1) You should get your telegram chat id (with [Chat id bot](https://t.me/GetMyChatID_Bot) for example) and place it to the secret which you should call `CHAT_ID`

### How it works
The service is invoked once per day in github actions defined in this [file](C:\Users\alex\Desktop\projects\aurora_notifier\.github\workflows\test.yaml). It installs all dependencies and parses meteoblue website to get clouds data and uses noaa api to get kp index predictions. After that it formats it as pandas tables, does time matching(since kp predictions are UTC) and table join + checking if kp is higher than threshold. Then, if there are any rows, it sends the notification to a user using telegram api.

### To run locally
> To run locally you would need to define `BOT_TOKEN` and `CHAT_ID` variables in .env file which you should put in the same directory as the main.py script

To install dependencies:
```
pip install -r requirements.txt
```
To run the script:
```
python main.py
```