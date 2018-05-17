# Instagram Engagement Assistant
It does the research so you do the easywork

## What it is
This project serves to allow Instagrammers wanting to grow their page better methods of researching potential followers and allowing a simple way to interact with them in masses.

The project will be composed of three main entities
1. Scraper (scraper.py)
The scraper is responsible for manually going through the instagram data and storing it in the database. As it stands it will take an input of related users to scan and it will go through their pictures and pull this information as well as the picture comments. From this we can find who comments the most and target those users later on. Currently written in Python
2. Middle Tier web service / API
An API needs to be made available to allow for the dynamic client to exist. This will allow for easy querying to fetch the list of users that will likely respond well to engagement. Will be utilized by the web client. Potentially will be written in Python with the help of Flask
3. Front End / Web client
A web client is what ties this all together. The web client will serve as an interface to easily iterate through the users that have been targetted to allow for a simplified interaction process


## What it isn't
This is not a bot that will get you more likes, it will not auto like and auto follow other accounts or provide unethical account manipulation. It simply serves as a data aggregator and allows you to do less work in that area

#### More information to come eventually including running, setup, etc