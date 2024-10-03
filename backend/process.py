class Slot:
    # inputs: day [string], time [string], duration [float]
    
    def __init__(self, day: str, time: str, duration: float) -> None:
        self.day = day
        self.time = time
        self.duration = duration
        self.students = [] # create students vector for each Slot
        self.selected = [] # create selected vector for each Slot that stores selected student(s)

    def student_names(self): # returns students vector
        available_names = [student.name for student in self.students]
        return available_names
    
    def selected_name(self): # returns selected vector
        selected_name_getter = [student.name for student in self.selected]
        return selected_name_getter

    def __repr__(self): # print the slot
        return f"Slot Day: {self.day}, Slot Time: {self.time}, Slot Duration: {self.duration} hours, Available Students: {self.student_names()}, Selected Student: {self.selected_name()}"


# slotter_function takes inputs student [Student], student_slots [list of the student's available time slots], day_slots [all slots in that day]
# appends student names to each slot they're available during in all days
def slotter_function(student, student_slots: list, day_slots: list):
    for student_slot in student_slots:
        for day_slot in day_slots:
            if student_slot == day_slot.time:
                day_slot.students.append(student)

# Student class
class Student:

    def __init__(self, name, id, des_hours, av_hours, monday_availability, tuesday_availability, wednesday_availability, thursday_availability, friday_availability, saturday_availability, sunday_availability) -> None:
        self.name = name
        self.id = id
        self._idh = float(des_hours) # total number of hours desired
        self.monday_availability = monday_availability
        self.tuesday_availability = tuesday_availability
        self.wednesday_availability = wednesday_availability
        self.thursday_availability = thursday_availability
        self.friday_availability = friday_availability
        self.saturday_availability = saturday_availability
        self.sunday_availability = sunday_availability
        self._iah = float(av_hours) # input number of hours available
        self.ratio = self.compute_ratio()
        self.total_hours = 0

    def __repr__(self): # print  
        return f"Student Name: {self.name}, Number of Hours Desired: {self._idh}, Number of Hours Available: {self._iah}, Monday Availability: {self.monday_availability}, Tuesday Availability: {self.tuesday_availability}, Wednesday Availability: {self.wednesday_availability}, Thursday Availability: {self.thursday_availability}, Friday Availability: {self.friday_availability}, Saturday Availability: {self.saturday_availability}, Sunday Availability: {self.sunday_availability}, Total Hours: {self.total_hours}, Ratio: {self.ratio}"
    
    def compute_ratio(self): # flexibility ratio is the individual's desired hours / their available hours -> how flexible are they?
        if self._iah <= 0 or self._idh <= 0:
            return 0
        else:
            value = self._idh / self._iah
            return round(value, 2)

    def set_idh(self, value): # set each student's desired, available, and total scheduled hours after they are scheduled to work a slot, re-compute and update the flexibility ratio
        self._idh = self._idh - value
        self._iah = self._iah - value
        self.total_hours = self.total_hours + value
        self.ratio = self.compute_ratio()


def employee_parser(employee_list, all_students, monday, tuesday, wednesday, thursday, friday, saturday, sunday):
    for employee in employee_list:
        student_name = employee.get("name")
        student_id = employee.get("id")
        student_des_hours = int(employee.get("desiredHours"))
        student_all_slots = [slot.strip() for slot in employee.get("slots").split(",")]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        student_slot_dict = {day: [] for day in days}
        student_av_hours = 0.0
        for slot in student_all_slots:
            if slot[-4:] == "7:00":
                student_av_hours += 3
            elif slot[-2:] == "30":
                student_av_hours += 2.5
            else:
                student_av_hours += 2
            for day in days:
                if slot.startswith(day):
                    student_slot_dict.get(day).append(slot[-11:])
        student = Student(student_name, student_id, student_des_hours, student_av_hours, student_slot_dict.get("Monday"), student_slot_dict.get("Tuesday"), student_slot_dict.get("Wednesday"), student_slot_dict.get("Thursday"), student_slot_dict.get("Friday"), student_slot_dict.get("Saturday"), student_slot_dict.get("Sunday"))
        all_students.append(student)
        slotter_function(student, student.monday_availability, monday) # add name to each day's slots
        slotter_function(student, student.tuesday_availability, tuesday)
        slotter_function(student, student.wednesday_availability, wednesday)
        slotter_function(student, student.thursday_availability, thursday)
        slotter_function(student, student.friday_availability, friday)
        slotter_function(student, student.saturday_availability, saturday)
        slotter_function(student, student.sunday_availability, sunday)
