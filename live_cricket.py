import requests
from pycricbuzz import Cricbuzz
import json
import time
from datetime import datetime
from win10toast import ToastNotifier
import argparse

IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/<IFTTT KEY>'


def post_ifttt_webhook(event, value):

    data = {'value1': value}  # The payload that will be sent to IFTTT service
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)  # Inserts our desired event
    # Sends a HTTP POST request to the webhook URL
    print str(datetime.now().time()) + ' : ' + str(requests.post(ifttt_event_url, json=data))


def notify_desktop(value):
    toaster = ToastNotifier()
    toaster.show_toast("Ipl 2018 Update", value, duration=10)


def get_score(cricbuzz, match, tournament, match_status=None):
    result = []
    if match['srs'] == tournament:
        live_match = cricbuzz.livescore(match['id'])
        matchInfo = live_match['matchinfo']
        result.append(matchInfo['mchdesc']+' ('+matchInfo['mchstate']+')')
        result.append(matchInfo['status'])

        if live_match.has_key('batting'):

            batting = live_match['batting']
            score = batting['score'][0]
            result.append(batting['team'] + " : "+score['runs']+"/" +
                          score['wickets']+" ("+score['overs']+")")
            batsmen = batting['batsman']
            batsmen_stats = ''
            for batsman in batsmen:
                batsmen_stats += batsman['name']+" : "+batsman['runs']+"("+batsman['balls']+")  "
            result.append(batsmen_stats)

            bowling = live_match['bowling']
            bowlers = bowling['bowler']
            bowler_stats = ''
            for bowler in bowlers:
                bowler_stats += bowler['name']+' : '+bowler['overs']+"-" + \
                    bowler['maidens']+'-'+bowler['runs']+'-'+bowler['wickets']+'  '
            result.append(bowler_stats)

            if bowling.has_key('score') and len(bowling['score']) > 0:
                score = bowling['score'][0]
                result.append(bowling['team']+' : '+score['runs']+'/' +
                              score['wickets']+' ('+score['overs']+')')

        return '\n'.join(result)
    return None


def send_updates(tournament, desktop_notification):
    while True:
        cricbuzz = Cricbuzz()
        matches = cricbuzz.matches()
        for match in matches:
            result = get_score(cricbuzz, match, tournament)
            if result:
                post_ifttt_webhook('cricket_info', result)
                if desktop_notification:
                    notify_desktop(result)
        print '-'*20
        time.sleep(600)


if __name__ == '__main__':

    desktop_notification = False

    parser = argparse.ArgumentParser()
    parser.add_argument('--desktop', help='set this to true to enable Desktop Notification')

    args = parser.parse_args()

    if args.desktop and args.desktop.lower() == 'true':
        desktop_notification = True

    send_updates('Indian Premier League, 2018', desktop_notification)
