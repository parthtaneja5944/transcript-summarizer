chrome.runtime.onMessage.addListener(async function (request, sender, sendResponse) {
    console.log("Content Script Loaded");
    if (request.action === 'GENERATE_SUMMARY') {
        try {
            const summary = await generateSummary(request.url);
            sendResponse({ summary: summary });
        } catch (error) {
            console.error("Error generating summary:", error);
            sendResponse({ summary: "Error generating summary." });
        }
        return true;
    }
});

async function generateSummary(url) {
    const videoId = new URL(url).searchParams.get("v");
    console.log(videoId);
    if (videoId) {
        const apiEndpoint = `http://127.0.0.1:5000/transcript?video_id=${encodeURIComponent(videoId)}`;
        const response = await fetch(apiEndpoint);
        const data = await response.json();
        console.log(data)
        const summary = data.summary
        chrome.runtime.sendMessage({ action: 'SUMMARY_RESULT', summary: summary });
        //return data.summary || "No summary available.";
    } else {
        console.error("No video ID found in the URL.");
        //return "No video ID found in the URL.";
    }
}

