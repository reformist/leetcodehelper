// content.js
console.log("LeetCode Helper content script loaded!");

chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
  let url = tabs[0].url;
  // use `url` here inside the callback because it's asynchronous!
  // console.log(url);
  if (url.includes("leetcode.com/problems/")) {
    console.log("this is the correct url");
    url_parts = url.split('/');
    
    // console.log(url_parts) the problem is url_parts[4]
    //

    problem = url_parts[4];
    console.log(problem);  
  }
});

// test change

// // Access the prompt or other information on the page
// const promptElement = document.querySelector('.question-content');

// if (promptElement) {
//   const promptText = promptElement.textContent.trim();
//   console.log("LeetCode prompt:", promptText);

//   // Now, you can manipulate or use the promptText as needed.
// }
