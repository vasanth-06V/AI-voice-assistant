$(document).ready(function () {
    
    $('.text').textillate({
        loop: true,
        sync: true,
        in:{
            effect: "bounceIn",
        },
        out:{
            effect: "bounceOut",
        }
    });

    // Siri configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1.5",
        speed: "0.20",
        autostart: true
    });

    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in:{
            effect: "fadeInUp",
            sync: true,
        },
        out:{
            effect: "fadeOutUp",
            sync: true,
        }
    });

    //mic botton
    $("#MicBtn").click(function () {
        eel.playAssistantSound()
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()()
    });


    //added shortcut key Win+J
    function doc_keyUp(e){
        if(e.key === 'j' && e.metaKey){
            eel.playAssistantSound()
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()()
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    function PlayAssistant(message) {

        if (message != "") {

            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("")
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);

        }

    }

    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)
    
    });
    
    $("#SendBtn").click(function () {
    
        let message = $("#chatbox").val()
        PlayAssistant(message)
    
    });

    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    });

    // Add to main.js
    async function loadSettings() {
        const websites = await eel.get_websites()();
        const apps = await eel.get_applications()();
        
        // Load websites
        const websiteList = $('#websiteList');
        websiteList.empty();
        websites.forEach(web => {
            websiteList.append(`
                <div class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${web[1]}</strong>
                        <div class="text-muted small">${web[2]}</div>
                    </div>
                    <button class="btn btn-sm btn-danger delete-web" data-id="${web[0]}">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            `);
        });

        // Load applications
        const appList = $('#appList');
        appList.empty();
        apps.forEach(app => {
            appList.append(`
                <div class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${app[1]}</strong>
                        <div class="text-muted small">${app[2]}</div>
                    </div>
                    <button class="btn btn-sm btn-danger delete-app" data-id="${app[0]}">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            `);
        });
    }

    // Add website
    // Add website with prevention
    $('#addWebsiteBtn').click(async function(e) {
        e.preventDefault();
        const name = $('#websiteName').val().trim();
        const url = $('#websiteUrl').val().trim();
        
        if(!name || !url) {
            alert('Please fill in both fields');
            return;
        }

        try {
            const success = await eel.add_website(name, url)();
            if(success) {
                loadSettings();
                $('#websiteName, #websiteUrl').val('');
            } else {
                alert('Failed to add website');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred');
        }
    });

    // Add application with prevention
    $('#addAppBtn').click(async function(e) {
        e.preventDefault();
        const name = $('#appName').val().trim();
        const path = $('#appPath').val().trim();
        
        if(!name || !path) {
            alert('Please fill in both fields');
            return;
        }

        try {
            const success = await eel.add_application(name, path)();
            if(success) {
                loadSettings();
                $('#appName, #appPath').val('');
            } else {
                alert('Failed to add application');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred');
        }
    });

    // Delete handlers
    $(document).on('click', '.delete-web', function() {
        const id = $(this).data('id');
        eel.delete_website(id);
        $(this).closest('.list-group-item').remove();
    });

    $(document).on('click', '.delete-app', function() {
        const id = $(this).data('id');
        eel.delete_application(id);
        $(this).closest('.list-group-item').remove();
    });

    // Load settings when offcanvas opens
    $('#offcanvasSettings').on('shown.bs.offcanvas', function() {
        loadSettings();
    });


});
