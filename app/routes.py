from app import app, db
from flask import render_template, request, jsonify
from app.models import Text, Writer
from random import randint
from datetime import datetime
import re
import os

# config
data_fmt = "%Y-%m-%d %H:%M:%S.%f"  # db timestamp time format
item_per_page = 12  # number of Text delivered per request(page)
min_post_interval = 12  # minimun time between submission in hours
dev = False  # no ip restriction; random ip assigment
max_length = 20  # maximum number of char per text posted
book_max_post = 500   # maximum number of post til finish the book


def load_words():
    """ load eng_words file"""

    file_dir = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'words.txt')
    with open(file_dir, 'r') as f:
        valid_words = set(f.read().split())
    return valid_words


eng_words = load_words()


def finish_perc():
    """Get percetage of book finished"""
    posts = Text.query.count()
    return round((posts / book_max_post) * 100)


@app.route('/')
def index():
    return render_template('main.html', finish_perc=finish_perc(),
                           max_length=max_length, min_post_interval=min_post_interval,
                           book_max_post=book_max_post, item_per_page=item_per_page)


@app.route('/getBookText', methods=['POST'])
def getBookText():
    page = int(request.form['page'])
    ip = str(request.remote_addr)
    lastTextID = request.form['lastTextID']
    last_text_id = Text.query.order_by(
        Text.id.desc()).first()  # get last text submited

    try:
        lastTextID = int(lastTextID)
    except ValueError:
        pass

    # first request ( page ==1 ) or not sync (user lastBookId not updated)
    if page == 1 or lastTextID != last_text_id.id:
        page = 1
        # paginated text.ids by old to newer
        book_text = Text.query.order_by(Text.id.desc()).paginate(
            page, item_per_page, False).items

        if book_text != []:  # has Texts in database

            txts = []
            for i in book_text:
                text_list = [i.id, i.text, i.writer_ip, i.timestamp]
                txts.append(text_list)

            return jsonify(result=txts, last_text_id=last_text_id.id, page=page, max_length=max_length)

        else:  # has no more item in page (has no Text in db)

            return jsonify(result='no text in book', last_text_id=last_text_id.id, page=0, max_length=max_length)

    # server last page is iqual to user last page and not first request (page==1)
    else:
        book_text = Text.query.order_by(Text.id.desc()).paginate(
            page, item_per_page, False).items

        if book_text != []:  # has item in page

            txts = []
            for i in book_text:
                text_list = [i.id, i.text, i.writer_ip, i.timestamp]
                txts.append(text_list)

            return jsonify(result=txts, last_text_id=last_text_id.id, page=page, max_length=max_length)

        else:

            return jsonify(result='no more text in book', last_text_id=last_text_id.id, page=0, max_length=max_length)


# user submit a new text in the book
@app.route('/postBookText', methods=['POST'])
def postBookText():

    # check if book is finished
    if finish_perc() >= 100:
        return jsonify(result='6', error='The Book is finish!')

    # text post by user
    text = request.form['txt']

    # check text length
    if len(text) > max_length:
        return jsonify(result='0', error='len > {}'.format(max_length))

    # check if text is chars or ,,!?-\n
    char = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!?.,\' "')
    if not any((i in char) for i in text):
        return jsonify(result='4', error='unauthorized char')

    # double space check
    double_space = re.match(r'^((?!\s{2}).)*$', text)
    if double_space is None:
        return jsonify(result='6', error='Double Space, please check')

    # check if is the last text posted
    lastTextID = int(request.form['lastTextID'])
    last_text_id = Text.query.order_by(
        Text.id.desc()).first()  # get last text submited

    if last_text_id.id != lastTextID:
        # A new text was posted in this location id.
        return jsonify(result='2', error='Someone posted in that location', last_text_id=last_text_id.id)

    # check if words are valid english word
    # remove pontuation and split words
    words = re.sub('\!|\?|\.|\,|\-|\"', '', text).lower().split()

    if words == []:
        # just space no words
        return jsonify(result='6', error='Empty field')

    words_not_valid = []
    for word in words:
        if word not in eng_words:
            words_not_valid.append(word)
    if words_not_valid != []:
        return jsonify(result='5', error='Not valid english word', words=words_not_valid)

    # get IP
    if dev is True:
        ip = (str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + '.' + str(randint(0, 9)) +
              str(randint(0, 9)) + str(randint(0, 9)) + '.' + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)))
    else:
        ip = request.headers['X-Real-IP']

    post_writer = Writer.query.filter(Writer.ip == ip).first()

    # remove space trailling
    text = text.strip()

    # if user not in db
    if post_writer is None:

        # create user and save in db
        writer = Writer(ip=ip)
        db.session.add(writer)

        # save post in db
        post_text = Text(text=text)
        writer.texts.append(post_text)
        db.session.commit()

        return jsonify(result='1', error='success')  # no erros

    # if user exist
    else:

        # check last post timestamp
        last_text_timestamp = post_writer.texts.all(
        )[-1].timestamp  # get last text's timestamp

        duration = datetime.utcnow() - last_text_timestamp
        # get time last submiting in hours
        last_text_post = duration.total_seconds() // 3600

        if last_text_post > min_post_interval:  # if last user's post time >  min post

            post_text = Text(text=text)
            post_writer.texts.append(post_text)
            db.session.commit()

            return jsonify(result='1', error='success')  # no erros

        else:
            # if user submited not in the min_post_interval range
            return jsonify(result='3', error='Can only submit every {} hours'.format(min_post_interval), min_post_interval=min_post_interval, reset=last_text_post - min_post_interval)


@app.route('/lastTextID', methods=['POST'])
def lastTextID():
    last_text_id = Text.query.order_by(Text.id.desc()).first()
    return jsonify(result=last_text_id.id)


@app.route('/postEmail', methods=['POST'])
def postEmail():
    email = request.form['email']
    email_re = re.match(
        r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)

    if email_re is None:
        return jsonify(result='0')  # not valid e-mail

    # get IP
    if dev is True:
        ip = (str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + '.' + str(randint(0, 9)) +
              str(randint(0, 9)) + str(randint(0, 9)) + '.' + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)))
    else:
        ip = request.headers['X-Real-IP']

    user = Writer.query.filter(Writer.ip == ip).first()

    if user is None:
        # create a new user
        writer = Writer(ip=ip, email=email)
        db.session.add(writer)
    else:
        user.email = email

    db.session.commit()
    return jsonify(result='1')  # successfully added
