var bookSet = $.Class.create({
	/**
	 * Class to handle books like Masterclass
	 */

	initialize: function(options) {
		this.URL = options.URL || '';
		this.BOOKMARK_URL = options.URL || '';
		
		this.main = options.main || '';
		this.loading = options.loading || '';
		this.content = options.content || '';
		this.navPrefix = options.navPrefix || '';
	
		this.pages = options.pages || [];
		this.page = 0;
		
		this.duration = options.duration || 500;
		this.easing = options.easing || 'easeOutExpo';
	
		this.transition = new SideTransition({'main': this.main, 'loading': this.loading, 'content': this.content, 'duration': this.duration, 'easing': this.easing });
		this.lastURL = this.URL + this.pages[this.page].page +'/';

		var book = this;
		

		$(document).ready(function(){
			book.setNav();
			book.updateNav();
		});
		
	},
	
	prevPage: function() {
		if(this.page > 0) {
			this.lastURL = this.URL + this.pages[--this.page].page +'/';
			this.transition.leftLoad(this.lastURL);
			this.updateNav();
		}
	},
	
	nextPage: function() {
		if(this.page < this.pages.length - 1) {
			this.lastURL = this.URL + this.pages[++this.page].page +'/';
			this.transition.rightLoad(this.lastURL);
			this.updateNav();
		}
	},
	
	reload: function() {
		if(this.pages.length > 0) {
			this.transition.rightLoad(this.URL + this.pages[this.page].page +'/');
			this.updateNav();
		} else {
			$('#'+this.content).html('<div class="book-no-chapters">No chapters has been created yet.</div>');
			this.updateNav();
		}
	},
	
	updateNav: function() {
		$('.'+this.navPrefix+'-page-no').html('' + (this.page + 1));

		if(this.page > 0)
			$('.'+this.navPrefix+'-prev').fadeIn();
		else
			$('.'+this.navPrefix+'-prev').fadeOut();
		
		if(this.page < this.pages.length - 1)
			$('.'+this.navPrefix+'-next').fadeIn();	
		else
			$('.'+this.navPrefix+'-next').fadeOut();
		
		
		if(this.pages.length>0) {
			$('.book-actions').removeClass('hidden');			
			$('.book-click-bubble').addClass('hidden');			
		}
		else {
			$('.book-actions').addClass('hidden');
			$('.book-click-bubble').removeClass('hidden');			
		}
	},
	
	setNav: function() {
		var book = this;
		$('.'+this.navPrefix+'-prev').click(function(){ book.prevPage(); }); 
		$('.'+this.navPrefix+'-next').click(function(){ book.nextPage(); });
		$('.'+this.navPrefix+'-top').click(function(){ $("html:not(:animated),body:not(:animated)").animate({ scrollTop: 0 }, 500 ); });
	},
	
	getPageID: function() {
		return this.pages[this.page].page;
	},
	
	addChapter: function(page, chapter) {
		var position = this.pages.length;
		this.pages.splice(position, 0, {'chapter': parseInt(chapter), 'page': parseInt(page)});
		this.page = position;
		this.reload();
	},

	removeChapter: function(){
		chapter = this.pages[this.page].chapter;
		while(this.page < this.pages.length && this.pages[this.page].chapter == chapter) {
			this.pages.splice(this.page, 1);
		}
		this.page = (this.page >= this.pages.length) ? this.pages.length-1 : this.page; 
		this.page = (this.page < 0)? 0 : this.page;
		this.reload();
	},

	addPage: function(page){
		this.pages.splice(this.page+1, 0, {'chapter': this.pages[this.page].chapter, 'page': parseInt(page)});
		this.nextPage();
	},

	removePage: function(){
		this.pages.splice(this.page, 1);
		this.page = (this.page >= this.pages.length) ? this.pages.length-1 : this.page; 
		this.page = (this.page < 0)? 0 : this.page;
		this.reload();
	},

	moveupPage: function(id){
		var page = -1;
		for(i=0; i<this.pages.length; i++) {
			if(this.pages[i].page == id) {
				page = i;
				break;
			}
		}
		
		if(page > 0 && this.pages.length > page) {
			var page_content = this.pages[page];
			this.pages[page] = this.pages[page-1];
			this.pages[page-1] = page_content;
			this.page = page-1;
			this.reload();	
		}
		
	},
	
	movedownPage: function(id){
		var page = -1;
		for(i=0; i<this.pages.length; i++) {
			if(this.pages[i].page == id) {
				page = i;
				break;
			}
		}
		
		if(page >= 0 && this.pages.length > page+1) {
			var page_content = this.pages[page];
			this.pages[page] = this.pages[page+1];
			this.pages[page+1] = page_content;
			this.page = page+1;
			this.reload();	
		}		
	},

	movedownChapter: function(id){
		var by_chapter = new Array();
		var chapters = -1;
		var chapter_id = 0;
		var chapter = -1;
		
		for(i=0; i<this.pages.length; i++) {
			if(chapter_id != this.pages[i].chapter) {
				chapter_id = this.pages[i].chapter;
				chapters++;
				by_chapter[chapters] = new Array();
			}
			
			if(chapter_id == id) {
				chapter = chapters;
			}

			by_chapter[chapters][by_chapter[chapters].length] = this.pages[i];		
		}


		if(chapter >= 0 && by_chapter.length > chapter+1) {
			var chapter_content = by_chapter[chapter];
			by_chapter[chapter] = by_chapter[chapter+1];
			by_chapter[chapter+1] = chapter_content;
		
			this.pages = new Array();
			for (i=0; i<by_chapter.length; i++) {
				for (j=0; j<by_chapter[i].length; j++) {
					this.pages[this.pages.length] = by_chapter[i][j];
				}
			}
			this.loadByChapterID(id);
		}		
	},


	moveupChapter: function(id){
		var by_chapter = new Array();
		var chapters = -1;
		var chapter_id = 0;
		var chapter = -1;
		
		for(i=0; i<this.pages.length; i++) {
			if(chapter_id != this.pages[i].chapter) {
				chapter_id = this.pages[i].chapter;
				chapters++;
				by_chapter[chapters] = new Array();
			}
			
			if(chapter_id == id) {
				chapter = chapters;
			}

			by_chapter[chapters][by_chapter[chapters].length] = this.pages[i];		
		}


		if(chapter > 0 && by_chapter.length > chapter) {
			var chapter_content = by_chapter[chapter];
			by_chapter[chapter] = by_chapter[chapter-1];
			by_chapter[chapter-1] = chapter_content;
		
			this.pages = new Array();
			for (i=0; i<by_chapter.length; i++) {
				for (j=0; j < by_chapter[i].length; j++) {
					this.pages[this.pages.length] = by_chapter[i][j];
				}
			}
			this.loadByChapterID(id);
		}		
	},
		
	loadByPageID: function(id){
		for(i=0; i<this.pages.length; i++) {
			if(this.pages[i].page == id) {
				this.page = i;
				this.reload();
				break;
			}
		}
	},
	
	loadByChapterID: function(id){
		for(i=0; i<this.pages.length; i++) {
			if(this.pages[i].chapter == id) {
				this.page = i;
				this.reload();
				break;
			}
		}
	}
});

