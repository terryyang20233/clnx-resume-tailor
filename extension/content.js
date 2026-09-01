(() => {
  if (window.__clnxResumeLoaded) return;
  window.__clnxResumeLoaded = true;

  function pageKind() {
    if (document.querySelector("#postingDiv")) return "detail";
    if (document.querySelector("#postingsTable")) return "list";
    return "other";
  }

  function extractList() {
    const table = document.querySelector("#postingsTable");
    if (!table) return [];
    const jobs = [];
    table.querySelectorAll("tr[id^='posting']").forEach((row) => {
      const id = (row.id || "").replace(/^posting/, "");
      const titleEl = row.querySelector("[data-totitle]");
      const title =
        (titleEl && titleEl.getAttribute("data-totitle")) ||
        (row.querySelector("a.np-view-btn-" + id) || {}).innerText ||
        "";
      const cells = Array.from(row.querySelectorAll("td")).map((td) =>
        td.innerText.replace(/\s+/g, " ").trim()
      );
      jobs.push({
        id,
        title: title.trim(),
        division: cells[4] || "",
        type: cells[5] || "",
        deadline: cells[6] || "",
      });
    });
    return jobs;
  }

  function extractDetail() {
    const root = document.querySelector("#postingDiv");
    if (!root) return null;
    const fields = {};
    root.querySelectorAll("tr").forEach((tr) => {
      const cells = tr.children;
      if (cells.length < 2) return;
      const k = cells[0].innerText.replace(/\s+/g, " ").trim().replace(/:$/, "");
      const v = cells[1].innerText.trim();
      if (k && v) fields[k] = v;
    });
    const headingEl = root.querySelector("h1, h2");
    const heading = (headingEl && headingEl.innerText.trim()) || "";
    return {
      heading,
      url: location.href,
      fields,
    };
  }

  function el(tag, attrs, ...children) {
    const node = document.createElement(tag);
    Object.entries(attrs || {}).forEach(([k, v]) => {
      if (k === "className") node.className = v;
      else if (k.startsWith("on") && typeof v === "function") node.addEventListener(k.slice(2).toLowerCase(), v);
      else node.setAttribute(k, v);
    });
    children.flat().forEach((c) => {
      if (c == null || c === false) return;
      node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return node;
  }

  function setStatus(panel, text, cls) {
    const s = panel.querySelector(".status");
    s.textContent = text;
    s.className = "status " + (cls || "");
  }

  function send(type, extra) {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage({ type, ...extra }, (resp) => {
        if (chrome.runtime.lastError) {
          resolve({ ok: false, error: chrome.runtime.lastError.message });
          return;
        }
        resolve(resp || { ok: false, error: "no response" });
      });
    });
  }

  function mountList(panel) {
    const jobs = extractList();
    panel.appendChild(el("h1", {}, "CLNx → one-page resume"));
    panel.appendChild(
      el(
        "div",
        { className: "muted" },
        jobs.length
          ? `${jobs.length} postings on this page. Open one, then send the description.`
          : "No posting table found."
      )
    );
    const search = el("input", {
      type: "search",
      placeholder: "Filter by title, division, id…",
    });
    const list = el("ul", {});
    panel.appendChild(search);
    panel.appendChild(list);

    function render(filter) {
      list.innerHTML = "";
      const q = (filter || "").toLowerCase();
      jobs
        .filter((j) =>
          `${j.id} ${j.title} ${j.division} ${j.type}`.toLowerCase().includes(q)
        )
        .slice(0, 40)
        .forEach((j) => {
          const open = el("button", { className: "secondary" }, "Open posting");
          open.addEventListener("click", () => {
            const btn = document.querySelector("a.np-view-btn-" + j.id);
            if (btn) btn.click();
            else setStatus(panel, "Could not find the View button for " + j.id, "err");
          });
          list.appendChild(
            el(
              "li",
              {},
              el("div", { className: "title" }, `${j.id} · ${j.title}`),
              el("div", { className: "meta" }, `${j.division} · ${j.type} · ${j.deadline}`),
              open
            )
          );
        });
    }
    search.addEventListener("input", () => render(search.value));
    render("");
    panel.appendChild(el("div", { className: "status" }, ""));
    send("health").then((r) => {
      if (r.ok) setStatus(panel, "Local server connected.", "ok");
      else
        setStatus(
          panel,
          "Local server not running. In this repo: python3 server.py",
          "err"
        );
    });
  }

  function mountDetail(panel) {
    const job = extractDetail();
    panel.appendChild(el("h1", {}, "CLNx → one-page resume"));
    const title =
      (job && (job.fields["Work Study Position Title"] || job.heading)) ||
      "Job posting";
    panel.appendChild(el("div", { className: "muted" }, title));
    const go = el("button", {}, "Create 1-page resume");
    const ping = el("button", { className: "secondary" }, "Check server");
    panel.appendChild(el("div", { className: "row" }, go, ping));
    panel.appendChild(el("div", { className: "status" }, ""));

    ping.addEventListener("click", async () => {
      const r = await send("health");
      setStatus(
        panel,
        r.ok ? "Server OK" : "Server down. Run python3 server.py",
        r.ok ? "ok" : "err"
      );
    });

    go.addEventListener("click", async () => {
      if (!job || !Object.keys(job.fields || {}).length) {
        setStatus(panel, "Could not read posting fields from this page.", "err");
        return;
      }
      setStatus(panel, "Sending posting and compiling…");
      const r = await send("tailor", { job });
      if (r.ok) {
        setStatus(
          panel,
          `Saved (${r.pages} page)\n${r.folder}\nPDF: ${r.pdf || "(tex only)"}`,
          "ok"
        );
      } else {
        setStatus(panel, r.error || JSON.stringify(r), "err");
      }
    });

    send("health").then((r) => {
      if (!r.ok)
        setStatus(
          panel,
          "Local server not running. In this repo: python3 server.py",
          "err"
        );
    });
  }

  function start() {
    if (document.getElementById("clnx-resume-panel")) return;
    const kind = pageKind();
    if (kind === "other") return;
    const panel = el("div", { id: "clnx-resume-panel" });
    document.documentElement.appendChild(panel);
    if (kind === "list") mountList(panel);
    else mountDetail(panel);
  }

  const ready = () => pageKind() !== "other";
  if (ready()) start();
  const obs = new MutationObserver(() => {
    if (ready() && !document.getElementById("clnx-resume-panel")) start();
  });
  obs.observe(document.documentElement, { childList: true, subtree: true });
})();
