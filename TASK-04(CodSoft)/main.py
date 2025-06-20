#### Task-04 ####

import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty


class RPSGame(BoxLayout):
    user_choice = StringProperty("")
    computer_choice = StringProperty("")
    result = StringProperty("")
    user_score = NumericProperty(0)
    computer_score = NumericProperty(0)

    def play(self, choice):
        self.user_choice = choice
        self.computer_choice = random.choice(["Rock", "Paper", "Scissors"])
        self.result = self.determine_winner(self.user_choice, self.computer_choice)

    def determine_winner(self, user, computer):
        if user == computer:
            return "It's a Tie!"
        elif (
            (user == "Rock" and computer == "Scissors") or
            (user == "Scissors" and computer == "Paper") or
            (user == "Paper" and computer == "Rock")
        ):
            self.user_score += 1
            return "You Win!"
        else:
            self.computer_score += 1
            return "Computer Wins!"

    def reset_game(self):
        self.user_choice = ""
        self.computer_choice = ""
        self.result = ""


class RPSApp(App):
    def build(self):
        return RPSGame()


if __name__ == "__main__":
    RPSApp().run()
