// Theme switcher. Auto follows the system, Light and Dark override it.
(function () {
  "use strict";

  var STORAGE_KEY = "theme";
  var buttons = Array.prototype.slice.call(
    document.querySelectorAll("[data-theme-choice]")
  );
  if (!buttons.length) return;

  function readChoice() {
    try {
      var stored = localStorage.getItem(STORAGE_KEY);
      return stored === "light" || stored === "dark" ? stored : "auto";
    } catch (error) {
      return "auto";
    }
  }

  function writeChoice(choice) {
    try {
      if (choice === "auto") {
        localStorage.removeItem(STORAGE_KEY);
      } else {
        localStorage.setItem(STORAGE_KEY, choice);
      }
    } catch (error) {
      /* Storage is blocked. The choice still applies to this page. */
    }
  }

  function apply(choice) {
    if (choice === "auto") {
      document.documentElement.removeAttribute("data-theme");
    } else {
      document.documentElement.setAttribute("data-theme", choice);
    }
    buttons.forEach(function (button) {
      var pressed = button.getAttribute("data-theme-choice") === choice;
      button.setAttribute("aria-pressed", pressed ? "true" : "false");
    });
  }

  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      var choice = button.getAttribute("data-theme-choice");
      writeChoice(choice);
      apply(choice);
    });
  });

  apply(readChoice());
})();

// Motion runtime. Loads anime.js only for a reader who did not ask for less motion.
// Every other block treats motion as decoration and works without it.
(function () {
  "use strict";

  var CARD_QUERY = "(max-width: 719.98px)";
  var REDUCE_QUERY = "(prefers-reduced-motion: reduce)";
  var waiting = [];

  var runtime = {
    ready: false,
    lib: null,
    cardQuery: window.matchMedia ? window.matchMedia(CARD_QUERY) : null,

    // True while the card layout applies. The media query is the single source of truth.
    cards: function () {
      return runtime.cardQuery ? runtime.cardQuery.matches : false;
    },

    // Run the callback once anime.js is ready. It never runs when the file never loads.
    onReady: function (callback) {
      if (runtime.ready) {
        callback(runtime.lib);
      } else {
        waiting.push(callback);
      }
    },

    // Safari before 14 only has the deprecated listener API.
    watch: function (query, handler) {
      if (!query) return;
      if (query.addEventListener) {
        query.addEventListener("change", handler);
      } else if (query.addListener) {
        query.addListener(handler);
      }
    }
  };

  window.PageMotion = runtime;

  function startMotion() {
    if (!window.anime || !window.anime.animate) return;
    runtime.lib = window.anime;
    runtime.ready = true;
    document.documentElement.classList.add("motion-ready");
    waiting.forEach(function (callback) {
      callback(runtime.lib);
    });
    waiting.length = 0;
  }

  if (!window.matchMedia) return;
  var motionOK = window.matchMedia(REDUCE_QUERY).matches === false;
  if (!motionOK) return;

  var script = document.createElement("script");
  script.src = "assets/anime.umd.min.js";
  script.defer = true;
  script.onload = startMotion;
  script.onerror = function () {
    /* Leave the page in its static state. */
  };
  document.head.appendChild(script);
})();

// Sidebar disclosure. Only the narrow layout collapses the panel.
(function () {
  "use strict";

  var motion = window.PageMotion;
  var sidebar = document.querySelector(".sidebar");
  var toggle = document.getElementById("nav-toggle");
  var panel = document.getElementById("sidebar-panel");
  if (!sidebar || !toggle) return;

  sidebar.setAttribute("data-nav", "js");

  // The panel slides when anime.js is ready. Otherwise the class alone switches it.
  function animatePanel(open) {
    var lib = motion && motion.ready ? motion.lib : null;
    if (!lib || !panel) return;

    lib.utils.remove(panel);
    if (open) {
      panel.style.height = "0px";
      var target = panel.scrollHeight;
      lib.animate(panel, {
        height: ["0px", target + "px"],
        duration: 220,
        ease: "outQuad",
        onComplete: function () {
          panel.style.height = "auto";
        }
      });
    } else {
      lib.animate(panel, {
        height: [panel.scrollHeight + "px", "0px"],
        duration: 180,
        ease: "outQuad",
        onComplete: function () {
          sidebar.classList.remove("is-open");
          panel.style.height = "";
        }
      });
    }
  }

  function setOpen(open) {
    var animated = !!(motion && motion.ready && panel);
    if (open) {
      sidebar.classList.add("is-open");
    } else if (!animated) {
      sidebar.classList.remove("is-open");
    }
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    animatePanel(open);
  }

  toggle.addEventListener("click", function () {
    setOpen(!sidebar.classList.contains("is-open"));
  });

  // A jump to a provider block closes the panel again.
  sidebar.addEventListener("click", function (event) {
    var link = event.target.closest("a");
    if (!link || !sidebar.classList.contains("is-open")) return;
    setOpen(false);
  });
})();