var TabSet = $.Class.create({
	/**
	 * Class to handle Tabs on the site
	 */
	
	initialize: function(options) {
		this.TAB = options.TAB || '';
		this.FILTER = options.FILTER || '';
		this.URL = options.URL || '';
		
		this.main = options.main || '';
		this.loading = options.loading || '';
		this.content = options.content || '';
		this.tabPrefix = options.tabPrefix || '';
		this.filterPrefix = options.filterPrefix || this.tabPrefix;
		this.filtered = options.filtered || false;
	
		this.tabs = options.tabs || null;
		this.filters = options.filters || null;

		this.options = options.options || '';
		
		this.beforeChange = options.beforeChange || null;
		
		this.tabPos = this.getTabPosition(this.TAB);

		if (this.filtered)
			this.filterPos = this.getFilterPosition(this.FILTER);

		this.duration = options.duration || 500;
		this.easing = options.easing || 'easeOutExpo';
	
		this.transition = new SideTransition({'main': this.main, 'loading': this.loading, 'content': this.content, 'duration': this.duration, 'easing': this.easing, 'beforeChange': this.beforeChange });
	
		this.lastURL = this.getURL(this.TAB, this.FILTER);
	},

	getTabPosition: function(tab) {
		return $.inArray(tab, this.tabs);
	},

	getFilterPosition: function(filter) {
		return $.inArray(filter, this.filters);
	},	

	loadTab: function(tab) {
		this.change(tab, this.FILTER);
		
		var new_pos = this.getTabPosition(tab);
		this.lastURL = this.getURL(tab, this.FILTER);

		if (new_pos < this.tabPos) {
			this.transition.leftLoad(this.lastURL);
		} else {
			this.transition.rightLoad(this.lastURL);
		}

		this.TAB = tab;
		this.tabPos = new_pos;
	},

	reloadLeft: function(options) {
		if(options) {
			if (this.options)
				options = options.replace('?', '&');
			this.transition.leftLoad(this.lastURL + options);
		} else {
			this.transition.leftLoad(this.lastURL);
		}
	},

	reloadRight: function(options) {
		if(options) {
			if (this.options)
				options = options.replace('?', '&');
			this.transition.rightLoad(this.lastURL + options);
		} else {
			this.transition.rightLoad(this.lastURL);
		}
	},


	slideTab: function(tab) {
		this.change;
	},

	loadFilter: function(filter) {
		this.change(this.TAB, filter);
		
		var new_pos = this.getFilterPosition(filter);
		this.lastURL = this.getURL(this.TAB, filter);

		if (new_pos < this.filterPos) {
			this.transition.leftLoad(this.lastURL);
		} else {
			this.transition.rightLoad(this.lastURL);
		}

		this.FILTER = filter;		
		this.filterPos = new_pos;
	},
	
	change: function(tab, filter) {
		$('#'+ this.tabPrefix +'tab-'+ this.TAB).removeClass('active');
		$('#'+ this.tabPrefix +'tab-'+ tab).addClass('active');
		Cufon.refresh();
		
		if(this.filtered) {
			$('#'+ this.filterPrefix +'filter-'+ this.FILTER).removeClass('active');
			$('#'+ this.filterPrefix +'filter-'+ filter).addClass('active');
		}
	},
	
	getURL: function(tab, filter) {
		if(this.filtered) {
			return this.URL + tab +'/'+ filter +'/' + this.options;
		} else {
			return this.URL + tab +'/'+ this.options;
		}
	}

});



