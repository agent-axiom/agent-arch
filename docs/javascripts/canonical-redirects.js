(function () {
  var canonicalDirectories = new Set([
    "/book",
    "/en/book",
    "/zh/book",
    "/start-here",
    "/reference",
    "/appendix/sources",
    "/book/part-i/chapter-1",
    "/book/part-v/chapter-13"
  ]);
  var projectPrefix = "/agent-arch";
  var path = window.location.pathname.replace(/\/+$/, "");
  var localPath = path.startsWith(projectPrefix) ? path.slice(projectPrefix.length) || "/" : path;

  if (canonicalDirectories.has(localPath)) {
    var targetUrl = window.location.origin + path + "/" + window.location.search + window.location.hash;
    if (targetUrl !== window.location.href) {
      window.location.replace(targetUrl);
    }
  }
})();
