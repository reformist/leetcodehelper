console.log("content script loaded");

chrome.runtime.onMessage.addListener(gotMessage);

function gotMessage(message, sender, sendResponse) {
    // console.log(message.txt);

    let url = message.url;
    console.log(url);

    // console.log("DEAR GOD HELP ME"); // this registers (goes into here)
    // console.log(document);

    if (url.includes("leetcode.com/problems/")) {
        // console.log("This is the correct url");
        const url_parts = url.split('/');
        const problem = url_parts[4];
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
}