const SERVER = "http://127.0.0.1:18765";

chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  if (!msg || !msg.type) return;

  if (msg.type === "health") {
    fetch(`${SERVER}/health`)
      .then(async (r) => {
        const data = await r.json().catch(() => ({}));
        sendResponse({ ok: r.ok, ...data });
      })
      .catch((err) => sendResponse({ ok: false, error: err.message }));
    return true;
  }

  if (msg.type === "tailor") {
    fetch(`${SERVER}/tailor`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(msg.job),
    })
      .then(async (r) => {
        const data = await r.json().catch(() => ({}));
        sendResponse({ http: r.status, ...data });
      })
      .catch((err) =>
        sendResponse({
          ok: false,
          error:
            err.message +
            " — start the local server: python3 server.py in this repo",
        })
      );
    return true;
  }
});
