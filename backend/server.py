from flask import Flask, request
from flask_cors import CORS
import process

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/generate", methods=['POST'])
def generate_schedule():
    data = request.get_json()

    # create the week: each day is saved as a process.Slot class object
    monday = [process.Slot("monday", "10:00-12:00", 2), process.Slot("monday", "12:00-14:00", 2), process.Slot("monday", "14:00-16:00", 2), process.Slot("monday", "16:00-18:00", 2), process.Slot("monday", "18:00-20:00", 2), process.Slot("monday", "20:00-22:30", 2.5)]
    tuesday = [process.Slot("tuesday", "10:00-12:00", 2), process.Slot("tuesday", "12:00-14:00", 2), process.Slot("tuesday", "14:00-16:00", 2), process.Slot("tuesday", "16:00-18:00", 2), process.Slot("tuesday", "18:00-20:00", 2), process.Slot("tuesday", "20:00-22:30", 2.5)]
    wednesday = [process.Slot("wednesday", "10:00-12:00", 2), process.Slot("wednesday", "12:00-14:00", 2), process.Slot("wednesday", "14:00-16:00", 2), process.Slot("wednesday", "16:00-18:00", 2), process.Slot("wednesday", "18:00-20:00", 2), process.Slot("wednesday", "20:00-22:30", 2.5)]
    thursday = [process.Slot("thursday", "10:00-12:00", 2), process.Slot("thursday", "12:00-14:00", 2), process.Slot("thursday", "14:00-16:00", 2), process.Slot("thursday", "16:00-18:00", 2), process.Slot("thursday", "18:00-20:00", 2), process.Slot("thursday", "20:00-22:30", 2.5)]
    friday = [process.Slot("friday", "10:00-12:00", 2), process.Slot("friday", "12:00-14:00", 2), process.Slot("friday", "14:00-17:00", 3)]
    saturday = [process.Slot("saturday", "10:00-12:00", 2), process.Slot("saturday", "12:00-14:00", 2), process.Slot("saturday", "14:00-17:00", 3)]
    sunday = [process.Slot("sunday", "10:00-12:00", 2), process.Slot("sunday", "12:00-14:00", 2), process.Slot("sunday", "14:00-17:00", 3)]

    # all_slots contains all slots from all days
    all_slots = monday + tuesday + wednesday + thursday + friday + saturday + sunday
    all_day_durations = [slot.duration for slot in all_slots]

    # add mtwt closing slots to all slots
    mtwt_closing_durations = [slot.duration for slot in all_slots if slot.time == "20:00-22:30"]
    total_available_hours = sum(all_day_durations) + sum(mtwt_closing_durations)

    # vector that contains all students, students are added upon initialization
    all_students = []

    # parses json and readies data for slotting functions
    process.employee_parser(data, all_students, monday, tuesday, wednesday, thursday, friday, saturday, sunday)

    hours_requested = {}
    for student in all_students:
        hours_requested[student.name] = student._idh

    # sort all slots based on the number of students available to work them
    all_slots_sorted = sorted(all_slots, key = lambda slot: len(slot.students))

    # student selection loop
    for slot in all_slots_sorted: # loop through all slots in order starting from the one with the least available students
        flexibility_ratios = [student.ratio for student in slot.students] # using the selected slot, create a list with all students' flexibility ratios
        if flexibility_ratios != []: # ensure there are available students, else move on to the next slot
            max_ratio = max(flexibility_ratios) # choose the max flexibility ratio (greatest desired hours, least available hours, i.e. the least flexible student)
            if max_ratio != 0: # ensure the max_ratio isn't 0 (if it's 0, everyone's desired hours have been satisfied)
                max_ratio_index = flexibility_ratios.index(max(flexibility_ratios))
                max_student = slot.students[max_ratio_index] # select the student corresponding to the max flexibility ratio
                max_student.set_idh(slot.duration) # update student's hours and ratio
                slot.selected.append(max_student) # add the student to the slot's selected student list
                if slot.time == "20:00-22:30": # if it's a closing slot, repeat the same process to add one more student
                    slot.students.remove(max_student) # remove the student that has already been selected
                    flexibility_ratios = [student.ratio for student in slot.students]
                    if flexibility_ratios != []:
                        max_ratio = max(flexibility_ratios)
                        if max_ratio != 0:
                            max_ratio_index = flexibility_ratios.index(max(flexibility_ratios))
                            max_student = slot.students[max_ratio_index]
                            max_student.set_idh(slot.duration)
                            slot.selected.append(max_student)
                            slot.students.remove(max_student)

    weekday_order = {"monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4, "friday": 5, "saturday": 6, "sunday": 7}

    # sort all slots again
    all_slots_resorted = sorted(all_slots_sorted, key = lambda slot: (weekday_order[slot.day], slot.time))

    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    schedule_dict = {day: [] for day in days}
    availability_dict = {day: {} for day in days}
    hours_received = {}
    for student in all_students:
        hours_received[student.name] = student.total_hours
    for slot in all_slots_resorted:
        for day in days:
            if slot.day == day:
                schedule_dict.get(day).append(f"{slot.time}: {slot.selected_name()}")
                availability_dict.get(day).append(f"{slot.time}: {slot.student_names()}")

    print(schedule_dict)
    print(availability_dict)
    return [{"schedule": schedule_dict, "availability": availability_dict, "hoursRequested": hours_requested, "hoursReceived": hours_received}], 200

if __name__ == '__main__':
    app.run(debug=True) 
