document.getElementById('registerForm').addEventListener('submit', async function(e) {
    e.preventDefault();
  
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
  
    const response = await fetch('http://127.0.0.1:8000/api/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username: username, email: email, password: password })
    });
  
    const data = await response.json();
  
    if (data.status === 'success') {
      alert('Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz...');
      window.location.href = 'login.html';
    } else {
      alert(data.message);
    }
  });
  