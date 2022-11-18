"""A Markov chain generator that can tweet random messages."""

from email import message
import sys
from random import choice
import os
import discord


def open_and_read_file(filenames):
    """Take list of files. Open them, read them, and return one long string."""

    body = ''
    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string, n):
    """Take input text as string; return dictionary of Markov chains."""

    chains = {}

    words = text_string.replace('\n', ' ').split(' ')

    for i in range(len(words) - n):
        length = 0
        curr_list = []

        while length < n:
            curr_list.append(words[i + length])
            length += 1

        pair = tuple(curr_list)
        chains[pair] = []

    for i in range(len(words) - n):
        length = 0
        temp_list = []

        while length < n:
            temp_list.append(words[i + length])
            length += 1

        temp = tuple(temp_list)
        if temp in chains:
            chains[temp].append(words[i+n])

    return chains


def make_text(chains):
    """Return text from chains."""
    values = list(chains.values())

    lines = [choice(values) for _ in range(20)]
    words = []

    for item in lines:
        new_word = choice(item)
        words.append(new_word)

    return ' '.join(words)

def get_quote(filename):
    file = open(filename)

    quotes = [line.strip() for line in file]

    return choice(quotes)


# def make_chains(text_string):
#     """Take input text as string; return dictionary of Markov chains."""

#     chains = {}

#     words = text_string.split()
#     for i in range(len(words) - 2):
#         key = (words[i], words[i + 1])
#         value = words[i + 2]

#         if key not in chains:
#             chains[key] = []

#         chains[key].append(value)

#     return chains


# def make_text(chains):
    # """Take dictionary of Markov chains; return random text."""

    # keys = list(chains.keys())
    # key = choice(keys)

    # words = [key[0], key[1]]
    # while key in chains:
    #     # Keep looping until we have a key that isn't in the chains
    #     # (which would mean it was the end of our original text).

    #     # Note that for long texts (like a full book), this might mean
    #     # it would run for a very long time.

    #     word = choice(chains[key])
    #     words.append(word)
    #     key = (key[1], word)

    #     words = words[:20]

    # return ' '.join(words)


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text, 4)


# Create Discord Bot
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} is logged in and ready to chat!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'wisdom' in message.content.lower():
        await message.channel.send(get_quote('quotes.txt'))

client.run(os.environ['DISCORD_TOKEN'])