// Empty cell marking. A cell holding only an em dash is noise in the card layout.
(function () {
  "use strict";

  var EM_DASH = "—";
  var tables = Array.prototype.slice.call(document.querySelectorAll(".data-table"));

  tables.forEach(function (table) {
    if (!table.tBodies.length) return;
    var cells = Array.prototype.slice.call(table.tBodies[0].querySelectorAll("td"));
    cells.forEach(function (cell) {
      if (cell.classList.contains("cell-title")) return;
      if (cell.textContent.trim() === EM_DASH) cell.setAttribute("data-empty", "");
    });
  });
})();

// Client-side filter and column sort. The tables render fully without this file.
// The card layout hides the header row, so a select and a direction button replace it.
(function () {
  "use strict";

  var motion = window.PageMotion;
  var FILTER_DELAY = 120;
  var controlId = 0;

  function slice(list) {
    return Array.prototype.slice.call(list);
  }

  function anime() {
    return motion && motion.ready ? motion.lib : null;
  }

  var tables = slice(document.querySelectorAll(".data-table"));
  if (!tables.length) return;

  // One record per table. It survives the card-mode teardown, so the sort sticks.
  var states = tables.map(function (table) {
    return { table: table, index: 0, ascending: true, control: null, select: null, button: null };
  });

  function stateOf(table) {
    for (var i = 0; i < states.length; i += 1) {
      if (states[i].table === table) return states[i];
    }
    return null;
  }

  // A note row belongs to the data row directly above it.
  function rowGroups(table) {
    var groups = [];
    Array.prototype.forEach.call(table.tBodies[0].rows, function (row) {
      if (row.classList.contains("note-row") && groups.length) {
        groups[groups.length - 1].push(row);
      } else {
        groups.push([row]);
      }
    });
    return groups;
  }

  // Row text never changes, so cache it before the collapse button adds its label.
  var rowText = [];
  var rowTextIndex = "data-filter-key";
  tables.forEach(function (table) {
    if (!table.tBodies.length) return;
    slice(table.tBodies[0].rows).forEach(function (row) {
      row.setAttribute(rowTextIndex, String(rowText.length));
      rowText.push(row.textContent.toLowerCase());
    });
  });

  function textOf(row) {
    var key = row.getAttribute(rowTextIndex);
    return key === null ? row.textContent.toLowerCase() : rowText[key];
  }

  // The provider name is a heading now, so read it from the enclosing block.
  function providerName(table) {
    var block = table.closest(".provider-block");
    var heading = block && block.querySelector(".provider-name");
    return heading ? heading.textContent.toLowerCase() : "";
  }

  // A row settles into the state the last filter pass asked for, whatever ran before it.
  function settle(row) {
    row.hidden = row.getAttribute("data-filter-hidden") === "1";
    row.style.opacity = "";
    row.style.transform = "";
  }

  function clearPending(row) {
    row.removeAttribute("data-motion");
  }

  function moveRows(toShow, toHide) {
    var lib = anime();
    if (!lib) {
      toShow.concat(toHide).forEach(settle);
      return;
    }

    var all = toShow.concat(toHide);
    if (all.length) lib.utils.remove(all);

    if (toShow.length) {
      toShow.forEach(function (row) {
        row.hidden = false;
        clearPending(row);
      });
      lib.animate(toShow, {
        opacity: [0, 1],
        translateY: [4, 0],
        duration: 180,
        ease: "outQuad",
        onComplete: function () {
          toShow.forEach(settle);
        }
      });
    }

    if (toHide.length) {
      lib.animate(toHide, {
        opacity: [1, 0],
        translateY: [0, -4],
        duration: 140,
        ease: "outQuad",
        onComplete: function () {
          toHide.forEach(settle);
        }
      });
    }
  }

  function filterTables(query) {
    var needle = query.trim().toLowerCase();
    var sections = [];
    var toShow = [];
    var toHide = [];
    var animated = !!anime();

    tables.forEach(function (table) {
      var provider = providerName(table);
      var visible = 0;
      rowGroups(table).forEach(function (group) {
        var haystack = textOf(group[0]) + " " + provider;
        var match = !needle || haystack.indexOf(needle) !== -1;
        group.forEach(function (row) {
          row.setAttribute("data-filter-hidden", match ? "0" : "1");
          if (!animated) {
            row.hidden = !match;
          } else if (match && row.hidden) {
            toShow.push(row);
          } else if (!match && !row.hidden) {
            toHide.push(row);
          }
        });
        if (match) visible += 1;
      });

      var block = table.closest(".provider-block");
      if (block) block.hidden = visible === 0;

      var section = table.closest("section");
      if (section) {
        if (sections.indexOf(section) === -1) sections.push(section);
        if (visible > 0) section.dataset.visibleTables = "1";
      }
    });

    // A section stays visible while at least one provider block still matches.
    sections.forEach(function (section) {
      section.hidden = section.dataset.visibleTables !== "1";
      delete section.dataset.visibleTables;
    });

    if (animated) moveRows(toShow, toHide);
  }

  var input = document.getElementById("filter");
  if (input) {
    var timer = null;
    input.addEventListener("input", function () {
      if (timer) window.clearTimeout(timer);
      timer = window.setTimeout(function () {
        timer = null;
        filterTables(input.value);
      }, FILTER_DELAY);
    });
  }

  function sortKey(cell) {
    var text = cell.textContent.trim();
    var numeric = text.replace(/[^0-9.\-]/g, "");
    if (numeric && /[0-9]/.test(numeric)) {
      var value = parseFloat(numeric);
      if (!isNaN(value)) return value;
    }
    return text.toLowerCase();
  }

  function headerCells(table) {
    return table.tHead ? slice(table.tHead.rows[0].cells) : [];
  }

  // The reordered rows fade back in, so the jump reads as a move rather than a flicker.
  function animateSort(table) {
    var lib = anime();
    if (!lib) return;
    var rows = slice(table.tBodies[0].rows).filter(function (row) {
      return !row.hidden;
    });
    if (!rows.length) return;

    lib.utils.remove(rows);
    rows.forEach(clearPending);
    var step = rows.length > 1 ? Math.min(18, 240 / (rows.length - 1)) : 0;
    lib.animate(rows, {
      opacity: [0, 1],
      translateY: [6, 0],
      duration: 220,
      ease: "outQuad",
      delay: lib.stagger(step),
      onComplete: function () {
        rows.forEach(settle);
      }
    });
  }

  // The one sort path. The header click and the card control both call it.
  function sortTable(table, index, ascending) {
    var state = stateOf(table);
    var headers = headerCells(table);
    if (index < 0 || index >= headers.length) return;

    headers.forEach(function (header) {
      header.removeAttribute("aria-sort");
    });
    headers[index].setAttribute("aria-sort", ascending ? "ascending" : "descending");

    var groups = rowGroups(table);
    groups.sort(function (a, b) {
      var left = sortKey(a[0].cells[index]);
      var right = sortKey(b[0].cells[index]);
      if (left < right) return ascending ? -1 : 1;
      if (left > right) return ascending ? 1 : -1;
      return 0;
    });

    var body = table.tBodies[0];
    groups.forEach(function (group) {
      group.forEach(function (row) {
        body.appendChild(row);
      });
    });

    if (state) {
      state.index = index;
      state.ascending = ascending;
      syncControl(state);
    }
    animateSort(table);
  }

  function directionLabel(ascending) {
    return ascending ? "↑ A–Z" : "↓ Z–A";
  }

  function syncControl(state) {
    if (!state.control) return;
    state.select.value = String(state.index);
    state.button.textContent = directionLabel(state.ascending);
    state.button.setAttribute("aria-pressed", state.ascending ? "false" : "true");
    state.button.setAttribute(
      "aria-label",
      state.ascending ? "Sort direction: ascending" : "Sort direction: descending"
    );
  }

  function buildControl(state) {
    if (state.control) return;
    var table = state.table;
    var wrap = table.closest(".table-wrap");
    var headers = headerCells(table);
    if (!wrap || !wrap.parentNode || !headers.length) return;

    controlId += 1;
    var control = document.createElement("div");
    control.className = "card-sort";

    var label = document.createElement("label");
    label.className = "card-sort-label";
    label.htmlFor = "card-sort-" + controlId;
    label.textContent = "Sort by";

    var select = document.createElement("select");
    select.id = "card-sort-" + controlId;
    select.className = "card-sort-select";
    headers.forEach(function (header, index) {
      var option = document.createElement("option");
      option.value = String(index);
      option.textContent = header.textContent.trim() || "Column " + (index + 1);
      select.appendChild(option);
    });

    var button = document.createElement("button");
    button.type = "button";
    button.className = "card-sort-dir";

    select.addEventListener("change", function () {
      sortTable(table, parseInt(select.value, 10) || 0, state.ascending);
    });
    button.addEventListener("click", function () {
      sortTable(table, state.index, !state.ascending);
    });

    control.appendChild(label);
    control.appendChild(select);
    control.appendChild(button);
    wrap.parentNode.insertBefore(control, wrap);

    state.control = control;
    state.select = select;
    state.button = button;
    syncControl(state);
  }

  function removeControl(state) {
    if (!state.control) return;
    if (state.control.parentNode) state.control.parentNode.removeChild(state.control);
    state.control = null;
    state.select = null;
    state.button = null;
  }

  function syncCardMode() {
    var cards = motion ? motion.cards() : false;
    states.forEach(function (state) {
      if (cards) {
        buildControl(state);
      } else {
        removeControl(state);
      }
    });
  }

  // The header row keeps its own click and keyboard sort on every viewport.
  tables.forEach(function (table) {
    headerCells(table).forEach(function (header, index) {
      header.setAttribute("role", "button");
      header.setAttribute("tabindex", "0");

      function run() {
        sortTable(table, index, header.getAttribute("aria-sort") !== "ascending");
      }

      header.addEventListener("click", run);
      header.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          run();
        }
      });
    });
  });

  if (motion) motion.watch(motion.cardQuery, syncCardMode);
  syncCardMode();
})();

