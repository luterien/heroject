/*
*
* Grade.js 1.0
*
* (c) 2013 by Yaşar İÇLİ, Tacirnet
* For all details and documentation:
* http://grade.tacirnet.com.tr
*
* Date: @DATE
*/
(function() {

    // root object, `window` in the browser, or `global` on the server.
    var root = this;

    // empty Base prototype object.
    var prototype = ({});

    // The base Grade Class
    root.Grade = function() {};

    // jQuery Grade 
    Grade.jQuery = Grade.$ = root.jQuery;

    // Grade.Utils Object
    Grade.Utils = prototype;

    // Extends a destination object
    // with a source object
    Grade.Utils._extend = function(dest,source) {
        if(!source) { return dest; }
        for (var prop in source) {
            dest[prop] = source[prop];
        };
        return dest;
    };

    // PageIs htmlid
    Grade.Utils._pageIs = function(pagename) {
        var body = document.getElementsByTagName("html")[0];
        return (body.getAttribute("id") == pagename);
    };

    // Return a shallow copy of an object. Sub-objects (and sub-arrays) are not cloned.
    Grade.Utils._clone = function(obj) {
        return this._extend({},obj);
    };

    // Check if something is a string
    Grade.Utils._isString = function(obj) {
        return typeof obj === "string";
    };

    // Check if something is a isnumber
    Grade.Utils._isNumber = function(obj) {
        return Object.prototype.toString.call(obj) === '[object Number]';
    };

    // Check if something is a function
    Grade.Utils._isFunction = function(obj) {
        return Object.prototype.toString.call(obj) === '[object Function]';
    };

    // Check if something is a object
    Grade.Utils._isObject = function(obj) {
        return Object.prototype.toString.call(obj) === '[object Object]';
    };

    // Check if something is a array
    Grade.Utils._isArray = function(obj) {
        return Object.prototype.toString.call(obj) === '[object Array]';
    };

    // Check if something is undefined
    Grade.Utils._isUndefined = function(obj) {
        return obj === void 0;
    };

    // each function
    Grade.Utils._each = function(obj, iterator, context) {
        if (obj == null) { return; }
        for (var key in obj) {
            iterator.call(context, key, obj[key], obj);
        };
    };

    /*
    * Application
    * @param {Object} prop
    */
    Grade.Application = function(prop) {
        var _super = this.prototype;

        // public initializing
        initializing = false;
       
        // Instantiate a base class (but only create the instance,
        // don't run the init constructor)
        initializing = true;
        var prototype = new this();
        initializing = false;

        // Copy the properties over onto the new prototype
        var name;
        for (name in prop) {
            var prop_type = typeof prop[name] == "function";
            var super_type = typeof _super[name] == "function";
            var fnTest = /\b_super\b/.test(prop[name]);

            prototype[name] = prop_type && super_type && fnTest ?
            
            (function(name, fn){
                return function() {
                    var tmp = this._super;
                    this._super = _super[name];

                    var ret = fn.apply(this, arguments); 
                    this._super = tmp;
                    return ret;
                };
            })(name, prop[name]) : prop[name];
        };

        var construct = function(constructor, args) {
        
            var APP = function() { return constructor.apply(this, args); };
            APP.prototype = constructor.prototype;

            // prototype.pageName == html[id=='pagename'] then new App;
            if (prototype.pageName && Grade.Utils._pageIs(prototype.pageName) || !prototype.pageName) {
                return new APP();
            };
        };

        var run = function() { return construct(this, arguments); };
        var App = function() {
        
            if ( !initializing && this.initialize ) {
                var klass = this;
                
                // this.initialize(arguments);
                klass.initialize.apply(this, arguments);

                // events;
                Grade.Utils._each(this.events, function(property, value) {
                    var event_split = property.split(" ");
                    var event_type = event_split[0];
                    var selectors = event_split.slice(1, event_split.length);

                    Grade.jQuery(document).on(event_type, selectors.join(" "), function(e) {
                    
                        klass[value].call(klass, e);
                    });
                });
            };
        };

        /*
        * @SET {App Object}
        *   Prototype 
        *   Constructor
        *   Application
        *   Run
        */
        App.prototype = prototype;
        App.prototype.constructor = App;
        App.extend = arguments.callee;
        App.Run = run;

        return App;
    };

}).call(this);
