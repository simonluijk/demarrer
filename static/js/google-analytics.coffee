window._gaq = window._gaq or []

window.Anly = (opt) ->
    @settings =
        outIgnoreDomains: []
        downloadFileTypes: ["doc", "xls", "pdf", "mp3"]

    for p of opt
        @settings[p] = opt[p] if opt.hasOwnProperty(p)

    _gaq.push ["_setAccount", @settings.account]


Anly.loadScript = ->
    g = document.createElement("script")
    s = document.getElementsByTagName("script")[0]
    g.async = true
    prefix = (if "https:" is location.protocol then "https://ssl" else "http://www")
    g.src = prefix + ".google-analytics.com/ga.js"
    s.parentNode.insertBefore g, s


Anly:: =
    trackPageview: ->
        _gaq.push ["_trackPageview"]

    setCustomVar: (slot, name, value, scope) ->
        _gaq.push ["_setCustomVar", slot, name, value, scope]

    trackEvent: (category, action, label, value) ->
        _gaq.push ["_trackEvent", category, action, label, value]

    trackClickEvent: (category, href, event) ->
        event.preventDefault()
        @trackEvent category, "click", href
        window.setTimeout (->
            document.location = href
            undefined
        ), 200

    trackOutgoing: (event) ->
        href = event.currentTarget.href
        if (href.match(/^http/)) and (not href.match(document.domain))
            domian = href.split("/")[2]
            if @settings.outIgnoreDomains.indexOf(domian) is -1
                @trackClickEvent "outgoing", href, event

    trackDownload: (event) ->
        href = event.currentTarget.href
        extension = href.split(".").pop()
        unless @settings.downloadFileTypes.indexOf(extension) is -1
                @trackClickEvent "download", href, event
