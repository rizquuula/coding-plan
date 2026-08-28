// Client-side filter and column sort. The tables render fully without this file.
(function () {
  "use strict";

  var tables = Array.prototype.slice.call(document.querySelectorAll(".data-table"));

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

  function filterTables(query) {
    var needle = query.trim().toLowerCase();
    tables.forEach(function (table) {
      var visible = 0;
      rowGroups(table).forEach(function (group) {
        var match = !needle || group[0].textContent.toLowerCase().indexOf(needle) !== -1;
        group.forEach(function (row) {
          row.hidden = !match;
        });
        if (match) visible += 1;
      });
      var section = table.closest("section");
      if (section) section.hidden = visible === 0;
    });
  }

  var input = document.getElementById("filter");
  if (input) {
    input.addEventListener("input", function () {
      filterTables(input.value);
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

  tables.forEach(function (table) {
    var headers = Array.prototype.slice.call(table.tHead.rows[0].cells);
    headers.forEach(function (header, index) {
      header.setAttribute("role", "button");
      header.setAttribute("tabindex", "0");

      function sort() {
        var ascending = header.getAttribute("aria-sort") !== "ascending";
        headers.forEach(function (other) {
          other.removeAttribute("aria-sort");
        });
        header.setAttribute("aria-sort", ascending ? "ascending" : "descending");

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
      }

      header.addEventListener("click", sort);
      header.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          sort();
        }
      });
    });
  });
})();
