window.onload = function() {
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
				"position": "absolute",
				"left": lefts[index],
				"top": tops[index]
			})
		})
		$articles.each(function(index) {
			if (this.id != id) {
				$(this).fadeTo("fast", 0)
			}
		})

		// expand this article
		// $('div.article').promise().done(function() {
			$('html, body').animate({
				scrollTop: $("#" + id).offset().top
			});
			$article.animate({
				'width': "100%",
				'height': "100%",
				"border-radius":"0",
				"left": "0",
				"margin-left": "0",
				"margin-right": "0"
			})
			var $smallArticle = $article.find(".article-small")
			var $bigArticle = $article.find(".article-big")
			// layer the buttons properly
			$smallArticle.css({
				"z-index":"99"
			})
			$bigArticle.css({
				"z-index":"100"
			})
			$smallArticle.fadeTo("fast", 0)
			$bigArticle.fadeTo("slow", 1)			
		// })
	})

	$('a.contract-article').click(function() {
		var id = this.id
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
		$smallArticle.css({
			"z-index":"100"
		})
		$bigArticle.css({
			"z-index":"99"
		})
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
					"position": "initial"
				})
			})
		})
		articleOpen = false
	})
}