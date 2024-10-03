/*jshint strict:false */
/*jshint esversion: 8 */
/*global console*/

document.getElementById("top-logo").addEventListener("click", function() {
    window.location.href="index.html";
});

document.addEventListener('DOMContentLoaded', () => {
    const addButton = document.getElementById('add-employee');
    const employeeBox = document.getElementById('employee-box');
    const availabilityMain = document.getElementById('availability-main');
    const template = document.getElementById('availability-template');
    let employeeCount = 0;

    addButton.addEventListener('click', () => {
        employeeCount ++;
        const newEmployee = document.createElement('div');
        newEmployee.className = 'employee';

        const employeeID = 'employee-' + employeeCount;
        newEmployee.dataset.employeeID = employeeID;

        const nameInput = document.createElement('input');
        nameInput.type = 'text';
        nameInput.placeholder = 'name';
        nameInput.name = 'employee ' + employeeCount;
        nameInput.addEventListener('click', function (event) {
            event.stopPropagation();
        });

        const hoursInput = document.createElement('input');
        hoursInput.type = 'number';
        hoursInput.name = 'employee ' + employeeCount;
        hoursInput.min = 0;
        hoursInput.value = 0;
        hoursInput.classList.add('hours-input');
        hoursInput.addEventListener('click', function (event) {
            event.stopPropagation();
        });

        const saveButton = document.createElement('button');
        saveButton.classList.add('save-button');
        saveButton.textContent = '🆗';
        saveButton.addEventListener('click', (event) => {
            event.stopPropagation();
            var currName = nameInput.value;
            var currHours = hoursInput.value;
            newEmployee.dataset.name = currName;
            newEmployee.dataset.hours = currHours;
        });

        const deleteCheckbox = document.createElement('input');
        deleteCheckbox.type = 'checkbox';
        deleteCheckbox.classList.add('delete-checkbox', 'hidden');
        deleteCheckbox.dataset.employeeID = employeeID;
        deleteCheckbox.addEventListener('click', function (event) {
            event.stopPropagation();
        });

        const allEmployees = employeeBox.querySelectorAll('.employee');
        allEmployees.forEach(employee => employee.classList.remove('employee-selected'))
        newEmployee.classList.toggle('employee-selected');

        const allAvailability = availabilityMain.querySelectorAll('.availability-container');
        allAvailability.forEach(availabilityContainer => availabilityContainer.classList.add('hidden'));
        const clone = template.content.cloneNode(true);
        const availabilityContainer = clone.querySelector('.availability-container');
        availabilityContainer.dataset.employeeID = employeeID;

        newEmployee.append(nameInput);
        newEmployee.append(hoursInput);
        newEmployee.append(saveButton);
        newEmployee.append(deleteCheckbox);
        employeeBox.append(newEmployee);
        availabilityMain.append(availabilityContainer);

        newEmployee.addEventListener('click', () => {
            const allEmployees = employeeBox.querySelectorAll('.employee');
            allEmployees.forEach(employee => employee.classList.remove('employee-selected'))
            newEmployee.classList.add('employee-selected');
        });

        const availabilityBox = availabilityContainer.querySelector('#availability-box');
        const allButtons = availabilityBox.querySelectorAll('.slots');
        allButtons.forEach(button => button.addEventListener('click', () => {
            button.classList.toggle('clicked');
            let slots = new Set(newEmployee.dataset.slots ? newEmployee.dataset.slots.split(',') : []);
            if (slots.has(button.id)) {
                slots.delete(button.id)
            } else {
                slots.add(button.id)
            }
            newEmployee.dataset.slots = Array.from(slots).join(',');
        }));
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const employeeBox = document.getElementById('employee-box');
    employeeBox.addEventListener('click', function (event) {
        const availabilityContainers = document.querySelectorAll('.availability-container');
        if (event.target.classList.contains('employee')) {
            availabilityContainers.forEach(container => container.classList.add('hidden'));
            availabilityContainers.forEach(container => {
                if (container.dataset.employeeID == event.target.dataset.employeeID) {
                    container.classList.remove('hidden');
                }
            });
        };
    });
});

document.querySelector('#edit-employee').addEventListener('click', () => {
    const checkboxes = document.querySelectorAll('.delete-checkbox');
    const deleteButton = document.getElementById('del-button');
    const backButton = document.getElementById('bk-button');
    const addButton = document.getElementById("add-employee");
    addButton.disabled = true;
    checkboxes.forEach(checkbox => checkbox.classList.remove('hidden'));
    deleteButton.classList.add('delete-button', 'gray-buttons');
    deleteButton.classList.remove('hidden');
    backButton.classList.add('back-button', 'gray-buttons');
    backButton.classList.remove('hidden');
});

document.querySelector('#bk-button').addEventListener('click', () => {
    const checkboxes = document.querySelectorAll('.delete-checkbox');
    const deleteButton = document.getElementById('del-button');
    const backButton = document.getElementById('bk-button');
    const addButton = document.getElementById("add-employee");
    addButton.disabled = false;
    checkboxes.forEach(checkbox => checkbox.classList.add('hidden'));
    deleteButton.classList.add('hidden');
    backButton.classList.add('hidden');
});

document.querySelector('#del-button').addEventListener('click', () => {
    const checkboxes = document.querySelectorAll('.delete-checkbox');
    const employees = document.querySelectorAll('.employee');
    const availabilityContainers = document.querySelectorAll('.availability-container');
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            employees.forEach(employee => {
                if (checkbox.dataset.employeeID == employee.dataset.employeeID) {
                    employee.remove();
                };
            });
            availabilityContainers.forEach(container => {
                if (checkbox.dataset.employeeID == container.dataset.employeeID) {
                    container.remove();
                };
            });
        };
    });
});

document.getElementById('generate-schedule').addEventListener('click', function() {
    const employees = document.querySelectorAll('.employee');
    let data = [];
    employees.forEach(employee => {
        data.push({
            id: employee.dataset.employeeID,
            name: employee.dataset.name,
            desiredHours: employee.dataset.hours,
            slots: employee.dataset.slots
        });
    });
    const jsonData = JSON.stringify(data);
    fetch("http://127.0.0.1:5000/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: jsonData
    })
    .then(response => response.json())
    .then(file => {
        const schedule = file[0].schedule;
        console.log(make_csv(schedule))})
    .catch(error => console.error('Error:', error));
});


/* how to make an api request to my own flask server to a route */
/* enabling cors in flask -> cross origin requests */
/* making a POST request from frontend to flask api */
/* GET, POST, PUT, DELETE requests */

/* questions: 
- why does http://localhost:5000/ not work but http://127.0.0.1:5000/ does, aren't they the same address in different forms?
*/

function make_csv(schedule) {
    const days = Object.keys(schedule);
    const slot_groups = Object.values(schedule);
    const replacer = (key, value) => value === null ? '' : value;
    const csv = [
        days.join(","),
        ...slot_groups.map(row => days.map(fieldName => JSON.stringify(row[fieldName], replacer)).join(','))
    ].join('\r\n');
    return csv;
}
/*
function download_csv(data)
const blob = new Blob([jsonData], {type:'application/json'});
const url = URL.createObjectURL(blob);
const link = document.createElement('a');
link.setAttribute('href', url);
link.setAttribute('download', 'data.json');
link.style.visibility = 'hidden';
document.body.appendChild(link);
link.click();
document.body.removeChild(link);
*/
         