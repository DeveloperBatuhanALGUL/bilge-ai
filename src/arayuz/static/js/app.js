/**
 * Bilge AI - Web Arayüz Mantığı
 * Tanım: Kullanıcı etkileşimlerini yönetir ve API ile iletişim kurar.
 */

const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');


const oturumId = 'web_session_' + Math.random().toString(36).substr(2, 9);

function addMessage(text, sender) {
    const div = document.createElement('div');
    div.classList.add('message', sender);
    
    if (sender === 'bot') {
        div.innerHTML = `<strong>Bilge:</strong> ${text}`;
    } else {
        div.textContent = text;
    }
    
    chatContainer.appendChild(div);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function showTyping() {
    const div = document.createElement('div');
    div.id = 'typing-indicator';
    div.classList.add('message', 'bot');
    div.innerHTML = `<span class="typing-indicator">Bilge düşünüyor...</span>`;
    chatContainer.appendChild(div);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function removeTyping() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) indicator.remove();
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage(text, 'user');
    userInput.value = '';
    userInput.disabled = true;
    sendBtn.disabled = true;

   
    showTyping();

    try {
        
        const response = await fetch('/cevapla', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                soru: text,
                oturum_id: oturumId
            })
        });

        const data = await response.json();
        removeTyping();

        if (data.basarili) {
            addMessage(data.yanit, 'bot');
        } else {
            addMessage(`Hata: ${data.hata || 'Bilinmeyen hata'}`, 'bot');
        }

    } catch (error) {
        removeTyping();
        addMessage('Bağlantı hatası oluştu. Lütfen sunucunun çalıştığından emin olun.', 'bot');
        console.error(error);
    } finally {
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}


sendBtn.addEventListener('click', sendMessage);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
