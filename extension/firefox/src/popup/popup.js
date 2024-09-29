const scamHunterURL = "http://127.0.0.1:5000";

function parseUrl(url) {
  const parsedUrl = new URL(url);
  try {
    return `${parsedUrl.host}`;
  } catch {
    console.error("Wrong URL");
    return null;
  }
}

function sendUrlToBackend(url) {
  fetch("http://127.0.0.1:5000/api/site", {
    method: "POST",
    body: JSON.stringify({ domain: url }),
    header: {
      "Access-Control-Allow-Origin": "*",
    },
  })
    .then((response) => console.log(response))
    .catch((error) => console.error(error));
}

document.getElementById("redirect-button").addEventListener("click", (e) => {
  browser.tabs
    .query({ active: true, currentWindow: true })
    .then(function (tabs) {
      // Get the URL of the active tab
      const activeTab = tabs[0];
      const activeTabURL = parseUrl(activeTab.url);

      // Create a tab with current url as query to Scam Hunter site
      browser.tabs.create({ url: scamHunterURL + "=" + activeTabURL });
    });
});

document.getElementById("check-button").addEventListener("click", (e) => {
  browser.tabs
    .query({ active: true, currentWindow: true })
    .then(function (tabs) {
      // Get the URL of the active tab
      const activeTab = tabs[0];
      const activeTabUrl = parseUrl(activeTab.url);

      // Create a tab with current url as query to Scam Hunter site
      sendUrlToBackend(activeTabUrl);
    });
});
