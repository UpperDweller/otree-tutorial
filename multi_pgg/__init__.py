from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'multi_pgg'
    PLAYERS_PER_GROUP = 3
    # Increase number of rounds
    NUM_ROUNDS = 3
    ENDOWMENT_R = 10.0
    ENHANCEMENT = 2



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
        # Balance is defined by last round's balance plus the net payoff in the current round
        p.balance = p.in_round(max(group.round_number - 1, 1)).balance + p.returned + (C.ENDOWMENT_R - p.contribution)




class Player(BasePlayer):
    contribution = models.FloatField(min=0, max=C.ENDOWMENT_R, label="How much do you wish to contribute?")
    returned = models.FloatField()
    # Add balance variable to keep track of payoff over the course of the game
    balance = models.FloatField(initial=0)




# PAGES
class Contribution(Page):
    form_model = "player"
    form_fields = ["contribution"]


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = "set_payoffs"


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            round_payoff=player.returned + (C.ENDOWMENT_R - player.contribution)
        )

# Final Results page to sum up the game
class FinalResults(Page):
    @staticmethod
    # Only is displayed when the current round is the last round
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


# Added final results page on the end of sequence
page_sequence = [Contribution, ResultsWaitPage, Results, FinalResults]
