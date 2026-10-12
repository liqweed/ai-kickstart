/* AI Kickstart — shared behaviour: nav highlight, copy buttons, tabs. No dependencies. */
(function () {
  // Highlight the current page in the nav.
  var here = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".site-nav a").forEach(function (a) {
    if (a.getAttribute("href") === here) a.classList.add("active");
  });

  // Copy-to-clipboard, with a fallback for browsers that block the async API on file:// pages.
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand("copy") ? resolve() : reject(); } catch (e) { reject(e); }
      document.body.removeChild(ta);
    });
  }
  window.kitCopy = copyText;

  function wireCopy(btn, getText) {
    btn.addEventListener("click", function () {
      copyText(getText()).then(function () {
        btn.textContent = "Copied ✓";
        btn.classList.add("done");
        setTimeout(function () { btn.textContent = "Copy"; btn.classList.remove("done"); }, 1600);
      }, function () {
        btn.textContent = "Select & copy manually";
      });
    });
  }
  window.kitWireCopy = wireCopy;

  document.querySelectorAll(".prompt").forEach(function (box) {
    var pre = box.querySelector("pre");
    var bar = box.querySelector(".bar");
    if (!pre || !bar) return;
    var btn = document.createElement("button");
    btn.className = "copy-btn";
    btn.type = "button";
    btn.textContent = "Copy";
    bar.appendChild(btn);
    wireCopy(btn, function () { return pre.innerText.trim(); });
  });

  // Tabs: <div class="tabs" data-remember="os"> with .tab-list buttons [data-tab] and panels [data-panel].
  function guessOS() {
    var ua = navigator.userAgent || "";
    if (/iPhone|iPad|Android/i.test(ua)) return "phone";
    if (/Mac/i.test(ua)) return "mac";
    if (/Win/i.test(ua)) return "windows";
    if (/Linux|X11/i.test(ua)) return "linux";
    return null;
  }
  document.querySelectorAll(".tabs").forEach(function (tabs) {
    var key = tabs.getAttribute("data-remember");
    var buttons = tabs.querySelectorAll(".tab-list button");
    function select(name) {
      var found = false;
      buttons.forEach(function (b) {
        var on = b.getAttribute("data-tab") === name;
        if (on) found = true;
        b.setAttribute("aria-selected", on ? "true" : "false");
      });
      if (!found) return false;
      tabs.querySelectorAll("[data-panel]").forEach(function (p) {
        p.hidden = p.getAttribute("data-panel") !== name;
      });
      if (key) { try { localStorage.setItem("kit-tab-" + key, name); } catch (e) {} }
      return true;
    }
    buttons.forEach(function (b) {
      b.setAttribute("role", "tab");
      b.addEventListener("click", function () { select(b.getAttribute("data-tab")); });
    });
    var saved = null;
    if (key) { try { saved = localStorage.getItem("kit-tab-" + key); } catch (e) {} }
    if (!(saved && select(saved)) && !(key === "os" && select(guessOS()))) {
      select(buttons[0].getAttribute("data-tab"));
    }
  });
})();
