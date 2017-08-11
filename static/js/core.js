var weekDays = [];
$(document).ready(function(){


    var languageMenu = $("#language-dropdown");
    var currentCookieLanguage = getCookieValue("language");
    var cookieLanguageCode = "es";
    if(currentCookieLanguage != ""){
        var language = "";
        if(currentCookieLanguage == "es"){
            language = "Spanish";
        }else if(currentCookieLanguage == "en"){
            language = "English";
        }
        languageMenu.text(language);
    }else{
        changeLanguage(cookieLanguageCode, "en");
    }


    $('#login-form').submit(function(event) {
        event.preventDefault();
        // var hash = CryptoJS.SHA1($('#signin-userPassword').val());
        //
        // $('#signin-userPassword').val(hash);

        this.submit();
    });

	setTimeout(function() {
	    $('#signinError-alert').fadeOut('slow');
	    $('#signupSuccess-alert').fadeOut('slow');
	}, 5000);

	$.ajaxSetup({
        beforeSend: function(xhr, settings) {
            var csrftoken = getCookieValue('csrftoken');
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(".signup-role").click(function(){
        console.log($(this).data("role") + " pressed");
        if(!$(this).hasClass("signup-role-selected")) {
            $(this).addClass("signup-role-selected");
        }else{
            $(this).removeClass("signup-role-selected");
        }
    });

    $(".week-day").click(function(){
        console.log($(this).data("weeks-day") + " pressed");
        if(!$(this).hasClass("week-day-selected")) {
            $(this).addClass("week-day-selected");
        }else{
            $(this).removeClass("week-day-selected");
        }
        var value = $(this).data("weeks-day");
        var isInArray = $.inArray(value, weekDays);
        if(isInArray != -1){
            weekDays.splice(isInArray,1);
        }else{
            weekDays.push(value);
        }
        var days = $("#week-days").val(weekDays)
    });
});

function changeLanguage(cookieLanguageCode, language) {
    var currentLanguage = getCookieValue(cookieLanguageCode);
    
    if(language != currentLanguage){
		document.cookie =  cookieLanguageCode + "=" + language;
	    location.reload();
	}
}

function getCookieValue(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function paypalButton(elementId, amount, description, eventId, eventType, functionAfterExecutePayment){
   var host = window.location.href.split('/').slice(0, 3).join('/');

    var CREATE_PAYMENT_URL  = host + '/paypal/create-payment';
    var EXECUTE_PAYMENT_URL = host + '/paypal/execute-payment';

    paypal.Button.render({

        env: 'sandbox', // Or 'sandbox'

        commit: false, // Show a 'Pay Now' button

        payment: function() {
            return paypal.request.post(CREATE_PAYMENT_URL,
                {
                    amount: amount,
                    description: description,
                    csrfmiddlewaretoken: getCookieValue("csrftoken"),
                    eventId: eventId,
                    eventType: eventType
                }
            ).then(function(data) {
                console.log(data.paypal_payment_id);
                if(data.paypal_payment_id != null) {
                    return data.paypal_payment_id;
                }else{
                    alert("Error al crear el pago");
                }
            });
        },

        onAuthorize: function(data) {
            return paypal.request.post(EXECUTE_PAYMENT_URL, {
                csrfmiddlewaretoken: getCookieValue("csrftoken"),
                paymentID: data.paymentID,
                payerID:   data.payerID
            }).then(function() {
                console.log("Payment Executed!!!");
                try{
                    functionAfterExecutePayment();
                }catch(e){
                    console.log(e);
                }
            });
        }

    }, elementId);
}

function initSearchBox() {
    var input = document.getElementById('menu-searcher');
    var menuSearchBox = new google.maps.places.SearchBox(input);
    menuSearchBox.addListener('places_changed', function () {
        var places = menuSearchBox.getPlaces();
        var url = $("#menu-searcher").data("url");

        if (places.length == 0) {
            return;
        }
        // For each place, get the icon, name and location.
        var bounds = new google.maps.LatLngBounds();
        places.forEach(function (place) {
            var lat = place.geometry.location.lat();
            var lng = place.geometry.location.lng();
            // $.post( url, {
            //     "latitude": lat,
            //     "longitude": lng
            // });
            window.location.href = url + "?latitude=" + lat + "&longitude=" + lng
        });
    });
}