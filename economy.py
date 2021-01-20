# os.chdir()

@client.command()
async def balance(ctx):
  await open_account(ctx.author)
  user = ctx.author
  
  db = await get_bank_data()
  wallet_amount = db[str(user.id)]
  # wallet_amount = users[str(user.id)]["wallet"]
  bank_amount = db[str(user.id)]
  # bank_amount = users[str(user.id)]["bank"]

  em = discord.Embed(title = f"{ctx.author.name}'s balance", color = discord.Color.blue())
  em.add_field(name="Wallet", value=wallet_amount)
  em.add_field(name="Bank", value=bank_amount)
  await ctx.send(embed=em)

async def open_account(user):
  db = await get_bank_data()

  if str(user.id in db):
    return False
  else:
    db[str(user)] = {}
    db[str(user)]["wallet"] = 0
    db[str(user)]["bank"] = 0

  # with open("mainbank.json", "w") as f:
    # json.dump(users, f)
  return True
  

@client.command()
async def beg(ctx):
  await open_account(ctx.author)

  db = await get_bank_data()
  user = ctx.author
  earnings = random.randrange(500)
  await ctx.send(f"Someone gave you {earnings} coins!")
  db[str(user.id)]["wallet"] += earnings
  # users[str(user.id)]["wallet"] += earnings
  # with open("mainbank.json", "w") as f:
    # json.dump(users, f)
  db["key"] = "value"

async def get_bank_data():
  # with open("mainbank.json", "r") as f:
    
  keys = db.keys()
    # users = json.load(f)
  return keys