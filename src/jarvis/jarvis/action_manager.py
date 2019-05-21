import re
import subprocess
import wikipedia
import logging
from pyowm import OWM
from datetime import datetime

from jarvis.settings import TRIGGERING_WORDS, WEATHER_API
from jarvis.assistant_utils import assistant_response


class ActionManager:

    @classmethod
    def open_website_in_browser(cls, words):
        """
        Opens a web page in the browser.
        :param words: string (e.g Open the site youtube)
        """
        reg_ex = re.search(TRIGGERING_WORDS['open_browser'] + ' ([a-zA-Z]+)', words)
        if reg_ex:
            domain = reg_ex.group(1)
            assistant_response('Yes sir, I will open the {0}'.format(domain))
            url = cls._create_url(domain)
            subprocess.Popen(["python", "-m",  "webbrowser",  "-t",  url], stdout=subprocess.PIPE)
        else:
            pass

    @classmethod
    def _create_url(cls, domain):
        """
        Creates a url. It checks if there is .com suffix and add it if it not exist.
        :param domain: string (e.g youtube)
        :return: string (e.g http://www.youtube.com)
        """
        if re.search('.com', domain):
            url = 'http://www.' + domain
        else:
            url = 'http://www.' + domain + '.com'
        return url

    @classmethod
    def tell_the_weather(cls, words):
        """
        Tells the weather of a place
        :param words: string (e.g weather in London)
        """
        reg_ex = re.search('weather in (.*)', words)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key=WEATHER_API['key'])
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(WEATHER_API['unit'])
            assistant_response('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum '
                               'temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))

    @classmethod
    def tell_the_time(cls, *args):
        """
        Tells ths current time
        """
        now = datetime.now()
        assistant_response('Current time is: {0}:{1}'.format(now.hour, now.minute))

    @classmethod
    def tell_me_about(cls, words):
        """
        Tells about something by searching in wikipedia
        :param words: string (e.g about google)
        """
        reg_ex = re.search('about (.*)', words)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                assistant_response(ny.content[:500].encode('utf-8'))
        except Exception as e:
            logging.error(e)