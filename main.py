

# .env

'''PAWSE COMMANDS:

$start - register (do every time u run)
$setpet - with space + any emoji
$namepet - with space + any name u want :heart_eyes: 
$watertime - with space + any number of minutes for ur timer
$begin - starts timer
$drink - adds +1 water life
$stats - all ur stats
$sleep - goes to sleep, can't do anything
$wake - wakes up
$hi + $pleasesing + $pleasecompliment + $pleasethank - quirky cute fun

can change whenever!'''

import time, asyncio

from discord.ext import tasks, commands

class User:
  
    def __init__(self, id):
        self.id = id
        self.name = "Name"
        self.sleeping = False

    def return_id(self):
        return self.id

    def set_pet(self, pet):
        self.pet = pet

    def get_pet(self):
        return self.pet

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_water_time(self, water_time):
        self.water_time = water_time
        self.water_life = 5
        self.drink = False

    def get_water_time(self):
        return self.water_time

    def set_food_time(self, food_time):
        #self.food_time = 60 * int(food_time)
        self.food_time = food_time

    def get_food_time(self):
        return self.food_time

    async def start_water(self, ctx):
      index = user_names.index(ctx.author.id)
      t = users[index].get_water_time()
      await self.countdown(int(t), False)
      if self.sleeping == False:
        self.set_water_life()
        if self.get_water_life() > 0:
          await ctx.send(self.get_pet() + "Your water time is up. I have " + str(self.get_water_life()) + " lives left") 
        else:
          await ctx.send(self.get_pet() + "Please drink water so I can feel better too :pleading_face:")
        self.drink = False
        await self.start_water(ctx)


    '''async def start_food(self, ctx):
      index = user_names.index(ctx.author.id)
      t = users[index].get_food_time()
      await countdown(int(t))
      await ctx.send('Your food time is up')'''

    def set_water_life(self):
      if self.drink == False and self.water_life > 0:
        self.water_life -= 1
      if self.drink == True:
        if self.water_life < 5:
          self.water_life += 1

    def get_water_life(self):
      return self.water_life

    def drinking(self):
      self.drink = True
      self.set_water_life()
      return self.drink

    def asleep(self, sl):
      self.sleeping = sl

    def check_wokeness(self):
      return self.sleeping

    async def countdown(self, t, sleep):
        self.drink = False
        for x in range(t):
          await asyncio.sleep(60)
          if self.drink == True or self.sleeping == True:
            break

    '''async def countdown_food(t):

      for x in range(t):
        await asyncio.sleep(60)
        if eat == True:
          break'''
  
    def stats(self):
      stats = 'Stats for '
      stats += self.name + " "
      stats += self.pet
      stats += "\nHydration: " + str(self.get_water_life())
      stats += "\n"
      if self.sleeping:
        stats += "Asleep"
      else:
        stats += "Awake"
      return stats

    #vars: water_life, food_life, screen_breaks, food_times, sleep_times, screen_time, water_time


# bot.py
import os
import random
import discord
from dotenv import load_dotenv

TOKEN = os.environ['DISCORD_TOKEN']
GUILD_TOKEN = os.environ['DISCORD_GUILD']

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')
"""@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')"""
user_names = []
users = []


@bot.command(name='start')
async def start(ctx):
    user_match = False
    for user in user_names:
        if user == ctx.author.id:
            await ctx.send("You've already registered!")
            user_match = True
            break
    if user_match == False:
      user_names.append(ctx.author.id)
      users.append(User(ctx.author.id))
      await ctx.send("You've registered!")


@bot.command(name='setpet')
async def setpet(ctx):

    pet = ctx.message.content[8:]
    index = user_names.index(ctx.author.id)
    users[index].set_pet(pet)

    await ctx.send("Your pet is now " + users[index].get_pet() + "!")


@bot.command(name='namepet')
async def namepet(ctx):
    name = ctx.message.content[9:]
    index = user_names.index(ctx.author.id)
    users[index].set_name(name)

    await ctx.send(users[index].get_pet() + "Hi, I'm " +
                   users[index].get_name() + ", your pet!")


