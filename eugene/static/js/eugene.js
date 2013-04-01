$(document).ready(function() {
    var timerID = null;

    var updateMessages = function updateMessages(msgs) {
        // Takes list of {sender, text} objects.
        var allMessages = $('#message-table tbody').children();
        var firstID = -1;

        if (allMessages.length > 0) {
            firstID = allMessages.first().data('msg-id');
        }

        for (var i = 0; i < msgs.length; i++) {
            var msg = msgs[i];

            if (msg.id <= firstID) {
                continue;
            }

            // GROSS!
            var new_row =  $('<tr class="msg-data">' +
                             '<td>' + msg.created + '</td>' +
                             '<td>' + msg.sender + '</td>' +
                             '<td>' + msg.text + '</td></tr>');
            new_row.data('msg-id', msg.id);
            new_row.insertBefore('#message-table tbody tr:first-child');
        }
    };

    var getNewMessages = function getNewMessages() {
        var ship_name = $('body').data('ship-name');
        if (!ship_name) {
            return;
        }

        $.ajax({
            type: 'GET',
            url: '/api/v1/message/' + ship_name,
            dataType: 'json',
            success: function(resp, status, jqxhr) {
                updateMessages(resp.messages);
            }});
    };

    var timerClick = function timerClick() {
        getNewMessages();
        timerID = window.setTimeout(timerClick, 5000);
    };

    $('#enable-comms').click(function(event) {
        event.preventDefault();
        
        // Set everything up
        var name = $('#ship-name-input').val().toUpperCase();
        $('#ship-name').text('COMMS: ' + name);
        $('title').text('C: ' + name);
        $('body').data('ship-name', name);
        $('#message-table tbody tr.msg-data').empty();

        // Hide login form and unhide display
        $('#comms-name-form').addClass('hidden');
        $('#comms-display').removeClass('hidden');

        timerClick();
    });

    $('#disable-comms').click(function(event) {
        event.preventDefault();

        window.clearTimeout(timerID);
        timerID = null;

        // Tell the server we're offlline.
        $.ajax({
            type: 'POST',
            url: '/api/v1/user/' + ship_name,
            data: JSON.stringify({
                available: false
            }),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json'
        });

        // Disable things
        $('#ship-name').text('COMMS');
        $('title').text('(C: ' + $('body').data('ship-name') + ')');
        $('body').data('ship-name', '');

        // Hide display and unhide login form
        $('#comms-name-form').removeClass('hidden');
        $('#comms-display').addClass('hidden');

    });

    $('#send-message').click(function(event) {
        event.preventDefault();

        var name = $('body').data('ship-name');
        var msg = $('#message-input').val();

        if (msg) {
            // quick sanitize of msg.
            msg = msg.toUpperCase();
            msg = msg.replace(/[<>'"\\\/]/g, '.');

            $.ajax({
                type: 'POST',
                url: '/api/v1/message',
                data: JSON.stringify({
                    sender: name,
                    recipient: 'EVERYONE',
                    text: msg
                }),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json'
            });
            $('#message-input').val('');

            getNewMessages();
        }
    });
});
