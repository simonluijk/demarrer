window.APP = window.APP or {}

anly = new Anly(
    account: "UA-XXXX-1"
    outIgnoreDomains: ["XXX.cloudfront.net"]
)

APP.Main = ->
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

        undefined

    undefined
