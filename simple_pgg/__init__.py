from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'simple_pgg'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    # Constant parameters of the game
    ENDOWMENT_R = 10.0
    ENHANCEMENT = 2



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # Create field to aggregate
    total_contribution = models.FloatField(initial=0)

# Define payoff function on the group level
def set_payoffs(group: Group):
    # Create an object containing the list of players
    players = group.get_players()
    # Looping through players
    for p in players:
        # Aggregate individual contributions
        group.total_contribution += p.contribution
    for p in players:
        # Calculate individual share of the public good
        p.returned = (group.total_contribution * C.ENHANCEMENT)/C.PLAYERS_PER_GROUP




class Player(BasePlayer):
    # Create input field for contribution
    contribution = models.FloatField(min=0, max=C.ENDOWMENT_R, label="How much do you wish to contribute?")
    # Field to store PGG return
    returned = models.FloatField()




# PAGES
class Contribution(Page):
    # Form model refers to the Class which contains the formfields
    form_model = "player"
    # Formfields to include in this page
    form_fields = ["contribution"]



class ResultsWaitPage(WaitPage):
    #Call the payoff function
    after_all_players_arrive = "set_payoffs"


class Results(Page):
    # Calculate variable only to display on the results page
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            round_payoff=player.returned + (C.ENDOWMENT_R - player.contribution)
        )

# All the pages of this app
page_sequence = [Contribution, ResultsWaitPage, Results]
