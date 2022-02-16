
window.addEventListener('load', function () {
    setTimeout(function () {
        var surveyScript = document.getElementById("survey-script");
        var surveyid = surveyScript.getAttribute('data-surveyid')

        var s = document.createElement("script");
        s.type = "text/javascript";
        s.setAttribute("crossorigin", "anonymous");
        s.setAttribute("referrerpolicy", "no-referrer");
        s.setAttribute("src", "https://cdnjs.cloudflare.com/ajax/libs/tingle/0.8.4/tingle.min.js");
        s.setAttribute("integrity", "sha512-SxopZNPB/jzFpgtGdR6lI7dK8EbbheOZVLNDI0FsMNM0NAqNkJyVoT83C72esOJCTdPVfDb8miZ3whsW4o/+fA==");
        document.body.append(s);

        s.addEventListener('load', function () {
            var cssNode = document.createElement("link");
            cssNode.setAttribute("rel", "stylesheet");
            cssNode.setAttribute("type", "text/css");
            cssNode.setAttribute("href", "https://cdnjs.cloudflare.com/ajax/libs/tingle/0.8.4/tingle.min.css");
            cssNode.setAttribute("integrity", "sha512-j5NOES5oZiza0awDPWoDCbU50obvmJUQobyAqYzhsXFxaXaxkcxB2WhnRcZa5wRGNyborruWuJaeg9J508HfQg==");
            cssNode.setAttribute("referrerpolicy", "no-referrer");
            cssNode.setAttribute("crossorigin", "anonymous");
            document.getElementsByTagName("head")[0].appendChild(cssNode);

            // instanciate new modal
            var modal = new tingle.modal({
                footer: false,
                stickyFooter: false,
                closeMethods: ['button'],
                closeLabel: "Close",
                onOpen: function () {
                    console.log('modal open');
                },
                onClose: function () {
                    console.log('modal closed');
                },
                beforeClose: function () {
                    return true; // close the modal
                }
            });

            // set content
            modal.setContent(`<iframe style="height: 70vh;"src=${basepath}/assets/${surveyid}/view" frameborder="0" style="overflow:hidden;overflow-x:hidden;overflow-y:hidden;height:100%;width:100%;position:absolute;top:0px;left:0px;right:0px;bottom:0px" height="100%" width="100%"></iframe>`);
            // open modal
            modal.open();
        })
    }, 4000);

})