@bot.command(name='watertime')
async def watertime(ctx):
    water_time = ctx.message.content[11:]
    index = user_names.index(ctx.author.id)
    users[index].set_water_time(water_time)

    await ctx.send(users[index].get_pet() + "Water time set for " +
                   users[index].get_water_time() +
                   " minutes. Try $begin to start the timer.")


@bot.command(name='foodtime')
async def foodtime(ctx):
    food_time = ctx.message.content[10:]
    index = user_names.index(ctx.author.id)
    users[index].set_food_time(food_time)

    await ctx.send(users[index].get_pet() + "Food time set for" +
                   users[index].get_food_time() +
                   "minutes. Try $begin to start all timers.")


@bot.command(name='begin')
async def begin(ctx):
    index = user_names.index(ctx.author.id)
    if users[index].check_wokeness() == False:
      await ctx.send("Setting timer... go!")
      await asyncio.gather(
        
        #users[index].start_food(ctx),
        users[index].start_water(ctx),
    )
    else:
      await ctx.send(users[index].get_pet() + "Sorry, I'm asleep! :sleeping:")


@bot.command(name='drink')
async def drink(ctx):
    
    index = user_names.index(ctx.author.id)
    if users[index].check_wokeness() == False:
      await ctx.send(users[index].get_pet() + "Thanks for the water! :yum: I now have "+ str(users[index].get_water_life() + 1) + " lives.")
      users[index].drinking()
      await users[index].start_water(ctx)
    else:
      await ctx.send(users[index].get_pet() + "Sorry, I'm asleep! :sleeping:")

@bot.command(name='sleep')
async def sleep(ctx):
  index = user_names.index(ctx.author.id)
  users[index].asleep(True)
  await users[index].countdown(0,True)
  await ctx.send(users[index].get_pet() +" " + users[index].get_name() + " is going to sleep! :sleeping:")

@bot.command(name='wake')
async def wake(ctx):
  index = user_names.index(ctx.author.id)
  users[index].asleep(False)
  await ctx.send(users[index].get_pet() +" " + users[index].get_name() + " is awake!")

@bot.command(name='stats')
async def stats(ctx):
  index = user_names.index(ctx.author.id)
  await ctx.send(users[index].stats())




#bot.run(TOKEN)


'''@bot.command(name='seeallusers')
async def userlist(ctx):
  response = ''
  for user in users:
    response += str(user.return_id())
  await ctx.send(response)'''

