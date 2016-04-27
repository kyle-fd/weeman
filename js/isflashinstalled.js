(function() {
	var afpdkc			= {
			type:		'Unknown',
			version:	'Unknown'
		},

		jsfdl			= {
			installed:	'Unknown',
			raw:		'Unknown',
			major:		'Unknown',
			minor:		'Unknown',
			revision:	'Unknown',
			revisionSt:	'Unknown'
		},

		installed		= -1,

		answers			= {
			'-1':		'May&#8203;be',
			'0':		'Nope!',
			'1':		'Yes!'
		},

		messages		= {
			'-1':		'Unfortunately, I can’t tell for sure if <span class="macromedia">Macromedia/</span>Adobe Flash is installed. <a href="#details">See details below</a>.',
			'0':		'<span class="macromedia">Macromedia/</span>Adobe Flash is not installed!',
			'1':		'<span class="macromedia">Macromedia/</span>Adobe Flash <span class="version"></span> is installed!'
		};

	detect();
	display();

	function detect() {
		jsfdl = jsfdlDetect(jsfdl);
		afpdkc = afpdkcDetect(afpdkc);

		if (jsfdl.installed == "Yes" && afpdkc.type != 'Unknown' && afpdkc.version != 'Unknown') {
			installed	= 1;
		} else if (jsfdl.installed == "Yes" || afpdkc.type != 'Unknown' || afpdkc.version != 'Unknown') {
			installed	= -1;
		} else {
			installed	= 0;
		}
	}

	function display() {
		if (installed === 1) {
			document.getElementsByTagName('body')[0].className += 'flash';
		}

		document.getElementById('results-answer').innerHTML = answers[installed];
		document.getElementById('results-message').innerHTML = messages[installed];

		document.getElementById('jsfdl-installed').innerHTML = jsfdl.installed;
		document.getElementById('jsfdl-raw').innerHTML = jsfdl.raw;
		document.getElementById('jsfdl-major').innerHTML = jsfdl.major;
		document.getElementById('jsfdl-minor').innerHTML = jsfdl.minor;
		document.getElementById('jsfdl-revision').innerHTML = jsfdl.revision;
		document.getElementById('jsfdl-revisionSt').innerHTML = jsfdl.revisionSt;

		document.getElementById('afpdkc-type').innerHTML = afpdkc.type;
		document.getElementById('afpdkc-version').innerHTML = afpdkc.version;
	}

	// JavaScript Flash Detection Library (Flash Detect) (Version 1.0.4):
	function jsfdlDetect(jsfdl) {
		if (FlashDetect) {
			// installed
			jsfdl.installed	= 'No';
			if (FlashDetect.installed) {
				jsfdl.installed	= 'Yes';
			}

			// raw version
			if (FlashDetect.raw && FlashDetect.raw !== '') {
				jsfdl.raw = FlashDetect.raw;
			}

			// major version
			if (FlashDetect.major != -1) {
				jsfdl.major = FlashDetect.major;
			}

			// minor version
			if (FlashDetect.minor != -1) {
				jsfdl.minor = FlashDetect.minor;
			}

			// revision
			if (FlashDetect.revision != -1) {
				jsfdl.revision = FlashDetect.revision;
			}

			// revision string
			if (FlashDetect.revisionStr && FlashDetect.revisionStr !== '') {
				jsfdl.revisionSt = FlashDetect.revisionStr;
			}
		}
		return jsfdl;
	}

	// Adobe Flash Player Detection Kit (Revision 1.5) - client-side:
	function afpdkcDetect(afpdkc) {
		var vers = GetSwfVer(),
			type = GetSwfType();
		if (vers && vers != -1) {
			afpdkc.version = vers;
		}
		if (type && type != -1) {
			afpdkc.type = type;
		}
		return afpdkc;
	}

	// GetSwfType() -- modified from Adobe Flash Player Detection Kit (Revision 1.5) GetSwfVer()
	// uses some crappy UA detection, unfortunately
	function GetSwfType(){
		var flashType = -1;
		if (navigator.plugins !== null && navigator.plugins.length > 0) {
			if (navigator.plugins["Shockwave Flash 2.0"] || navigator.plugins["Shockwave Flash"]) {
				flashType = "Plugin (Non-IE)";
			}
		}
		else if (navigator.userAgent.toLowerCase().indexOf("webtv/2.6") != -1) flashType = "ActiveX (WebTV 2.6)";
		else if (navigator.userAgent.toLowerCase().indexOf("webtv/2.5") != -1) flashType = "ActiveX (WebTV 2.5)";
		else if (navigator.userAgent.toLowerCase().indexOf("webtv") != -1) flashType = "ActiveX (WebTV older than 2.5)";
		else if ( isIE && isWin && !isOpera ) {
			flashType = "ActiveX (IE)";
		}
		return flashType;
	}
})(this);
