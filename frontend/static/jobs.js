document.getElementById('filterForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const schedule = document.getElementById('scheduleFilter').value;
    const salary = document.getElementById('salaryFilter').value;
    const experience = document.getElementById('experienceFilter').value;

    const query = new URLSearchParams({ schedule, salary, experience });

    // Получение списка вакансий с фильтрацией
    fetch(`http://localhost:8000/jobs/?${query.toString()}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const jobList = document.getElementById('jobList');
            jobList.innerHTML = '';

            data.forEach(job => {
                const jobDiv = document.createElement('div');
                jobDiv.innerHTML = `<strong>${job.title}</strong><br>Schedule: ${job.schedule}<br>Salary: ${job.salary}<br>Experience: ${job.experience}`;
                jobList.appendChild(jobDiv);
            });
        })
        .catch(error => {
            console.error('Error fetching jobs:', error);
        });
});
