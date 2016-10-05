__author__ = 'owais'
from will.plugin import WillPlugin
from will.decorators import respond_to
from will.decorators import hear
from will.decorators import periodic
from will.decorators import rendered_template
from will import settings
import requests


class CustomPluginBot(WillPlugin):
    @hear("who are you")
    def hear_who_are_you(self, message):
        self.say("I am a Bot", message=message)

    @respond_to("who are you")
    def hear_who_are_you_wr(self, message):
        self.say("I am a Bot")

    @hear("Are you a Bot")
    def hear_are_you(self, message):
        self.say("Yes I am a Bot", message=message)

    @respond_to("Are you a Bot")
    def hear_are_you_wr(self, message):
        self.say("Yes I am a Bot")

    @periodic(hour='13', minute='00')
    def schedule_1300_message(self):
        context = group_stats()
        self.say("@all Group Stats", notify=True, color='green')
        self.say(rendered_template("group_stats.html", context), notify=True,
                 color='green', html=True)

    @periodic(hour='5', minute='00')
    def schedule_1400_message(self):
        context = group_stats()
        self.say("@all Group Stats", notify=True, color='green')
        self.say(rendered_template("group_stats.html", context), notify=True,
                 color='green', html=True)


class Fitbot(WillPlugin):
    @respond_to("group stats")
    def group_stats(self, message):
        context = group_stats()
        self.say("@all Group Stats", notify=True, color='green')
        self.say(rendered_template("group_stats.html", context), notify=True,
                 color='green', html=True)

    @respond_to("group users")
    def group_users(self, message):
        response = requests.get(
            settings.FIT_BOT_URL + 'get_group_users/1/')
        data = response.json()
        userlist = data.get('userlist', '')
        context = {"userlist": userlist}
        self.say(rendered_template("group_users.html", context), message, html=True)

    @respond_to("stats (?P<user_name>.*)$")
    def getuser(self, message, user_name):
        response = requests.get(
            settings.FIT_BOT_URL + 'get_group_user/?username={0}'.format(user_name))
        data = response.json()
        calories = data.get('calories', '0.00')
        steps = data.get('steps', '0.00')
        weight = data.get('weight', '0.00')
        sleep = data.get('sleep', '0.00')
        try:
            calories = int(float(calories))
            steps = int(float(steps))
            weight = int(float(weight))
            sleep = int(float(sleep))
        except Exception as e:
            pass
        context = {"calories": calories,
                   "steps": steps,
                   "weight": weight,
                   "sleep": sleep
                   }
        self.say(rendered_template("group_user.html", context), message, html=True)

    @respond_to("send email to (?P<email>.*)$")
    def sendemail(self, message, email):
        response = requests.get(
            settings.FIT_BOT_URL + 'get_group_users/1/')
        data = response.json()
        userlist = data.get('userlist', '')
        context = {"userlist": userlist}
        self.send_email(from_email='fitbot@ai.info.au', email_list=[email],
                        subject="Here's the latest report from Fitbot",
                        message=rendered_template("group_users.html", context))


def group_stats():
    url = settings.FIT_BOT_URL + 'get_stats_group/' + str(settings.FITBOT_GROUP) + '/'
    response = requests.get(url=url)
    data = response.json()
    calories = data.get('calories', '0.00')
    steps = data.get('steps', '0.00')
    weight = data.get('weight', '0.00')
    sleep = data.get('sleep', '0.00')
    try:
        calories = int(float(calories))
        steps = int(float(steps))
        weight = int(float(weight))
        sleep = int(float(sleep))
    except Exception as e:
        pass
    context = {"calories": calories,
               "steps": steps,
               "weight": weight,
               "sleep": sleep}
    return context
