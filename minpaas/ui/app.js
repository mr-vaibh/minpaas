const API = "";

function parseEnv(text) {
  const env = {};
  text.split("\n").forEach(line => {
    line = line.trim();
    if (!line) return;
    if (!line.includes("=")) return;
    const [k, ...v] = line.split("=");
    env[k] = v.join("=");
  });
  return env;
}

function statusBadge(status) {
  const colors = {
    running: "bg-green-100 text-green-700",
    exited: "bg-red-100 text-red-700",
    not_found: "bg-gray-200 text-gray-600",
    unknown: "bg-yellow-100 text-yellow-700"
  };

  const cls = colors[status] || colors.unknown;
  return `<span class="px-2 py-1 rounded text-xs ${cls}">${status}</span>`;
}

async function loadApps() {
  const table = document.getElementById("apps");

  try {
    const res = await fetch("/apps");
    const apps = await res.json();

    table.innerHTML = `
      <thead>
        <tr class="border-b text-left">
          <th class="p-2">Name</th>
          <th class="p-2">Runtime</th>
          <th class="p-2">Status</th>
          <th class="p-2">Local Port</th>
          <th class="p-2">Command</th>
          <th class="p-2">Actions</th>
        </tr>
      </thead>
      <tbody></tbody>
    `;

    const tbody = table.querySelector("tbody");

    Object.entries(apps).forEach(([name, app]) => {
      const tr = document.createElement("tr");
      tr.className = "border-b hover:bg-gray-50";

      tr.innerHTML = `
        <td class="p-2 font-mono">${name}</td>
        <td class="p-2">${app.runtime || "-"}</td>
        <td class="p-2">${statusBadge(app.status || "unknown")}</td>
        <td class="p-2">
            <div>
              <a
                href="http://${name}.localhost"
                target="_blank"
                class="text-blue-600 hover:underline font-mono"
              >
                ${name}.localhost
              </a>
              ${
                app.port
                  ? `<div class="text-xs text-gray-500">port ${app.port}</div>`
                  : ""
              }
            </div>
        </td>
        <td class="p-2 font-mono text-xs">${app.command || "default"}</td>
        <td class="p-2 space-x-2">
          <button
            onclick="viewLogs('${name}')"
            class="px-2 py-1 text-xs bg-gray-200 rounded hover:bg-gray-300"
          >
            Logs
          </button>
          <button
            onclick="deleteApp('${name}')"
            class="px-2 py-1 text-xs bg-red-100 text-red-700 rounded hover:bg-red-200"
          >
            Delete
          </button>
        </td>
      `;

      tbody.appendChild(tr);
    });

  } catch (err) {
    table.innerHTML = `<tr><td class="p-2 text-red-600">Failed to load apps</td></tr>`;
  }
}

async function deploy() {
  const resultEl = document.getElementById("deploy-result");
  resultEl.textContent = "Deploying...";

  const payload = {
    app: document.getElementById("app").value,
    repo: document.getElementById("repo").value,
    runtime: document.getElementById("runtime").value,
    env: parseEnv(document.getElementById("env").value)
  };

  const command = document.getElementById("command").value;
  if (command) payload.command = command;

  try {
    const res = await fetch("/deploy", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    resultEl.textContent = JSON.stringify(data, null, 2);
    loadApps();

  } catch (err) {
    resultEl.textContent = "Deploy failed";
  }
}

async function deleteApp(name) {
  if (!confirm(`Delete app '${name}'?`)) return;
  await fetch(`/apps/${name}`, { method: "DELETE" });
  loadApps();
}

async function viewLogs(name) {
  const modal = document.getElementById("logs-modal");
  const content = document.getElementById("logs-content");

  content.textContent = "Loading logs...";
  modal.classList.remove("hidden");
  modal.classList.add("flex");

  try {
    const res = await fetch(`/apps/${name}/logs`);
    const data = await res.json();
    content.textContent = data.logs || "No logs available";
  } catch {
    content.textContent = "Failed to load logs";
  }
}

function closeLogs() {
  const modal = document.getElementById("logs-modal");
  modal.classList.add("hidden");
  modal.classList.remove("flex");
}

loadApps();
