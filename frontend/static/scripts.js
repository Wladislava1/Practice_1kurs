document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const title = document.getElementById('searchQuery').value;
    const schedule = document.getElementById('searchSchedule').value;
    const salary = parseInt(document.getElementById('searchSalary').value);
    const experience = document.getElementById('searchExperience').value;

    const jobRequest = {
        title: title,
        schedule: schedule,
        salary: isNaN(salary) ? null : salary, 
        experience: experience
    };

    // Отправка запроса на сервер для парсинга вакансий и добавления их в БД
    fetch('http://localhost:8000/parse_job/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jobRequest)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(JSON.stringify(errorData));
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        // Перенаправление на страницу со списком вакансий
        window.location.href = '/jobs.html';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
