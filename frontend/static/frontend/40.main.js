(window["webpackJsonp"] = window["webpackJsonp"] || []).push([[40],{

/***/ "./node_modules/@ionic/core/dist/esm-es5/ion-img.entry.js":
/*!****************************************************************!*\
  !*** ./node_modules/@ionic/core/dist/esm-es5/ion-img.entry.js ***!
  \****************************************************************/
/*! exports provided: ion_img */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"ion_img\", function() { return Img; });\n/* harmony import */ var _index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./index-44bf8136.js */ \"./node_modules/@ionic/core/dist/esm-es5/index-44bf8136.js\");\n/* harmony import */ var _ionic_global_837be8f3_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./ionic-global-837be8f3.js */ \"./node_modules/@ionic/core/dist/esm-es5/ionic-global-837be8f3.js\");\n\n\nvar imgCss = \":host{display:block;-o-object-fit:contain;object-fit:contain}img{display:block;width:100%;height:100%;-o-object-fit:inherit;object-fit:inherit;-o-object-position:inherit;object-position:inherit}\";\nvar Img = /** @class */ (function () {\n    function Img(hostRef) {\n        var _this = this;\n        Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"r\"])(this, hostRef);\n        this.ionImgWillLoad = Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"e\"])(this, \"ionImgWillLoad\", 7);\n        this.ionImgDidLoad = Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"e\"])(this, \"ionImgDidLoad\", 7);\n        this.ionError = Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"e\"])(this, \"ionError\", 7);\n        this.onLoad = function () {\n            _this.ionImgDidLoad.emit();\n        };\n        this.onError = function () {\n            _this.ionError.emit();\n        };\n    }\n    Img.prototype.srcChanged = function () {\n        this.addIO();\n    };\n    Img.prototype.componentDidLoad = function () {\n        this.addIO();\n    };\n    Img.prototype.addIO = function () {\n        var _this = this;\n        if (this.src === undefined) {\n            return;\n        }\n        if (typeof window !== 'undefined' &&\n            'IntersectionObserver' in window &&\n            'IntersectionObserverEntry' in window &&\n            'isIntersecting' in window.IntersectionObserverEntry.prototype) {\n            this.removeIO();\n            this.io = new IntersectionObserver(function (data) {\n                // because there will only ever be one instance\n                // of the element we are observing\n                // we can just use data[0]\n                if (data[0].isIntersecting) {\n                    _this.load();\n                    _this.removeIO();\n                }\n            });\n            this.io.observe(this.el);\n        }\n        else {\n            // fall back to setTimeout for Safari and IE\n            setTimeout(function () { return _this.load(); }, 200);\n        }\n    };\n    Img.prototype.load = function () {\n        this.loadError = this.onError;\n        this.loadSrc = this.src;\n        this.ionImgWillLoad.emit();\n    };\n    Img.prototype.removeIO = function () {\n        if (this.io) {\n            this.io.disconnect();\n            this.io = undefined;\n        }\n    };\n    Img.prototype.render = function () {\n        return (Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"h\"])(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"H\"], { class: Object(_ionic_global_837be8f3_js__WEBPACK_IMPORTED_MODULE_1__[\"b\"])(this) }, Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"h\"])(\"img\", { decoding: \"async\", src: this.loadSrc, alt: this.alt, onLoad: this.onLoad, onError: this.loadError, part: \"image\" })));\n    };\n    Object.defineProperty(Img.prototype, \"el\", {\n        get: function () { return Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_0__[\"i\"])(this); },\n        enumerable: false,\n        configurable: true\n    });\n    Object.defineProperty(Img, \"watchers\", {\n        get: function () {\n            return {\n                \"src\": [\"srcChanged\"]\n            };\n        },\n        enumerable: false,\n        configurable: true\n    });\n    return Img;\n}());\nImg.style = imgCss;\n\n\n\n//# sourceURL=webpack:///./node_modules/@ionic/core/dist/esm-es5/ion-img.entry.js?");

/***/ })

}]);