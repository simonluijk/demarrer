window.APP = window.APP or {}

anly = new Anly(
  account: "UA-XXXX-1"
  outIgnoreDomains: ["XXX.cloudfront.net"]
)

APP.Main = ->
  $(document).ready ->
    anly.trackPageview()
    $("a").click (event) ->
      anly.trackOutgoing event
      anly.trackDownload event

    if typeof DEBUG is "undefined"
      $(window).load ->
        Anly.loadScript()

    else
      console.log _gaq
