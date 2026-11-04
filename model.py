import uuid
            
class Choice:

    """A choice for a question."""

    def __init__(self, id: int, text: str, is_correct: bool = False):

        if len(text) == 0:
            raise Exception('Text cannot be empty')
        if len(text) > 100:
            raise Exception('Text cannot be longer than 100 characters')

        self.id = id
        self.text = text
        self.is_correct = is_correct

class Question:

    """A question with multiple choices."""

    def __init__(self, title: str, points: int=1, max_selections: int=1):

        if len(title) == 0:
            raise Exception('Title cannot be empty')
        if len(title) > 200:
            raise Exception('Title cannot be longer than 200 characters')
        if points < 1 or points > 100:
            raise Exception('Points must be between 1 and 100')

        self.title = title
        self.points = points
        self.max_selections = max_selections

        self.id = uuid.uuid4().hex
        self.choices = []

    """
    Adds a choice to the question.

    Args:
        text (str): The text of the choice.
        is_correct (bool): Whether the choice is correct. Defaults to False.

    Returns:
        Choice: The created choice object.
    """

    def add_choice(self, text: str, is_correct: bool = False) -> Choice:
        choice = self._create_choice(text, is_correct)
        self.choices.append(choice)
        return choice
    
    """
    Removes a choice from the question by its ID.

    Args:
        id (int): The ID of the choice to remove.
    
    Raises:
        Exception: If the choice ID is invalid.
    """
    
    def remove_choice_by_id(self, id: int):
        choice = self._find_choice_by_id(id)
        self.choices.remove(choice)

    """
    Removes all choices from the question.
    """
    
    def remove_all_choices(self):
        self.choices.clear()

    """
    Sets the correct choices for the question.

    Args:
        correct_choice_ids (list[int]): A list of IDs of the choices that are correct.
    
    Raises:
        Exception: If any of the provided choice IDs are invalid.
    """

    def set_correct_choices(self, correct_choice_ids: list[int]):
        for choice_id in correct_choice_ids:
            choice = self._find_choice_by_id(choice_id)
            if choice:
                choice.is_correct = True

    """
    Corrects the selected choices.

    Args:
        selected_choice_ids (list[int]): A list of IDs of the selected choices.

    Returns:
        list[int]: A list of IDs of the correct choices that were selected.

    Raises:
        Exception: If more than the maximum allowed selections are made.
    """

    def correct_selected_choices(self, selected_choice_ids: list[int]) -> list[int]:
        
        if len(selected_choice_ids) > self.max_selections:
            raise Exception(f'Cannot select more than {self.max_selections} choices')
        
        return [selected_choice_id for selected_choice_id in selected_choice_ids if selected_choice_id in self._find_correct_choice_ids()]
    
    def _create_choice(self, text: str, is_correct: bool) -> Choice:
        return Choice(id=self._generate_choice_id(), text=text, is_correct=is_correct)
    
    def _generate_choice_id(self) -> int:
        if len(self.choices) == 0:
            return 1
        last_choice = self.choices[-1]
        return last_choice.id + 1

    def _find_choice_by_id(self, choice_id: int) -> Choice | None:
        self._check_valid_choice_id(choice_id)
        for choice in self.choices:
            if choice.id == choice_id:
                return choice
        return None
    
    def _find_correct_choice_ids(self) -> list[int]:
        return [choice.id for choice in self.choices if choice.is_correct]

    def _check_valid_choice_id(self, choice_id: int):
        if choice_id not in self._list_choice_ids():
            raise Exception(f'Invalid choice id {choice_id}')
        
    def _list_choice_ids(self) -> list[int]:
        return [choice.id for choice in self.choices]
        