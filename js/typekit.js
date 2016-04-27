/* based on the official asynch typekit code
 * http://blog.typekit.com/2012/07/19/new-improved-embed-code/
 */

(function() {
	var config = {
			kitId: 'cdg4kxg',
			scriptTimeout: 3000
		},
		tk	= document.createElement("script"),
		d	= false,
		b	= document.getElementsByTagName("body")[0];

	tk.src='//use.typekit.net/' + config.kitId + '.js';
	tk.type = "text/javascript";
	tk.async = "true";

	tk.onload = tk.onreadystatechange = function() {
		var a = this.readyState;
		if (d || a && a != "complete" && a != "loaded") return;
		d=true;
		try {
			Typekit.load(config);
		} catch(b) {}
	};

	b.appendChild(tk);
})();

