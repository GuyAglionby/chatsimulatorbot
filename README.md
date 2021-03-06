# Chat Simulator Bot
Use Markov chains to generate messages based on Telegram group's chat history. Inspired by [/r/SubredditSimulator](http://www.reddit.com/r/subreddisimulator), which includes a much better description [here](https://www.reddit.com/r/SubredditSimulator/comments/3g9ioz/what_is_rsubredditsimulator/).

## Dependencies
Utilises [Markovify](https://github.com/jsvine/markovify) for Markov chains, and a few other libraries for various things. These are listed in `requirements.txt`, and can be installed using `pip install -r requirements.txt`.

## Usage
You can run your own version of this bot by following the instructions [here](https://core.telegram.org/bots#botfather) to get an API key, which should be put in the config.yml file. This bot is available for your usage at [here](http://www.telegram.me/ChatSimulatorBot).

## Todo
- Unicode support - accented characters do not work.
- Use [NLTK](http://www.nltk.org/) to produce more sensible sentences (possibly optionally)
