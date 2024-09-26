import os

from dotenv import load_dotenv
import urllib.parse
import urllib.request
import json

load_dotenv()
match_match_url = os.environ.get('MATCH_MATCH_URL')
slack_url = os.environ.get('SLACK_URL')
id = os.environ.get('id')


def process():
    data = {'idx': id}
    json_data = call(data)
    print(json_data)

    if not json_data:
        slack_fail_call()

    count = calc_position_counting(json_data)
    slack_call({'text': 'success', 'message': count})


def call(data: dict) -> dict:
    payload = urllib.parse.urlencode(data).encode('utf-8')
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # POST 요청 보내기
    req = urllib.request.Request(url=match_match_url, data=payload, headers=headers)
    with urllib.request.urlopen(req) as response:
        # 응답 데이터 읽기 및 JSON 변환
        result = response.read().decode('utf-8')
        print('response Status Is', response.code, response.reason)
        return json.loads(result)


def calc_position_counting(json_data: dict) -> int:
    a_team_text = json_data['gameMap']['position_end_team_a']
    b_team_text = json_data['gameMap']['position_end_team_b']
    disable_position_count = count_by_team_text(a_team_text) + count_by_team_text(b_team_text)
    players = json_data['gamePlayerMapList']
    player_count = len(players)

    print('disable Position count Is {}'.format(disable_position_count))
    print('Player Count Is {}'.format(player_count))
    return disable_position_count + player_count


def count_by_team_text(text: str) -> int:
    return text.count('Y')


def slack_fail_call():
    slack_call({'text': 'fail', 'message': ''})


def slack_call(data: dict):
    headers = {'Content-Type': 'application/json'}
    payload = {
        'channel': '# 알림',
        'text': '{} {}'.format(data['text'], data['message'])
    }
    data = json.dumps(payload).encode('utf-8')
    print(data)
    req = urllib.request.Request(url=slack_url, data=data, headers=headers)

    with urllib.request.urlopen(req) as response:
        # 응답 데이터 읽기 및 JSON 변환
        print('Call Slack API')


process()
