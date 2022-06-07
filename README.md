# Roblox accepted trade checker with discord webhook because I wanted to create this because of boredom. 
✨ and it just works ✨

![ur nan](https://i.imgur.com/GtvSrhF.png)

## Features
* Waits for inventory to change using inventory api's (so doesn't involve in trade ratelimits)
* When inventory changes tries to get trade from trade api (if ratelimited, try again 5 seconds later)
* Creates a real looking picture as if you got a trade :0
* Checks if projected using Rolimon's
* Gets value of the items from Rolimon's

## How to install
Install the dependencies:
```
# Linux/macOS
python3 -m pip install -r requirements.txt

# Windows
py -3 -m pip install -r requirements.txt
# or whatever Windows uses, literally every user has their own way to do Python for some reason
```

Put your .ROBLOSECURITY cookie in cookie.txt<br>Put your Discord webhook in webhook.txt

Start program:
```
# Linux/macOS
python3 start.py

# Windows
py -3 start.py
# or whatever again
```
quick side note: this hasn't been tested

## License
This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details.