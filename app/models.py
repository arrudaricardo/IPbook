from app import db
from datetime import datetime

# one to one relationship


class Writer(db.Model):
    __tablename__ = 'writer'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(40), index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    email = db.Column(db.String(120))
    texts = db.relationship("Text", backref="author", lazy='dynamic')


class Text(db.Model):
    __tablename__ = 'text'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    writer_ip = db.Column(db.Integer, db.ForeignKey('writer.ip'))


def db_test_init():
    db.create_all()  # create db

    # fill the db test

    ip1 = Writer(ip='000.000.000.001')
    db.session.add(ip1)
    text1 = Text(text="Take this kiss upon the brow!")
    ip1.texts.append(text1)

    ip2 = Writer(ip='000.000.000.002')
    db.session.add(ip2)
    text2 = Text(text="And, in parting from you now,")
    ip2.texts.append(text2)

    ip3 = Writer(ip='000.000.000.003')
    db.session.add(ip3)
    text3 = Text(text="Thus much let me avow")
    ip3.texts.append(text3)

    ip4 = Writer(ip='000.000.000.004')
    db.session.add(ip4)
    text4 = Text(text="You are not wrong, who deem")
    ip4.texts.append(text4)

    ip5 = Writer(ip='000.000.000.005')
    db.session.add(ip5)
    text5 = Text(text="That my days have been a dream;")
    ip5.texts.append(text5)

    ip6 = Writer(ip='000.000.000.006')
    db.session.add(ip6)
    text6 = Text(text="Yet if hope has flown away")
    ip6.texts.append(text6)

    ip7 = Writer(ip='000.000.000.007')
    db.session.add(ip7)
    text7 = Text(text="In a night, or in a day,")
    ip7.texts.append(text7)

    ip8 = Writer(ip='000.000.000.008')
    db.session.add(ip8)
    text8 = Text(text="In a vision, or in none,")
    ip8.texts.append(text8)

    ip9 = Writer(ip='000.000.000.009')
    db.session.add(ip9)
    text9 = Text(text="Is it therefore the less gone?")
    ip9.texts.append(text9)

    ip10 = Writer(ip='000.000.000.0010')
    db.session.add(ip10)
    text10 = Text(text="All that we see or seem")
    ip10.texts.append(text10)

    ip11 = Writer(ip='000.000.000.0011')
    db.session.add(ip11)
    text11 = Text(text="Is but a dream within a dream.")
    ip11.texts.append(text11)

    ip12 = Writer(ip='000.000.000.0012')
    db.session.add(ip12)
    text12 = Text(text="I stand amid the roar")
    ip12.texts.append(text12)

    ip13 = Writer(ip='000.000.000.0013')
    db.session.add(ip13)
    text13 = Text(text="Of a surf-tormented shore,")
    ip13.texts.append(text13)

    ip14 = Writer(ip='000.000.000.0014')
    db.session.add(ip14)
    text14 = Text(text="And I hold within my hand")
    ip14.texts.append(text14)

    ip15 = Writer(ip='000.000.000.0015')
    db.session.add(ip15)
    text15 = Text(text="Grains of the golden sand")
    ip15.texts.append(text15)

    ip16 = Writer(ip='000.000.000.0016')
    db.session.add(ip16)
    text16 = Text(text="How few! yet how they creep")
    ip16.texts.append(text16)

    ip17 = Writer(ip='000.000.000.0017')
    db.session.add(ip17)
    text17 = Text(text="Through my fingers to the deep,")
    ip17.texts.append(text17)

    ip18 = Writer(ip='000.000.000.0018')
    db.session.add(ip18)
    text18 = Text(text="While I weep while I weep!")
    ip18.texts.append(text18)

    ip19 = Writer(ip='000.000.000.0019')
    db.session.add(ip19)
    text19 = Text(text="O God! Can I not grasp")
    ip19.texts.append(text19)

    ip20 = Writer(ip='000.000.000.0020')
    db.session.add(ip20)
    text20 = Text(text="Them with a tighter clasp?")
    ip20.texts.append(text20)

    ip21 = Writer(ip='000.000.000.0021')
    db.session.add(ip21)
    text21 = Text(text="O God! can I not save")
    ip21.texts.append(text21)

    ip22 = Writer(ip='000.000.000.0022')
    db.session.add(ip22)
    text22 = Text(text="One from the pitiless wave?")
    ip22.texts.append(text22)

    ip23 = Writer(ip='000.000.000.0023')
    db.session.add(ip23)
    text23 = Text(text="Is all that we see or seem")
    ip23.texts.append(text23)

    ip24 = Writer(ip='000.000.000.0024')
    db.session.add(ip24)
    text24 = Text(text="I have")
    ip24.texts.append(text24)

    ip25 = Writer(ip='000.000.000.0025')
    db.session.add(ip25)
    text25 = Text(text="all your power.")
    ip25.texts.append(text25)

    ip26 = Writer(ip='000.000.000.0026')
    db.session.add(ip26)
    text26 = Text(text="The end!")
    ip26.texts.append(text26)

    db.session.commit()


def db_harry_init():
    """ fill database with harry potter book """
    db.create_all()  # create db
    import pickle
    with open('harry', 'rb') as f:
        harry_list = pickle.load(f)
        for i in range(len(harry_list)):

            exec('ip' + str(i) + ' = Writer(ip="000.000.' + str(i) + '")')
            db.session.add(eval('ip' + str(i)))
            exec('text' + str(i) + ' = Text(text=harry_list[i])')
            exec('ip' + str(i) + '.texts.append(' + 'text' + str(i) + ')')

        db.session.commit()


def first_init():
    db.create_all()

    ip = Writer(ip='144.36.119.187')
    db.session.add(ip)
    text = Text(text="Some time ago")

    ip.texts.append(text)
    db.session.commit()
