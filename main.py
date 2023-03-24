import webuntis
import requests
import pytz


class WebUntis:
    def __init__(self, username, password, school=None, server=None, port=None, school_id=None, url=None):

        """"
        :param username: Username
        :param password: Password
        Give either school, server, port, school_id
        :param school: School name
        :param server: Server name
        :param port: Port
        :param school_id: School ID
        or url
        :param url: Login URL to the webuntis page of your school
        """

        self._username = username
        self._password = password
        self._port = "8080" if not port else port

        if school and server and school_id:
            self._school = school
            self._server = server
            self._school_id = school_id
        elif not url:
            raise Exception("No school, server, school_id or login url given")
        else:
            self._url = url
            self._server, self._school, self._school_id = self._get_info_from_login_url()

        self._session = webuntis.Session(username=self._username, password=self._password, server=self._server, school=self._school, useragent='Untis to Google Calendar')
        self._session.login()

    @property
    def classes(self):
        return [x for x in self._session.klassen()]

    @property
    def teachers(self):
        return [x for x in self._session.teachers()]

    @property
    def rooms(self):
        return [x for x in self._session.rooms()]

    @property
    def holidays(self):
        return [x for x in self._session.holidays()]

    def _get_timetable_raw(self, klasse, start_date, end_date):
        if type(klasse) is str:
            try:
                klasse = [k for k in self._session.klassen() if k.name.removeprefix("0") == klasse or k.name == klasse][0].id
            except IndexError:
                raise Exception(f"Class {klasse} not found")
        return self._session.timetable(klasse=klasse, start=start_date, end=end_date)

    def _get_info_from_login_url(self):
        server = self._url.split("/")[2]
        school = self._url.split("/")[4].removeprefix("?school=").removesuffix("#")

        school_name = requests.get(self._url).cookies.get("schoolname")

        return server, school, school_name

    def get_timetable(self, klasse, start_date, end_date):
        if type(klasse) is str:
            for k in self._session.klassen():
                if k.name == klasse:
                    klasse = k.id
                    break

        time_table_raw = list(self._get_timetable_raw(klasse=klasse, start_date=start_date, end_date=end_date))
        time_table = []
        tz = pytz.timezone("Europe/Berlin")
        new_tz = pytz.timezone("GMT")

        """
        {
                "state": l.code,
                "start": tz.localize(l.start).astimezone(new_tz),
                "end": tz.localize(l.end).astimezone(new_tz),
                "id": l.id,
                "subject": {"name": l.subjects._data[0].name, "longname": l.subjects._data[0].long_name} if l.subjects._data else None,
                "classes": l.klassen,
                "rooms": l.rooms
            }
        """

        for l in time_table_raw:
            time_table.append(
                Lesson(
                    name=l.subjects[0].name if l.subjects._data else None,
                    longname=l.subjects[0].long_name if l.subjects._data else None,
                    state=l.code,
                    start=tz.localize(l.start).astimezone(new_tz),
                    end=tz.localize(l.end).astimezone(new_tz),
                    id=l.id,
                    classes=l.klassen,
                    rooms=l.rooms
                )
            )
        return time_table

    def get_time_table_by_subjects(self, klasse, start, end, subjects):  # filter by subjects
        time_table = self.get_timetable(klasse, start, end)
        # remove from time_table if subject not in subjects
        time_table_filtered = [l for l in time_table if l["subject"] and l["subject"]["name"] in subjects]
        return time_table_filtered


class Lesson:
    def __init__(self, name, longname, id, start, end, state, classes, rooms):
        self.name = name
        self.longname = longname
        self.id = id
        self.start = start
        self.end = end
        self.state = state
        self.classes = classes
        self.rooms = rooms

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
