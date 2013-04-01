$(document).ready(function() {
    var timerID;
    var shipName;
    var messageTable = $('#message-table');

    window.top.scrollTo(0, 1);

    var updateMessages = function (msgs) {
        // Takes list of {sender, text} objects.
        var allMessages = messageTable.find('tbody').children();
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
            var newRow =  $('<tr class="msg-data">' +
                            '<td class="td-created"></td>' +
                            '<td class="td-sender"></td>' +
                            '<td class="td-text"></td></tr>');
            newRow.data('msg-id', msg.id);
            newRow.find('.td-created').text(msg.created);
            newRow.find('.td-sender').text(msg.sender);
            newRow.find('.td-text').text(msg.text);

            newRow.insertBefore(messageTable.find('tbody tr:first-child'));
        }
    };

    var updateOnlineUsers = function (users) {
        $('#online').text(users.join(', '));
    };

    var getNewData = function () {
        if (!shipName) {
            return;
        }

        $.ajax({
            type: 'GET',
            url: '/api/v1/message/' + shipName,
            dataType: 'json',
            success: function(resp, status, jqxhr) {
                updateMessages(resp.messages);
            }});

        $.ajax({
            type: 'GET',
            url: '/api/v1/user',
            dataType: 'json',
            success: function(resp, status, jqxhr) {
                updateOnlineUsers(resp.users);
            }});
    };

    var timerClick = function () {
        getNewData();
        timerID = window.setTimeout(timerClick, 5000);
    };

    $('#enable-comms').click(function(event) {
        event.preventDefault();
        
        // Set everything up
        shipName = $('#ship-name-input').val().toUpperCase();
        shipName = shipName.replace(/[^ \w]/g, '');

        // Tell the server we're online.
        $.ajax({
            type: 'POST',
            url: '/api/v1/user/' + shipName,
            data: JSON.stringify({
                available: true
            }),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json'
        });

        $('#ship-name').text('COMMS: ' + shipName);
        $('title').text('C: ' + shipName);
        messageTable.find('tbody tr.msg-data').empty();

        // Hide login form and unhide display
        $('#comms-name-form').addClass('hidden');
        $('#comms-display').removeClass('hidden');

        timerClick();
    });

    $('#disable-comms').click(function(event) {
        event.preventDefault();

        if (timerID) {
            window.clearTimeout(timerID);
            timerID = null;
        }

        if (!shipName) {
            return;
        }

        // Tell the server we're offlline.
        $.ajax({
            type: 'POST',
            url: '/api/v1/user/' + shipName,
            data: JSON.stringify({
                available: false
            }),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json'
        });

        // Disable things
        $('#ship-name').text('COMMS');
        $('title').text('(C: ' + shipName + ')');

        // Hide display and unhide login form
        $('#comms-name-form').removeClass('hidden');
        $('#comms-display').addClass('hidden');

    });

    $('#send-message').click(function(event) {
        event.preventDefault();

        var msg = $('#message-input').val();

        if (msg) {
            // quick sanitize of msg.
            msg = msg.toUpperCase();
            msg = msg.replace(/[<>"\\\/]/g, '.');

            $.ajax({
                type: 'POST',
                url: '/api/v1/message',
                data: JSON.stringify({
                    sender: shipName,
                    recipient: 'EVERYONE',
                    text: msg
                }),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json'
            });
            $('#message-input').val('');

            getNewData();
        }
    });
});
