document.getElementById('loginForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('http://127.0.0.1:8000/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: username, password: password })
    });

    const data = await response.json();

    if (data.status === 'success') {
        localStorage.setItem('username', username);
        alert('Giriş başarılı!');
        window.location.href = 'index.html'; // Buraya yönlendirilecek
    } else {
        alert('Hatalı giriş bilgileri!');
    }
});