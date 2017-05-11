// ==UserScript==
// @id LocalLoader SVQ-LaunchEvents
// @name LocalLoader SVQ-LaunchEvents
// @description LocalLoader SVQ-LaunchEvents
// @category Tool
// @version 1.0
// @include        https://www.ingress.com/intel*
// @include        http://www.ingress.com/intel*
// @include        *://*.ingress.com/intel*
// @include        *://*.ingress.com/mission/*
// @match          *://*.ingress.com/intel*
// @match          *://*.ingress.com/mission/*
// @grant          none
// ==/UserScript==


function wrapper(plugin_info) {
// ensure plugin framework is there, even if iitc is not yet loaded
if(typeof window.plugin !== 'function') window.plugin = function() {};

//PLUGIN AUTHORS: writing a plugin outside of the IITC build environment? if so, delete these lines!!
//(leaving them in place might break the 'About IITC' page or break update checks)
plugin_info.buildName = 'jonatkins-test';
plugin_info.dateTimeVersion = '20170323.172100';
plugin_info.pluginId = 'map-fixed-zoom';
//END PLUGIN AUTHORS NOTE

// PLUGIN START ////////////////////////////////////////////////////////

var setup = function() {
    window.addHook('mapDataRefreshEnd', function(data) {
        $('body').append("<div id='svq_loaded'></div>")
    });

    window.addHook('mapDataRefreshStart', function(data) {
        $('#svq_loaded').remove()
    })
}

// PLUGIN END //////////////////////////////////////////////////////////

setup.info = plugin_info; //add the script info data to the function as a property
if(!window.bootPlugins) window.bootPlugins = [];
window.bootPlugins.push(setup);
// if IITC has already booted, immediately run the 'setup' function
if(window.iitcLoaded && typeof setup === 'function') setup();
} // wrapper end
// inject code into site context
var script = document.createElement('script');
var info = {};
if (typeof GM_info !== 'undefined' && GM_info && GM_info.script) info.script = { version: GM_info.script.version, name: GM_info.script.name, description: GM_info.script.description };
script.appendChild(document.createTextNode('('+ wrapper +')('+JSON.stringify(info)+');'));
(document.body || document.head || document.documentElement).appendChild(script);


