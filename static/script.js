let chatBot = "";

async function generateSessionid() {
    if (!sessionStorage.getItem('session-id')) {
        const response = await fetch('https://testapi.unomiru.com/api/Waysbot/generate_sessionid');
        const sessionId = await response.text();
        sessionStorage.setItem('sessionId', sessionId);
    }
}

window.onload = () => {
    generateSessionid();
    const bot = new URLSearchParams(window.location.search.split('?')[1]);

    if (bot.get('bot') === "renoswift") {
        document.getElementById('chat-header-waysbot').style.display = "none";
        document.getElementById('chat-header-kalaa').style.display = "none";
        document.getElementById('chat-header-rewpaz').style.display = "none";
        introduceChatbot("Hello! I am RenoSwift Bot and I am here to help you reinvent your bathroom. I can help you with bathroom design ideas, product recommendations, and much more. Let's get started!");
    } else if (bot.get('bot') === "kalaa") {
        document.getElementById('chat-header-waysbot').style.display = "none";
        document.getElementById('chat-header-renoswift').style.display = "none";
        document.getElementById('chat-header-rewpaz').style.display = "none";
        introduceChatbot("Hello! I am Kalaa Planet Bot and I am here to take you on an artistic journey. Come and explore the world of Kalaa Planet with me. I will be happy to be your guide.");
    } else if (bot.get('bot') === "rewpaz") {
        document.getElementById('chat-header-waysbot').style.display = "none";
        document.getElementById('chat-header-renoswift').style.display = "none";
        document.getElementById('chat-header-kalaa').style.display = "none";
        introduceChatbot("Hi I am a virtual assistant for Rewpaz , If you have any queries regarding Rewpaz , its services and mental health , feel free to ask! I am here to support you every step of the way.");
    } else {
        document.getElementById('chat-header-renoswift').style.display = "none";
        document.getElementById('chat-header-kalaa').style.display = "none";
        document.getElementById('chat-header-rewpaz').style.display = "none";
        introduceChatbot("Hello! I am LUMI G24R, Waysahead's latest AI creation. I am still in the learning process and I will be happy to assist you with anything.");
    }

    if (bot.get('bot') === "renoswift" || bot.get('bot') === "kalaa" || bot.get('bot') === "rewpaz"){
        chatBot = bot.get('bot');
        document.querySelector('html').classList.add(chatBot);
    }
}


function toggleOption(option) {
    document.getElementById('textToText').classList.remove('option-active');
    document.getElementById('textToSpeech').classList.remove('option-active');
    document.getElementById('videoCall').classList.remove('option-active');
    document.getElementById(option).classList.add('option-active');

    switch (option) {
        case 'textToText':
            textToText();
            break;
        case 'textToSpeech':
            textToSpeech();
            break;
        case 'videoCall':
            videoCall();
            break;
        default:
            break;
    }
}

function textToText() {
    const userInput = getUserInput();
    if (userInput.trim() !== "") {
        sendMessage("You", userInput);
        receiveMessage("Chatbot", "This is a response from the chatbot.");
    }
}

function textToSpeech() {
    const userInput = getUserInput();
    if (userInput.trim() !== "") {
        sendMessage("You", userInput);
        receiveMessage("Chatbot", "This is a response from the chatbot.");
    }
}

function videoCall() {
    const userInput = getUserInput();
    if (userInput.trim() !== "") {
        sendMessage("You", userInput);
        receiveMessage("Chatbot", "This is a response from the chatbot.");
    }
}

