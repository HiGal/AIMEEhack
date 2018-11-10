const pusher = new Pusher('706ab48dca940577335b', {
    cluster: 'eu',
    encrypted: true
});

// Subscribe to movie_bot channel
const channel = pusher.subscribe('movie_bot');

// bind new_message event to movie_bot channel
channel.bind('new_message', function (data) {
    // Append human message
    $('.chat-container').append(`
        <div class="chat-message col-md-5 human-message">
            ${input_message}
        </div>
    `);

    // Append bot message
    $('.chat-container').append(`
        <div class="chat-message col-md-5 offset-md-7 bot-message">
            ${data.message}
        </div>
    `)
});


function submit_message(message) {

    $.post("/send_message", {
        message: message,
        socketId: pusher.connection.socket_id
    }, handle_response);

    function handle_response(data) {
        // append the bot repsonse to the div
        try {
            mes = JSON.parse(data.message);
            if (mes['Type'] === 'film') {
                $('.chat-container').append(`
            <div class="chat-message col-md-6 offset-md-6 bot-message">
                <div class="row">
                    <div class=" col-sm-4">
                     <img src="${mes['Poster']}" width="120px">
                     </div>
                    <div class="col-sm-8 film-widget">
                        <div><b>Название:</b> ${mes['Title']}</div>
                        <div><b>Дата выхода:</b> ${mes['Released']} </div>
                        <div><b>Лозунг:</b> ${mes['Tagline']}</div>
                        <div><b>Оценка:</b> ${mes['Score']}</div>
                    </div>  
                </div>
            </div>
            
            <div class="chat-message col-md-6 offset-md-6 bot-message">
                <iframe width="350" height="200" src="${mes['Video']}"></iframe>
            </div>
            `);

            if(mes['Status'] === 'true'){
                $('.film-widget').append(`
                    <div><a class="btn btn-primary" href="https://karofilm.ru/theatres/26" target="_blank">
                        Купить билеты
                    </a>
                    </div>
                `)
            }
            }

            if (mes["Type"] === "ticket") {
             alert('PSOSO');
                $('.chat-container').append(`
            <div class="chat-message col-md-6 offset-md-6 bot-message">
                <div class="row">
                    <div class="class="col-sm-8 film-widget">
                        <div><b>Цена:</b> ${mes["Price"]}</div>
                        <div><b>Дата отправления:</b> ${mes["Departure"]} </div>
                        <div><b>Предложение:</b> ${mes["Insurance"]}  <p><a href="https://sgabs.ru/">Узнать больше</a></p> </div>
                    </div>  
                </div>
            </div>
            
      `)
            }

        } catch (e) {

            $('.chat-container').append(`
            <div class="chat-message col-md-6 offset-md-6 bot-message">
                ${data.message}
            </div>
             `)
        }

        // remove the loading indicator
        $("#loading").remove();
    }
}


$('#target').on('submit', function (e) {
    e.preventDefault();
    const input_message = $('#input_message').val();
    // return if the user does not enter any text
    if (!input_message) {
        return
    }

    $('.chat-container').append(`
        <div class="chat-message col-md-5 human-message">
            ${input_message}
        </div>
    `);

    // loading
    $('.chat-container').append(`
        <div class="chat-message text-center col-md-2 offset-md-10 bot-message" id="loading">
            <b>...</b>
        </div>
    `);

    // clear the text input
    $('#input_message').val('');

    // send the message
    submit_message(input_message)
});
