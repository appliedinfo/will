import requests

__author__ = 'owais'
from will.plugin import WillPlugin
from will.decorators import respond_to, hear, periodic, rendered_template


class CustomPluginBot(WillPlugin):
    # @hear("who are you")
    # def hear_who_are_you(self, message):
    #     self.say("I am a Bot", message=message)

    @respond_to("who are you")
    def hear_who_are_you_wr(self, message):
        self.say("I am a Bot")

    # @hear("^mahraaz$")
    # def hear_mahraaz(self, message):
    #     self.say("In search of Maharin ...", message=message)

    # @respond_to("^mahraaz$")
    # def hear_mahraaz_wr(self, message):
    #     self.say("In search of Maharin ...")

    @hear("Are you a Bot")
    def hear_are_you(self, message):
        self.say("Yes I am a Bot", message=message)

    @respond_to("Are you a Bot")
    def hear_are_you_wr(self, message):
        self.say("Yes I am a Bot")

    @respond_to("^awo owais activity$")
    def hear_awo(self, message):
        import requests
        response = requests.get(
            'http://awo.ainfo.io:8888/api/users/5/?range=&source=activity&project=DXAPI&user=5&_=1470393472680')
        data = response.json()
        activities = data.get('activities', [])
        activity_text = ''
        for activity in activities:
            activity_text += "\n"
            activity_text += str(activity['category']) + " " + str(activity['estimated_time']) \
                             + " " + str(activity['actual_time']) \
                             + str(activity['project']) + " " + str(activity['task_name'])

        self.say(activity_text, message=message)

    @periodic(hour='12', minute='55', day_of_week="mon-fri")
    def schedule_message(self):
        response = requests.get(
            'http://127.0.0.1:8000/get_stats_group/1/')
        self.say("@owais " + str(response.json()), notify=True, color='red')


class Fitbot(WillPlugin):
    @respond_to("group stats")
    def group_stats(self, message):
        response = requests.get(
            'http://127.0.0.1:8000/get_stats_group/1/')
        data = response.json()
        calories = data.get('calories', '')
        steps = data.get('steps', '')
        weight = data.get('weight', '')
        sleep = data.get('sleep', '')
        context = {"calories": calories,
                   "steps": steps,
                   "weight": weight,
                   "sleep": sleep}

        card_data = {"style": "application", "url": "https://www.application.com/an-object", "format": "medium",
                     "id": "db797a68-0aff-4ae8-83fc-2e72dbb1a707", "title": "GroupStatistics",
                     "description": "GroupstaticsbasesontotalSleep\ntotalcalories",
                     "icon": {"url": "http://bit.ly/1S9Z5dF"},
                     "attributes": [{"label": "calories", "value": {"label": calories}}, {"label": "steps", "value": {
                         "icon": {"url": "http://bit.ly/1S9Z5dF"}, "label": steps, "style": "lozenge-complete"}},
                                    {"label": "Avgweight",
                                     "value": {"icon": {"url": "http://bit.ly/1S9Z5dF"}, "label": weight,
                                               "style": "lozenge-complete"}}, {"label": "sleep", "value": {
                             "icon": {"url": "http://bit.ly/1S9Z5dF"}, "label": sleep, "style": "lozenge-complete"}}]}
        # self.say(message, html=True, card=json.dumps(card_data), notify=True)
        # self.say(html_body, notify=True, html=True, color='random')
        self.say(rendered_template("group_stats.html", context), message, html=True)

    @respond_to("group users")
    def group_users(self, message):
        response = requests.get(
            'http://127.0.0.1:8000/get_group_users/1/')
        data = response.json()
        userlist = data.get('userlist', '')
        context = {"userlist": userlist}

        # card_data={"style":"application","url":"https://www.application.com/an-object","format":"medium","id":"db797a68-0aff-4ae8-83fc-2e72dbb1a707","title":"GroupStatistics","description":"GroupstaticsbasesontotalSleep\ntotalcalories","icon":{"url":"http://bit.ly/1S9Z5dF"},"attributes":[{"label":"calories","value":{"label":calories}},{"label":"steps","value":{"icon":{"url":"http://bit.ly/1S9Z5dF"},"label":steps,"style":"lozenge-complete"}},{"label":"Avgweight","value":{"icon":{"url":"http://bit.ly/1S9Z5dF"},"label":weight,"style":"lozenge-complete"}},{"label":"sleep","value":{"icon":{"url":"http://bit.ly/1S9Z5dF"},"label":sleep,"style":"lozenge-complete"}}]}
        # self.say(message, html=True, card=json.dumps(card_data), notify=True)
        # self.say(html_body, notify=True, html=True, color='random')
        self.say(rendered_template("group_users.html", context), message, html=True)

    @respond_to("stats (?P<user_name>.*)$")
    def getuser(self, message, user_name):
        response = requests.get(
            'http://127.0.0.1:8000/get_group_user/?username={0}'.format(user_name))
        data = response.json()
        username = data.get('username', '')
        id = data.get('id', '')
        email = data.get('email', '')
        context = {"username": username,
                   "id": id,
                   "email": email,
                   }
        self.say(rendered_template("group_user.html", context), message, html=True)
