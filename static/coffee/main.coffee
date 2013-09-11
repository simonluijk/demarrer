Anly = require('./google-analytics.coffee')

anly = new Anly(
    account: "UA-XXXX-1"
    outIgnoreDomains: ["XXX.cloudfront.net"]
)

Main = ->
    window.DEBUG = typeof DEBUG is 'boolean' and DEBUG is true

    $(document).ready ->
        anly.trackPageview()

        $("a").click (event) ->
            anly.trackOutgoing event
            anly.trackDownload event

        if not DEBUG
            $(window).load ->
                Anly.loadScript()
        else
            console.log _gaq