var SideTransition = $.Class.create({
	/**
	 * Class to handle SideTransitions on the site
	 */
	
	initialize: function(options) {
		this.main = options.main || '';
		this.loading = options.loading || '';
		this.content = options.content || '';
		this.duration = options.duration || 500;
		this.easing = options.easing || 'easeOutExpo';
		this.beforeChange = options.beforeChange || null;
	},

	leftLoad: function(url) {
		var transition = this;

		if (transition.beforeChange) {
			transition.beforeChange();
		}
		
		$('#'+ transition.loading).insertBefore($('#'+ transition.content));
		$('#'+ transition.main).css('margin-left', '-' +$('#'+transition.loading).width()+ 'px');
		$('#'+ transition.main).animate({'margin-left': '0px'}, {
			'duration': transition.duration,
			'easing': transition.easing,
			'complete': function() {
				$.ajax({
					url: url,
					error: function(jqXHR, textStatus, errorThrown) {
						transition.error(textStatus, errorThrown);
					},
					success: function(data, textStatus, jqXHR) {
						$('#'+ transition.content).html(data);
						Cufon.refresh();
					},
					complete: function() {
						$('#'+ transition.loading).insertAfter($('#' + transition.content));
						$('#'+ transition.main).css('margin-left', '-' +$('#'+ transition.content).width()+ 'px');
						$('#'+ transition.main).animate({'margin-left': '0px'}, {
							'duration': transition.duration,
							'easing': transition.easing
						});
					}
				});
			}
		});
	},
	
	rightLoad: function(url) {
		var transition = this;
		
		if (transition.beforeChange) {
			transition.beforeChange();
		}
		
		$('#'+ transition.loading).insertAfter($('#'+ transition.content));
		$('#'+ transition.main).css('margin-left', '0px');
		$('#'+ transition.main).animate({'margin-left': '-' +$('#'+transition.loading).width()+ 'px'}, {
			'duration': transition.duration,
			'easing': transition.easing,
			'complete': function() {
				$.ajax({
					url: url,
					error: function(jqXHR, textStatus, errorThrown) {
						transition.error(textStatus, errorThrown);
					},
					success: function(data, textStatus, jqXHR) {
						$('#'+ transition.content).html(data);
						Cufon.refresh();
					},
					complete: function() {
						$('#'+ transition.loading).insertBefore($('#' + transition.content));
						$('#'+ transition.main).css('margin-left', '0px');
						$('#'+ transition.main).animate({'margin-left': '-' +$('#'+transition.loading).width()+ 'px'}, {
							'duration': transition.duration,
							'easing': transition.easing
						});
					}
				});
			}
		});
	},
	
	error: function(textStatus, errorThrown) {
		$('#'+ this.content).html('<div class="simple-content">'+
						  		  '   <div class="main-heading"><span>The page cannot be loaded! ('+ textStatus.toLowerCase() +': '+ errorThrown.toLowerCase() +')</span></div>'+
						  		  '   <div class="message"> Please try again later.</div>'+
						  		  '</div>');
	}
});


