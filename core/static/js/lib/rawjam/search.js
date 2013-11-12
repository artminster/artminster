var siteSearch = $.Class.create({
	
	initialize: function(options) {
		this.input = options.input || '#search_input';
		this.container = options.container || '#search_results_container';
		this.results = options.results || '#search_results';
		this.form = options.form || '#search_form';
		this.url = options.url || '';
		this.min_chars = options.min_chars || 3;
		this.timeout = options.timeout || 350;
		this.method = options.method || 'get';

		this.timer = null;
		
		var self = this;
		
		$(document).ready( function(){
			$(self.input).keyup(function(event) {
				if($(this).val().length < self.min_chars) {
					$(self.container).fadeOut('fast', function() {
						$(self.results).hide();
					});
				} else {
					$(this.form).find('.search-spinner').fadeIn('fast');
					if(self.timer)
						clearTimeout(self.timer);
					self.timer = setTimeout(function(){ self.search(); }, self.timeout);		
				}
			});
			
			$(self.input).blur(function(){
				$(self.results).fadeOut('fast');
			});
		});		
	},
	
	search: function(){
		var self = this;
		
		if ( $(self.input).val() ) {
			$(self.results).fadeOut('fast', function(){
				$(self.container).fadeIn('fast', function(){
					$.ajax({
						url: self.url,
						method: self.method,
						data: $(self.form).serialize(),
						success: function(data) {
							$(self.results).html(data);
							$(self.form).find('.search-spinner').fadeOut('fast');
							$(self.results).fadeIn('fast');
						}
					});
				});
			});
		}
	}
});