// Card collapse. A wide row becomes a tall card, so hide the tail behind one button.
(function () {
  "use strict";

  var motion = window.PageMotion;
  var VISIBLE_CELLS = 6;

  function slice(list) {
    return Array.prototype.slice.call(list);
  }

  var rows = [];
  slice(document.querySelectorAll(".data-table")).forEach(function (table) {
    if (!table.tBodies.length) return;
    slice(table.tBodies[0].rows).forEach(function (row) {
      if (!row.classList.contains("note-row")) rows.push(row);
    });
  });
  if (!rows.length) return;

  function valueCells(row) {
    return slice(row.cells).filter(function (cell) {
      return !cell.classList.contains("cell-title") && !cell.hasAttribute("data-empty");
    });
  }

  function setExpanded(row, button, expanded) {
    if (expanded) {
      row.classList.remove("is-collapsed");
    } else {
      row.classList.add("is-collapsed");
    }
    button.textContent = expanded ? "Show less" : "Show all";
    button.setAttribute("aria-expanded", expanded ? "true" : "false");
  }

  // The card grows and shrinks instead of jumping when anime.js is ready.
  function toggle(row, button) {
    var expanded = row.classList.contains("is-collapsed");
    var lib = motion && motion.ready ? motion.lib : null;
    if (!lib) {
      setExpanded(row, button, expanded);
      return;
    }

    var from = row.getBoundingClientRect().height;
    lib.utils.remove(row);
    row.style.height = "";
    setExpanded(row, button, expanded);
    var to = row.getBoundingClientRect().height;
    if (!from || !to || Math.abs(to - from) < 1) return;

    row.style.overflow = "hidden";
    lib.animate(row, {
      height: [from + "px", to + "px"],
      duration: 220,
      ease: "outQuad",
      onComplete: function () {
        row.style.height = "";
        row.style.overflow = "";
      }
    });
  }

  function build(row) {
    if (row.getAttribute("data-collapsible") === "1") return;
    var cells = valueCells(row);
    if (cells.length <= VISIBLE_CELLS) return;
    var last = row.cells[row.cells.length - 1];
    if (!last) return;

    cells.slice(VISIBLE_CELLS).forEach(function (cell) {
      cell.setAttribute("data-overflow", "");
    });
    row.classList.add("is-collapsed");
    row.setAttribute("data-collapsible", "1");

    var button = document.createElement("button");
    button.type = "button";
    button.className = "card-more";
    button.textContent = "Show all";
    button.setAttribute("aria-expanded", "false");
    button.addEventListener("click", function () {
      toggle(row, button);
    });
    last.appendChild(button);
  }

  function teardown(row) {
    if (row.getAttribute("data-collapsible") !== "1") return;
    row.removeAttribute("data-collapsible");
    row.classList.remove("is-collapsed");
    row.style.height = "";
    row.style.overflow = "";
    slice(row.querySelectorAll("[data-overflow]")).forEach(function (cell) {
      cell.removeAttribute("data-overflow");
    });
    var button = row.querySelector(".card-more");
    if (button && button.parentNode) button.parentNode.removeChild(button);
  }

  function syncCardMode() {
    var cards = motion ? motion.cards() : false;
    rows.forEach(cards ? build : teardown);
  }

  if (motion) motion.watch(motion.cardQuery, syncCardMode);
  syncCardMode();
})();

