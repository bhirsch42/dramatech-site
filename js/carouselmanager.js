window.onload = function() {

// * * * * * * * * * * * * * *
// slide preview updater
// * * * * * * * * * * * * * *
function urlExists(url, callback) {
	$.ajax({
		type: 'HEAD',
		async: false,
		url: url,
		success: function(){
			callback(true);
		},
		error: function() {
			callback(false);
		}
	});
}

$('.create-new-slide[name=button-url]').keyup(function() {
	var url = $(this).val()
	$button = $('button.template')
	$button.attr('href', url)
	console.log('hi')
})

$('.create-new-slide').each(function() {
	$(this).keyup(function() {
		$('.template[name=' + $(this).attr('name') + ']').html($(this).val())
	})
})

$('.create-new-slide[name=button-text]').keyup(function() {
	content = $(this).val()
	if (content.length > 0) {
		$('.button-template').show()
	} else {
		$('.button-template').hide()
	}
})

$('.button-template').hide()
$('img.template').hide()

}