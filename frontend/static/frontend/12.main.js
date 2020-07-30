(window["webpackJsonp"] = window["webpackJsonp"] || []).push([[12],{

/***/ "./node_modules/@ionic/core/dist/esm-es5/haptic-7b8ba70a.js":
/*!******************************************************************!*\
  !*** ./node_modules/@ionic/core/dist/esm-es5/haptic-7b8ba70a.js ***!
  \******************************************************************/
/*! exports provided: a, b, c, d, h */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"a\", function() { return hapticSelectionStart; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"b\", function() { return hapticSelectionChanged; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"c\", function() { return hapticSelection; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"d\", function() { return hapticImpact; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"h\", function() { return hapticSelectionEnd; });\nvar HapticEngine = {\n    getEngine: function () {\n        var win = window;\n        return (win.TapticEngine) || (win.Capacitor && win.Capacitor.isPluginAvailable('Haptics') && win.Capacitor.Plugins.Haptics);\n    },\n    available: function () {\n        return !!this.getEngine();\n    },\n    isCordova: function () {\n        return !!window.TapticEngine;\n    },\n    isCapacitor: function () {\n        var win = window;\n        return !!win.Capacitor;\n    },\n    impact: function (options) {\n        var engine = this.getEngine();\n        if (!engine) {\n            return;\n        }\n        var style = this.isCapacitor() ? options.style.toUpperCase() : options.style;\n        engine.impact({ style: style });\n    },\n    notification: function (options) {\n        var engine = this.getEngine();\n        if (!engine) {\n            return;\n        }\n        var style = this.isCapacitor() ? options.style.toUpperCase() : options.style;\n        engine.notification({ style: style });\n    },\n    selection: function () {\n        this.impact({ style: 'light' });\n    },\n    selectionStart: function () {\n        var engine = this.getEngine();\n        if (!engine) {\n            return;\n        }\n        if (this.isCapacitor()) {\n            engine.selectionStart();\n        }\n        else {\n            engine.gestureSelectionStart();\n        }\n    },\n    selectionChanged: function () {\n        var engine = this.getEngine();\n        if (!engine) {\n            return;\n        }\n        if (this.isCapacitor()) {\n            engine.selectionChanged();\n        }\n        else {\n            engine.gestureSelectionChanged();\n        }\n    },\n    selectionEnd: function () {\n        var engine = this.getEngine();\n        if (!engine) {\n            return;\n        }\n        if (this.isCapacitor()) {\n            engine.selectionEnd();\n        }\n        else {\n            engine.gestureSelectionEnd();\n        }\n    }\n};\n/**\n * Trigger a selection changed haptic event. Good for one-time events\n * (not for gestures)\n */\nvar hapticSelection = function () {\n    HapticEngine.selection();\n};\n/**\n * Tell the haptic engine that a gesture for a selection change is starting.\n */\nvar hapticSelectionStart = function () {\n    HapticEngine.selectionStart();\n};\n/**\n * Tell the haptic engine that a selection changed during a gesture.\n */\nvar hapticSelectionChanged = function () {\n    HapticEngine.selectionChanged();\n};\n/**\n * Tell the haptic engine we are done with a gesture. This needs to be\n * called lest resources are not properly recycled.\n */\nvar hapticSelectionEnd = function () {\n    HapticEngine.selectionEnd();\n};\n/**\n * Use this to indicate success/failure/warning to the user.\n * options should be of the type `{ style: 'light' }` (or `medium`/`heavy`)\n */\nvar hapticImpact = function (options) {\n    HapticEngine.impact(options);\n};\n\n\n\n//# sourceURL=webpack:///./node_modules/@ionic/core/dist/esm-es5/haptic-7b8ba70a.js?");

/***/ }),

/***/ "./node_modules/@ionic/core/dist/esm-es5/ion-reorder_2.entry.js":
/*!**********************************************************************!*\
  !*** ./node_modules/@ionic/core/dist/esm-es5/ion-reorder_2.entry.js ***!
  \**********************************************************************/
