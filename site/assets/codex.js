function setTheme(name) {
  document.documentElement.setAttribute('data-theme', name);
  try { localStorage.setItem('codex-theme', name); } catch (e) {}
  var sel = document.getElementById('theme-select');
  if (sel) sel.value = name;
}
window.addEventListener('DOMContentLoaded', function () {
  var cur = document.documentElement.getAttribute('data-theme') || 'dark';
  var sel = document.getElementById('theme-select');
  if (sel) sel.value = cur;
});
