window.onload = function() {

function getUser(username) {
	data = $.ajax({
		type: "GET",
		url: '/control/getuser?username='+username,
		async: false
	}).responseText
	var obj = JSON.parse(data)
	return obj
}

$('input:radio[name=username]').change(function() {
	$('input:submit').prop('disabled', false)
	user = getUser($(this).val())
	permissions = user.permissions
	if (permissions.indexOf('bio_is_displayed') > -1) {
		$('input:checkbox[name=bio_is_displayed]').prop('checked', true)
	} else {
		$('input:checkbox[name=bio_is_displayed]').prop('checked', false)
	}
	if (permissions.indexOf('is_a_moderator') > -1) {
		$('input:checkbox[name=is_a_moderator]').prop('checked', true)
	} else {
		$('input:checkbox[name=is_a_moderator]').prop('checked', false)
	}
	if (permissions.indexOf('can_create_news_posts') > -1) {
		$('input:checkbox[name=can_create_news_posts]').prop('checked', true)
	} else {
		$('input:checkbox[name=can_create_news_posts]').prop('checked', false)
	}
	if (permissions.indexOf('can_edit_news_posts') > -1) {
		$('input:checkbox[name=can_edit_news_posts]').prop('checked', true)
	} else {
		$('input:checkbox[name=can_edit_news_posts]').prop('checked', false)
	}
	if (permissions.indexOf('can_claim_workshops') > -1) {
		$('input:checkbox[name=can_claim_workshops]').prop('checked', true)
	} else {
		$('input:checkbox[name=can_claim_workshops]').prop('checked', false)
	}
	if (permissions.indexOf('can_free_workshops') > -1) {
		$('input:checkbox[name=can_free_workshops]').prop('checked', true)
	} else {
		$('input:checkbox[name=can_free_workshops]').prop('checked', false)
	}
	if (permissions.indexOf('can_cancel_workshops') > -1) {
		$('input:checkbox[name=can_cancel_workshops]').prop('checked', true)
	} else {
		$('input:checkbox[name=can_cancel_workshops]').prop('checked', false)
	}
	if (permissions.indexOf('can_edit_homepage') > -1) {
		$('input:checkbox[name=can_edit_homepage]').prop('checked', true)
	} else {
		$('input:checkbox[name=can_edit_homepage]').prop('checked', false)
	}
})

}