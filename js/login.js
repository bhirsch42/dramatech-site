window.onload = function() {

// * * * * * * * * * * * * * * * 
// Login and Registration forms
// * * * * * * * * * * * * * * * 

// login form panel
loginForm = $('form', $(".login"))
loginForm.submit(function(event) {
var $form = $(this)
var $inputs = $form.find('input')
var serializedData = $form.serialize();
$inputs.prop("disabled", true);
request = $.ajax({
	url: "/control/login",
	type: "post",
	data: serializedData
});
request.done(function (response, textStatus, jqXHR){
	if (response == 'Success') {
		$('.error', $form).html("")
		window.location = '/members'
	} else {
		$('span.error#username-password', $form).html("<div class=\"error\">Username or password is invalid.</div>")
	}
});
request.fail(function (jqXHR, textStatus, errorThrown){
});
request.always(function () {
	$inputs.prop("disabled", false);
});
event.preventDefault();
})

// registration form panel
registerForm = $('form', $(".register"))
registerForm.submit(function(event) {
	var $form = $(this)
	var $inputs = $form.find('input')
	var serializedData = $form.serialize();
	$inputs.prop("disabled", true);
	request = $.ajax({
		url: "/control/register",
		type: "post",
		data: serializedData
	});
	request.done(function (response, textStatus, jqXHR){
		if (response.indexOf('Success') > -1) {
			window.location = '/members'
		} else {
			if (response.indexOf('username_is_invalid') > -1) {
				$('span.error#username-is-invalid', $form).html("<div class=\"error\">Username must be 3 to 20 characters and contain only numbers, letters, hyphens, and underscores.</div>")
			} else {
				$('span.error#username-is-invalid', $form).html("")
			}
			if (response.indexOf('username_is_taken') > -1) {
				$('span.error#username-is-taken', $form).html("<div class=\"error\">This username is taken.</div>")
			} else {
				$('span.error#username-is-taken', $form).html("")
			}
			if (response.indexOf('passwords_dont_match') > -1) {
				$('span.error#passwords-dont-match', $form).html("<div class=\"error\">Passwords don't match.</div>")
			} else {
				$('span.error#passwords-dont-match', $form).html("")
			}
			if (response.indexOf('email_is_invalid') > -1) {
				$('span.error#email-is-invalid', $form).html("<div class=\"error\">Email is invalid.</div>")
			} else {
				$('span.error#email-is-invalid', $form).html("")
			}
		}
	});
	request.fail(function (jqXHR, textStatus, errorThrown){
	});
	request.always(function () {
		$inputs.prop("disabled", false);
	});
	event.preventDefault();
})

}