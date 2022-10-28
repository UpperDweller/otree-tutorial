from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'inequal_pgg'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3
    ENDOWMENT_R = 10
    ENHANCEMENT = 2
    # Define Roles
    POOR_ROLE = "poor"
    RICH_ROLE = "rich"



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.FloatField(initial=0)


def set_payoffs(group: Group):
    players = group.get_players()
    for p in players:
        group.total_contribution += p.contribution
    for p in players:
        p.returned = (group.total_contribution * C.ENHANCEMENT)/C.PLAYERS_PER_GROUP
        #Adjust balance to role
        endow = C.ENDOWMENT_R + 5 if p.role == "rich" else C.ENDOWMENT_R-5
        p.balance = p.in_round(max(group.round_number - 1, 1)).balance + p.returned + (endow - p.contribution)




class Player(BasePlayer):
    contribution = models.FloatField(label="How much do you wish to contribute?")
    returned = models.FloatField()
    balance = models.FloatField(initial=0)
# Customise field validation based on role
def contribution_error_message(player, value):
    if value > C.ENDOWMENT_R + 5 and player.role == "rich":
        return "You may not invest more than your endowment"
    elif value > C.ENDOWMENT_R - 5 and player.role == "poor":
        return "You may not invest more than your endowment"


# PAGES
class Contribution(Page):
    form_model = "player"
    form_fields = ["contribution"]
# Return variable to template to display availabe endowment
    @staticmethod
    def vars_for_template(player: Player):
        return dict(end=C.ENDOWMENT_R + 5 if player.role == "rich" else C.ENDOWMENT_R-5)




class ResultsWaitPage(WaitPage):
    after_all_players_arrive = "set_payoffs"


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        # Adjust round_payoff based on role
        endow = C.ENDOWMENT_R + 5 if player.role == "rich" else C.ENDOWMENT_R - 5
        return dict(
            round_payoff=player.returned + (endow - player.contribution)
        )


class FinalResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS



page_sequence = [Contribution, ResultsWaitPage, Results, FinalResults]
