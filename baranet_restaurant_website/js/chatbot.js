document.getElementById("chatbotButton").addEventListener("click", function () {
    const chatbot = document.getElementById("chatbot");
    // Eğer chatbox kapalıysa, açıyoruz; açıksa kapatıyoruz
    if (chatbot.style.display === "none" || chatbot.style.display === "") {
        chatbot.style.display = "block";
    } else {
        chatbot.style.display = "none";
    }
});

// Chatbot'u açma/kapama fonksiyonu
function toggleChatbox() {
    const chatbox = document.getElementById("chatbox");
    if (chatbox.style.display === "none" || chatbox.style.display === "") {
        chatbox.style.display = "block";  // Chatbox'ı aç
    } else {
        chatbox.style.display = "none";   // Chatbox'ı kapat
    }
}

// Mesaj gönderme fonksiyonu
async function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    if (!userInput.trim()) return; // Boş mesaj gönderme

    // Kullanıcı mesajını chatbox'a ekleyin
    const chatbox = document.getElementById("chatboxContent");
    chatbox.innerHTML += `<div class="message"><strong>Sen:</strong> ${userInput}</div>`;

    document.getElementById("userInput").value = ""; // Giriş kutusunu temizle

    // API çağrısını yaparak botun cevabını alın (örneğin, OpenAI API)
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer sk-proj-XXXX" // API anahtarınızı buraya koyun
        },
        body: JSON.stringify({
            model: "gpt-3.5-turbo",
            messages: [{ role: "user", content: userInput }]
        })
    });

    const data = await response.json();
    const botMessage = data.choices[0].message.content;

    // Bot cevabını chatbox'a ekleyin
    chatbox.innerHTML += `<div class="message"><strong>Bot:</strong> ${botMessage}</div>`;

    // Son mesaja kaydır
    chatbox.scrollTop = chatbox.scrollHeight; // Son mesaja kaydır
}


// Chatbotu kapama fonksiyonu
function closeChat() {
    const chatbot = document.getElementById("chatbot");
    chatbot.style.display = "none";
}

