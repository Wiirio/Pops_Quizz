# Create your views here.
# -*- coding: utf-8 -*-
from Quizz.models import *
from Quizz.requests.request_user_answers import *


def getQuestionsByForm(form):
    return Question.objects.filter(form=form).order_by('order')


def get_question_by_id(question_id):
    print(question_id)
    return Question.objects.get(id=question_id)


def need_correction_for_question(question):
    question.need_correction = True
    question.save()


def getNbQuestionsByForm(form):
    return len(Question.objects.filter(form=form).order_by('order'))


def getNextQuestion(form, actual_row):
    try:
        q = Question.objects.filter(form=form).order_by('order')[actual_row]
    except IndexError:
        q = False

    return q


def getPossibleAnswersByQuestions(questions):
    Tquestion = []
    for q in questions:
        pa = PossibleAnswer.objects.filter(question=q)
        Tquestion.append({'question': q, 'answers': pa})
    return Tquestion

def getPossibleAnswersByQuestion(question):
    Tquestion = []
    pa = PossibleAnswer.objects.filter(question=question)
    Tquestion.append({'question': question, 'answers': pa})
    return Tquestion

def addQuestion(form, at, label, order):
    q = Question()
    q.form = form
    q.answer_type = at
    q.label = label
    q.order = order
    q.need_correction = False
    q.save()
    return q


def getUserAnswersByQuestions(questions, player):
    Tquestion = []
    for q in questions:
        pa = PossibleAnswer.objects.filter(question=q)
        for p in pa:
            if len(UserAnswers.objects.filter(player=player, possible_answer=p)) > 0:
                p.ua = UserAnswers.objects.get(player=player, possible_answer=p)

        if q.answer_type.type == "INPUT":
            if is_input_response_have_user_answer(q, player):
                possible_input_values = []
                for possible_answer in pa:
                    possible_input_values.append(possible_answer.value.strip().upper())
                q.input_valide = False
                user_answer_input = get_input_response_by_question_by_player(q, player)
                if user_answer_input.value.strip().upper() in possible_input_values:
                    q.input_valide = True

        Tquestion.append({'question': q, 'answers': pa})

    return Tquestion
