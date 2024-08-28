fetch('/add', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name: 'John Doe', phone: '123-456-7890' }),
})
.then(response => response.json())
.then(data => console.log(data));
