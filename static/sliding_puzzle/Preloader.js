
BasicGame.Preloader = function (game) {

	this.background = null;
	this.preloadBar = null;

	this.ready = false;

};

BasicGame.Preloader.prototype = {

	preload: function () {

		
		this.bck = this.add.sprite(this.world.centerX, this.world.centerY, 'preloaderBackground');
		this.bck.anchor.setTo(0.5,0.5);
		this.bck.scale.setTo(0.5,0.5);
		this.preloadBar = this.add.sprite(this.world.centerX, this.world.centerY, 'preloaderBar');
		this.preloadBar.anchor.setTo(0,0.5);
		this.preloadBar.scale.setTo(0.5,1);
		this.preloadBar.x = this.world.centerX - this.preloadBar.width/2;
		
		
		this.load.setPreloadSprite(this.preloadBar);

		this.load.atlas('spriteset', STATIC_SLIDING_PUZZLE+'/assets/spriteset.png', STATIC_SLIDING_PUZZLE+'/assets/spriteset.jsona');
		this.load.audio('music', [STATIC_SLIDING_PUZZLE+'/assets/music.mp3',STATIC_SLIDING_PUZZLE+'/assets/music.ogg',
		STATIC_SLIDING_PUZZLE+'/assets/music.wav',STATIC_SLIDING_PUZZLE+'/assets/music.m4a']);


	},

	create: function () {

		this.preloadBar.cropEnabled = false;

	},

	update: function () {

		
		
		if (this.cache.isSoundDecoded('music') && this.ready == false)
		{
			this.ready = true;
			this.state.start('Game');
		}

	}

};
