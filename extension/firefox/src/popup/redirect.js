const scamHunterURL = "google.com/search?q=";

browser.tabs.query({ active: true, currentWindow: true }).then(function (tabs) {
    // Get the URL of the active tab
    const activeTab = tabs[0];
    const activeTabURL = activeTab.url;

    // Create a tab with current url as query to Scam Hunter site
    browser.tabs.create({ url: scamHunterURL + activeTabURL });
});