// Row entrance. One observer per provider block keeps a 114-row page cheap.
(function () {
  "use strict";

  var motion = window.PageMotion;
  if (!motion || !window.IntersectionObserver) return;

  var DURATION = 320;
  var BUDGET = 600;

  function slice(list) {
    return Array.prototype.slice.call(list);
  }

  motion.onReady(function (lib) {
    var blocks = slice(document.querySelectorAll(".provider-block"));
    // The changelog page has no provider block, so fall back to its table.
    if (!blocks.length) blocks = slice(document.querySelectorAll(".table-wrap"));
    if (!blocks.length) return;

    function rowsOf(block) {
      return slice(block.querySelectorAll("tbody tr")).filter(function (row) {
        return row.getAttribute("data-motion") === "pending";
      });
    }

    blocks.forEach(function (block) {
      slice(block.querySelectorAll("tbody tr")).forEach(function (row) {
        row.setAttribute("data-motion", "pending");
      });
    });

    function reveal(block) {
      var rows = rowsOf(block);
      if (!rows.length) return;
      var step = rows.length > 1 ? Math.min(28, (BUDGET - DURATION) / (rows.length - 1)) : 0;

      // Each row drops its pending flag at its own finish time.
      rows.forEach(function (row, index) {
        window.setTimeout(function () {
          row.removeAttribute("data-motion");
        }, index * step + DURATION);
      });

      lib.animate(rows, {
        opacity: [0, 1],
        translateY: [8, 0],
        duration: DURATION,
        ease: "outQuad",
        delay: lib.stagger(step),
        onComplete: function () {
          rows.forEach(function (row) {
            row.removeAttribute("data-motion");
            row.style.opacity = "";
            row.style.transform = "";
          });
        }
      });
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          observer.unobserve(entry.target);
          reveal(entry.target);
        });
      },
      { rootMargin: "80px 0px" }
    );

    blocks.forEach(function (block) {
      observer.observe(block);
    });
  });
})();