async function sendMessage(sender, message) {
    let chatDisplay = document.getElementById("chat-display");
    let messageClass = sender === 'You' ? 'user-message' : 'chatbot-message';

    // Create a div for the message bubble
    let messageBubble = document.createElement('div');
    messageBubble.className = messageClass;

    // Create the message bubble content
    let messageContent = document.createElement('div');
    messageContent.className = 'message-bubble';
    messageContent.textContent = message;

    // Append the user or chatbot icon to the message bubble
    let iconSrc = sender === 'You'
        ? '../static/userImage.svg'
        : '../static/bot-gif.gif';

    let iconAlt = sender === 'You' ? 'User Icon' : 'Chatbot Icon';

    let messageIcon = document.createElement('img');
    messageIcon.src = iconSrc;
    messageIcon.alt = iconAlt;
    messageIcon.className = sender === 'You' ? 'user-icon' : 'chatbot-icon';

    // Append the message content and icon to the message bubble
    messageBubble.appendChild(messageContent);
    messageBubble.appendChild(messageIcon);

    // Append the message bubble to the chat display
    chatDisplay.appendChild(messageBubble);

    chatDisplay.scrollTop = chatDisplay.scrollHeight;

    // Clear the user input
    document.getElementById("user-input").value = "";

    document.getElementById('loading-spinner').setAttribute('data-visibility', 'true');

    let url = `https://testapi.unomiru.com/api/Waysbot/chat`;

    if (chatBot === "renoswift" || chatBot === "kalaa" || chatBot === "rewpaz") {
        url = `https://testapi.unomiru.com/api/Waysbot/chat/${chatBot}`;
    }

    // Send user input to the server
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "session-id": sessionStorage.getItem('sessionId'),
        },
        body: JSON.stringify({
            user_input: message,
        }),
    });

    const data = await response.json();
    document.getElementById('loading-spinner').setAttribute('data-visibility', 'false');
    // Display the chatbot's response
    receiveMessage("Chatbot", data.response);

    chatDisplay.scrollTop = chatDisplay.scrollHeight;
}



function receiveMessage(sender, message) {
    let chatDisplay = document.getElementById("chat-display");
    let messageClass = sender === 'You' ? 'user-message' : 'chatbot-message';
    let messageLines = message.split('\n');

    // Replace '.' with '<br>' to display points in a new line
    let formattedMessage = messageLines.join('<br>');

    chatDisplay.innerHTML += `<div class="${messageClass}">
                                <img src="${sender === 'You' ? '../static/userImage.svg' : '../static/bot-gif.gif'}" alt="${sender} Icon" class="${sender === 'You' ? 'user-icon' : 'chatbot-icon'}">
                                <div class="message-bubble ${messageClass === 'chatbot-message' && 'chatbot'}">${formattedMessage}</div>                             
                            </div>`;


    document.getElementById("user-input").value = "";

    chatDisplay.scrollTop = chatDisplay.scrollHeight;

    // Speak the message using the text-to-speech API
    if (sender === 'Chatbot' && !isChatbotVoiceMuted) {
        speakMessage(message);
    }
}


let isChatbotVoiceMuted = false;
let currentUtterance;

function toggleChatbotVoice(type) {
    isChatbotVoiceMuted = !isChatbotVoiceMuted;

    if (type === 'on') {
        document.getElementById('sound-on').style.display = 'none';
        document.getElementById('sound-off').style.display = 'block';
    } else {
        document.getElementById('sound-off').style.display = 'none';
        document.getElementById('sound-on').style.display = 'block';
    }

    currentUtterance = new SpeechSynthesisUtterance(Array(...document.querySelectorAll(".chatbot")).at(-1).textContent)
    currentUtterance.lang = 'en';

    if (isChatbotVoiceMuted && isSpeaking) {
        // If currently speaking, cancel the speech
        window.speechSynthesis.cancel();
        isSpeaking = false;
    } else if (!isChatbotVoiceMuted && currentUtterance) {
        // If unmuted and there was a previous utterance, resume speaking
        window.speechSynthesis.speak(currentUtterance);
        isSpeaking = true;
    }
}

let isSpeaking = false;


function speakChatbotIntroduction() {
    // Speak the initial chatbot introduction
    let introductionMessage = "Hello! I'm LUMI G24R, WaysAhead Global's latest AI creation. I am here to assist you and learn new things.  Alternatively, If you want me to take your interview just ask! But please provide your mail id first so I can remember you.";

    if (chatBot === "renoswift") {
        introductionMessage = "Hello! I am RenoSwift Bot and I am here to help you reinvent your bathroom. I can help you with bathroom design ideas, product recommendations, and much more. Let's get started!";
    }

    if (chatBot === "kalaa") {
        introductionMessage = "Hello! I am Kalaa Planet Bot and I am here to take you on an artistic journey. Come and explore the world of Kalaa Planet with me. I will be happy to be your guide.";
    }

    if (chatBot === "rewpaz") {
        introductionMessage = "Hi I am a virtual assistant for Rewpaz , If you have any queries regarding Rewpaz , its services and mental health , feel free to ask! I am here to support you every step of the way";    
    }

    speakMessage(introductionMessage);
}


