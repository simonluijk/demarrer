var APP = this.APP || {};
var anly = new Anly({
    account: 'UA-XXXX-1',
    outIgnoreDomains: ['XXX.cloudfront.net']
});

APP.Main = function() {
    $(document).ready(function() {
        anly.trackPageview();
        $('a').click(function(event) {
            anly.trackOutgoing(event);
            anly.trackDownload(event);
        });
        if (typeof DEBUG == 'undefined') {
            $(window).load(function() {
                Anly.loadScript();
            });
        } else {
            console.log(_gaq);
        }
    });
};
