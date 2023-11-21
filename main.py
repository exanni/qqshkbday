import discord
from discord.ext import commands
import sqlite3
import random
import os

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

conn = sqlite3.connect('qq.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS players 
                (user_id INTEGER PRIMARY KEY,
                 username TEXT,
                 outcome INTEGER,
                 pivo_used INTEGER,
                 prazd INTEGER)''')


@bot.command()
async def праздник(ctx):
 x = [
    discord.File('p.png'),
    discord.File('i.png'),
    discord.File('v.png'),
    discord.File('o.png')
  ]
 random.shuffle(x)
 c.execute('SELECT * FROM players WHERE user_id = ?', (ctx.author.id,))
 existing_user = c.fetchone()
 if existing_user is None:
    c.execute('INSERT INTO players (user_id, username, outcome, pivo_used, prazd) VALUES (?, ?, ?, ?, ?)', (ctx.author.id, ctx.author.name, 0, 0, 0))
  
    await ctx.send("Ну чё, хакер, молодец! Ты расшифровал сообщение, но работа не закончена. Теперь отыщи команду, спрятанную в этих картинках. Вперёд!", files=x)
 else:
  c.execute('''UPDATE players SET prazd = ? WHERE user_id = ?''', (1, ctx.author.id))
  
  await ctx.send("Ну чё, хакер, молодец! Ты расшифровал сообщение, но работа не закончена. Теперь отыщи команду, спрятанную в этих картинках. Вперёд", files=x)
  

@bot.command()
async def пиво(ctx):
  c.execute('''SELECT prazd FROM players WHERE user_id = ?''', (ctx.author.id,))
  prazd_used = c.fetchone()
  if prazd_used is None:
      await ctx.send('Нет, пить сегодня нельзя...')
      return
  c.execute('''SELECT pivo_used FROM players WHERE user_id = ?''', (ctx.author.id,))
  existing_user = c.fetchone()
  if existing_user[0] == 1:
    await ctx.send("Предложение пьянчуги всё ещё в силе! Просто напиши **!битва** для алкогольной битвы с ним!")
  elif existing_user is None or existing_user[0] != 1:
    c.execute('''UPDATE players SET pivo_used = ? WHERE user_id = ?''', (1, ctx.author.id))
    await ctx.send("Неожиданно, ты телепортируешься в бар и встречаешься лицом к лицу с каким-то пьяницей. Он вызывает тебя на алкогольную битву. Чтобы принять его предложение, напиши **!битва**")

@bot.command()
async def битва(ctx):
 try:

  c.execute("SELECT pivo_used FROM players WHERE user_id = ?", (ctx.author.id,))
  existing_user = c.fetchone()[0]
  if existing_user == 1:
    player_hp = 5
    player_coins = 100
    bot_hp = 5
    bot_coins = 100
    user_id = ctx.author.id
    username = ctx.author.name

    await ctx.send("В волнующем вызове дуэли, ты устраиваешься рядом с пьянчугой, свет в баре исчезает, все вокруг замирают, а прожекторы мерцают, устремленные на вас двоих... Приготовься к началу эпического столкновения!")

    while player_hp > 0 and bot_hp > 0 and player_coins > 0 and bot_coins > 0:
        event = random.choice(["пьем", "Принесите что по крепче", "тыменянеуважаешь?", "Закусь", "А давай сыграем", "Крапленые карты", "Боярышник"])
        
        if event == "пьем":
            player_hp -= 1
            plostc = random.randint(8, 15)
            player_coins -= plostc
            emsg = f"Ты решаешь выпить бокальчик пива. Ты заплатил {plostc} за него. Ты немного опьянел."
            
        elif event == "Принесите что по крепче":
            player_hp -= random.randint(2, 3)
            plostc = random.randint(20, 35)
            player_coins -= plostc
            emsg = (f'Ты просишь бармена принести рюмку {random.choice(["коньяка", "водки", "текилы", "виски"])}, заплатив {plostc} за выпивку. Ты сильно опьянел!')         
            
        elif event == "тыменянеуважаешь?":
            player_hp += 1
            bot_hp += 1
            emsg = "Вы с пьянчугой начали странный спор. С головой погружённые в него, вы немного протрезвели."
            
        elif event == "Закусь":
            player_hp += 1
            plostc = random.randint(2, 10)
            player_coins -= plostc
            emsg = f'Ты попросил бармена принести {random.choice(["чипсы", "рыбу", "закусь"])}, заплатив {plostc} монет за еду. Это позволит тебе дольше продержаться на плаву.'
            
        elif event == "А давай сыграем":
            player_win = random.randint(-25, 25)
            player_coins += player_win
            bot_coins -= player_win
            if abs(player_win) == 1:
                mone = "монету"
            if abs(player_win) >= 2 and abs(player_win) <=4:
                mone = "монеты"
            else:
                mone = "монет"
            if player_win > 0:
              emsg = f'Вам с пьянчугой стало скучно, поэтому вы решили сыграть в {random.choice(["дурака", "покер", "очко"])}. Ты победил, забирая выигрыш: {player_win} {mone}.'
            elif player_win < 0:
              emsg = f'Вам с пьянчугой стало скучно, поэтому вы решили сыграть в {random.choice(["дурака", "покер", "очко"])}. Ты проиграл, потеряв {abs(player_win)} {mone}.'
            elif player_win == 0:
              emsg = f'Вам с пьянчугой стало скучно, поэтому вы решили сыграть в дурака. Ничья.'
            
        elif event == "Крапленые карты":
            player_win = random.randint(8, 25)
            player_coins += player_win
            bot_coins -= player_win
            emsg = f'Вы решили сыграть в {random.choice(["дурака", "покер", "очко"])}. Благодаря хитрым манипуляциям с картами ты выиграл {player_win} монет. Грязный шулер.'
            
        elif event == "Боярышник":
            player_hp -= 2
            player_coins -= random.randint(5, 10)
            emsg = f'Ты решил выпить боярышника. Ты сильно опьянел, и чувствешь себя не очень хорошо. Ты заплатил {random.randint(5, 10)} монет за выпивку.'
        if player_hp > 10:
           player_hp = 10
    
        bot_event = random.choice(["пьем", "Принесите что по крепче", "тыменянеуважаешь?", "Закусь", "А давай сыграем", "Крапленые карты", "Боярышник"])
        if bot_event == "пьем":
            bot_hp -= 1
            botloss = random.randint(8, 15)
            bot_coins -= botloss
            bmsg = f"Пьянчуга решает выпить бокальчик пива, заплатив {botloss} за него. Он немного опьянел."
            
        elif bot_event == "Принесите что по крепче":
            bot_hp -= random.randint(2, 3)
            botloss = random.randint(20, 35)
            bot_coins -= botloss
            bmsg = f'Пьянчуга просит бармена принести рюмку {random.choice(["коньяка", "водки", "текилы", "виски"])}, заплатив {botloss} за выпивку. Кажется, его повело!'         
          
            
        elif bot_event == "тыменянеуважаешь?":
            bot_hp += 1
            player_hp += 1
            bmsg = "Вы с пьянчугой начали странный спор. С головой погружённые в него, вы немного протрезвели."
            
        elif bot_event == "Закусь":
            bot_hp -= 1
            botloss = random.randint(2, 10)
            bot_coins -= botloss
            bmsg = f'Пьянчуга попросил бармена принести {random.choice(["чипсы", "рыбу", "закусь"])}, заплатив {botloss} монет за еду. Кажется, было вкусно.'
            
        elif bot_event == "А давай сыграем":
          bot_win = random.randint(-25, 25)
          bot_coins += bot_win
          player_coins -= bot_win
          if abs(bot_win) == 1:
                mone = "монету"
          if abs(bot_win) >= 2 and abs(bot_win) <=4:
                mone = "монеты"
          else:
                mone = "монет"
          if bot_win > 0:
              bmsg = f'Вам с пьянчугой стало скучно, поэтому вы решили сыграть в {random.choice(["дурака", "покер", "очко"])}. Ты проиграл, потеряв {bot_win} {mone}.'
          elif bot_win < 0:
              bmsg = f'Вам с пьянчугой стало скучно, поэтому вы решили сыграть в {random.choice(["дурака", "покер", "очко"])}. Ты победил, забирая выигрыш: {abs(bot_win)} {mone}.'
          elif bot_win == 0:
              bmsg = f'Вам с пьянчугой стало скучно, поэтому вы решили сыграть в дурака. Ничья.'          
            
        elif bot_event == "Крапленые карты":
            bot_win = random.randint(8, 25)
            bot_coins += bot_win
            player_coins -= bot_win
            bmsg = f'Вам с пьянчугой стало скучно, поэтому вы решили сыграть в {random.choice(["дурака", "очко", "покер"])}. Ты потерял {bot_win} монет. Что-то тут не так...'
        elif bot_event == "Боярышник":
            bot_hp -= 2
            bot_coins -= random.randint(5, 10)
          
            bmsg = f'Пьянчуга решил заказать боярышник, заплатив за него {random.randint(5, 10)} монет. Он, кажись, сильно опьянел.'
        if bot_hp > 10:
           bot_hp = 10
        await ctx.send(f"- {emsg}\n- {bmsg} \n- Твоё ХП: {player_hp}\n- ХП Пьянчуги: {bot_hp}\n- Твои монеты: {player_coins}\n- Монеты Пьянчуги: {bot_coins}")

    if player_hp > 0 and player_coins > 0 and bot_coins <= 0:
      outcome = "win"
      outmsg = "У пьянчуги кончились монеты, он не может продолжать битву. Ты победил!"
    elif player_hp > 0 and player_coins > 0 and bot_hp <= 0:
      outcome = "win"
      outmsg = "Пьянчуга вырубился быстрее тебя... А ты следом за ним. В любом случае, победа за тобой!"
    elif player_hp > 0 and player_coins > 0 and bot_hp <= 0 and bot_coins <= 0:
      outcome = "win"
      outmsg = "Пьянчуга вырубился быстрее тебя, так ты ещё и ободрал его до нитки. Ты победил!"
    elif player_hp <= 0 and player_coins > 0:
      outcome = "lose"
      outmsg = "Мир вокруг тебя плывёт, глаза закатываются и ты вырубаешься. Ты проиграл! Может стоит попробовать ещё разок?"
    elif player_hp > 0 and player_coins <= 0:
      outcome = "lose"
      outmsg = "Тебе больше не на что пить. Так ты ещё и в долгу. Мдэм. Может, стоит попробовать ещё разок?"
    elif player_hp <= 0 and player_coins <= 0:
      outcome = "lose"
      outmsg = "Ты вырубился быстрее пьянчуги. Так ты ещё и в долгу. Мдэм. Может, стоит попробовать ещё разок?"
    else:
      outcome = "draw"
      outmsg = "В конце битвы сложилась непредвиденная ситуация. Вы сошлись на ничьей. Может, стоит попробовать ещё разок?"
    await ctx.send(outmsg)
    
    if outcome == "win":
      
      c.execute(f'''UPDATE players SET outcome = ? WHERE user_id = ?''', (1, ctx.author.id))
      await ctx.send('Немного оклемавшись, пьянчуга произнёс:\n "Это было ошеломляющее сражение!"\nОтряхнувшись, ты решил выйти из бара, но вдруг пьянчуга прошептал тебе:\n*"Передай кукушке, что ему стоит отправиться в парк. И не забудь **!поздравить** его."*')
    else:
      return
        
  else:
    await ctx.send("С кем ты биться собрался, дуралей?")
 except:
  await ctx.send("С кем ты биться собрался, дуралей?")

@bot.command()
async def поздравить(ctx, *, pozdr=None):
 try:
  c.execute("SELECT outcome FROM players WHERE user_id = ?", (ctx.author.id,))
  existing_user = c.fetchone()
  if existing_user[0] == 1:
    if pozdr is None:
      await ctx.send("Мне кажется, ты ничего не написал в своём поздравлении...")
      return
    if len(pozdr) > 50:
        await ctx.send("Твоё поздравление принято! Спасибо за участие в квесте.")
        channel = bot.get_channel(1169956810342531185)
        sentmsg = await channel.send(f"{ctx.author.display_name} поздравил кукушку: {pozdr}. \n <@&1169956809306542194> Спонсорка?")
    else:
      if pozdr is None:
        await ctx.send("Мне кажется, ты ничего не написал в своём поздравлении...")
        return
      await ctx.send("Ну разве так поздравляют? Попробуй ещё разок, а то уж слишком коротко...")
  else:
    await ctx.send("Читерим? Не туда тебя запёрло, дружок. Пройди весь квест перед этим.")
 except:
   await ctx.send("Читерим? Не туда тебя запёрло, дружок. Пройди весь квест перед этим.")
  
bot.run(os.getenv("TOKEN"))