function speakMessage(text) {
    let utterance = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(utterance);
    if (isSpeaking) {
        window.speechSynthesis.cancel();
        isSpeaking = false;
        return;
    }
    // Optionally set properties like voice, rate, pitch, etc.
    utterance.lang = 'en';
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    isSpeaking = true;
    currentUtterance = utterance;
    // Listen for the end event to know when the speech is finished
    utterance.addEventListener('end', () => {
        isSpeaking = false;
        currentUtterance = utterance// Reset the isSpeaking flag when speech ends
    });

}


function getUserInput() {
    return document.getElementById("user-input").value;
}

function introduceChatbot(message) {
    setTimeout(function () {
        receiveMessage("Chatbot", message);
    }, 1000);
}

function showOptions(options) {
    let chatDisplay = document.getElementById("chat-display");
    options.forEach(function (option, index) {
        chatDisplay.innerHTML += `<div class="chatbot-message">
                                        <div class="message-bubble option-button" onclick="handleOptionClick('${option}')">
                                            ${option}
                                        </div>
                                      </div>`;
    });
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
}

function selectOption(option) {
    sendMessage("You", ` ${option}`);
}



document.getElementById("user-input").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevents adding a new line
        sendMessage('You', getUserInput());
    }
});

let isRecording = false;
let recognition;

function startRecording() {
    if (!isRecording) {
        recognition = new webkitSpeechRecognition() || new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.onstart = function () {
            isRecording = true;
            console.log('Speech recognition started.')
        };
        recognition.onresult = function (event) {
            const result = event.results[event.results.length - 1][0].transcript;
            document.getElementById('user-input').value = result;
        };
        recognition.onend = function () {
            isRecording = false;
        };

        recognition.start();
    } else {
        recognition.stop();
    }
}

// Modify the existing send-button onclick to use the speech-to-text API
document.getElementById('send-button').onclick = function () {
    const userInput = getUserInput();
    if (userInput.trim() !== "") {
        // If the user has entered text manually, send it as a normal text message
        sendMessage("You", userInput);
    } else {
        // If the user used speech-to-text, send the audio file to the server
        const audioInput = document.getElementById('audio-input').files[0];
        if (audioInput) {
            sendAudioMessage(audioInput);
        }
    }
};

function sendAudioMessage(audioInput) {
    const formData = new FormData();
    formData.append('audio', audioInput);

    fetch('/speech-to-text', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            // Display the transcribed text as a user message
            receiveMessage("You", data.transcription);
        })
        .catch(error => console.error('Error:', error));
}

function startTextToSpeech() {
    let userInput = getUserInput();

    // Send user input to the server for text-to-speech
    fetch('/text-to-speech', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'text': userInput,
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('Text-to-speech successful.');
            } else {
                console.error('Text-to-speech error:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
}

function toggleChatbot() {
    let chatIcon = document.getElementById('chatbot-icon');
    let chatContainer = document.getElementById('chat-container');

    if (chatContainer.style.display === 'none') {
        // Show the chat container
        chatContainer.classList.add('fadeInAnimation');
        chatContainer.style.display = 'flex';
        chatIcon.style.display = 'none';
        // Start speaking when the chatbot interface is opened
        speakChatbotIntroduction();
    } else {
        // Hide the chat container
        chatContainer.style.display = 'none';
        chatContainer.classList.remove('fadeInAnimation');

        // Stop speaking when the chatbot interface is closed
        if (isSpeaking) {
            window.speechSynthesis.cancel();
            isSpeaking = false;
        }
    }

    chatContainer.classList.add('zoom-in');
}

function closeChatbot() {
    let chatIcon = document.getElementById('chatbot-icon');
    let chatContainer = document.getElementById('chat-container');

    if (isSpeaking) {
        window.speechSynthesis.cancel();
        isSpeaking = false;
    }

    // Show the chat icon
    chatIcon.style.display = 'block';

    // Hide the chat container
    chatContainer.style.display = 'none';

    chatContainer.classList.remove('zoom-in');
}
