from flask import Flask, session, render_template, request
from operator import itemgetter
import time as t
import random
import pickle


'''
Author: Roger Marciniak
Student#: C00169733
Program: WordGame
'''


app = Flask(__name__)


# check if word is made up of letters contained in source word
def containsAll(s_word, word):
    s_charlist = list(s_word)

    for c in word:
        if c in s_charlist:
            s_charlist.remove(c)
        else:
            return False
    return True


# check if word is an actual word from the dictionary
def isInDictionary(candidate):
    with open('acceptable_words.txt', 'r') as f:
        for line in f:
            if candidate in line.lower():
                return True
    return False


@app.route('/')
def begin_challenge():
    session['source_word'] = random.choice(
        list(open("source_words.txt"))).lower().strip()
    session['start_time'] = t.time()
    return render_template('challenge_form.html',
                           title='Game of Words',
                           header='Game of Words')


@app.route('/processform', methods=['POST'])
def process_form():
    session['score'] = round((t.time() - session['start_time']), 2)
    data = []
    invalid = []

    for k, v in request.form.items():
        v_low = v.lower()
        if (len(v_low) > 2 and
            v_low != session['source_word'] and
            v_low not in data and
            containsAll(session['source_word'], v_low) and
                isInDictionary(v_low)):
            data.append(v_low)
        else:
            invalid.append(v_low)

    if len(data) == 7:
        return render_template('results_form.html',
                               title='Game of Words|Results',
                               header='Your Results',
                               data=data)

    else:
        return render_template('results_error_form.html',
                               title='Game of Words|Results',
                               header='Your Results',
                               invalid=invalid)


@app.route('/topscorers', methods=['POST'])
def top_scorers():
    uname = request.form['name']
    score_list = []

    score_list = pickle.load(open('topscorers.p', 'rb'))

    score_list.append((uname, session['score']))
    score_list = sorted(score_list, key=itemgetter(1))
    score_top10 = score_list[:10]
    for index, item in enumerate(score_list):
        if item == (uname, session['score']):
            current_index = index + 1

    if current_index > 10:
        current_index = str(current_index)
        message = ' '.join(['Your ranking position:',
                            current_index,
                            'with score of:',
				str(session['score'])])
    else:
        message = "You've made it to the hall of fame!"

    pickle.dump(score_list, open('topscorers.p', 'wb'))

    return render_template('topscorers_form.html',
                           title='Game of Words|Hall of Fame',
                           header='Hall of Fame',
                           score_top10=score_top10,
                           message=message)


@app.errorhandler(404)
def fourOhFour(error):
    return '404: You have wandered too far young adventurer!'


app.secret_key = 'yVQa{ZWKZmCzJ.H/Q7R<je+7y@UwD"?5'


if __name__ == '__main__':
    app.run(debug=True)

