document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = document.getElementById('searchQuery').value;

    // Отправка запроса на сервер для парсинга вакансий и добавления их в БД
    fetch('http://localhost:8000/parse_job/', { // Указываем порт 8000
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ title: query, schedule: "", salary: 0, experience: "" }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Перенаправление на страницу со списком вакансий
        window.location.href = '/jobs.html';
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});