@bot.command(name='hi')
async def interaction(ctx):
  index = user_names.index(ctx.author.id)
  if users[index].check_wokeness() == False:
    quirkyQuotes = [
        'the minimal threshold of deliciousness for a ham sandwhich is 4:2, ham:bread slice ratio :bread:',
        'Live, laugh, love, drink hot chili oil',
        'It\'s sunny outside! The perfect weather for a nice walk!',
        'I\'ve always wanted to die clean and pretty but I\'d be too busy on working days',
        'I\'m filled with determination!',
        'Syntax error after syntax error...',
        'One of my friends wrote a program to write programs to write programs to write programs to write programs to write programs',
        'Have you ever seen the stunning waterfalls of Iceland?',
        'My new year\'s resolution: learn a new language. I haven\'t started yet...',
        'An apple a day keeps the doctor away? I\'d expected there to be more...',
        'I\'ll get started on it. Tomorrow.',
        'It\'s really turtles all the way down.',
        'What\'s your favorite ice cream flavor? Mine is rocky road!',
        'Have you been to Disneyland before? Let\'s go together next time!',
        'I think the pool\'s open today... let\'s go swimming!',
        'Bears are so cute!',
        'Can you help me with my AP Bio homework? I\'m having a little bit of trouble with plants...',
        'Wanna try this cob? It\'s fresh from the cornfield!',
        'I\'ve always wanted to visit New York City! I could meet Carnegie Mellon in real life!',
        'Oh... it\'s quinoa.',
        'I just learned about generating functions... I wish I hadn\'t...',
        'You should try participating in a hackathon! They\'re super fun!',
        'I think the cold\'s better than the heat... that\'s why winter\'s my favorite season!',
        'Why do we bake cookies but cook bacon?',
        'Is water wet?',
        'Does a straw have one or two holes?',
        'Do you like the taste of snow?',
        'Wharf roaches! Wharf roaches! Wharf roaches!',
        'One of my other friends wrote a program to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs',
        'My other other friend wrote a program to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs to write programs',
        'Proscuitto is yummy!',
        'Proscuitto! Proscuitto!',
        'Fruit-print clothing brings back a lot of memories for me.',
        'Rolling backpacks... oh...',
        'There\'s just something about the smell of airports that feels magical.',
        'Going to the convenience store at night feels weird.',
        'Have you ever been to a concert before?',
        'It looks like a new shop\'s going to open up in the plaza soon!',
        'Playing with legos is fun!',
        'Agh, I ran out of tape again!',
        'Woof! Woof!',
        'I can\'t see what you\'re pointing to--it looks like my vision got worse.',
        'Be careful! I saw some spiders crawling next to your bed!',
        'Have you ever considered taking care of potted plants?',
        'Yellow\'s such a great color. So warm and calming.',
        'I don\'t know, there\'s just *something* about lakeside villas.',
        'Do you like to read? I used to, but it took me hours and hours to get through a single book!',
        'Oh, the horrors of exclusive licensing...',
        'Got a lot of tabs open in my brain.',
        'Around and around we go...',
        'Too many travel brochures not enough time!',
        'Who thought up the word \"squirrel\"?',
        'You should ask Siri why firetrucks are red.',
    ]

    response = random.choice(quirkyQuotes)
    await ctx.send(response)
  else:
      await ctx.send(users[index].get_pet() + "Sorry, I'm asleep! :sleeping:")

@bot.command(name='pleasesing')
async def happySong(ctx):
  index = user_names.index(ctx.author.id)
  if users[index].check_wokeness() == False:
    happySongsLinks = [
        'https://youtu.be/URShTwQe7nQ',
        'https://youtu.be/27FcfeMAJLk',
        'https://youtu.be/4k6lVKllNYw',
        'https://youtu.be/rB7XFQgJHBI',
        'https://www.youtube.com/watch?v=pco91kroVgQ',
        'https://www.youtube.com/watch?v=bvWRMAU6V-c',
        'https://www.youtube.com/watch?v=Ic7NqP_YGlg',
        'https://youtu.be/yd8jh9QYfEs',
        'https://youtu.be/8jTjNMkWOzM',
        'https://youtu.be/PHn5Q7hCjxw',
        'https://youtu.be/nfWlot6h_JM',
        'https://youtu.be/JGwWNGJdvx8',
        'https://youtu.be/WIKqgE4BwAY',
        'https://youtu.be/dv13gl0a-FA',
        'https://youtu.be/teMdjJ3w9iM',
        'https://youtu.be/lY2yjAdbvdQ',
        'https://youtu.be/HClIlUv_zpA',
        'https://youtu.be/IcpzqZrpLVM',
        'https://youtu.be/qAeybdD5UoQ',
        'https://youtu.be/ShEAiFqkY0E',
        'https://youtu.be/vjRiLKSPbqc',
        'https://youtu.be/GgVcgbtHY9k',
        'https://youtu.be/JQcp3UWQOmM',
        'https://youtu.be/dQw4w9WgXcQ',
        'https://youtu.be/QK8mJJJvaes',
        'https://youtu.be/UTHLKHL_whs',
        'https://youtu.be/k1BneeJTDcU',
        'https://youtu.be/F4AJfasBRxA'
    ]

    response = random.choice(happySongsLinks)
    await ctx.send(response)
  else:
    await ctx.send(users[index].get_pet() + "Sorry, I'm asleep! :sleeping:")