/*! exports provided: ion_reorder, ion_reorder_group */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"ion_reorder\", function() { return Reorder; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"ion_reorder_group\", function() { return ReorderGroup; });\n/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ \"./node_modules/tslib/tslib.es6.js\");\n/* harmony import */ var _index_44bf8136_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./index-44bf8136.js */ \"./node_modules/@ionic/core/dist/esm-es5/index-44bf8136.js\");\n/* harmony import */ var _ionic_global_837be8f3_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./ionic-global-837be8f3.js */ \"./node_modules/@ionic/core/dist/esm-es5/ionic-global-837be8f3.js\");\n/* harmony import */ var _haptic_7b8ba70a_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./haptic-7b8ba70a.js */ \"./node_modules/@ionic/core/dist/esm-es5/haptic-7b8ba70a.js\");\n\n\n\n\nvar reorderIosCss = \":host([slot]){display:none;line-height:0;z-index:100}.reorder-icon{display:block;font-size:22px}.reorder-icon{font-size:34px;opacity:0.4}\";\nvar reorderMdCss = \":host([slot]){display:none;line-height:0;z-index:100}.reorder-icon{display:block;font-size:22px}.reorder-icon{font-size:31px;opacity:0.3}\";\nvar Reorder = /** @class */ (function () {\n    function Reorder(hostRef) {\n        Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_1__[\"r\"])(this, hostRef);\n    }\n    Reorder.prototype.onClick = function (ev) {\n        ev.preventDefault();\n        ev.stopImmediatePropagation();\n    };\n    Reorder.prototype.render = function () {\n        var mode = Object(_ionic_global_837be8f3_js__WEBPACK_IMPORTED_MODULE_2__[\"b\"])(this);\n        var reorderIcon = mode === 'ios' ? 'reorder-three-outline' : 'reorder-two-sharp';\n        return (Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_1__[\"h\"])(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_1__[\"H\"], { class: mode }, Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_1__[\"h\"])(\"slot\", null, Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_1__[\"h\"])(\"ion-icon\", { name: reorderIcon, lazy: false, class: \"reorder-icon\", part: \"icon\" }))));\n    };\n    return Reorder;\n}());\nReorder.style = {\n    ios: reorderIosCss,\n    md: reorderMdCss\n};\nvar reorderGroupCss = \".reorder-list-active>*{-webkit-transition:-webkit-transform 300ms;transition:-webkit-transform 300ms;transition:transform 300ms;transition:transform 300ms, -webkit-transform 300ms;will-change:transform}.reorder-enabled{-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}.reorder-enabled ion-reorder{display:block;cursor:-webkit-grab;cursor:grab;pointer-events:all;-ms-touch-action:none;touch-action:none}.reorder-selected,.reorder-selected ion-reorder{cursor:-webkit-grabbing;cursor:grabbing}.reorder-selected{position:relative;-webkit-transition:none !important;transition:none !important;-webkit-box-shadow:0 0 10px rgba(0, 0, 0, 0.4);box-shadow:0 0 10px rgba(0, 0, 0, 0.4);opacity:0.8;z-index:100}.reorder-visible ion-reorder .reorder-icon{-webkit-transform:translate3d(0,  0,  0);transform:translate3d(0,  0,  0)}\";\nvar ReorderGroup = /** @class */ (function () {\n    function class_1(hostRef) {\n        Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_1__[\"r\"])(this, hostRef);\n        this.ionItemReorder = Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_1__[\"e\"])(this, \"ionItemReorder\", 7);\n        this.lastToIndex = -1;\n        this.cachedHeights = [];\n        this.scrollElTop = 0;\n        this.scrollElBottom = 0;\n        this.scrollElInitial = 0;\n        this.containerTop = 0;\n        this.containerBottom = 0;\n        this.state = 0 /* Idle */;\n        /**\n         * If `true`, the reorder will be hidden.\n         */\n        this.disabled = true;\n    }\n    class_1.prototype.disabledChanged = function () {\n        if (this.gesture) {\n            this.gesture.enable(!this.disabled);\n        }\n    };\n    class_1.prototype.connectedCallback = function () {\n        return Object(tslib__WEBPACK_IMPORTED_MODULE_0__[\"__awaiter\"])(this, void 0, void 0, function () {\n            var contentEl, _a, _b;\n            var _this = this;\n            return Object(tslib__WEBPACK_IMPORTED_MODULE_0__[\"__generator\"])(this, function (_c) {\n                switch (_c.label) {\n                    case 0:\n                        contentEl = this.el.closest('ion-content');\n                        if (!contentEl) return [3 /*break*/, 2];\n                        _a = this;\n                        return [4 /*yield*/, contentEl.getScrollElement()];\n                    case 1:\n                        _a.scrollEl = _c.sent();\n                        _c.label = 2;\n                    case 2:\n                        _b = this;\n                        return [4 /*yield*/, Promise.resolve(/*! import() */).then(__webpack_require__.bind(null, /*! ./index-eea61379.js */ \"./node_modules/@ionic/core/dist/esm-es5/index-eea61379.js\"))];\n                    case 3:\n                        _b.gesture = (_c.sent()).createGesture({\n                            el: this.el,\n                            gestureName: 'reorder',\n                            gesturePriority: 110,\n                            threshold: 0,\n                            direction: 'y',\n                            passive: false,\n                            canStart: function (detail) { return _this.canStart(detail); },\n                            onStart: function (ev) { return _this.onStart(ev); },\n                            onMove: function (ev) { return _this.onMove(ev); },\n                            onEnd: function () { return _this.onEnd(); },\n                        });\n                        this.disabledChanged();\n                        return [2 /*return*/];\n                }\n            });\n        });\n    };\n    class_1.prototype.disconnectedCallback = function () {\n        this.onEnd();\n        if (this.gesture) {\n            this.gesture.destroy();\n            this.gesture = undefined;\n        }\n    };\n    /**\n     * Completes the reorder operation. Must be called by the `ionItemReorder` event.\n     *\n     * If a list of items is passed, the list will be reordered and returned in the\n     * proper order.\n     *\n     * If no parameters are passed or if `true` is passed in, the reorder will complete\n     * and the item will remain in the position it was dragged to. If `false` is passed,\n     * the reorder will complete and the item will bounce back to its original position.\n     *\n     * @param listOrReorder A list of items to be sorted and returned in the new order or a\n     * boolean of whether or not the reorder should reposition the item.\n     */\n    class_1.prototype.complete = function (listOrReorder) {\n        return Promise.resolve(this.completeSync(listOrReorder));\n    };\n    class_1.prototype.canStart = function (ev) {\n        if (this.selectedItemEl || this.state !== 0 /* Idle */) {\n            return false;\n        }\n        var target = ev.event.target;\n        var reorderEl = target.closest('ion-reorder');\n        if (!reorderEl) {\n            return false;\n        }\n        var item = findReorderItem(reorderEl, this.el);\n        if (!item) {\n            return false;\n        }\n        ev.data = item;\n        return true;\n    };\n    class_1.prototype.onStart = function (ev) {\n        ev.event.preventDefault();\n        var item = this.selectedItemEl = ev.data;\n        var heights = this.cachedHeights;\n        heights.length = 0;\n        var el = this.el;\n        var children = el.children;\n        if (!children || children.length === 0) {\n            return;\n        }\n        var sum = 0;\n        for (var i = 0; i < children.length; i++) {\n            var child = children[i];\n            sum += child.offsetHeight;\n            heights.push(sum);\n            child.$ionIndex = i;\n        }\n        var box = el.getBoundingClientRect();\n        this.containerTop = box.top;\n        this.containerBottom = box.bottom;\n        if (this.scrollEl) {\n            var scrollBox = this.scrollEl.getBoundingClientRect();\n            this.scrollElInitial = this.scrollEl.scrollTop;\n            this.scrollElTop = scrollBox.top + AUTO_SCROLL_MARGIN;\n            this.scrollElBottom = scrollBox.bottom - AUTO_SCROLL_MARGIN;\n        }\n        else {\n            this.scrollElInitial = 0;\n            this.scrollElTop = 0;\n            this.scrollElBottom = 0;\n        }\n        this.lastToIndex = indexForItem(item);\n        this.selectedItemHeight = item.offsetHeight;\n        this.state = 1 /* Active */;\n        item.classList.add(ITEM_REORDER_SELECTED);\n        Object(_haptic_7b8ba70a_js__WEBPACK_IMPORTED_MODULE_3__[\"a\"])();\n    };\n    class_1.prototype.onMove = function (ev) {\n        var selectedItem = this.selectedItemEl;\n        if (!selectedItem) {\n            return;\n        }\n        // Scroll if we reach the scroll margins\n        var scroll = this.autoscroll(ev.currentY);\n        // // Get coordinate\n        var top = this.containerTop - scroll;\n        var bottom = this.containerBottom - scroll;\n        var currentY = Math.max(top, Math.min(ev.currentY, bottom));\n        var deltaY = scroll + currentY - ev.startY;\n        var normalizedY = currentY - top;\n        var toIndex = this.itemIndexForTop(normalizedY);\n        if (toIndex !== this.lastToIndex) {\n            var fromIndex = indexForItem(selectedItem);\n            this.lastToIndex = toIndex;\n            Object(_haptic_7b8ba70a_js__WEBPACK_IMPORTED_MODULE_3__[\"b\"])();\n            this.reorderMove(fromIndex, toIndex);\n        }\n        // Update selected item position\n        selectedItem.style.transform = \"translateY(\" + deltaY + \"px)\";\n    };\n    class_1.prototype.onEnd = function () {\n        var selectedItemEl = this.selectedItemEl;\n        this.state = 2 /* Complete */;\n        if (!selectedItemEl) {\n            this.state = 0 /* Idle */;\n            return;\n        }\n        var toIndex = this.lastToIndex;\n        var fromIndex = indexForItem(selectedItemEl);\n        if (toIndex === fromIndex) {\n            this.completeSync();\n        }\n        else {\n            this.ionItemReorder.emit({\n                from: fromIndex,\n                to: toIndex,\n                complete: this.completeSync.bind(this)\n            });\n        }\n        Object(_haptic_7b8ba70a_js__WEBPACK_IMPORTED_MODULE_3__[\"h\"])();\n    };\n    class_1.prototype.completeSync = function (listOrReorder) {\n        var selectedItemEl = this.selectedItemEl;\n        if (selectedItemEl && this.state === 2 /* Complete */) {\n            var children = this.el.children;\n            var len = children.length;\n            var toIndex = this.lastToIndex;\n            var fromIndex = indexForItem(selectedItemEl);\n            if (toIndex !== fromIndex && (listOrReorder === undefined || listOrReorder === true)) {\n                var ref = (fromIndex < toIndex)\n                    ? children[toIndex + 1]\n                    : children[toIndex];\n                this.el.insertBefore(selectedItemEl, ref);\n            }\n            if (Array.isArray(listOrReorder)) {\n                listOrReorder = reorderArray(listOrReorder, fromIndex, toIndex);\n            }\n            for (var i = 0; i < len; i++) {\n                children[i].style['transform'] = '';\n            }\n            selectedItemEl.style.transition = '';\n            selectedItemEl.classList.remove(ITEM_REORDER_SELECTED);\n            this.selectedItemEl = undefined;\n            this.state = 0 /* Idle */;\n        }\n        return listOrReorder;\n    };\n    class_1.prototype.itemIndexForTop = function (deltaY) {\n        var heights = this.cachedHeights;\n        var i = 0;\n        // TODO: since heights is a sorted array of integers, we can do\n        // speed up the search using binary search. Remember that linear-search is still\n        // faster than binary-search for small arrays (<64) due CPU branch misprediction.\n        for (i = 0; i < heights.length; i++) {\n            if (heights[i] > deltaY) {\n                break;\n            }\n        }\n        return i;\n    };\n    /********* DOM WRITE ********* */\n    class_1.prototype.reorderMove = function (fromIndex, toIndex) {\n        var itemHeight = this.selectedItemHeight;\n        var children = this.el.children;\n        for (var i = 0; i < children.length; i++) {\n            var style = children[i].style;\n            var value = '';\n            if (i > fromIndex && i <= toIndex) {\n                value = \"translateY(\" + -itemHeight + \"px)\";\n            }\n            else if (i < fromIndex && i >= toIndex) {\n                value = \"translateY(\" + itemHeight + \"px)\";\n            }\n            style['transform'] = value;\n        }\n    };\n    class_1.prototype.autoscroll = function (posY) {\n        if (!this.scrollEl) {\n            return 0;\n        }\n        var amount = 0;\n        if (posY < this.scrollElTop) {\n            amount = -SCROLL_JUMP;\n        }\n        else if (posY > this.scrollElBottom) {\n            amount = SCROLL_JUMP;\n        }\n        if (amount !== 0) {\n            this.scrollEl.scrollBy(0, amount);\n        }\n        return this.scrollEl.scrollTop - this.scrollElInitial;\n    };\n    class_1.prototype.render = function () {\n        var _a;\n        var mode = Object(_ionic_global_837be8f3_js__WEBPACK_IMPORTED_MODULE_2__[\"b\"])(this);\n        return (Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_1__[\"h\"])(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_1__[\"H\"], { class: (_a = {},\n                _a[mode] = true,\n                _a['reorder-enabled'] = !this.disabled,\n                _a['reorder-list-active'] = this.state !== 0 /* Idle */,\n                _a) }));\n    };\n    Object.defineProperty(class_1.prototype, \"el\", {\n        get: function () { return Object(_index_44bf8136_js__WEBPACK_IMPORTED_MODULE_1__[\"i\"])(this); },\n        enumerable: false,\n        configurable: true\n    });\n    Object.defineProperty(class_1, \"watchers\", {\n        get: function () {\n            return {\n                \"disabled\": [\"disabledChanged\"]\n            };\n        },\n        enumerable: false,\n        configurable: true\n    });\n    return class_1;\n}());\nvar indexForItem = function (element) {\n    return element['$ionIndex'];\n};\nvar findReorderItem = function (node, container) {\n    var parent;\n    while (node) {\n        parent = node.parentElement;\n        if (parent === container) {\n            return node;\n        }\n        node = parent;\n    }\n    return undefined;\n};\nvar AUTO_SCROLL_MARGIN = 60;\nvar SCROLL_JUMP = 10;\nvar ITEM_REORDER_SELECTED = 'reorder-selected';\nvar reorderArray = function (array, from, to) {\n    var element = array[from];\n    array.splice(from, 1);\n    array.splice(to, 0, element);\n    return array.slice();\n};\nReorderGroup.style = reorderGroupCss;\n\n\n\n//# sourceURL=webpack:///./node_modules/@ionic/core/dist/esm-es5/ion-reorder_2.entry.js?");

/***/ })

}]);