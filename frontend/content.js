console.log("content script loaded");

chrome.runtime.onMessage.addListener(gotMessage);

async function gotMessage(message, sender, sendResponse) {
    // console.log(message.txt);

    let url = message.url;
    console.log(url);

    // console.log("DEAR GOD HELP ME"); // this registers (goes into here)
    // console.log(document);

    let problem = ''

    if (url.includes("leetcode.com/problems/")) {
        // console.log("This is the correct url");
        const url_parts = url.split('/');
        problem = url_parts[4];
        console.log(problem);
    }

    // extract the code

    const codeLines = document.querySelectorAll('.view-line');
    let code = '';

    // Iterate through each line except the last one
    for (let i = 0; i < codeLines.length - 1; i++) {
        const text = codeLines[i].textContent.replace(/\u00a0/g, ' '); // Replace non-breaking spaces with regular spaces
        code += text + '\n'; // Add a newline after each line
    }

    // Log the code or do something with it here
    console.log(code);

    // Check if 'problem' is not empty and 'code' has content
    if (problem && code) {

        // const BACKEND_URL = 'https://beetcode-deploy-c7a83262de6a.herokuapp.com/hints?problem_name=' + problem;
        const BACKEND_URL = 'http://127.0.0.1:8001/hints?problem_name=' + problem;

        try {
            const response = await fetch(BACKEND_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    problem_name: problem,
                    problem_code: code,
                }),
                mode: 'no-cors',
            });
            const data = await response.json(); // Assuming your server responds with JSON
            // console.log('Server response:', data);

            let GPT_response = JSON.parse(data.response);
            let hint = GPT_response.hints;

            console.log('Hint:', hint);
            
            // if the popup is not open when we try to send the hint, then it won't receive it
            // so store it in chrome local storage instead

            // chrome.runtime.sendMessage({hint: hint}); // send to popup

            // Inside your fetch try block, after receiving and processing the hint
            chrome.storage.local.set({hint: hint}, function() {
                console.log("Hint saved to storage.");
            });
            
        } catch (error) {
            console.error('Error sending data to server:', error);
        }
    }


}