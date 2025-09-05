import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

# meus testes
def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=500)
    with pytest.raises(Exception):
        Question(title='q1', points=-500)

def test_create_question_with_invalid_edge_case_point():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_create_invalid_choice():
    with pytest.raises(Exception):
        question = Question(title='q1', points=10)
        question.add_choice('', is_correct=False)
    with pytest.raises(Exception):
        question = Question(title='q1', points=10)
        question.add_choice('a'*101, is_correct=False)

def test_removes_all_choices():
    question = Question(title='q1', points=10)
    question.add_choice('choice1', is_correct=False)
    question.add_choice('choice2', is_correct=False)
    question.add_choice('choice3', is_correct=False)
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_removes_choice_by_id():
    question = Question(title='q1', points=10)
    question.add_choice('not removed', is_correct=False)
    removedid = question.add_choice('to be removed', is_correct=False).id
    question.add_choice('not removed either', is_correct=False)
    question.remove_choice_by_id(removedid)
    assert len(question.choices) == 2
    assert question.choices[0].id != removedid
    assert question.choices[1].id != removedid

def test_removing_choice_with_invalid_id():
    question = Question(title='q1', points=10)
    question.add_choice('choice', is_correct=False)
    with pytest.raises(Exception):
        question.remove_choice_by_id(-1)

def test_sets_choice_as_correct():
    question = Question(title='q1', points=10)
    choice = question.add_choice('false choice', is_correct=False)
    question.set_correct_choices([choice.id])
    assert choice.is_correct

def test_sets_multiple_choices_as_correct():
    question = Question(title='q1', points=10)
    choice1 = question.add_choice('false choice', is_correct=False)
    choice2 = question.add_choice('false choice', is_correct=False)
    choice3 = question.add_choice('false choice', is_correct=False)
    question.set_correct_choices([choice1.id, choice2.id, choice3.id])
    assert choice1.is_correct
    assert choice2.is_correct
    assert choice3.is_correct

def test_sets_invalid_choice_as_correct():
    question = Question(title='q1', points=10)
    question.add_choice('false choice', is_correct=False)
    with pytest.raises(Exception):
        question.set_correct_choices([-1])

def test_sets_multiple_invalid_choices_as_correct():
    question = Question(title='q1', points=10)
    choice1 = question.add_choice('false choice', is_correct=False)
    question.add_choice('false choice', is_correct=False)
    choice3 = question.add_choice('false choice', is_correct=False)
    with pytest.raises(Exception):
        question.set_correct_choices([choice1.id, -1, choice3.id])
    