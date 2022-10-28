from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Fields may contain the datatype included in their name
    name = models.StringField(label="Please enter your first name")
    age = models.IntegerField(label="What is your age?")
    # Choice variables are included as integer fields with numeric choices and labels
    gender = models.IntegerField(label="Please choose your gender",
                                 choices=[
                                     [1, "male"],
                                     [2, "female"],
                                     [3, "other"]
                                 ])
    # Widgets allow for different presentation of choice variables
    happy = models.IntegerField(label="How happy are you?",
                                choices=[
                                    [1, "very unhappy"],
                                    [2, ""],
                                    [3, ""],
                                    [4, ""],
                                    [5, ""],
                                    [6, ""],
                                    [7, "very happy"]
                                ],
                                widget=widgets.RadioSelectHorizontal
                                )


# PAGES
class Survey(Page):
    form_model = 'player'
    form_fields = ["name", "age", "gender", "happy"]


page_sequence = [Survey]
