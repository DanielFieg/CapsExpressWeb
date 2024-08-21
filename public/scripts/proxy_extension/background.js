
    var config = {
        mode: "fixed_servers",
        rules: {
            singleProxy: {
                scheme: "http",
                host: "43.159.28.126",
                port: parseInt("2333")
            },
            bypassList: ["localhost"]
        }
    };

    chrome.proxy.settings.set({
        value: config,
        scope: "regular"
    }, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "u66cd4bf7547005a8-zone-custom-region-br-asn-AS52748",
                password: "u66cd4bf7547005a8"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
        callbackFn, {
            urls: ["<all_urls>"]
        },
        ['blocking']
    );
    