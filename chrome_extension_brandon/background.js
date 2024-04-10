console.log("background script loaded");

chrome.action.onClicked.addListener(buttonClicked); // executes when you click on the extension icon

function buttonClicked(tab) {

    let msg = {
        txt: "hello",
        url: tab.url
    }

    console.log(tab.url); // this works, but need to handle it in the content script
    // send the tab.url to the content script

    chrome.tabs.sendMessage(tab.id, msg);
    // chrome.runtime.sendMessage(tab.id, msg);

    /*
    chrome.scripting.executeScript({
        target: {tabId: tab.id},
        files: ['content.js']
    });
    */
}