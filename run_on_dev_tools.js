const issueKeys = [
  "ABC-1234",
  "ABC-9999",
];

const checkInterval = 1000;

async function openAndCloseTabs() {
  const domain = window.location.href
    .substring(
      0,
      window.location.href.indexOf('.atlassian.net'),
    )
    .slice(8);

  for (let issueKey of issueKeys) {
    let tab = window.open(`https://${domain}.atlassian.net/browse/${issueKey}`, '_blank');

    let elementExists = false;

    while (!elementExists) {
      await new Promise(resolve => setTimeout(resolve, checkInterval));

      try {
        elementExists = tab.document.querySelector("iframe") !== null;
      } catch (e) {
      }
    }

    while (!tab.closed) {
      await new Promise(resolve => setTimeout(resolve, checkInterval));
    }
  }
}

openAndCloseTabs();
