/**
 * SchnitzMenu front-end: table search + sort, jump-nav highlighting,
 * meal builder, print button and back-to-top. No dependencies.
 */
(function () {
	'use strict';

	var $$ = function (sel, root) {
		return Array.prototype.slice.call((root || document).querySelectorAll(sel));
	};

	/* ---------------------------------------------------------------- Search */
	function initSearch() {
		var input = document.getElementById('sm-search-input');
		if (!input) return;
		var status = document.querySelector('.sm-search__status');
		var rows = $$('.sm-table tbody tr[data-name]');

		input.addEventListener('input', function () {
			var q = input.value.trim().toLowerCase();
			var shown = 0;
			rows.forEach(function (row) {
				var match = !q || row.getAttribute('data-name').indexOf(q) !== -1;
				row.classList.toggle('sm-hidden', !match);
				if (match) shown++;
			});
			// Hide whole category blocks with nothing left in them.
			$$('.sm-table-block').forEach(function (block) {
				var visible = block.querySelectorAll('tbody tr:not(.sm-hidden)').length;
				block.classList.toggle('sm-hidden', !!q && !visible);
			});
			if (status) {
				status.textContent = q ? shown + (shown === 1 ? ' item matches' : ' items match') + ' "' + input.value.trim() + '"' : '';
			}
		});
	}

	/* ------------------------------------------------------------------ Sort */
	function cellValue(row, index) {
		var cell = row.children[index];
		if (!cell) return '';
		return cell.textContent.trim();
	}

	function initSort() {
		$$('table[data-sm-sortable]').forEach(function (table) {
			var headers = $$('thead th', table);
			headers.forEach(function (th, index) {
				if (!th.hasAttribute('data-sort')) return;
				th.setAttribute('tabindex', '0');
				th.setAttribute('role', 'button');
				var sort = function () {
					var dir = th.getAttribute('aria-sort') === 'ascending' ? 'descending' : 'ascending';
					headers.forEach(function (h) { h.removeAttribute('aria-sort'); });
					th.setAttribute('aria-sort', dir);
					var body = table.tBodies[0];
					var rows = Array.prototype.slice.call(body.rows);
					rows.sort(function (a, b) {
						var x = parseFloat(cellValue(a, index).replace(/[^0-9.]/g, ''));
						var y = parseFloat(cellValue(b, index).replace(/[^0-9.]/g, ''));
						// Unknown values always sink to the bottom.
						if (isNaN(x) && isNaN(y)) return 0;
						if (isNaN(x)) return 1;
						if (isNaN(y)) return -1;
						return dir === 'ascending' ? x - y : y - x;
					});
					rows.forEach(function (r) { body.appendChild(r); });
				};
				th.addEventListener('click', sort);
				th.addEventListener('keydown', function (e) {
					if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); sort(); }
				});
			});
		});
	}

	/* -------------------------------------------------------------- Jump nav */
	function initJumpNav() {
		var links = $$('.sm-jump a[href^="#"]');
		if (!links.length || !('IntersectionObserver' in window)) return;
		var byId = {};
		links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });

		var observer = new IntersectionObserver(function (entries) {
			entries.forEach(function (entry) {
				if (!entry.isIntersecting) return;
				links.forEach(function (a) { a.classList.remove('is-active'); });
				var active = byId[entry.target.id];
				if (active) {
					active.classList.add('is-active');
					active.scrollIntoView({ block: 'nearest', inline: 'center' });
				}
			});
		}, { rootMargin: '-30% 0px -60% 0px' });

		Object.keys(byId).forEach(function (id) {
			var target = document.getElementById(id);
			if (target) observer.observe(target);
		});
	}

	/* ---------------------------------------------------------- Meal builder */
	var STORE_KEY = 'smMeal';

	function loadMeal() {
		try { return JSON.parse(window.localStorage.getItem(STORE_KEY)) || []; } catch (e) { return []; }
	}
	function saveMeal(items) {
		try { window.localStorage.setItem(STORE_KEY, JSON.stringify(items)); } catch (e) { /* private mode */ }
	}

	function initBuilder() {
		var box = document.querySelector('.sm-builder');
		var buttons = $$('.sm-add');
		if (!box) return;
		var list = box.querySelector('.sm-builder__list');
		var priceEl = box.querySelector('.sm-builder__price');
		var kcalEl = box.querySelector('.sm-builder__kcal');
		var unknownEl = box.querySelector('.sm-builder__unknown');
		var meal = loadMeal();

		function render() {
			list.innerHTML = '';
			var price = 0, kcal = 0, unknown = 0;
			meal.forEach(function (item, i) {
				var li = document.createElement('li');
				var name = document.createElement('span');
				name.textContent = item.name;
				var remove = document.createElement('button');
				remove.type = 'button';
				remove.setAttribute('aria-label', 'Remove ' + item.name);
				remove.textContent = '×';
				remove.addEventListener('click', function () { meal.splice(i, 1); update(); });
				li.appendChild(name);
				li.appendChild(remove);
				list.appendChild(li);
				if (item.price !== null) { price += item.price; } else { unknown++; }
				if (item.kcal !== null) { kcal += item.kcal; } else { unknown++; }
			});
			priceEl.textContent = '$' + price.toFixed(2);
			kcalEl.textContent = Math.round(kcal).toLocaleString('en-AU');
			unknownEl.textContent = unknown ? ' + items not yet listed' : '';
			box.hidden = meal.length === 0;
		}
		function update() { saveMeal(meal); render(); }

		buttons.forEach(function (btn) {
			btn.addEventListener('click', function () {
				var row = btn.closest('tr');
				var num = function (v) { return v === '' || v === null ? null : parseFloat(v); };
				meal.push({
					name: row.querySelector('th').childNodes[0].textContent.trim(),
					price: num(row.getAttribute('data-price')),
					kcal: num(row.getAttribute('data-kcal'))
				});
				btn.classList.add('is-added');
				setTimeout(function () { btn.classList.remove('is-added'); }, 400);
				update();
			});
		});
		box.querySelector('.sm-builder__clear').addEventListener('click', function () { meal = []; update(); });
		render();
	}

	/* ------------------------------------------------------ Print + to top */
	function initMisc() {
		$$('.sm-print').forEach(function (btn) {
			btn.addEventListener('click', function () { window.print(); });
		});

		var top = document.querySelector('.sm-top');
		if (top) {
			var toggle = function () { top.hidden = window.scrollY < 600; };
			window.addEventListener('scroll', toggle, { passive: true });
			toggle();
			top.addEventListener('click', function (e) {
				e.preventDefault();
				window.scrollTo({ top: 0, behavior: 'smooth' });
			});
		}
	}

	function init() {
		initSearch();
		initSort();
		initJumpNav();
		initBuilder();
		initMisc();
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', init);
	} else {
		init();
	}
})();
