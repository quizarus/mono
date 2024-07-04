from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Question:
    uuid: uuid4
    round_uuid: uuid4
    theme_uuid: uuid4
    order: int
    answer: str
    content: str = None
    type: str = 'text'
    cost: int = 0


@dataclass
class Theme:
    uuid: uuid4
    round_uuid: uuid4
    name: str


@dataclass
class Round:
    uuid: uuid4
    order: int
    name: str


def parse_questions(questions: list | dict):
    def parse_question(question: dict):
        question_id = uuid4()
        question_cost = 0
        question_cost = int(question['@price'])
        question_text = ''
        question_type = 'text'
        question_content = None
        post_question_content = None
        question_data = question['scenario']['atom']
        if isinstance(question_data, dict):
            question_type = question_data['@type']
            question_content = question_data['#text']
        if isinstance(question_data, list):
            if len(question_data) == 4:
                question_text = question_data[0]
                question_content = question_data[1]['#text']
                post_question_content = question_data[3]['#text']
            else:
                try:
                    question_type = question_data[-1]['@type']
                except TypeError:
                    question_content = ' '.join(p for p in question_data)
                if question_type == 'marker':
                    question_text = question_data[0]
                elif question_type in ('voice', 'say', 'image', 'video'):
                    if isinstance(question_data[0], str):
                        question_text = question_data[0]
                    elif isinstance(question_data[0], dict) and '#text' in question_data[0]:
                        question_text = question_data[0]['#text']
                    else:
                        print('IS NOT STR QUESTION TEXT, SAVED ONLY FIRST', question) # TODO: прологировать или убрать, если это не баг и в других паках будет больше 1 варианта техта
                    question_content = question_data[-1]['#text']
        if isinstance(question_data, str):
            question_text = question_data
        question_answer = question['right']['answer']
        if question_answer is not None:
            parsed_question = {'uuid': question_id,
                               'cost': question_cost,
                               'type': question_type,
                               'text': question_text,
                               'content': question_content,
                               'answer': question_answer.lower()}
            parsed_questions.append(parsed_question)

            if question_content:
                if question_content.startswith('@'):
                    internal_contents[question_id] = {'content': question_content[1:]}
                if question_content.startswith('http'):
                    external_contents[question_id] = {'content': question_content}
            if post_question_content:
                if post_question_content.startswith('@'):
                    internal_contents[question_id]['post_content'] = post_question_content[1:]
                if post_question_content.startswith('http'):
                    internal_contents[question_id]['post_content'] = post_question_content

    parsed_questions = []
    external_contents: {uuid4, dict[str, str]} = {}
    internal_contents: {uuid4, dict[str, str]} = {}
    if isinstance(questions, list):
        for question in questions:
            parse_question(question)
    else:
        parse_question(questions)

    return parsed_questions, internal_contents, external_contents


def parse_rounds(rounds: dict):
    parsed_rounds = []
    external_contents = {}
    internal_contents = {}

    for round_index, _round in enumerate(rounds):
        round_name = _round['@name']
        themes = _round['themes']['theme']
        parsed_round = {'name': round_name,
                        'themes': []}
        for theme_index, theme in enumerate(themes):
            theme_name = theme['@name']
            if not theme_name:
                continue
            questions = theme['questions']['question']
            parsed_theme = {'name': theme_name,
                            'questions': []}
            parsed_round['themes'].append(parsed_theme)

            parsed_theme['questions'], theme_internal_contents, theme_external_contents = parse_questions(questions)
            external_contents = external_contents | theme_external_contents
            internal_contents = internal_contents | theme_internal_contents
        parsed_rounds.append(parsed_round)

    return parsed_rounds, internal_contents, external_contents