@bot.command(name='pleasecompliment')
async def compliment(ctx):
  index = user_names.index(ctx.author.id)
  if users[index].check_wokeness() == False:
    compliments = [
        'Thanks for always taking great care of me!',
        'You\'re a ray of sunshine!',
        'I like you a lot!',
        'Keep up the great work :D',
        'I\'m not telling you to be cocky... just to think of yourself as you really are.',
        'You always sound cool when you tell me about what you love...',
        'I like when you\'re sincere.',
        'Thank you for everything!',
        'There\'s nobody out there who can do all the things you do, in just the same way. I think you should be proud of that.',
        'Your hair looks great today!',
        'You\'re going to work so hard today!',
        'You\'re going to get so much done today!',
        'Look how far you\'ve come already :)',
        'Tell the people you care about that you care about them! They probably feel the same way.',
        'You always give me the yummiest food!',
        'You\'re a great owner!',
        'You\'ve got a great taste in music!',
        'You\'re looking good today!',
        'You can do this!',
        'You can get through this!',
        'Keep up the good work!',
        'Go get \'em!',
        'You\'ve got this.',
        'You\'re amazing!',
        'You\'re spectacular!',
        'You\'re fantastic!',
        'You\'re marvelous!',
        'There\'s always going to be negative people. Don\'t let them get you down.',
        'You\'re doing good work.',
        'You\'ve got great taste in friends... and pets :)',
        'Nobody can take care of me quite like you!',
        'You chose a great name for me! I wouldn\'t have it any other way!',
        'Good job!'
        
    ]

    response = random.choice(compliments)
    await ctx.send(response)
  else:
    await ctx.send(users[index].get_pet() + "Sorry, I'm asleep! :sleeping:")

@bot.command(name='pleasesmile')
async def happyThing(ctx):
  '''from discord_webhook import DiscordWebhook, DiscordEmbed

webhook = DiscordWebhook(url='https://discord.com/api/webhooks/985328529208119346/4HiTeIYJ0_3HJDTfmyHhX0pzV0_D_485P9TJDuRQIyqMCM70AVOeHoNGdLuF7KKSx1kq')

with open("uwu.jpg", "rb") as f:
    webhook.add_file(file=f.read(), filename='ve.jpg')

# create embed object for webhook
embed = DiscordEmbed(title='Your mom weight status', description='a lot :fearful:', color='ffc0cb')

# set image
embed.set_image(url='attachment://ve.jpg')

# set thumbnail
#embed.set_thumbnail(url='your thumbnail url')

# set footer
embed.set_footer(text='hope you enjoy!')

# set timestamp (default is now)
embed.set_timestamp()

# add fields to embed
embed.add_embed_field(name='Exact weight', value='Too much to quantify')
embed.add_embed_field(name='Amount of health problems', value='one MILLION!!!')


response = webhook.execute()'''
  index = user_names.index(ctx.author.id)
  if users[index].check_wokeness() == False:
    from discord_webhook import DiscordWebhook, DiscordEmbed

    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/985328529208119346/4HiTeIYJ0_3HJDTfmyHhX0pzV0_D_485P9TJDuRQIyqMCM70AVOeHoNGdLuF7KKSx1kq')
    with open("cute1.jpg", "rb") as f:
     webhook.add_file(file=f.read(),       filename='uwu1.jpg')
    
    with open("cute2.jpg", "rb") as f:
      webhook.add_file(file=f.read(), filename='uwu2.jpg')

    with open("smile1.jpg", "rb") as f:
      webhook.add_file(file=f.read(), filename='uwu5.jpg')
    with open("smile2.jpg", "rb") as f:
      webhook.add_file(file=f.read(), filename='uwu6.jpg')
    embed = DiscordEmbed(title='Smile! :blush:', color='ffc0cb')

    happyPics = [
        'attachment://uwu1.jpg',
        'attachment://uwu2.jpg',
        'attachment://uwu5.jpg',
        'attachment://uwu6.jpg',

    ]
    
    embed.set_image(url=random.choice(happyPics))
    embed.set_footer(text='hope you enjoy!')
    embed.set_timestamp()
    happyFaces = [
        '(•ᴥ•) /',
        'ง(¬‿¬ )ง ',
        '(｡´•ᴗ•̀｡) ',
        '⋐(ల◕ᴗ◕ల)⋑',
        '⁽⁽(*꒪ัᴗ꒪ั*)⁾⁾',
        '(◕ω◕)',
        '୧(＾ ᴥ ＾)୨',
        '(&gt; ^ᴥ^ )&gt;'
    ]
    embed.add_embed_field(name='~', value=random.choice(happyFaces))
    embed.add_embed_field(name='~', value=random.choice(happyFaces))
    response = webhook.execute()
    await ctx.send(response)
  else:
   await ctx.send(users[index].get_pet() + "Sorry, I'm asleep! :sleeping:")

