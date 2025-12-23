const API = "";

async function loadApps() {
  const res = await fetch("/apps");
  const apps = await res.json();

  const table = document.getElementById("apps");
  table.innerHTML = `
    <tr>
      <th>Name</th>
      <th>Runtime</th>
      <th>URL</th>
      <th>Actions</th>
    </tr>
  `;

  Object.entries(apps).forEach(([name, app]) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${name}</td>
      <td>${app.runtime || "unknown"}</td>
      <td><a href="${app.url}" target="_blank">${app.url}</a></td>
      <td>
        <button onclick="viewLogs('${name}')">Logs</button>
        <button onclick="deleteApp('${name}')">Delete</button>
      </td>
    `;
    table.appendChild(row);
  });
}

async function deploy() {
  const app = document.getElementById("app").value;
  const repo = document.getElementById("repo").value;
  const runtime = document.getElementById("runtime").value;

  const res = await fetch("/deploy", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ app, repo, runtime })
  });

  const result = await res.json();
  document.getElementById("deploy-result").textContent =
    JSON.stringify(result, null, 2);

  loadApps();
}

async function deleteApp(name) {
  await fetch(`/apps/${name}`, { method: "DELETE" });
  loadApps();
}

async function viewLogs(name) {
  const res = await fetch(`/apps/${name}/logs`);
  const data = await res.json();
  alert(data.logs || "No logs");
}

loadApps();