var SlideShowSet = $.Class.create({
	/**
	 * Class to handle slide shows on the site
	 */
	
	initialize: function(options) {
		this.TAB = options.TAB || '';
		
		this.main = options.main || null;
		this.tabPrefix = options.tabPrefix || '';
		this.itemPrefix = options.itemPrefix || options.tabPrefix || '';
	
		this.tabs = options.tabs || null;

		this.tabPos = this.getTabPosition(this.TAB);

		this.duration = options.duration || 5000;
		this.timer = null;
		this.secondItems = options.secondItems || false;
		
		this.setTimeout();
		
		var self = this;
		
		$(document).ready(function(){
			$(window).blur(function(){
				if(self.timer)
					clearTimeout(self.timer);				
			});
			$(window).focus(function(){
				self.nextTab();
			});
		});
	},

	setTimeout: function() {
		if(this.timer)
			clearTimeout(this.timer);

		if(this.tabs.length > 1) { 
			var self = this;
			this.timer = setTimeout(function(){ self.nextTab(); }, this.duration);
		}
	},

	getTabPosition: function(tab) {
		return $.inArray(tab, this.tabs);
	},

	nextTab: function() {
		if(this.tabPos < this.tabs.length - 1) {
			this.loadTab(this.tabs[++this.tabPos]);
		} else {
			this.tabPos = 0;
			this.loadTab(this.tabs[0]);
		}
	},

	loadTab: function(tab) {
		var self = this;
		
		self.setTimeout()
		
		$('#'+ self.tabPrefix +'tab-'+ self.TAB).removeClass('active', 500);
		$('#'+ self.tabPrefix +'tab-'+ tab).addClass('active', 500);
		Cufon.refresh();

		if(self.main) {
			// my solution for jquery bug
			$('#'+ self.itemPrefix +'item-'+ tab).addClass('next____tab');
			$(self.main).animate({'opacity':'0.1'}, function() {
				$(self.main).animate({'opacity':'1.0'});
				$(self.main +' li').addClass('hidden');
				$(self.main +' .next____tab').removeClass('hidden');
				$(self.main +' .next____tab').removeClass('next____tab');
			});
		} else {
			$('#'+ self.itemPrefix +'item-'+ self.TAB).fadeOut('slow', function(){
				$('#'+ self.itemPrefix +'item-'+ tab).fadeIn('slow');
			});
		}
		
		if(self.secondItems) {
			$('#'+ self.itemPrefix +'seconditem-'+ self.TAB).fadeOut('slow', function(){
				$('#'+ self.itemPrefix +'seconditem-'+ tab).fadeIn('slow');
			});
		}
		
		Cufon.refresh();
		
		self.TAB = tab;
		self.tabPos = self.getTabPosition(tab);

	},

	slideTab: function(tab) {
		this.change;
	}
});
