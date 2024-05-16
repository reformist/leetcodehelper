// chrome.action.onClicked.addListener((tab) => {
//     chrome.scripting.executeScript({
//       target: {tabId: tab.id},
//       files: ['content.js']
//     });
//   });

chrome.runtime.onInstalled.addListener(function() {
  // Register the onClicked event listener
  chrome.browserAction.onClicked.addListener(buttonClicked);
});
function buttonClicked() {
  console.log("button clicked!");
}
  

console.log("background is running")

