(function () {
  var canonicalDirectories = new Set([
    "/book",
    "/en/book",
    "/zh/book"
  ]);
  var projectPrefix = "/agent-arch";
  var path = window.location.pathname.replace(/\/+$/, "");
  var localPath = path.startsWith(projectPrefix) ? path.slice(projectPrefix.length) || "/" : path;

  if (canonicalDirectories.has(localPath)) {
    window.location.replace(window.location.origin + path + "/" + window.location.search + window.location.hash);
  }
})();
