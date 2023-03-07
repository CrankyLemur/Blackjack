  def write_leaderboard(self):
    if self.player_name in db:
      print(("\nYou already have a registered score of "\
      f"{db[self.player_name]}. Overwrite?"))
      while True:
        choice = input(("Select one of the following:\n"
                        "y - Yes\n"
                        "n - No\n"
                        ":")).lower()
        if choice == 'y':
          db[self.player_name] = int(self.score)
          print("New score added!")
          break
        elif choice == 'n':
          break
        else:
          print("Invalid choice")
    else:
      db[self.player_name] = int(self.score)

  def show_leaderboard(self):
    try:
      print("These are the current highscores:\n")
      for key in db.keys():
        print(f"{key}: {db[key]}")
    except:
      print("Actually there aren't any yet. What a chance for you to shine!")