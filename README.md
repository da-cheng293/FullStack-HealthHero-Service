# HealthHero

Recently, people all around the world are suffering from coronavirus. However, many people failed to understand how severe the situation is, so it is quite important to educate people and help them know how to protect themselves.

Inspired by this, our team decided to build a simple dialogue system, which is able to interact with users, and give them the latest information about what the situation is. Also, considering there are many rumors about coronavirus which panic people, we also decided to build a small game to test user's knowledge about the virus, and give them feedback based on their performance.

So, in order to implement the first system, we choose wit.ai, an online NLP platform to extract entities from the user's query, including location, intent, query type, etc. Then, from these entities, we build queries to get corresponding data from MongoDB Atlas, which stored up-to-date information got from websites using a web crawler. According to the user's query, we extract needed data fields and combine the data to form answers to the user. In the True/False game, we built a mobile fashioned website to let users answer T/F by swiping left or right, and when the game completed, they will get a final score.

We hope our project will inspire more people to be aware of coronavirus, gain knowledge about it, and protect themselves from being affected.

Devpost link: https://devpost.com/software/healthhero
https://github.com/da-cheng293/HealthHero/tree/master/HealthHero/structure.PNG
https://github.com/da-cheng293/HealthHero/tree/master/HealthHero/webpage.PNG

