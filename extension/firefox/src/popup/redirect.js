const scamHunterURL = "https://google.com/search?q=";

function getDomain(url) {
    try {
      // Create a URL object
      const parsedUrl = new URL(url);
      
      // Return the protocol and hostname (domain)
      return `${parsedUrl.protocol}//${parsedUrl.hostname}`;
    } catch (e) {
      // If the input is not a valid URL, return an error message or handle it
      console.error('Invalid URL:', e);
      return null;
    }
  }
  
browser.tabs.query({ active: true, currentWindow: true }).then(function (tabs) {
    // Get the URL of the active tab
    const activeTab = tabs[0];
    const activeTabURL = getDomain(activeTab.url);

    // Create a tab with current url as query to Scam Hunter site
    browser.tabs.create({ url: scamHunterURL + activeTabURL });
});

