import json
from difflib import get_close_matches
import random

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def append_knowledge_base(file_path, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, fp=file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict):
    if question:
        for q in knowledge_base['questions']:
            if q['question'] == question:
                return q['answer']


    # replies = [
    #         'Apologies, I don\'nt know much about that, could you try rephrasing?',
    #         'I don\'t seem to have access to that information, sorry, could you try asking me something else ?'
    #         'I might look all sophisticated but I haven\'t been trainded to respond to this, could you try something else please ?'
    # ]
    return 'Bot: Apologies, I don\'t seem to have that information, could you teach me ?'

def chat_bot():
    knowledge_base: dict = load_knowledge_base('json/knowledge_base.json')

    user_input: str

    while True:
        user_question = input('You: ')

        if user_question.lower == 'quit':
            break

        best_match: str = find_best_match(user_question, [q['question'] for q in knowledge_base['questions']])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            best_answer = get_answer_for_question(best_match, knowledge_base)
            print(best_answer)
            user_answer = input('Give me an answer or type \'skip\' to skip')

            if user_answer != 'skip':
                knowledge_base['questions'].append({'question': user_question, 'answer': user_answer})
                append_knowledge_base('json/knowledge_base.json', knowledge_base)
                print('Thank you')


if __name__ == '__main__':
    chat_bot()