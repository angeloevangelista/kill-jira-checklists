async function initialize() {
  const iframe = await new Promise((resolve, reject) => {
    let interval;

    interval = setInterval(
      () => {
        const iframe = document.querySelector("iframe[id^='com.herocoders.plugins.jira.issuechecklist-free']")

        if (!iframe) return;

        clearInterval(interval);
        resolve(iframe);
      },
      100,
    )
  });

  const response = await fetch(
    "http://127.0.0.1:3333/log_url",
    {
      method: "POST",
      body: JSON.stringify({
        url: iframe.src,
      }),
      headers: {
        "Content-Type": "application/json"
      }
    },
  );
  const data = await response.json();

  const pageContent = data.page;

  const tempElement = document.createElement('div');
  tempElement.innerHTML = pageContent;


  const issueKey = tempElement.querySelector('meta[name="issueKey"]').content
  const token = tempElement.querySelector('meta[name="token"]').content
  const icToken = tempElement.querySelector('meta[name="icToken"]').content
  const checklist = JSON.parse(tempElement.querySelector('meta[name="prefetchedItems"]').content)

  await fetch(
    "http://127.0.0.1:3333/delete_checklist",
    {
      method: "POST",
      body: JSON.stringify({
        issueKey,
        token,
        icToken,
        checklist,
      }),
      headers: {
        "Content-Type": "application/json"
      }
    },
  );

  window.close()
}

document.addEventListener(
  'DOMContentLoaded',
  initialize,
);