@bot.command(name='pleasethank')
async def thank(ctx):
  index = user_names.index(ctx.author.id)
  if users[index].check_wokeness() == False:
    thankfulThings = [
        'I\'m thankful for my friends!',
        'I\'m thankful for my family!',
        'I\'m thankful for modern medicine!',
        'I\'m thankful for you!',
        'I\'m thankful for clean water!',
        'I\'m thankful for holidays!',
        'I\'m thankful for weekends!',
        'I\'m thankful for my TI-84 plus CE graphing calculator!',
        'I\'m thankful for food!',
        'I\'m thankful for the existence of mapo tofu!',
        'I\'m thankful for all the different animals on our Earth!',
        'I\'m thankful for lakes and oceans!',
        'I\'m thankful for the beautiful colors of fall!',
        'I\'m thankful for modern technology!',
        'I\'m thankful for the clouds in the sky!',
        'I\'m thankful for science!',
        'I\'m thankful for all the innovations that came before me!',
        'I\'m thankful for all the people who love me for who I am!',
        'I\'m thankful for kind strangers!',
        'I\'m thankful for random acts of kindness!',
        'I\'m thankful for breathable air!',
        'I\'m thankful for the home I\'m in right now!',
        'I\'m thankful for the team that developed me!',
        'I\'m thankful for computers!',
        'I\'m thankful for shelter!',
        'I\'m thankful for the education I\'ve gotten!',
        'I\'m thankful for all the scientists who have came before me!',
        'I\'m thankful for all the activists and changemakers who have came before me!',
        'I\'m thankful for great music!',
        'I\'m thankful for the Python programming language!',
        'I\'m thankful for replit.com!',
        'I\'m thankful for last minute reminders!',
        'I\'m thankful for the great owner I have!',
        'I\'m thankful for photosynthesis!',
        'I\'m thankful that I passed my AP Physics exam!',
        'I\'m thankful for my bed!',
        'I\'m thankful for blankets!',
        'I\'m thankful that you\'re taking care of me!'
    ]

    response = random.choice(thankfulThings)
    await ctx.send(response)
  else:
   await ctx.send(users[index].get_pet() + "Sorry, I'm asleep! :sleeping:")
  
'''to connect to a server

GUILD = os.environ['DISCORD_GUILD']

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')'''



'''from discord_webhook import DiscordWebhook, DiscordEmbed

webhook = DiscordWebhook(url='https://discord.com/api/webhooks/985328529208119346/4HiTeIYJ0_3HJDTfmyHhX0pzV0_D_485P9TJDuRQIyqMCM70AVOeHoNGdLuF7KKSx1kq')

with open("uwu.jpg", "rb") as f:
    webhook.add_file(file=f.read(), filename='ve.jpg')

# create embed object for webhook
embed = DiscordEmbed(title='Your mom weight status', description='a lot :fearful:', color='ffc0cb')

# set author
embed.set_author(name='fiona lu', proxy_icon_url='https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Flostinanime.com%2Fwp-content%2Fuploads%2F2018%2F01%2FViolet-Evergarden-01-01.jpg&f=1&nofb=1')

# set image
embed.set_image(url='attachment://ve.jpg')

# set thumbnail
#embed.set_thumbnail(url='your thumbnail url')

# set footer
embed.set_footer(text='we tried to weigh her but the scale broke')

# set timestamp (default is now)
embed.set_timestamp()

# add fields to embed
embed.add_embed_field(name='Exact weight', value='Too much to quantify')
embed.add_embed_field(name='Amount of health problems', value='one MILLION!!!')

# add embed object to webhook
webhook.add_embed(embed)

response = webhook.execute()'''

bot.run(TOKEN)