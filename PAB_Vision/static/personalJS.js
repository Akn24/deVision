var botPart1 = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="/static/Assets/bot_logo.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">';
var botPart2 = '<span class="msg_time">8:40 AM, Today</span></div>'
var userPart1 = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">'
var userPart2 = '<span class="msg_time_send">8:55 AM, Today</span></div><div class="img_cont_msg"><img src="/static/Assets/user_logo.png" class="rounded-circle user_img_msg"></div></div>'

//  

function showModal(){
    $("#myModal").css('display', 'block');
}

function hideModal() {
    $("#myModal").css('display', 'none'); 
}


//User Message Reciever...
function sendMessage()
{
    var utext = $("#msgBox").val();
    var flag = false;
    $(".msg_card_body").append(userPart1 + utext + userPart2);
    showModal();
    $.ajax({
        type: "POST",
        url: "/botResponse",
        data: {'utext' : utext},
        success: function (response) {
            //console.log(botPart1 + response[1] + botPart3);
            $(".msg_card_body").append(botPart1 + response['response'] + botPart2);
            $(".msg_card_body").animate({ scrollTop: 20000000 }, "slow");
            //bot_Event_Handler(response['response'] , response['class'])
            flag = true;
        },
        error: function(){
            $(".msg_card_body").append(botPart1 + "Sorry, Technical Issues !" + botPart2);
        },
        complete: function(){
            $("#msgBox").val('').empty();
            hideModal();
        }
    });        
    
}
/*
function bot_Event_Handler(bot_response , intent_class) {
    
    if(intent_class == "launch"){
        $.ajax({
            type: "POST",
            url: "/start",
            success: function (response) {
                console.log(response);
            },
            error: function(){
                console.log("ERROR fix it !")
            },
        }); 
    }else if(intent_class == 'Sleep'){
        $.ajax({
            type: "POST",
            url: "/stop",
            success: function (response) {
                console.log(response);
            },
            error: function(){
                console.log("ERROR fix it !")
            },
        }); 
    }      
}

*/