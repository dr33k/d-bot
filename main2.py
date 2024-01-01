import re
import long_responses


def message_probability(user_message, recognised_words, n=1, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or n == 1:
        return int(percentage/100)
    else: return 0


def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, n=1, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, n, required_words)


def get_response(user_input):
    split_message = re.split(r'\s+|[,.:;?!-]\s*', user_input.lower())

    response = check_all_messages(split_message)


while True:
    print('Bot: '+get_response(input('You: ')))

