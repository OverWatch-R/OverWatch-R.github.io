const $ = s => document.querySelector(s);
let packages = [], active = "all";
const repoURL = location.origin + location.pathname.replace(/index\\.html$/, "").replace(/\\/?$/, "/");
$("#sourceText").textContent = repoURL;
$("#addSource").href = "sileo://source/" + encodeURIComponent(repoURL);
$("#year").textContent = new Date().getFullYear();
function esc(s) { const el=document.createElement("span"); el.textContent=String(s||""); return el.innerHTML; }
function render() {
 const q=$("#search").value.toLowerCase();
 const list=packages.filter(p=>(active==="all"||(p.platforms||[]).includes(active)) && [p.name,p.package,p.description,p.author].join(" ").toLowerCase().includes(q));
 $("#packageCount").textContent=packages.length;
 $("#packageGrid").innerHTML=list.length ? list.map(p=>`<article class="card"><div class="card-head"><h3>${esc(p.name||p.package)}</h3><span class="version">${esc(p.version)}</span></div><p class="desc">${esc(p.description||"No description provided.")}</p><div class="tags">${(p.platforms||[]).map(t=>`<span class="tag">${esc(t)}</span>`).join("")}</div><div class="card-foot"><span>${esc(p.author||"Unknown author")}</span><a href="${esc(p.depiction||"#")}">Details</a></div></article>`).join("") : '<div class="empty">No packages found. Add .deb files to pool/ and push to GitHub.</div>';
}
document.querySelectorAll(".filter").forEach(b=>b.addEventListener("click",()=>{document.querySelector(".filter.active").classList.remove("active");b.classList.add("active");active=b.dataset.filter;render();}));
$("#search").addEventListener("input",render);
fetch("repo/packages.json").then(r=>r.ok?r.json():[]).then(d=>{packages=Array.isArray(d)?d:[];render();}).catch(()=>{packages=[];render();});
