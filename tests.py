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


def test_create_choice_with_correct_answer():
    question = Question(title='q1')

    choice = question.add_choice('Correct answer', is_correct=True)

    assert choice.text == 'Correct answer'
    assert choice.is_correct is True


def test_create_choice_with_empty_text():
    question = Question(title='q1')

    with pytest.raises(Exception, match='Text cannot be empty'):
        question.add_choice('')


def test_create_choice_with_text_longer_than_100_characters():
    question = Question(title='q1')

    with pytest.raises(Exception, match='Text cannot be longer than 100 characters'):
        question.add_choice('a' * 101)


def test_add_multiple_choices_with_sequential_ids():
    question = Question(title='q1')

    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    choice3 = question.add_choice('c')

    assert [choice1.id, choice2.id, choice3.id] == [1, 2, 3]


def test_remove_choice_by_id():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    question.add_choice('b')

    question.remove_choice_by_id(choice1.id)

    assert len(question.choices) == 1
    assert question.choices[0].text == 'b'


def test_remove_choice_with_invalid_id():
    question = Question(title='q1')
    question.add_choice('a')

    with pytest.raises(Exception, match='Invalid choice id'):
        question.remove_choice_by_id(999)


def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')

    question.remove_all_choices()

    assert question.choices == []


def test_set_correct_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    choice3 = question.add_choice('c')

    question.set_correct_choices([choice1.id, choice3.id])

    assert choice1.is_correct is True
    assert choice2.is_correct is False
    assert choice3.is_correct is True


def test_correct_selected_choices():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a', is_correct=True)
    question.add_choice('b')
    choice3 = question.add_choice('c', is_correct=True)

    result = question.correct_selected_choices(
        [choice1.id, choice3.id]
    )

    assert result == [choice1.id, choice3.id]


def test_correct_selected_choices_exceed_maximum_selections():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', is_correct=True)
    question.add_choice('b', is_correct=True)
    question.add_choice('c', is_correct=True)

    with pytest.raises(Exception, match='Cannot select more than 2 choices'):
        question.correct_selected_choices([1, 2, 3])


@pytest.fixture
def question_with_multiple_choices():
    question = Question(title='What is 2 + 2?', max_selections=2)

    question.add_choice('3')
    question.add_choice('4', is_correct=True)
    question.add_choice('5')
    question.add_choice('6', is_correct=True)

    return question


def test_question_with_multiple_choices_has_four_choices(question_with_multiple_choices):
    question = question_with_multiple_choices

    assert len(question.choices) == 4
    assert question.choices[1].text == '4'
    assert question.choices[3].text == '6'


def test_question_corrects_multiple_selected_choices(question_with_multiple_choices):
    question = question_with_multiple_choices

    result = question.correct_selected_choices([2, 4])

    assert result == [2, 4]


def test_question_identifies_only_correct_selected_choices(question_with_multiple_choices):
    question = question_with_multiple_choices

    result = question.correct_selected_choices([1, 2])

    assert result == [2]