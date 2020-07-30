(window["webpackJsonp"] = window["webpackJsonp"] || []).push([[33],{

/***/ "./node_modules/@ionic/core/dist/esm-es5/ion-text.entry.js":
/*!*****************************************************************!*\
  !*** ./node_modules/@ionic/core/dist/esm-es5/ion-text.entry.js ***!
  \*****************************************************************/
/*! exports provided: ion_text */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"ion_text\", function() { return Text; });\n/* harmony import */ var _index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./index-44bf8136.js */ \"./node_modules/@ionic/core/dist/esm-es5/index-44bf8136.js\");\n/* harmony import */ var _ionic_global_837be8f3_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./ionic-global-837be8f3.js */ \"./node_modules/@ionic/core/dist/esm-es5/ionic-global-837be8f3.js\");\n/* harmony import */ var _theme_3f0b0c04_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./theme-3f0b0c04.js */ \"./node_modules/@ionic/core/dist/esm-es5/theme-3f0b0c04.js\");\n\n\n\nvar textCss = \":host(.ion-color){color:var(--ion-color-base)}\";\nvar Text = /** @class */ (function () {\n    function Text(hostRef) {\n        Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"r\"])(this, hostRef);\n    }\n    Text.prototype.render = function () {\n        var _a;\n        var mode = Object(_ionic_global_837be8f3_js__WEBPACK_IMPORTED_MODULE_1__[\"b\"])(this);\n        return (Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"h\"])(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"H\"], { class: Object.assign(Object.assign({}, Object(_theme_3f0b0c04_js__WEBPACK_IMPORTED_MODULE_2__[\"c\"])(this.color)), (_a = {}, _a[mode] = true, _a)) }, Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"h\"])(\"slot\", null)));\n    };\n    return Text;\n}());\nText.style = textCss;\n\n\n\n//# sourceURL=webpack:///./node_modules/@ionic/core/dist/esm-es5/ion-text.entry.js?");

/***/ }),

/***/ "./node_modules/@ionic/core/dist/esm-es5/theme-3f0b0c04.js":
/*!*****************************************************************!*\
  !*** ./node_modules/@ionic/core/dist/esm-es5/theme-3f0b0c04.js ***!
  \*****************************************************************/
/*! exports provided: c, g, h, o */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"c\", function() { return createColorClasses; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"g\", function() { return getClassMap; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"h\", function() { return hostContext; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"o\", function() { return openURL; });\n/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ \"./node_modules/tslib/tslib.es6.js\");\n\nvar hostContext = function (selector, el) {\n    return el.closest(selector) !== null;\n};\n/**\n * Create the mode and color classes for the component based on the classes passed in\n */\nvar createColorClasses = function (color) {\n    var _a;\n    return (typeof color === 'string' && color.length > 0) ? (_a = {\n            'ion-color': true\n        },\n        _a[\"ion-color-\" + color] = true,\n        _a) : undefined;\n};\nvar getClassList = function (classes) {\n    if (classes !== undefined) {\n        var array = Array.isArray(classes) ? classes : classes.split(' ');\n        return array\n            .filter(function (c) { return c != null; })\n            .map(function (c) { return c.trim(); })\n            .filter(function (c) { return c !== ''; });\n    }\n    return [];\n};\nvar getClassMap = function (classes) {\n    var map = {};\n    getClassList(classes).forEach(function (c) { return map[c] = true; });\n    return map;\n};\nvar SCHEME = /^[a-z][a-z0-9+\\-.]*:/;\nvar openURL = function (url, ev, direction, animation) { return Object(tslib__WEBPACK_IMPORTED_MODULE_0__[\"__awaiter\"])(void 0, void 0, void 0, function () {\n    var router;\n    return Object(tslib__WEBPACK_IMPORTED_MODULE_0__[\"__generator\"])(this, function (_a) {\n        if (url != null && url[0] !== '#' && !SCHEME.test(url)) {\n            router = document.querySelector('ion-router');\n            if (router) {\n                if (ev != null) {\n                    ev.preventDefault();\n                }\n                return [2 /*return*/, router.push(url, direction, animation)];\n            }\n        }\n        return [2 /*return*/, false];\n    });\n}); };\n\n\n\n//# sourceURL=webpack:///./node_modules/@ionic/core/dist/esm-es5/theme-3f0b0c04.js?");

/***/ })

}]);