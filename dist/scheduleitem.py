"""
Module Containing a Single Class: ScheduleItem
"""
from bs4 import BeautifulSoup
from utils import get_days


class ScheduleItem():
    """
    Object Representing a Single Element of a timetable
    Attributes:
        day_number: in [1,2,3,4,5]
        day_string in ["Monday",Tuesday....]
        duration_hours in [1,2...] (usually 1 or 2)
        hour_range: e.g. item at 11pm for 2 hours have hour range [11,12]
        lecturer: e.g. "Professor X"
        module_code: e.g. "COMP1234"
        module_number: Integer mostly used for module ordering
        room: e.g. "E216A"
        schedule_title: e.g. "Theory of Computation Lecture"
        schedule_type: e.g. Usually LECT or TUT
        time_hour: in [1...7] (representing 9am to 5pm start times
        time_string: Printable Representation of time, e.g. 18:00
        uid [day_string, time_string,
            module_name, schedule_type ]
        weeks: list of weeks the item is on, e.g. if the item runs
            from weeks 11-20, then weeks = [11,12,.....20]
    """

    def __init__(self, day_number, time_hour, duration_hours, data, module_list):
        """
        day_number: integer, in [1,2,3,4,5]
        """

        self.day_number = day_number
        self.day_string = get_days()[self.day_number]
        self.time_hour = int(time_hour - 8)
        self.time_string = self.parse_time_string(time_hour)
        self.duration_hours = duration_hours
        self.hour_range = range(self.time_hour, self.time_hour + self.duration_hours)
        table_entries = data.findAll('td')
        """
        Parsing table_entries list:
        ->P:Find by array position
        ->C:Find by font color
        ____________________________
        P:Red:ModuleCode/ScheduleType
        P:Blue: ???
        P:Black:Module Title

        C:Black:Week Numbers
        C:Green:Lecturer
        C:Brown: Room Numbers
        ____________________________
        """
        # Entry 1 - Module Code and Schedule Type
        module_data = table_entries[0].string.split("/")
        self.module_code = module_data[0]
        self.module_number = module_list.index(self.module_code)
        self.schedule_type = self.set_schedule_type(module_data[1])

        # Entry 2 - irrelevant

        # Entry 3 - Schedule Title
        self.schedule_title = self.parse_schedule_title(table_entries[2].string)

        # Entries 4,5,6 - by Colour
        # Weeks   : #000000
        # Lecturer: #00FF00
        # Room    : #800000
        for table_entry in table_entries[3:]:
            table_entry = BeautifulSoup(str(table_entry))
            font_attributes = table_entry.findAll('font')[0].attrs
            font_color = font_attributes['color']
            if font_color == "#000000":
                self.weeks = self.parse_weeks(table_entry.string)
            elif font_color == "#00FF00":
                self.lecturer = table_entry.string
            elif font_color == "#800000":
                self.room = table_entry.string

        """
        Schedule items are equivalent if they occur:
            On the same day,
            at the same time,
            on the same week,
            with the same module,
            and the same type of module item

            Therefore these attributes uniquely define
            a Schedule Item
        """

        self.uid = self.uid = [
            self.day_string,
            self.time_string,
            self.weeks,
            self.module_code,
            self.schedule_type,
        ]

    @staticmethod
    def parse_weeks(week_string):
        """
        Takes a string of form "11-20,21-30" and
        return a list of form [11,12...20,21....30]
        """
        week_numbers = week_string.split(",")
        for week_index in range(len(week_numbers)):
            try:
                week_numbers[week_index] = [int(x) for x in week_numbers[week_index].split("-")]
            except Exception, exception:
                raw_input("")
                raise exception
            if len(week_numbers[week_index]) > 1:
                week_numbers[week_index] = [x for x in
                                            range(week_numbers[week_index][0], week_numbers[week_index][1] + 1)]
        weeks = []
        for week_number in week_numbers:
            weeks += week_number
        return weeks

    @staticmethod
    def parse_schedule_title(schedule_title):
        """
        Takes a string defining the schedule title and standardises it
        e.g. "Tutorial A" -> "Tutorial"
        """
        schedule_title.replace("Tutorial A", "Tutorial")
        return schedule_title

    @staticmethod
    def parse_time_string(time):
        """
        Converts integer time to String representation
        e.g. 8.25 -> "8:15"
        """
        minutes = str(int((time - int(time))*3/5))
        return str(int(time)) + ":" + "0" * (2 - len(minutes)) + minutes
    @staticmethod
    def set_schedule_type(schedule_type):
        """
        Takes a string defining the type of schedule item and standardises it
        e.g. "LEC" -> "LECT"
        """
        if 'TUT' in schedule_type:
            schedule_type = 'TUT'
        if schedule_type in ['LECT', 'LEC', 'PROB', 'ADD']:
            schedule_type = 'LECT'
        return schedule_type

    def to_string(self):
        """
        Returns a string representation of the uid
        """
        return ", ".join([str(x) for x in self.uid])

    def __eq__(self, other):
        """
        Checks for equality with another object
        Objects are equal if they have the same hash value
        """
        try:
            if self.__hash__() == other.__hash__():
                return True
            return False
        except Exception, exception:
            print str(exception)
            return False

    def __hash__(self):
        """
        Returns a integer determined by the uid list
        converts the list into a integer uniquely defined by its uid
        """
        hash_number_string = "".join([str(ord(x)) for x in str(self.uid)])
        return int(hash_number_string)

    def clash(self, x):
        """
        Determines whether to ScheduleItems clash:
        Checks for intersection of their hours and weeks
        """
        if self != x:
            if self.day_number == x.day_number:
                if len(set(self.hour_range) & set(x.hour_range)) != 0 and len(set(self.weeks) & set(x.weeks)) != 0:
                    return set(self.weeks) & set(x.weeks)
        return None

