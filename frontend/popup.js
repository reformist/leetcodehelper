// we receive a message from the content script

/*
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.hint) {
        document.getElementById('hintContainer').textContent = message.hint;
    }
});
*/

// so that the hint can dynamically updated while the popup is open
chrome.storage.onChanged.addListener(function(changes, namespace) {
    for (let [key, { oldValue, newValue }] of Object.entries(changes)) {
        if (key === 'hint') {
            document.getElementById('hintContainer').textContent = newValue || 'No hint available.';
        }
    }
});

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

        // when a new hint is generated, we want to erase the like/dislike color
        const upVoteButton = document.getElementById('upVote');
        const downVoteButton = document.getElementById('downVote');
        
        upVoteButton.style.backgroundColor = "#007BFF"
        downVoteButton.style.backgroundColor = "#007BFF"
        
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

    // upvote / downvote buttons

    document.getElementById('upVote').addEventListener('click', function() {
        // console.log("test2");
        //how to get the hint from chrome storage--just using the below function

        console.log("UPVOTE");

        const upVoteButton = document.getElementById('upVote');
        const downVoteButton = document.getElementById('downVote');

        if (upVoteButton.style.backgroundColor === "green") { // user clicks it again
            upVoteButton.style.backgroundColor = "#007BFF"
        }
        else {
            upVoteButton.style.backgroundColor = "green"
            downVoteButton.style.backgroundColor = "#007BFF"
        }
        

        chrome.storage.local.get('hint', function(data) {
            if (data.hint) { // if there is a hint

                // just using dev env right now for backend_url
                const BACKEND_URL = 'http://127.0.0.1:8001/edit_rating';
                fetch(BACKEND_URL, { // not sure what to put here
                    method: 'POST',
                    body: JSON.stringify({
                        hint_generated: data.hint,
                        // problem_name: "two-sum", //hard coded for now just to see if other information works
                        like: 1
                    }),
                    mode: 'no-cors'
                })
                .then(response => response.json())  // Parse the response as JSON (shouldn't matter)
                .then(data => {
                    console.log('Success:', data);
                })
                .catch(err => {
                    console.error('Error:', err);
                });
                
            } else {
                console.log("upvote occured without a hint");
            }
        });

    });

    
    document.getElementById('downVote').addEventListener('click', function() {

        console.log("DOWNVOTE");

        const upVoteButton = document.getElementById('upVote');
        const downVoteButton = document.getElementById('downVote');

        if (downVoteButton.style.backgroundColor === "green") { // user clicks it again
            downVoteButton.style.backgroundColor = "#007BFF"
        }
        else {
            downVoteButton.style.backgroundColor = "green"
            upVoteButton.style.backgroundColor = "#007BFF"
        }

        chrome.storage.local.get('hint', function(data) {
            if (data.hint) {
                const BACKEND_URL = 'http://127.0.0.1:8001/edit_rating';
                fetch(BACKEND_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'  // Add headers for JSON
                    },
                    body: JSON.stringify({
                        hint_generated: data.hint,
                        problem_name: "two-sum",  // Hardcoded for now
                        like: -1
                    })
                })
                .then(response => response.json())  // Parse the response as JSON
                .then(data => {
                    console.log('Success:', data);
                })
                .catch(err => {
                    console.error('Error:', err);
                });
            } else {
                console.log("Downvote occurred without a hint");
            }
        });
    });


});
/*
chrome.storage.local.get('hint', function(data) {
    if (data.hint) {
        document.getElementById('hintContainer').textContent = data.hint;
    }
});
*/