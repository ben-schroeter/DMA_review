/* dc-lite: a small renderer for the interactive pages of the exported site (filters, toggles, the infographic viewer).
   The page holds its markup in <template id="dc-tpl">, with {{path}} holes, <template data-sc-if="{{x}}"> and
   <template data-sc-for="{{list}}" data-as="it"> blocks, and on*="{{handler}}" attributes; its logic (a class
   Component extending DCLogic, with renderVals() and setState()) is in <script id="dc-logic" type="text/plain">.
   Written for eutechlaws.org; no dependencies. */
(function () {
  "use strict";
  var tpl = document.getElementById("dc-tpl");
  var logicEl = document.getElementById("dc-logic");
  var root = document.getElementById("dc-root");
  if (!tpl || !root) return;

  var HOLE = /\{\{\s*([^}]*?)\s*\}\}/g;
  var ONLY = /^\s*\{\{\s*([^}]*?)\s*\}\}\s*$/;
  var PROPS = { checked: 1, selected: 1, disabled: 1, value: 1 };
  var pending = false, comp = null;

  function DCLogic(props) { this.props = props || {}; this.state = {}; }
  DCLogic.prototype.setState = function (u) {
    if (typeof u === "function") u = u(this.state);
    this.state = Object.assign({}, this.state, u);
    schedule();
  };

  function lookup(path, scope) {
    path = (path || "").trim();
    if (path === "true") return true;
    if (path === "false") return false;
    if (path === "") return undefined;
    var parts = path.split("."), v = scope;
    for (var i = 0; i < parts.length; i++) { if (v == null) return undefined; v = v[parts[i]]; }
    return v;
  }
  function interp(s, scope) {
    return s.replace(HOLE, function (_, p) { var v = lookup(p, scope); return v == null || v === false ? "" : String(v); });
  }
  function holeOf(s) { var m = ONLY.exec(s || ""); return m ? m[1] : (s || ""); }
  function truthy(v) { return Array.isArray(v) ? v.length > 0 : !!v; }

  function renderChildren(src, scope, out, post) {
    var kids = src.content ? src.content.childNodes : src.childNodes;
    for (var i = 0; i < kids.length; i++) renderNode(kids[i], scope, out, post);
  }

  function renderNode(n, scope, out, post) {
    if (n.nodeType === 3) { out.appendChild(document.createTextNode(n.nodeValue.indexOf("{{") < 0 ? n.nodeValue : interp(n.nodeValue, scope))); return; }
    if (n.nodeType !== 1) return;
    if (n.tagName === "TEMPLATE" && n.hasAttribute("data-sc-if")) {
      if (truthy(lookup(holeOf(n.getAttribute("data-sc-if")), scope))) renderChildren(n, scope, out, post);
      return;
    }
    if (n.tagName === "TEMPLATE" && n.hasAttribute("data-sc-for")) {
      var list = lookup(holeOf(n.getAttribute("data-sc-for")), scope) || [];
      var as = n.getAttribute("data-as") || "item";
      for (var k = 0; k < list.length; k++) {
        var s = Object.create(scope); s[as] = list[k]; s.index = k;
        renderChildren(n, s, out, post);
      }
      return;
    }
    var el = n.cloneNode(false);
    var attrs = Array.prototype.slice.call(n.attributes);
    for (var a = 0; a < attrs.length; a++) {
      var name = attrs[a].name, val = attrs[a].value, lname = name.toLowerCase();
      if (val.indexOf("{{") < 0) continue;
      el.removeAttribute(name);
      var only = ONLY.exec(val);
      if (lname.slice(0, 2) === "on" && only) {
        var fn = lookup(only[1], scope);
        if (typeof fn === "function") {
          var ev = lname.slice(2);
          var textish = el.tagName === "TEXTAREA" || (el.tagName === "INPUT" && !/^(checkbox|radio|file|submit|button)$/i.test(el.type));
          if (ev === "change" && textish) ev = "input";
          el.addEventListener(ev, fn);
        }
        continue;
      }
      if (only) {
        var v = lookup(only[1], scope);
        if (PROPS[lname]) { post.push([el, lname, v]); if (lname === "value" && v != null) el.setAttribute("value", String(v)); continue; }
        if (v == null || v === false || (v === "" && (lname === "src" || lname === "href"))) continue;
        el.setAttribute(name, v === true ? "" : String(v));
      } else {
        el.setAttribute(name, interp(val, scope));
      }
    }
    renderChildren(n, scope, el, post);
    out.appendChild(el);
  }

  function render() {
    pending = false;
    var vals = comp && comp.renderVals ? comp.renderVals() : {};
    var act = document.activeElement, focusId = null, selS = null, selE = null;
    if (act && act.id && root.contains(act)) {
      focusId = act.id;
      try { selS = act.selectionStart; selE = act.selectionEnd; } catch (e) { /* not a text field */ }
    }
    var frag = document.createDocumentFragment(), post = [];
    renderChildren(tpl, vals, frag, post);
    root.replaceChildren(frag);
    for (var i = 0; i < post.length; i++) {
      var el = post[i][0], prop = post[i][1], v = post[i][2];
      if (prop === "value") el.value = v == null ? "" : v; else el[prop] = !!v;
    }
    if (focusId) {
      var f = document.getElementById(focusId);
      if (f) { f.focus(); try { if (selS != null) f.setSelectionRange(selS, selE); } catch (e) { /* ignore */ } }
    }
  }
  function schedule() { if (!pending) { pending = true; (window.requestAnimationFrame || setTimeout)(render); } }

  var props = {};
  if (logicEl) {
    try {
      var decl = JSON.parse(logicEl.getAttribute("data-props") || "{}");
      Object.keys(decl).forEach(function (k) { if (k.charAt(0) !== "$" && decl[k] && "default" in decl[k]) props[k] = decl[k].default; });
    } catch (e) { /* no props */ }
    var C = new Function("DCLogic", logicEl.textContent + "\n;return typeof Component !== 'undefined' ? Component : null;")(DCLogic);
    if (C) comp = new C(props);
  }
  render();
})();
