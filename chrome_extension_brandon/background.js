console.log("background script loaded");

// hrome.action.onClicked.addListener(buttonClicked); // executes when you click on the extension icon

/*
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
// }

/*
function buttonClicked(tab) {

    console.log("CLICKED!")

    chrome.scripting.executeScript({ // inject content.js script
        target: {tabId: tab.id},
        files: ['content.js']
    }, () => {
        // After ensuring the content script is injected, send the message
        let msg = {
            txt: "hello",
            url: tab.url
        };
        chrome.tabs.sendMessage(tab.id, msg);
    });
}
*/