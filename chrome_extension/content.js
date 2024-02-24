// content.js
console.log("LeetCode Helper content script loaded!");

// Access the prompt or other information on the page
const promptElement = document.querySelector('.question-content');

if (promptElement) {
  const promptText = promptElement.textContent.trim();
  console.log("LeetCode prompt:", promptText);

  // Now, you can manipulate or use the promptText as needed.
}
