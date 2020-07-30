(window["webpackJsonp"] = window["webpackJsonp"] || []).push([[36],{

/***/ "./node_modules/@ionic/core/dist/esm-es5/focus-visible-15ada7f7.js":
/*!*************************************************************************!*\
  !*** ./node_modules/@ionic/core/dist/esm-es5/focus-visible-15ada7f7.js ***!
  \*************************************************************************/
/*! exports provided: startFocusVisible */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"startFocusVisible\", function() { return startFocusVisible; });\nvar ION_FOCUSED = 'ion-focused';\nvar ION_FOCUSABLE = 'ion-focusable';\nvar FOCUS_KEYS = ['Tab', 'ArrowDown', 'Space', 'Escape', ' ', 'Shift', 'Enter', 'ArrowLeft', 'ArrowRight', 'ArrowUp'];\nvar startFocusVisible = function () {\n    var currentFocus = [];\n    var keyboardMode = true;\n    var doc = document;\n    var setFocus = function (elements) {\n        currentFocus.forEach(function (el) { return el.classList.remove(ION_FOCUSED); });\n        elements.forEach(function (el) { return el.classList.add(ION_FOCUSED); });\n        currentFocus = elements;\n    };\n    var pointerDown = function () {\n        keyboardMode = false;\n        setFocus([]);\n    };\n    doc.addEventListener('keydown', function (ev) {\n        keyboardMode = FOCUS_KEYS.includes(ev.key);\n        if (!keyboardMode) {\n            setFocus([]);\n        }\n    });\n    doc.addEventListener('focusin', function (ev) {\n        if (keyboardMode && ev.composedPath) {\n            var toFocus = ev.composedPath().filter(function (el) {\n                if (el.classList) {\n                    return el.classList.contains(ION_FOCUSABLE);\n                }\n                return false;\n            });\n            setFocus(toFocus);\n        }\n    });\n    doc.addEventListener('focusout', function () {\n        if (doc.activeElement === doc.body) {\n            setFocus([]);\n        }\n    });\n    doc.addEventListener('touchstart', pointerDown);\n    doc.addEventListener('mousedown', pointerDown);\n};\n\n\n\n//# sourceURL=webpack:///./node_modules/@ionic/core/dist/esm-es5/focus-visible-15ada7f7.js?");

/***/ })

}]);