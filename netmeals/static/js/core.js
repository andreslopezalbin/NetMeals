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