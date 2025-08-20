  import os
  import requests
  from bs4 import BeautifulSoup
  from telegram import Bot
  from apscheduler.schedulers.blocking import BlockingScheduler

  BOT_TOKEN = os.getenv("8149627075:AAHTKFurd9J3n3Tb4q45jvJi0pIsYXZxW_I")
  CHAT_ID = os.getenv("5017126108")

  bot = Bot(token=BOT_TOKEN)

  seen_coins = set()
  seen_airdrops = set()

  def check_new_coins():
      url = "https://cryptorank.io/new-cryptocurrencies"
      response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
      soup = BeautifulSoup(response.text, "html.parser")

      coins = soup.select("a.chakra-link")
      for coin in coins:
          name = coin.get_text(strip=True)
          link = coin.get("href")

          if link and link.startswith("/"):
              link = "https://cryptorank.io" + link

          if link and link not in seen_coins and "cryptocurrencies" in link:
              seen_coins.add(link)
              message = f"📈 New Coin Listed!\n\n{name}\n🔗 {link}"
              bot.send_message(chat_id=CHAT_ID, text=message)

  def check_new_airdrops():
      url = "https://cryptorank.io/airdrops"
      response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
      soup = BeautifulSoup(response.text, "html.parser")

      airdrops = soup.select("a.chakra-link")
      for drop in airdrops:
          name = drop.get_text(strip=True)
          link = drop.get("href")

          if link and link.startswith("/"):
              link = "https://cryptorank.io" + link

          if link and link not in seen_airdrops and "airdrops" in link:
              seen_airdrops.add(link)
              message = f"🎁 New Airdrop Listed!\n\n{name}\n🔗 {link}"
              bot.send_message(chat_id=CHAT_ID, text=message)

  scheduler = BlockingScheduler()
  scheduler.add_job(check_new_coins, "interval", minutes=10)
  scheduler.add_job(check_new_airdrops, "interval", minutes=10)

  print("🤖 CryptoRank Bot is running...")
  scheduler.start()

