import json
from datetime import datetime
import requests
from pprint import pprint


class Lolesports_API:
    API_KEY = {"x-api-key": "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"}
    API_URL = "https://esports-api.lolesports.com/persisted/gw"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.API_KEY)

    def get_leagues(self, hl="en-US"):
        response = self.session.get(self.API_URL + "/getLeagues", params={"hl": hl})
        return json.loads(response.text)["data"]

    def get_schedule(self, hl="en-US", league_id=None, pageToken=None):
        response = self.session.get(
            self.API_URL + "/getSchedule",
            params={"hl": hl, "leagueId": league_id, "pageToken": pageToken},
        )

        return json.loads(response.text)["data"]


def schedule_return():
    api = Lolesports_API()
    lck_id = "98767991310872058"
    lpl_id = "98767991314006698"
    schedule_now = api.get_schedule(league_id=[int(lck_id)])["schedule"]
    newer_page_id = schedule_now["pages"]["newer"]
    schedule_newer = api.get_schedule(league_id=[int(lck_id)], pageToken=newer_page_id)[
        "schedule"
    ]["events"]
    all_schedule = schedule_now["events"] + schedule_newer

    final_games_total = []
    for i in all_schedule:
        if int(i["startTime"][:4]) >= 2022:
            team = i["match"]["teams"]
            year, month, day = i["startTime"][:10].split("-")
            hour, minute = i["startTime"][11:16].split(":")
            checker = i["startTime"].replace("T", "-")[:-1]
            # print(checker)
            record = [
                team[0]["name"],
                team[1]["name"],
                year,
                month,
                day,
                hour,
                minute,
                checker,
            ]

            final_games_total.append(record)
            result = sorted(
                final_games_total,
                key=lambda date: datetime.strptime(date[-1], "%Y-%m-%d-%H:%M:%S"),
            )
            # print(result)
            pass
    # pprint(schedule_newer)
    # pprint(type(schedule_now))
    return result
