// content.js
console.log("LeetCode Helper content script loaded!");

chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
  let url = tabs[0].url;
  // Use `url` here inside the callback because it's asynchronous!
  // console.log(url);
  if (url.includes("leetcode.com/problems/")) {
    console.log("This is the correct url");
    const url_parts = url.split('/');
    const problem = url_parts[4];
    console.log(problem);

    /** 
    // Inject code to extract text from view-line elements
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      function: extractCodeFromViewLines,
    });

    */

    extractCodeFromViewLines();
  }
});

// The function to extract code lines
function extractCodeFromViewLines() {
  const codeLines = document.querySelectorAll('.view-line');
  let code = '';

  // Iterate through each line except the last one
  for (let i = 0; i < codeLines.length - 1; i++) {
    const text = codeLines[i].textContent.replace(/\u00a0/g, ' '); // Replace non-breaking spaces with regular spaces
    code += text + '\n'; // Add a newline after each line
  }

  // Log the code or do something with it here
  console.log(code);
  // You can also communicate it to the background script or popup with chrome.runtime.sendMessage if needed
}

// Test change
