# r6econ
Consistantly monitors the R6 Marketplace based on a tracking list. 

The Discord bot tracks sales over time, also presenting extra item data not otherwise shown on the R6 Marketplace.

Much of the data this gathers can be used to manipulate the market to your advantage.



## Setup (Recommended)

### Prequisites
- Experience with Git
- Experience setting up a Discord Bot
### Program Requirements
- Python and Pip
- Git CLI
- [A discord bot and its token](https://www.writebots.com/discord-bot-token/)
  
First, clone and navigate to the repo:
```
git clone https://github.com/VillamBarna/r6econ.git
cd r6econ
```

Next, add a 'data.json' file to `/assets`, and leave the contents as:
```
{
}
```

Next, add an 'ids.json' file to `/assets`, and place any items and their item IDs in the contents. There is an starting example in the assets folder of this repo.

Make sure you have enabled Privledge Message Intent in the bot settings on the Discord Developer portal.

Finally, depending on your operating system and choice of terminal:

### Windows Command Prompt
```bat
set AUTH_EMAIL=foo@example.com
set AUTH_PW=mysecretpassword
set TOKEN=mydiscordbotstoken
pip install -r requirements.txt
python3.exe server.py
```

### PowerShell
```ps1
$env:AUTH_EMAIL="foo@example.com"
$env:AUTH_PW="mysecretpassword"
$env:TOKEN="mydiscordbotstoken"
pip install -r requirements.txt
python3.exe server.py
```

### Bash
```sh
export AUTH_EMAIL=foo@example.com
export AUTH_PW=mysecretpassword
export TOKEN=mydiscordbotstoken
pip install -r requirements.txt
python3 server.py
```

Congratulations, you're done! Invite the bot to your personal server and check that it works with `econ help`. 

## Commands:
- ### econ list
  Lists all available names you can search for. It's recommended that you use item IDs instead, however.
  

  Lists all tracked skins.
- ### econ id \<item id>
  Functionally the same as the above, but allows the direct lookup by the item's static ID.

  
- ### econ graph <# of entries | all> <unit of time (days | hours | minutes )> <item id>
  Displays a graph of the current state of an item.

  This is the most useful command, and can be used to determine when to buy or sell. A basic example of how to make informed decisions is in the linked article in the description of this repo.


- ### econ profit \<$ purchased for> \<item id>
  Calculates how much you need to sell for to gain profit, and estimates your profit if sold right now (according to the RAP 10x).

- ### econ margin \<item id>
  Displays a graph of the current state of an item, groups the the orders into to two groups and calculates the average of these groups giving a recommended selling/buying price.

- ### econ listprofit \<$ max price>
  Lists the most profitable investments under the given max price.

- ### econ help
 Default message that is shown when an invalid command is used or the user runs `econ help`.
  
 

## Credits
Much of the authentication code was sourced from https://github.com/CNDRD/siegeapi. 

Thank you for the well-documented code! <3
