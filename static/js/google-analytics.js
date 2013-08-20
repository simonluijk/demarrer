var _gaq = _gaq || [];

var Anly = function(opt) {
    this.settings = {
        outIgnoreDomains: [],
        downloadFileTypes: ['doc', 'xls', 'pdf', 'mp3']
    };
    for (var p in opt) {
        if (opt.hasOwnProperty(p)) {
            this.settings[p] = opt[p];
        }
    }
    _gaq.push(['_setAccount', this.settings.account]);
};

Anly.loadScript = function() {
    var g = document.createElement('script'),
        s = document.getElementsByTagName('script')[0];
    g.async = true;
    g.src = ('https:' == location.protocol ? 'https://ssl' : 'http://www') +
             '.google-analytics.com/ga.js';
    s.parentNode.insertBefore(g, s);
};

Anly.prototype = {
    trackPageview: function() {
        _gaq.push(['_trackPageview']);
    },
    setCustomVar: function(slot, name, value, scope) {
        _gaq.push(['_setCustomVar', slot, name, value, scope]);
    },
    trackEvent: function(category, action, label, value) {
        _gaq.push(['_trackEvent', category, action, label, value]);
    },
    trackClickEvent: function(category, href, event) {
        event.preventDefault();
        this.trackEvent(category, 'click', href);
        window.setTimeout(function() {
            document.location = href;
        }, 200);
    },
    trackOutgoing: function(event) {
        var href = event.currentTarget.href;
        if ( (href.match(/^http/)) && (!href.match(document.domain)) ) {
            var domian = href.split('/')[2];
            if ( this.settings.outIgnoreDomains.indexOf(domian) == -1 ) {
                this.trackClickEvent('outgoing', href, event);
            }
        }
    },
    trackDownload: function(event) {
        var href = event.currentTarget.href,
            extension = href.split('.').pop();
        if ( this.settings.downloadFileTypes.indexOf(extension) != -1 ) {
            this.trackClickEvent('download', href, event);
        }
    }
};
