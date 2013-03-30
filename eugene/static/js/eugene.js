$(document).ready(function() {
    $('#enable-comms').bind('click', function() {
        // Take the name out of the form and put it in the title
        // and h1
        var name = $('#ship-name-input').val().toUpperCase();
        $('#ship-name').text('COMMS: ' + name);
        $('title').text('COMMS: ' + name);
        $('body').data('ship-name', name);
        $('#comms-name-form').addClass('hidden');
        $('#comms-display').removeClass('hidden');
    });

    $('#disable-comms').bind('click', function() {
        $('#ship-name').text('COMMS');
        $('title').text('COMMS DISABLED');
        $('body').data('ship-name', '');

        $('#comms-name-form').removeClass('hidden');
        $('#comms-display').addClass('hidden');
    });

    $('#send-message').bind('click', function() {
        var name = $('body').data('ship-name');
        var msg = $('message-input').val();
        if (msg) {
            $.ajax({
                url: '/api/v1/message',
                type: 'POST',
                data: {
                    'sender': name,
                    'recipient': 'EVERYONE',
                    'text': msg
                },
                dataType: 'json'
            });
            $('message-input').val('');
        }
    });
});