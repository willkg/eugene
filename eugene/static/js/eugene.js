$(document).ready(function() {
    $('#enable-comms').click(function(event) {
        event.preventDefault();
        
        // Take the name out of the form and put it in the title
        // and h1
        var name = $('#ship-name-input').val().toUpperCase();
        $('#ship-name').text('COMMS: ' + name);
        $('title').text('COMMS: ' + name);
        $('body').data('ship-name', name);
        $('#comms-name-form').addClass('hidden');
        $('#comms-display').removeClass('hidden');
    });

    $('#disable-comms').click(function(event) {
        event.preventDefault();

        $('#ship-name').text('COMMS');
        $('title').text('COMMS DISABLED');
        $('body').data('ship-name', '');

        $('#comms-name-form').removeClass('hidden');
        $('#comms-display').addClass('hidden');
    });

    $('#send-message').click(function(event) {
        event.preventDefault();

        var name = $('body').data('ship-name');
        var msg = $('#message-input').val();

        if (msg) {
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
        }
    });
});