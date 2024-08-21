document.addEventListener('DOMContentLoaded',function(){
    const summarizeButton = document.getElementById('summarizeButton');
    console.log("summarizeButton");
    summarizeButton.addEventListener('click' ,function(){
        // chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        //     if (tabs.length > 0) {
        //         chrome.tabs.sendMessage(tabs[0].id, { action: "GENERATE_SUMMARY", url: tabs[0].url });
        //     } else {
        //         console.error("No active tab found.");
        //     }
        // });
        chrome.tabs.query({active: true, currentWindow: true}, async function(tabs){
            console.log(tabs[0]);
            //const response = await chrome.tabs.sendMessage(tabs[0].id, {action: "GENERATE_SUMMARY", url: tabs[0].url });
            await chrome.tabs.sendMessage(tabs[0].id, {action: "GENERATE_SUMMARY", url: tabs[0].url });
            //console.log(response);
            console.log(tabs[0].url);
         })
    });

    chrome.runtime.onMessage.addListener(function(message, sender, sendResponse){
        if(message.action === 'SUMMARY_RESULT'){
            console.log("outputing")
            outputSummary(message.summary);
        }
    });
    
    function outputSummary(summaryText) {
        const summaryDiv = document.getElementById('summary');
        summaryDiv.innerText = summaryText;
    }


})