from will.plugin import WillPlugin
from will.decorators import respond_to


class HelloPlugin(WillPlugin):
    @respond_to("hi")
    def say_hello(self, message):
        self.say("oh, hello!")
