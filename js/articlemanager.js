window.onload = function() {

// * * * * * * * * * * * * * *
// Article preview updater
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

$('input:text[name=image-url]').keyup(function() {
	var url = $(this).val()
	urlExists(url, function(exists){
		$image = $('img.template')
		if (exists) {
			$image.show()
			$image.attr('src', url)
		} else {
			$image.hide()
		}
	});
	console.log($('img.template'))
})

$('.create-new-article').each(function() {
	$(this).keyup(function() {
		$('.template[name=' + $(this).attr('name') + ']').html($(this).val())
	})
})

$('.create-new-article[name=content]').keyup(function() {
	content = $(this).val()
	if (content.length > 0) {
		$('.button-template').show()
	} else {
		$('.button-template').hide()
	}
})

$('.button-template').hide()
$('img.template').hide()
// * * * * * * * * * * * * * *
// Article preview animation
// * * * * * * * * * * * * * *

var duration = 300;
var oldLeft = 0
var articleOpen = false;
$('a.expand-article').click(function() {
	if (articleOpen) {
		return
	}
	articleOpen = true;
	var id = this.id
	var $article = $('div.article#' + id)
	var $smallArticle = $article.find(".article-small")
	var $bigArticle = $article.find(".article-big")
	var thisTop = $article.offset().top - 20
	oldLeft = $article.offset().left - 20
	console.log(thisTop)
	// hide all other articles
	// fix all articles absolutely
	var $articles = $('.article')
	var lefts = []
	var tops = []
	$articles.each(function(index) {
		lefts[index] = $(this).offset().left - 20
		tops[index] = $(this).offset().top - 20
	})
	$articles.each(function(index) {
		$(this).css({
			// "position": "absolute",
			"left": lefts[index],
			"top": tops[index]
		})
	})
	$articles.each(function(index) {
		if (this.id != id) {
			$(this).fadeTo("fast", 0)
			$(this).css({
				"z-index":-1
			})
		}
	})

	// expand this article
	$('html, body').animate({
		scrollTop: $("#" + id).offset().top
	});
	// var totalHeight = $bigArticle.outerHeight(true)
	// console.log($bigArticle.outerHeight(true))
	var curHeight = $article.height();
	$article.css('height', 'auto');
	var autoHeight = $article.height();
	if ($(window).height() > autoHeight) {
		autoHeight = $(window).height()
	}
	$article.height(curHeight).animate({
		'width': "100%",
		'height': autoHeight,
		"border-radius":"0",
		"left": "0",
		"margin-left": "0",
		"margin-right": "0",
		"z-index": 100
	})
		// layer the buttons properly

		$smallArticle.fadeTo("fast", 0)
		$bigArticle.fadeTo("slow", 1)
		$smallArticle.css({
			"z-index": 99
		})
		$bigArticle.css({
			"z-index": 100
		})
	})

$('a.contract-article').click(function() {
	var id = this.id
	contractArticle(id)
})

function contractArticle(id) {
	// contract this article
	var $article = $('div.article#' + id)
	console.log($article.oldLeft)
	console.log($article)
	$article.animate({
		'width': "300px",
		'height': "400px",
		"margin":"20px",
		"border-radius":"5px",
		"left": oldLeft
	})
	var $smallArticle = $article.find(".article-small")
	var $bigArticle = $article.find(".article-big")
	$smallArticle.fadeTo("slow", 1)
	$bigArticle.fadeTo("fast", 0)

	// show all other articles
	var $articles = $('.article')
	$articles.each(function(index) {
		console.log(this.id)
		if (id != this.id) {
			$(this).fadeTo("slow", 1)
		}
	})
	$('div.article').promise().done(function() {
		$articles.each(function(index) {
			$(this).css({
				"position": "initial",
				"z-index": "initial"
			})
		})
	})
	$smallArticle.css({
		"z-index": 100
	})
	$bigArticle.css({
		"z-index": 99
	})
	articleOpen = false
}

contractArticle($('a.contract-article').id)

}