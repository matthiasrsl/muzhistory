(window["webpackJsonp"] = window["webpackJsonp"] || []).push([[13],{

/***/ "./node_modules/@ionic/core/dist/esm-es5/ion-avatar_3.entry.js":
/*!*********************************************************************!*\
  !*** ./node_modules/@ionic/core/dist/esm-es5/ion-avatar_3.entry.js ***!
  \*********************************************************************/
/*! exports provided: ion_avatar, ion_badge, ion_thumbnail */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"ion_avatar\", function() { return Avatar; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"ion_badge\", function() { return Badge; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"ion_thumbnail\", function() { return Thumbnail; });\n/* harmony import */ var _index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./index-44bf8136.js */ \"./node_modules/@ionic/core/dist/esm-es5/index-44bf8136.js\");\n/* harmony import */ var _ionic_global_837be8f3_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./ionic-global-837be8f3.js */ \"./node_modules/@ionic/core/dist/esm-es5/ionic-global-837be8f3.js\");\n/* harmony import */ var _theme_3f0b0c04_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./theme-3f0b0c04.js */ \"./node_modules/@ionic/core/dist/esm-es5/theme-3f0b0c04.js\");\n\n\n\nvar avatarIosCss = \":host{border-radius:var(--border-radius);display:block}::slotted(ion-img),::slotted(img){border-radius:var(--border-radius);width:100%;height:100%;-o-object-fit:cover;object-fit:cover;overflow:hidden}:host{--border-radius:50%;width:48px;height:48px}\";\nvar avatarMdCss = \":host{border-radius:var(--border-radius);display:block}::slotted(ion-img),::slotted(img){border-radius:var(--border-radius);width:100%;height:100%;-o-object-fit:cover;object-fit:cover;overflow:hidden}:host{--border-radius:50%;width:64px;height:64px}\";\nvar Avatar = /** @class */ (function () {\n    function Avatar(hostRef) {\n        Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"r\"])(this, hostRef);\n    }\n    Avatar.prototype.render = function () {\n        return (Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"h\"])(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"H\"], { class: Object(_ionic_global_837be8f3_js__WEBPACK_IMPORTED_MODULE_1__[\"b\"])(this) }, Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"h\"])(\"slot\", null)));\n    };\n    return Avatar;\n}());\nAvatar.style = {\n    ios: avatarIosCss,\n    md: avatarMdCss\n};\nvar badgeIosCss = \":host{--background:var(--ion-color-primary, #3880ff);--color:var(--ion-color-primary-contrast, #fff);--padding-top:3px;--padding-end:8px;--padding-bottom:3px;--padding-start:8px;-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;padding-left:var(--padding-start);padding-right:var(--padding-end);padding-top:var(--padding-top);padding-bottom:var(--padding-bottom);display:inline-block;min-width:10px;background:var(--background);color:var(--color);font-family:var(--ion-font-family, inherit);font-size:13px;font-weight:bold;line-height:1;text-align:center;white-space:nowrap;contain:content;vertical-align:baseline}@supports ((-webkit-margin-start: 0) or (margin-inline-start: 0)) or (-webkit-margin-start: 0){:host{padding-left:unset;padding-right:unset;-webkit-padding-start:var(--padding-start);padding-inline-start:var(--padding-start);-webkit-padding-end:var(--padding-end);padding-inline-end:var(--padding-end)}}:host(.ion-color){background:var(--ion-color-base);color:var(--ion-color-contrast)}:host(:empty){display:none}:host{border-radius:10px}\";\nvar badgeMdCss = \":host{--background:var(--ion-color-primary, #3880ff);--color:var(--ion-color-primary-contrast, #fff);--padding-top:3px;--padding-end:8px;--padding-bottom:3px;--padding-start:8px;-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;padding-left:var(--padding-start);padding-right:var(--padding-end);padding-top:var(--padding-top);padding-bottom:var(--padding-bottom);display:inline-block;min-width:10px;background:var(--background);color:var(--color);font-family:var(--ion-font-family, inherit);font-size:13px;font-weight:bold;line-height:1;text-align:center;white-space:nowrap;contain:content;vertical-align:baseline}@supports ((-webkit-margin-start: 0) or (margin-inline-start: 0)) or (-webkit-margin-start: 0){:host{padding-left:unset;padding-right:unset;-webkit-padding-start:var(--padding-start);padding-inline-start:var(--padding-start);-webkit-padding-end:var(--padding-end);padding-inline-end:var(--padding-end)}}:host(.ion-color){background:var(--ion-color-base);color:var(--ion-color-contrast)}:host(:empty){display:none}:host{--padding-top:3px;--padding-end:4px;--padding-bottom:4px;--padding-start:4px;border-radius:4px}\";\nvar Badge = /** @class */ (function () {\n    function Badge(hostRef) {\n        Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"r\"])(this, hostRef);\n    }\n    Badge.prototype.render = function () {\n        var _a;\n        var mode = Object(_ionic_global_837be8f3_js__WEBPACK_IMPORTED_MODULE_1__[\"b\"])(this);\n        return (Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"h\"])(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"H\"], { class: Object.assign(Object.assign({}, Object(_theme_3f0b0c04_js__WEBPACK_IMPORTED_MODULE_2__[\"c\"])(this.color)), (_a = {}, _a[mode] = true, _a)) }, Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"h\"])(\"slot\", null)));\n    };\n    return Badge;\n}());\nBadge.style = {\n    ios: badgeIosCss,\n    md: badgeMdCss\n};\nvar thumbnailCss = \":host{--size:48px;--border-radius:0;border-radius:var(--border-radius);display:block;width:var(--size);height:var(--size)}::slotted(ion-img),::slotted(img){border-radius:var(--border-radius);width:100%;height:100%;-o-object-fit:cover;object-fit:cover;overflow:hidden}\";\nvar Thumbnail = /** @class */ (function () {\n    function Thumbnail(hostRef) {\n        Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"r\"])(this, hostRef);\n    }\n    Thumbnail.prototype.render = function () {\n        return (Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"h\"])(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"H\"], { class: Object(_ionic_global_837be8f3_js__WEBPACK_IMPORTED_MODULE_1__[\"b\"])(this) }, Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"h\"])(\"slot\", null)));\n    };\n    return Thumbnail;\n}());\nThumbnail.style = thumbnailCss;\n\n\n\n//# sourceURL=webpack:///./node_modules/@ionic/core/dist/esm-es5/ion-avatar_3.entry.js?");

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