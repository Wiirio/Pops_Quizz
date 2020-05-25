# Create your views here.
# -*- coding: utf-8 -*-
from Quizz.requests.request_question import *
from Quizz.requests.request_user_answers import *
from Quizz.requests.request_possible_answer import *


def get_player_by_id(id):
    return Player.objects.get(id)


def get_player_by_game_by_login(game, login):
    user = User.objects.get(login=login)
    return Player.objects.get(game=game, user=user)


def get_players_by_game_order_by_score_desc(game):
    return Player.objects.filter(game=game).order_by('-score')


def calculate_score(player_id):
    player = get_player_by_id(player_id)
    questions = getPossibleAnswersByQuestions(getQuestionsByForm(player.game.form))
    score = 0
    for q in questions:
        if q['question'].answer_type.type == "QCM" or q['question'].answer_type.type == "UNIQUE_ANSWER":
            for possible_answer in q["answers"]:
                if user_selected_possible_answer(possible_answer, player):
                    if possible_answer.correct:
                        score += 1
                    else:
                        # decrease score by one if QCM
                        score -= 0.5 if q['question'].answer_type.type == "QCM" else 0
        elif q['question'].answer_type.type == "INPUT":
            possible_input_values = []
            for possible_answer in q["answers"]:
                possible_input_values.append(possible_answer.value.strip())
            user_answer_input = get_input_response_by_question_by_player(q['question'], player)
            if user_answer_input.value in possible_input_values:
                score += 1
    player.score = score
    player.save()
