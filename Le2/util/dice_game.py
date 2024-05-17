import os
import time
import random
from util.score import Score

class DiceGame:
	def __init__(self, username):
		self.username = username
		self.score_folder = "scores"
		self.score_file = os.path.join(self.score_folder, "rankings.txt")
		self.create_score_folder()
		self.score = Score(self.username,"")

	def create_score_folder(self):
		if not os.path.exists(self.score_folder):
			os.makedirs(self.score_folder)

	def scores(self):
		scores = []	
		try:
			if os.path.exists(self.score_file):
				with open(self.score_file, "r") as file:
					for line in file:
						username, score, stage_score, date = line.strip().split(",")
						scores.append((username,int(score),int(stage_score), date))
			return scores
		except FileNotFoundError:
			return None

	def save_scores(self, scores):
		with open(self.score_file, "w") as file:
			for username, score, wins, game_id in scores:
				file.write(f"{username},{score},{wins},{game_id}\n")
				
	def top_scores(self):
		top_scores = self.scores()
		top_scores.append((self.score.record()))
		top_scores.sort(key=lambda i: i[1], reverse=True) 
		top_scores = top_scores[:10] 
		self.save_scores(top_scores) 

	def play_game(self):
		print(f"Starting game as {self.username}...\n")

		points = {"user": 0, "computer": 0, "points": 0, "stage": 0}

		times = 0
		round = 1
		stage = 1

		while True:
			if times == 0:
					print(f"=======+ STAGE {stage} +=======")
			for x in range(3-times):
				computer_roll = random.randint(1, 6)
				user_roll = random.randint(1, 6)
				
				print(f"------// ROUND {round} \\\------")
				print(f"{self.username} rolled: \t{user_roll}")
				print(f"Computer rolled: \t{computer_roll}")

				if user_roll < computer_roll:
					print("-COMPUTER WON THIS ROUND!\n")
					points["computer"] += 1
				elif user_roll > computer_roll:
					print(f"-YOU WON THIS ROUND!\n")
					points["user"] += 1
					points["points"] += 1
				else:
					print("-IT'S A TIE!\n")
				round += 1
				time.sleep(1)

			if points["user"] != points["computer"]:
				winner = "user" if points["user"] > points["computer"] else "computer"
				if winner == "user":
					print(f"You won this stage, {self.username}")
					points["points"] += 3
					points["stage"] += 1
					stage += 1

					#Update score
					self.score.update_score(points["points"], points["stage"])
					print("Total Points:", points["points"], ", Stages Won:", points["stage"])
					time.sleep(1)

					while True:
						option = input("\nDo you want to continue to the next stage? (1 for 'Yes' 0 for 'No'): ")
						if option == "1":
							times = 0
							points["user"] = 0
							points["computer"] = 0
							os.system("cls")
							print(f"Starting game as {self.username}...\n")
							break
						elif option == "0":
							self.score.update_score(points["points"], points["stage"])
							self.top_scores()
							print("Saving scores...")
							time.sleep(1)
							self.menu()
							return
						else:
							print("Invalid input. Please enter 1 for 'Yes' or 0 for 'No'.")
							time.sleep(1)
				else:
					print(f"You lost this stage, {self.username}! \nGame over. ", end = "")
					if points["stage"] == 0:
						print("You didn't win any stages.")
					else:
						print("You won", points["stage"], "stage/s and scored", points["points"], "points.")
						self.score.update_score(points["points"], points["stage"]) 
						self.top_scores()
					input("\nPress Enter to Continue...")
					return
			else:
				times = 2
				print("\n----// TIE BREAKER \\\----")
				time.sleep(1)

	def show_top_scores(self):
		os.system('cls')
		print("TOP SCORES:")
		scores = self.scores()
		if scores:
			for idx, (username, score, stage, date) in enumerate(scores, start = 1):
				print(f"{idx}.) Stages won - {stage}, Points - {score}, \n\tby: {username} on: {date}")
		else:
			print("No records yet. Play a game to see top scores.")
		input("\nPress Enter to Continue...")

	def logout(self):
		print("Logging out...")
		time.sleep(1)
		return True

	def menu(self):
		while True:
			try:
				os.system('cls')
				print(f"WELCOME, {self.username.upper()}!")
				option = int(input("Menu: \n1. Start Game\n2. Show top scores\n3. Log out \n\nEnter number only: "))

				if option == 1:
					os.system('cls')
					self.play_game()
				elif option == 2:
					self.show_top_scores()
				elif option == 3:
					if self.logout():
						return True
				else:
					raise ValueError("Enter number from list!")
				
			except ValueError as e:
				print("Error: ", e)
				time.sleep(1)
