(function () {
  var canonicalDirectories = new Set([
    "/book",
    "/en/book",
    "/zh/book",
    "/start-here",
    "/en/start-here",
    "/zh/start-here",
    "/reference",
    "/en/reference",
    "/zh/reference",
    "/appendix/sources",
    "/en/appendix/sources",
    "/zh/appendix/sources",
    "/book/part-i/chapter-1",
    "/en/book/part-i/chapter-1",
    "/zh/book/part-i/chapter-1",
    "/book/part-iv/chapter-9",
    "/en/book/part-iv/chapter-9",
    "/zh/book/part-iv/chapter-9",
    "/book/part-v/chapter-13",
    "/en/book/part-v/chapter-13",
    "/zh/book/part-v/chapter-13"
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
