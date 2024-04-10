// we receive a message from the content script

/*
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.hint) {
        document.getElementById('hintContainer').textContent = message.hint;
    }
});
*/

document.addEventListener('DOMContentLoaded', function() {

    const clearButton = document.getElementById('clearStorageButton');
    clearButton.addEventListener('click', function() {
        // Clear the extension's local storage
        chrome.storage.local.clear(function() {
            var error = chrome.runtime.lastError;
            if (error) {
                console.error(error);
            } else {
                console.log('Local storage cleared');
                // Optionally, provide feedback to the user that storage was cleared
                // For example, update the text content of an element to show a success message
            }
        });
    });

    document.getElementById('triggerAction').addEventListener('click', function() {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            // Extract the URL of the current tab
            let currentTab = tabs[0];
            let msg = {
                txt: "hello",
                url: currentTab.url
            };

            // Send the message to the content script running in the current tab
            chrome.tabs.sendMessage(currentTab.id, msg);
        });
    });

    chrome.storage.local.get('hint', function(data) {
        if (data.hint) {
            document.getElementById('hintContainer').textContent = data.hint;
        } else {
            document.getElementById('hintContainer').textContent = "No hint available";
        }
    });
});

/*
chrome.storage.local.get('hint', function(data) {
    if (data.hint) {
        document.getElementById('hintContainer').textContent = data.hint;
    }
});
*/