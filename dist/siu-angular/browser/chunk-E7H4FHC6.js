import{a as Ze}from"./chunk-6Q4QUX6Y.js";import{a as ie}from"./chunk-IABRCUVS.js";import{a as We}from"./chunk-XPONP6K5.js";import{a as Be,b as $e}from"./chunk-RHXYTOW7.js";import{a as Ve,b as He}from"./chunk-EBJYW3C2.js";import{a as je}from"./chunk-Q6MIBXXU.js";import{a as Ne,b as Fe}from"./chunk-EJWNUG5D.js";import"./chunk-CVA3OUYK.js";import{a as Ae,b as Re}from"./chunk-GWNY4E3S.js";import{a as te}from"./chunk-ISPOGFK5.js";import{a as ee}from"./chunk-NQ5JYPMZ.js";import{a as Ge,b as Ue}from"./chunk-FJY5KO7T.js";import"./chunk-L64YGAYQ.js";import{a as ke,b as Ee,c as Se,f as De,h as Te}from"./chunk-HFRGPHGK.js";import"./chunk-M2VBT7VT.js";import{a as K,b as Q}from"./chunk-STMJJCCP.js";import{$ as X,W as Oe,Y as Ie,_ as ze}from"./chunk-ZNVG5ZVS.js";import{a as we,c as Pe}from"./chunk-LMV7XNWS.js";import"./chunk-FBCHPQNP.js";import{p as J}from"./chunk-YGREV7VD.js";import{B as Le,Cb as E,D as Y,Db as S,Ec as y,Gb as he,H as ve,Hb as pe,Ib as R,Jb as p,Kb as u,Lb as U,R as ce,S as be,Sb as G,Wb as M,Xa as m,Y as q,Yb as v,ac as ye,ba as O,bc as Me,cc as xe,e as Z,f as _e,ga as x,ha as C,hc as Ce,ic as N,kc as f,l as le,lb as W,lc as I,mc as F,oa as de,sa as T}from"./chunk-E7AQ6X4Y.js";import{a as D,b as j,e as H,f as fe}from"./chunk-EQDQRRRY.js";var b=H(ie()),ni=H(We());(function(d,i,n){function r(e,t){for(;(e=e.parentElement)&&!e.classList.contains(t););return e}L.drawVersion="1.0.4",L.Draw={},L.drawLocal={draw:{toolbar:{actions:{title:"Cancel drawing",text:"Cancel"},finish:{title:"Finish drawing",text:"Finish"},undo:{title:"Delete last point drawn",text:"Delete last point"},buttons:{polyline:"Draw a polyline",polygon:"Draw a polygon",rectangle:"Draw a rectangle",circle:"Draw a circle",marker:"Draw a marker",circlemarker:"Draw a circlemarker"}},handlers:{circle:{tooltip:{start:"Click and drag to draw circle."},radius:"Radius"},circlemarker:{tooltip:{start:"Click map to place circle marker."}},marker:{tooltip:{start:"Click map to place marker."}},polygon:{tooltip:{start:"Click to start drawing shape.",cont:"Click to continue drawing shape.",end:"Click first point to close this shape."}},polyline:{error:"<strong>Error:</strong> shape edges cannot cross!",tooltip:{start:"Click to start drawing line.",cont:"Click to continue drawing line.",end:"Click last point to finish line."}},rectangle:{tooltip:{start:"Click and drag to draw rectangle."}},simpleshape:{tooltip:{end:"Release mouse to finish drawing."}}}},edit:{toolbar:{actions:{save:{title:"Save changes",text:"Save"},cancel:{title:"Cancel editing, discards all changes",text:"Cancel"},clearAll:{title:"Clear all layers",text:"Clear All"}},buttons:{edit:"Edit layers",editDisabled:"No layers to edit",remove:"Delete layers",removeDisabled:"No layers to delete"}},handlers:{edit:{tooltip:{text:"Drag handles or markers to edit features.",subtext:"Click cancel to undo changes."}},remove:{tooltip:{text:"Click on a feature to remove."}}}}},L.Draw.Event={},L.Draw.Event.CREATED="draw:created",L.Draw.Event.EDITED="draw:edited",L.Draw.Event.DELETED="draw:deleted",L.Draw.Event.DRAWSTART="draw:drawstart",L.Draw.Event.DRAWSTOP="draw:drawstop",L.Draw.Event.DRAWVERTEX="draw:drawvertex",L.Draw.Event.EDITSTART="draw:editstart",L.Draw.Event.EDITMOVE="draw:editmove",L.Draw.Event.EDITRESIZE="draw:editresize",L.Draw.Event.EDITVERTEX="draw:editvertex",L.Draw.Event.EDITSTOP="draw:editstop",L.Draw.Event.DELETESTART="draw:deletestart",L.Draw.Event.DELETESTOP="draw:deletestop",L.Draw.Event.TOOLBAROPENED="draw:toolbaropened",L.Draw.Event.TOOLBARCLOSED="draw:toolbarclosed",L.Draw.Event.MARKERCONTEXT="draw:markercontext",L.Draw=L.Draw||{},L.Draw.Feature=L.Handler.extend({initialize:function(e,t){this._map=e,this._container=e._container,this._overlayPane=e._panes.overlayPane,this._popupPane=e._panes.popupPane,t&&t.shapeOptions&&(t.shapeOptions=L.Util.extend({},this.options.shapeOptions,t.shapeOptions)),L.setOptions(this,t);var o=L.version.split(".");parseInt(o[0],10)===1&&parseInt(o[1],10)>=2?L.Draw.Feature.include(L.Evented.prototype):L.Draw.Feature.include(L.Mixin.Events)},enable:function(){this._enabled||(L.Handler.prototype.enable.call(this),this.fire("enabled",{handler:this.type}),this._map.fire(L.Draw.Event.DRAWSTART,{layerType:this.type}))},disable:function(){this._enabled&&(L.Handler.prototype.disable.call(this),this._map.fire(L.Draw.Event.DRAWSTOP,{layerType:this.type}),this.fire("disabled",{handler:this.type}))},addHooks:function(){var e=this._map;e&&(L.DomUtil.disableTextSelection(),e.getContainer().focus(),this._tooltip=new L.Draw.Tooltip(this._map),L.DomEvent.on(this._container,"keyup",this._cancelDrawing,this))},removeHooks:function(){this._map&&(L.DomUtil.enableTextSelection(),this._tooltip.dispose(),this._tooltip=null,L.DomEvent.off(this._container,"keyup",this._cancelDrawing,this))},setOptions:function(e){L.setOptions(this,e)},_fireCreatedEvent:function(e){this._map.fire(L.Draw.Event.CREATED,{layer:e,layerType:this.type})},_cancelDrawing:function(e){e.keyCode===27&&(this._map.fire("draw:canceled",{layerType:this.type}),this.disable())}}),L.Draw.Polyline=L.Draw.Feature.extend({statics:{TYPE:"polyline"},Poly:L.Polyline,options:{allowIntersection:!0,repeatMode:!1,drawError:{color:"#b00b00",timeout:2500},icon:new L.DivIcon({iconSize:new L.Point(8,8),className:"leaflet-div-icon leaflet-editing-icon"}),touchIcon:new L.DivIcon({iconSize:new L.Point(20,20),className:"leaflet-div-icon leaflet-editing-icon leaflet-touch-icon"}),guidelineDistance:20,maxGuideLineLength:4e3,shapeOptions:{stroke:!0,color:"#3388ff",weight:4,opacity:.5,fill:!1,clickable:!0},metric:!0,feet:!0,nautic:!1,showLength:!0,zIndexOffset:2e3,factor:1,maxPoints:0},initialize:function(e,t){L.Browser.touch&&(this.options.icon=this.options.touchIcon),this.options.drawError.message=L.drawLocal.draw.handlers.polyline.error,t&&t.drawError&&(t.drawError=L.Util.extend({},this.options.drawError,t.drawError)),this.type=L.Draw.Polyline.TYPE,L.Draw.Feature.prototype.initialize.call(this,e,t)},addHooks:function(){L.Draw.Feature.prototype.addHooks.call(this),this._map&&(this._markers=[],this._markerGroup=new L.LayerGroup,this._map.addLayer(this._markerGroup),this._poly=new L.Polyline([],this.options.shapeOptions),this._tooltip.updateContent(this._getTooltipText()),this._mouseMarker||(this._mouseMarker=L.marker(this._map.getCenter(),{icon:L.divIcon({className:"leaflet-mouse-marker",iconAnchor:[20,20],iconSize:[40,40]}),opacity:0,zIndexOffset:this.options.zIndexOffset})),this._mouseMarker.on("mouseout",this._onMouseOut,this).on("mousemove",this._onMouseMove,this).on("mousedown",this._onMouseDown,this).on("mouseup",this._onMouseUp,this).addTo(this._map),this._map.on("mouseup",this._onMouseUp,this).on("mousemove",this._onMouseMove,this).on("zoomlevelschange",this._onZoomEnd,this).on("touchstart",this._onTouch,this).on("zoomend",this._onZoomEnd,this))},removeHooks:function(){L.Draw.Feature.prototype.removeHooks.call(this),this._clearHideErrorTimeout(),this._cleanUpShape(),this._map.removeLayer(this._markerGroup),delete this._markerGroup,delete this._markers,this._map.removeLayer(this._poly),delete this._poly,this._mouseMarker.off("mousedown",this._onMouseDown,this).off("mouseout",this._onMouseOut,this).off("mouseup",this._onMouseUp,this).off("mousemove",this._onMouseMove,this),this._map.removeLayer(this._mouseMarker),delete this._mouseMarker,this._clearGuides(),this._map.off("mouseup",this._onMouseUp,this).off("mousemove",this._onMouseMove,this).off("zoomlevelschange",this._onZoomEnd,this).off("zoomend",this._onZoomEnd,this).off("touchstart",this._onTouch,this).off("click",this._onTouch,this)},deleteLastVertex:function(){if(!(this._markers.length<=1)){var e=this._markers.pop(),t=this._poly,o=t.getLatLngs(),a=o.splice(-1,1)[0];this._poly.setLatLngs(o),this._markerGroup.removeLayer(e),t.getLatLngs().length<2&&this._map.removeLayer(t),this._vertexChanged(a,!1)}},addVertex:function(e){if(this._markers.length>=2&&!this.options.allowIntersection&&this._poly.newLatLngIntersects(e))return void this._showErrorTooltip();this._errorShown&&this._hideErrorTooltip(),this._markers.push(this._createMarker(e)),this._poly.addLatLng(e),this._poly.getLatLngs().length===2&&this._map.addLayer(this._poly),this._vertexChanged(e,!0)},completeShape:function(){this._markers.length<=1||!this._shapeIsValid()||(this._fireCreatedEvent(),this.disable(),this.options.repeatMode&&this.enable())},_finishShape:function(){var e=this._poly._defaultShape?this._poly._defaultShape():this._poly.getLatLngs(),t=this._poly.newLatLngIntersects(e[e.length-1]);if(!this.options.allowIntersection&&t||!this._shapeIsValid())return void this._showErrorTooltip();this._fireCreatedEvent(),this.disable(),this.options.repeatMode&&this.enable()},_shapeIsValid:function(){return!0},_onZoomEnd:function(){this._markers!==null&&this._updateGuide()},_onMouseMove:function(e){var t=this._map.mouseEventToLayerPoint(e.originalEvent),o=this._map.layerPointToLatLng(t);this._currentLatLng=o,this._updateTooltip(o),this._updateGuide(t),this._mouseMarker.setLatLng(o),L.DomEvent.preventDefault(e.originalEvent)},_vertexChanged:function(e,t){this._map.fire(L.Draw.Event.DRAWVERTEX,{layers:this._markerGroup}),this._updateFinishHandler(),this._updateRunningMeasure(e,t),this._clearGuides(),this._updateTooltip()},_onMouseDown:function(e){if(!this._clickHandled&&!this._touchHandled&&!this._disableMarkers){this._onMouseMove(e),this._clickHandled=!0,this._disableNewMarkers();var t=e.originalEvent,o=t.clientX,a=t.clientY;this._startPoint.call(this,o,a)}},_startPoint:function(e,t){this._mouseDownOrigin=L.point(e,t)},_onMouseUp:function(e){var t=e.originalEvent,o=t.clientX,a=t.clientY;this._endPoint.call(this,o,a,e),this._clickHandled=null},_endPoint:function(e,t,o){if(this._mouseDownOrigin){var a=L.point(e,t).distanceTo(this._mouseDownOrigin),l=this._calculateFinishDistance(o.latlng);this.options.maxPoints>1&&this.options.maxPoints==this._markers.length+1?(this.addVertex(o.latlng),this._finishShape()):l<10&&L.Browser.touch?this._finishShape():Math.abs(a)<9*(d.devicePixelRatio||1)&&this.addVertex(o.latlng),this._enableNewMarkers()}this._mouseDownOrigin=null},_onTouch:function(e){var t,o,a=e.originalEvent;!a.touches||!a.touches[0]||this._clickHandled||this._touchHandled||this._disableMarkers||(t=a.touches[0].clientX,o=a.touches[0].clientY,this._disableNewMarkers(),this._touchHandled=!0,this._startPoint.call(this,t,o),this._endPoint.call(this,t,o,e),this._touchHandled=null),this._clickHandled=null},_onMouseOut:function(){this._tooltip&&this._tooltip._onMouseOut.call(this._tooltip)},_calculateFinishDistance:function(e){var t;if(this._markers.length>0){var o;if(this.type===L.Draw.Polyline.TYPE)o=this._markers[this._markers.length-1];else{if(this.type!==L.Draw.Polygon.TYPE)return 1/0;o=this._markers[0]}var a=this._map.latLngToContainerPoint(o.getLatLng()),l=new L.Marker(e,{icon:this.options.icon,zIndexOffset:2*this.options.zIndexOffset}),s=this._map.latLngToContainerPoint(l.getLatLng());t=a.distanceTo(s)}else t=1/0;return t},_updateFinishHandler:function(){var e=this._markers.length;e>1&&this._markers[e-1].on("click",this._finishShape,this),e>2&&this._markers[e-2].off("click",this._finishShape,this)},_createMarker:function(e){var t=new L.Marker(e,{icon:this.options.icon,zIndexOffset:2*this.options.zIndexOffset});return this._markerGroup.addLayer(t),t},_updateGuide:function(e){var t=this._markers?this._markers.length:0;t>0&&(e=e||this._map.latLngToLayerPoint(this._currentLatLng),this._clearGuides(),this._drawGuide(this._map.latLngToLayerPoint(this._markers[t-1].getLatLng()),e))},_updateTooltip:function(e){var t=this._getTooltipText();e&&this._tooltip.updatePosition(e),this._errorShown||this._tooltip.updateContent(t)},_drawGuide:function(e,t){var o,a,l,s=Math.floor(Math.sqrt(Math.pow(t.x-e.x,2)+Math.pow(t.y-e.y,2))),c=this.options.guidelineDistance,h=this.options.maxGuideLineLength,g=s>h?s-h:c;for(this._guidesContainer||(this._guidesContainer=L.DomUtil.create("div","leaflet-draw-guides",this._overlayPane));g<s;g+=this.options.guidelineDistance)o=g/s,a={x:Math.floor(e.x*(1-o)+o*t.x),y:Math.floor(e.y*(1-o)+o*t.y)},l=L.DomUtil.create("div","leaflet-draw-guide-dash",this._guidesContainer),l.style.backgroundColor=this._errorShown?this.options.drawError.color:this.options.shapeOptions.color,L.DomUtil.setPosition(l,a)},_updateGuideColor:function(e){if(this._guidesContainer)for(var t=0,o=this._guidesContainer.childNodes.length;t<o;t++)this._guidesContainer.childNodes[t].style.backgroundColor=e},_clearGuides:function(){if(this._guidesContainer)for(;this._guidesContainer.firstChild;)this._guidesContainer.removeChild(this._guidesContainer.firstChild)},_getTooltipText:function(){var e,t,o=this.options.showLength;return this._markers.length===0?e={text:L.drawLocal.draw.handlers.polyline.tooltip.start}:(t=o?this._getMeasurementString():"",e=this._markers.length===1?{text:L.drawLocal.draw.handlers.polyline.tooltip.cont,subtext:t}:{text:L.drawLocal.draw.handlers.polyline.tooltip.end,subtext:t}),e},_updateRunningMeasure:function(e,t){var o,a,l=this._markers.length;this._markers.length===1?this._measurementRunningTotal=0:(o=l-(t?2:1),a=L.GeometryUtil.isVersion07x()?e.distanceTo(this._markers[o].getLatLng())*(this.options.factor||1):this._map.distance(e,this._markers[o].getLatLng())*(this.options.factor||1),this._measurementRunningTotal+=a*(t?1:-1))},_getMeasurementString:function(){var e,t=this._currentLatLng,o=this._markers[this._markers.length-1].getLatLng();return e=L.GeometryUtil.isVersion07x()?o&&t&&t.distanceTo?this._measurementRunningTotal+t.distanceTo(o)*(this.options.factor||1):this._measurementRunningTotal||0:o&&t?this._measurementRunningTotal+this._map.distance(t,o)*(this.options.factor||1):this._measurementRunningTotal||0,L.GeometryUtil.readableDistance(e,this.options.metric,this.options.feet,this.options.nautic,this.options.precision)},_showErrorTooltip:function(){this._errorShown=!0,this._tooltip.showAsError().updateContent({text:this.options.drawError.message}),this._updateGuideColor(this.options.drawError.color),this._poly.setStyle({color:this.options.drawError.color}),this._clearHideErrorTimeout(),this._hideErrorTimeout=setTimeout(L.Util.bind(this._hideErrorTooltip,this),this.options.drawError.timeout)},_hideErrorTooltip:function(){this._errorShown=!1,this._clearHideErrorTimeout(),this._tooltip.removeError().updateContent(this._getTooltipText()),this._updateGuideColor(this.options.shapeOptions.color),this._poly.setStyle({color:this.options.shapeOptions.color})},_clearHideErrorTimeout:function(){this._hideErrorTimeout&&(clearTimeout(this._hideErrorTimeout),this._hideErrorTimeout=null)},_disableNewMarkers:function(){this._disableMarkers=!0},_enableNewMarkers:function(){setTimeout(function(){this._disableMarkers=!1}.bind(this),50)},_cleanUpShape:function(){this._markers.length>1&&this._markers[this._markers.length-1].off("click",this._finishShape,this)},_fireCreatedEvent:function(){var e=new this.Poly(this._poly.getLatLngs(),this.options.shapeOptions);L.Draw.Feature.prototype._fireCreatedEvent.call(this,e)}}),L.Draw.Polygon=L.Draw.Polyline.extend({statics:{TYPE:"polygon"},Poly:L.Polygon,options:{showArea:!1,showLength:!1,shapeOptions:{stroke:!0,color:"#3388ff",weight:4,opacity:.5,fill:!0,fillColor:null,fillOpacity:.2,clickable:!0},metric:!0,feet:!0,nautic:!1,precision:{}},initialize:function(e,t){L.Draw.Polyline.prototype.initialize.call(this,e,t),this.type=L.Draw.Polygon.TYPE},_updateFinishHandler:function(){var e=this._markers.length;e===1&&this._markers[0].on("click",this._finishShape,this),e>2&&(this._markers[e-1].on("dblclick",this._finishShape,this),e>3&&this._markers[e-2].off("dblclick",this._finishShape,this))},_getTooltipText:function(){var e,t;return this._markers.length===0?e=L.drawLocal.draw.handlers.polygon.tooltip.start:this._markers.length<3?(e=L.drawLocal.draw.handlers.polygon.tooltip.cont,t=this._getMeasurementString()):(e=L.drawLocal.draw.handlers.polygon.tooltip.end,t=this._getMeasurementString()),{text:e,subtext:t}},_getMeasurementString:function(){var e=this._area,t="";return e||this.options.showLength?(this.options.showLength&&(t=L.Draw.Polyline.prototype._getMeasurementString.call(this)),e&&(t+="<br>"+L.GeometryUtil.readableArea(e,this.options.metric,this.options.precision)),t):null},_shapeIsValid:function(){return this._markers.length>=3},_vertexChanged:function(e,t){var o;!this.options.allowIntersection&&this.options.showArea&&(o=this._poly.getLatLngs(),this._area=L.GeometryUtil.geodesicArea(o)),L.Draw.Polyline.prototype._vertexChanged.call(this,e,t)},_cleanUpShape:function(){var e=this._markers.length;e>0&&(this._markers[0].off("click",this._finishShape,this),e>2&&this._markers[e-1].off("dblclick",this._finishShape,this))}}),L.SimpleShape={},L.Draw.SimpleShape=L.Draw.Feature.extend({options:{repeatMode:!1},initialize:function(e,t){this._endLabelText=L.drawLocal.draw.handlers.simpleshape.tooltip.end,L.Draw.Feature.prototype.initialize.call(this,e,t)},addHooks:function(){L.Draw.Feature.prototype.addHooks.call(this),this._map&&(this._mapDraggable=this._map.dragging.enabled(),this._mapDraggable&&this._map.dragging.disable(),this._container.style.cursor="crosshair",this._tooltip.updateContent({text:this._initialLabelText}),this._map.on("mousedown",this._onMouseDown,this).on("mousemove",this._onMouseMove,this).on("touchstart",this._onMouseDown,this).on("touchmove",this._onMouseMove,this),i.addEventListener("touchstart",L.DomEvent.preventDefault,{passive:!1}))},removeHooks:function(){L.Draw.Feature.prototype.removeHooks.call(this),this._map&&(this._mapDraggable&&this._map.dragging.enable(),this._container.style.cursor="",this._map.off("mousedown",this._onMouseDown,this).off("mousemove",this._onMouseMove,this).off("touchstart",this._onMouseDown,this).off("touchmove",this._onMouseMove,this),L.DomEvent.off(i,"mouseup",this._onMouseUp,this),L.DomEvent.off(i,"touchend",this._onMouseUp,this),i.removeEventListener("touchstart",L.DomEvent.preventDefault),this._shape&&(this._map.removeLayer(this._shape),delete this._shape)),this._isDrawing=!1},_getTooltipText:function(){return{text:this._endLabelText}},_onMouseDown:function(e){this._isDrawing=!0,this._startLatLng=e.latlng,L.DomEvent.on(i,"mouseup",this._onMouseUp,this).on(i,"touchend",this._onMouseUp,this).preventDefault(e.originalEvent)},_onMouseMove:function(e){var t=e.latlng;this._tooltip.updatePosition(t),this._isDrawing&&(this._tooltip.updateContent(this._getTooltipText()),this._drawShape(t))},_onMouseUp:function(){this._shape&&this._fireCreatedEvent(),this.disable(),this.options.repeatMode&&this.enable()}}),L.Draw.Rectangle=L.Draw.SimpleShape.extend({statics:{TYPE:"rectangle"},options:{shapeOptions:{stroke:!0,color:"#3388ff",weight:4,opacity:.5,fill:!0,fillColor:null,fillOpacity:.2,clickable:!0},showArea:!0,metric:!0},initialize:function(e,t){this.type=L.Draw.Rectangle.TYPE,this._initialLabelText=L.drawLocal.draw.handlers.rectangle.tooltip.start,L.Draw.SimpleShape.prototype.initialize.call(this,e,t)},disable:function(){this._enabled&&(this._isCurrentlyTwoClickDrawing=!1,L.Draw.SimpleShape.prototype.disable.call(this))},_onMouseUp:function(e){if(!this._shape&&!this._isCurrentlyTwoClickDrawing)return void(this._isCurrentlyTwoClickDrawing=!0);this._isCurrentlyTwoClickDrawing&&!r(e.target,"leaflet-pane")||L.Draw.SimpleShape.prototype._onMouseUp.call(this)},_drawShape:function(e){this._shape?this._shape.setBounds(new L.LatLngBounds(this._startLatLng,e)):(this._shape=new L.Rectangle(new L.LatLngBounds(this._startLatLng,e),this.options.shapeOptions),this._map.addLayer(this._shape))},_fireCreatedEvent:function(){var e=new L.Rectangle(this._shape.getBounds(),this.options.shapeOptions);L.Draw.SimpleShape.prototype._fireCreatedEvent.call(this,e)},_getTooltipText:function(){var e,t,o,a=L.Draw.SimpleShape.prototype._getTooltipText.call(this),l=this._shape,s=this.options.showArea;return l&&(e=this._shape._defaultShape?this._shape._defaultShape():this._shape.getLatLngs(),t=L.GeometryUtil.geodesicArea(e),o=s?L.GeometryUtil.readableArea(t,this.options.metric):""),{text:a.text,subtext:o}}}),L.Draw.Marker=L.Draw.Feature.extend({statics:{TYPE:"marker"},options:{icon:new L.Icon.Default,repeatMode:!1,zIndexOffset:2e3},initialize:function(e,t){this.type=L.Draw.Marker.TYPE,this._initialLabelText=L.drawLocal.draw.handlers.marker.tooltip.start,L.Draw.Feature.prototype.initialize.call(this,e,t)},addHooks:function(){L.Draw.Feature.prototype.addHooks.call(this),this._map&&(this._tooltip.updateContent({text:this._initialLabelText}),this._mouseMarker||(this._mouseMarker=L.marker(this._map.getCenter(),{icon:L.divIcon({className:"leaflet-mouse-marker",iconAnchor:[20,20],iconSize:[40,40]}),opacity:0,zIndexOffset:this.options.zIndexOffset})),this._mouseMarker.on("click",this._onClick,this).addTo(this._map),this._map.on("mousemove",this._onMouseMove,this),this._map.on("click",this._onTouch,this))},removeHooks:function(){L.Draw.Feature.prototype.removeHooks.call(this),this._map&&(this._map.off("click",this._onClick,this).off("click",this._onTouch,this),this._marker&&(this._marker.off("click",this._onClick,this),this._map.removeLayer(this._marker),delete this._marker),this._mouseMarker.off("click",this._onClick,this),this._map.removeLayer(this._mouseMarker),delete this._mouseMarker,this._map.off("mousemove",this._onMouseMove,this))},_onMouseMove:function(e){var t=e.latlng;this._tooltip.updatePosition(t),this._mouseMarker.setLatLng(t),this._marker?(t=this._mouseMarker.getLatLng(),this._marker.setLatLng(t)):(this._marker=this._createMarker(t),this._marker.on("click",this._onClick,this),this._map.on("click",this._onClick,this).addLayer(this._marker))},_createMarker:function(e){return new L.Marker(e,{icon:this.options.icon,zIndexOffset:this.options.zIndexOffset})},_onClick:function(){this._fireCreatedEvent(),this.disable(),this.options.repeatMode&&this.enable()},_onTouch:function(e){this._onMouseMove(e),this._onClick()},_fireCreatedEvent:function(){var e=new L.Marker.Touch(this._marker.getLatLng(),{icon:this.options.icon});L.Draw.Feature.prototype._fireCreatedEvent.call(this,e)}}),L.Draw.CircleMarker=L.Draw.Marker.extend({statics:{TYPE:"circlemarker"},options:{stroke:!0,color:"#3388ff",weight:4,opacity:.5,fill:!0,fillColor:null,fillOpacity:.2,clickable:!0,zIndexOffset:2e3},initialize:function(e,t){this.type=L.Draw.CircleMarker.TYPE,this._initialLabelText=L.drawLocal.draw.handlers.circlemarker.tooltip.start,L.Draw.Feature.prototype.initialize.call(this,e,t)},_fireCreatedEvent:function(){var e=new L.CircleMarker(this._marker.getLatLng(),this.options);L.Draw.Feature.prototype._fireCreatedEvent.call(this,e)},_createMarker:function(e){return new L.CircleMarker(e,this.options)}}),L.Draw.Circle=L.Draw.SimpleShape.extend({statics:{TYPE:"circle"},options:{shapeOptions:{stroke:!0,color:"#3388ff",weight:4,opacity:.5,fill:!0,fillColor:null,fillOpacity:.2,clickable:!0},showRadius:!0,metric:!0,feet:!0,nautic:!1},initialize:function(e,t){this.type=L.Draw.Circle.TYPE,this._initialLabelText=L.drawLocal.draw.handlers.circle.tooltip.start,L.Draw.SimpleShape.prototype.initialize.call(this,e,t)},_drawShape:function(e){if(L.GeometryUtil.isVersion07x())var t=this._startLatLng.distanceTo(e);else var t=this._map.distance(this._startLatLng,e);this._shape?this._shape.setRadius(t):(this._shape=new L.Circle(this._startLatLng,t,this.options.shapeOptions),this._map.addLayer(this._shape))},_fireCreatedEvent:function(){var e=new L.Circle(this._startLatLng,this._shape.getRadius(),this.options.shapeOptions);L.Draw.SimpleShape.prototype._fireCreatedEvent.call(this,e)},_onMouseMove:function(e){var t,o=e.latlng,a=this.options.showRadius,l=this.options.metric;if(this._tooltip.updatePosition(o),this._isDrawing){this._drawShape(o),t=this._shape.getRadius().toFixed(1);var s="";a&&(s=L.drawLocal.draw.handlers.circle.radius+": "+L.GeometryUtil.readableDistance(t,l,this.options.feet,this.options.nautic)),this._tooltip.updateContent({text:this._endLabelText,subtext:s})}}}),L.Edit=L.Edit||{},L.Edit.Marker=L.Handler.extend({initialize:function(e,t){this._marker=e,L.setOptions(this,t)},addHooks:function(){var e=this._marker;e.dragging.enable(),e.on("dragend",this._onDragEnd,e),this._toggleMarkerHighlight()},removeHooks:function(){var e=this._marker;e.dragging.disable(),e.off("dragend",this._onDragEnd,e),this._toggleMarkerHighlight()},_onDragEnd:function(e){var t=e.target;t.edited=!0,this._map.fire(L.Draw.Event.EDITMOVE,{layer:t})},_toggleMarkerHighlight:function(){var e=this._marker._icon;e&&(e.style.display="none",L.DomUtil.hasClass(e,"leaflet-edit-marker-selected")?(L.DomUtil.removeClass(e,"leaflet-edit-marker-selected"),this._offsetMarker(e,-4)):(L.DomUtil.addClass(e,"leaflet-edit-marker-selected"),this._offsetMarker(e,4)),e.style.display="")},_offsetMarker:function(e,t){var o=parseInt(e.style.marginTop,10)-t,a=parseInt(e.style.marginLeft,10)-t;e.style.marginTop=o+"px",e.style.marginLeft=a+"px"}}),L.Marker.addInitHook(function(){L.Edit.Marker&&(this.editing=new L.Edit.Marker(this),this.options.editable&&this.editing.enable())}),L.Edit=L.Edit||{},L.Edit.Poly=L.Handler.extend({initialize:function(e){this.latlngs=[e._latlngs],e._holes&&(this.latlngs=this.latlngs.concat(e._holes)),this._poly=e,this._poly.on("revert-edited",this._updateLatLngs,this)},_defaultShape:function(){return L.Polyline._flat?L.Polyline._flat(this._poly._latlngs)?this._poly._latlngs:this._poly._latlngs[0]:this._poly._latlngs},_eachVertexHandler:function(e){for(var t=0;t<this._verticesHandlers.length;t++)e(this._verticesHandlers[t])},addHooks:function(){this._initHandlers(),this._eachVertexHandler(function(e){e.addHooks()})},removeHooks:function(){this._eachVertexHandler(function(e){e.removeHooks()})},updateMarkers:function(){this._eachVertexHandler(function(e){e.updateMarkers()})},_initHandlers:function(){this._verticesHandlers=[];for(var e=0;e<this.latlngs.length;e++)this._verticesHandlers.push(new L.Edit.PolyVerticesEdit(this._poly,this.latlngs[e],this._poly.options.poly))},_updateLatLngs:function(e){this.latlngs=[e.layer._latlngs],e.layer._holes&&(this.latlngs=this.latlngs.concat(e.layer._holes))}}),L.Edit.PolyVerticesEdit=L.Handler.extend({options:{icon:new L.DivIcon({iconSize:new L.Point(8,8),className:"leaflet-div-icon leaflet-editing-icon"}),touchIcon:new L.DivIcon({iconSize:new L.Point(20,20),className:"leaflet-div-icon leaflet-editing-icon leaflet-touch-icon"}),drawError:{color:"#b00b00",timeout:1e3}},initialize:function(e,t,o){L.Browser.touch&&(this.options.icon=this.options.touchIcon),this._poly=e,o&&o.drawError&&(o.drawError=L.Util.extend({},this.options.drawError,o.drawError)),this._latlngs=t,L.setOptions(this,o)},_defaultShape:function(){return L.Polyline._flat?L.Polyline._flat(this._latlngs)?this._latlngs:this._latlngs[0]:this._latlngs},addHooks:function(){var e=this._poly,t=e._path;e instanceof L.Polygon||(e.options.fill=!1,e.options.editing&&(e.options.editing.fill=!1)),t&&e.options.editing&&e.options.editing.className&&(e.options.original.className&&e.options.original.className.split(" ").forEach(function(o){L.DomUtil.removeClass(t,o)}),e.options.editing.className.split(" ").forEach(function(o){L.DomUtil.addClass(t,o)})),e.setStyle(e.options.editing),this._poly._map&&(this._map=this._poly._map,this._markerGroup||this._initMarkers(),this._poly._map.addLayer(this._markerGroup))},removeHooks:function(){var e=this._poly,t=e._path;t&&e.options.editing&&e.options.editing.className&&(e.options.editing.className.split(" ").forEach(function(o){L.DomUtil.removeClass(t,o)}),e.options.original.className&&e.options.original.className.split(" ").forEach(function(o){L.DomUtil.addClass(t,o)})),e.setStyle(e.options.original),e._map&&(e._map.removeLayer(this._markerGroup),delete this._markerGroup,delete this._markers)},updateMarkers:function(){this._markerGroup.clearLayers(),this._initMarkers()},_initMarkers:function(){this._markerGroup||(this._markerGroup=new L.LayerGroup),this._markers=[];var e,t,o,a,l=this._defaultShape();for(e=0,o=l.length;e<o;e++)a=this._createMarker(l[e],e),a.on("click",this._onMarkerClick,this),a.on("contextmenu",this._onContextMenu,this),this._markers.push(a);var s,c;for(e=0,t=o-1;e<o;t=e++)(e!==0||L.Polygon&&this._poly instanceof L.Polygon)&&(s=this._markers[t],c=this._markers[e],this._createMiddleMarker(s,c),this._updatePrevNext(s,c))},_createMarker:function(e,t){var o=new L.Marker.Touch(e,{draggable:!0,icon:this.options.icon});return o._origLatLng=e,o._index=t,o.on("dragstart",this._onMarkerDragStart,this).on("drag",this._onMarkerDrag,this).on("dragend",this._fireEdit,this).on("touchmove",this._onTouchMove,this).on("touchend",this._fireEdit,this).on("MSPointerMove",this._onTouchMove,this).on("MSPointerUp",this._fireEdit,this),this._markerGroup.addLayer(o),o},_onMarkerDragStart:function(){this._poly.fire("editstart")},_spliceLatLngs:function(){var e=this._defaultShape(),t=[].splice.apply(e,arguments);return this._poly._convertLatLngs(e,!0),this._poly.redraw(),t},_removeMarker:function(e){var t=e._index;this._markerGroup.removeLayer(e),this._markers.splice(t,1),this._spliceLatLngs(t,1),this._updateIndexes(t,-1),e.off("dragstart",this._onMarkerDragStart,this).off("drag",this._onMarkerDrag,this).off("dragend",this._fireEdit,this).off("touchmove",this._onMarkerDrag,this).off("touchend",this._fireEdit,this).off("click",this._onMarkerClick,this).off("MSPointerMove",this._onTouchMove,this).off("MSPointerUp",this._fireEdit,this)},_fireEdit:function(){this._poly.edited=!0,this._poly.fire("edit"),this._poly._map.fire(L.Draw.Event.EDITVERTEX,{layers:this._markerGroup,poly:this._poly})},_onMarkerDrag:function(e){var t=e.target,o=this._poly,a=L.LatLngUtil.cloneLatLng(t._origLatLng);if(L.extend(t._origLatLng,t._latlng),o.options.poly){var l=o._map._editTooltip;if(!o.options.poly.allowIntersection&&o.intersects()){L.extend(t._origLatLng,a),t.setLatLng(a);var s=o.options.color;o.setStyle({color:this.options.drawError.color}),l&&l.updateContent({text:L.drawLocal.draw.handlers.polyline.error}),setTimeout(function(){o.setStyle({color:s}),l&&l.updateContent({text:L.drawLocal.edit.handlers.edit.tooltip.text,subtext:L.drawLocal.edit.handlers.edit.tooltip.subtext})},1e3)}}t._middleLeft&&t._middleLeft.setLatLng(this._getMiddleLatLng(t._prev,t)),t._middleRight&&t._middleRight.setLatLng(this._getMiddleLatLng(t,t._next)),this._poly._bounds._southWest=L.latLng(1/0,1/0),this._poly._bounds._northEast=L.latLng(-1/0,-1/0);var c=this._poly.getLatLngs();this._poly._convertLatLngs(c,!0),this._poly.redraw(),this._poly.fire("editdrag")},_onMarkerClick:function(e){var t=L.Polygon&&this._poly instanceof L.Polygon?4:3,o=e.target;this._defaultShape().length<t||(this._removeMarker(o),this._updatePrevNext(o._prev,o._next),o._middleLeft&&this._markerGroup.removeLayer(o._middleLeft),o._middleRight&&this._markerGroup.removeLayer(o._middleRight),o._prev&&o._next?this._createMiddleMarker(o._prev,o._next):o._prev?o._next||(o._prev._middleRight=null):o._next._middleLeft=null,this._fireEdit())},_onContextMenu:function(e){var t=e.target;this._poly,this._poly._map.fire(L.Draw.Event.MARKERCONTEXT,{marker:t,layers:this._markerGroup,poly:this._poly}),L.DomEvent.stopPropagation},_onTouchMove:function(e){var t=this._map.mouseEventToLayerPoint(e.originalEvent.touches[0]),o=this._map.layerPointToLatLng(t),a=e.target;L.extend(a._origLatLng,o),a._middleLeft&&a._middleLeft.setLatLng(this._getMiddleLatLng(a._prev,a)),a._middleRight&&a._middleRight.setLatLng(this._getMiddleLatLng(a,a._next)),this._poly.redraw(),this.updateMarkers()},_updateIndexes:function(e,t){this._markerGroup.eachLayer(function(o){o._index>e&&(o._index+=t)})},_createMiddleMarker:function(e,t){var o,a,l,s=this._getMiddleLatLng(e,t),c=this._createMarker(s);c.setOpacity(.6),e._middleRight=t._middleLeft=c,a=function(){c.off("touchmove",a,this);var h=t._index;c._index=h,c.off("click",o,this).on("click",this._onMarkerClick,this),s.lat=c.getLatLng().lat,s.lng=c.getLatLng().lng,this._spliceLatLngs(h,0,s),this._markers.splice(h,0,c),c.setOpacity(1),this._updateIndexes(h,1),t._index++,this._updatePrevNext(e,c),this._updatePrevNext(c,t),this._poly.fire("editstart")},l=function(){c.off("dragstart",a,this),c.off("dragend",l,this),c.off("touchmove",a,this),this._createMiddleMarker(e,c),this._createMiddleMarker(c,t)},o=function(){a.call(this),l.call(this),this._fireEdit()},c.on("click",o,this).on("dragstart",a,this).on("dragend",l,this).on("touchmove",a,this),this._markerGroup.addLayer(c)},_updatePrevNext:function(e,t){e&&(e._next=t),t&&(t._prev=e)},_getMiddleLatLng:function(e,t){var o=this._poly._map,a=o.project(e.getLatLng()),l=o.project(t.getLatLng());return o.unproject(a._add(l)._divideBy(2))}}),L.Polyline.addInitHook(function(){this.editing||(L.Edit.Poly&&(this.editing=new L.Edit.Poly(this),this.options.editable&&this.editing.enable()),this.on("add",function(){this.editing&&this.editing.enabled()&&this.editing.addHooks()}),this.on("remove",function(){this.editing&&this.editing.enabled()&&this.editing.removeHooks()}))}),L.Edit=L.Edit||{},L.Edit.SimpleShape=L.Handler.extend({options:{moveIcon:new L.DivIcon({iconSize:new L.Point(8,8),className:"leaflet-div-icon leaflet-editing-icon leaflet-edit-move"}),resizeIcon:new L.DivIcon({iconSize:new L.Point(8,8),className:"leaflet-div-icon leaflet-editing-icon leaflet-edit-resize"}),touchMoveIcon:new L.DivIcon({iconSize:new L.Point(20,20),className:"leaflet-div-icon leaflet-editing-icon leaflet-edit-move leaflet-touch-icon"}),touchResizeIcon:new L.DivIcon({iconSize:new L.Point(20,20),className:"leaflet-div-icon leaflet-editing-icon leaflet-edit-resize leaflet-touch-icon"})},initialize:function(e,t){L.Browser.touch&&(this.options.moveIcon=this.options.touchMoveIcon,this.options.resizeIcon=this.options.touchResizeIcon),this._shape=e,L.Util.setOptions(this,t)},addHooks:function(){var e=this._shape;this._shape._map&&(this._map=this._shape._map,e.setStyle(e.options.editing),e._map&&(this._map=e._map,this._markerGroup||this._initMarkers(),this._map.addLayer(this._markerGroup)))},removeHooks:function(){var e=this._shape;if(e.setStyle(e.options.original),e._map){this._unbindMarker(this._moveMarker);for(var t=0,o=this._resizeMarkers.length;t<o;t++)this._unbindMarker(this._resizeMarkers[t]);this._resizeMarkers=null,this._map.removeLayer(this._markerGroup),delete this._markerGroup}this._map=null},updateMarkers:function(){this._markerGroup.clearLayers(),this._initMarkers()},_initMarkers:function(){this._markerGroup||(this._markerGroup=new L.LayerGroup),this._createMoveMarker(),this._createResizeMarker()},_createMoveMarker:function(){},_createResizeMarker:function(){},_createMarker:function(e,t){var o=new L.Marker.Touch(e,{draggable:!0,icon:t,zIndexOffset:10});return this._bindMarker(o),this._markerGroup.addLayer(o),o},_bindMarker:function(e){e.on("dragstart",this._onMarkerDragStart,this).on("drag",this._onMarkerDrag,this).on("dragend",this._onMarkerDragEnd,this).on("touchstart",this._onTouchStart,this).on("touchmove",this._onTouchMove,this).on("MSPointerMove",this._onTouchMove,this).on("touchend",this._onTouchEnd,this).on("MSPointerUp",this._onTouchEnd,this)},_unbindMarker:function(e){e.off("dragstart",this._onMarkerDragStart,this).off("drag",this._onMarkerDrag,this).off("dragend",this._onMarkerDragEnd,this).off("touchstart",this._onTouchStart,this).off("touchmove",this._onTouchMove,this).off("MSPointerMove",this._onTouchMove,this).off("touchend",this._onTouchEnd,this).off("MSPointerUp",this._onTouchEnd,this)},_onMarkerDragStart:function(e){e.target.setOpacity(0),this._shape.fire("editstart")},_fireEdit:function(){this._shape.edited=!0,this._shape.fire("edit")},_onMarkerDrag:function(e){var t=e.target,o=t.getLatLng();t===this._moveMarker?this._move(o):this._resize(o),this._shape.redraw(),this._shape.fire("editdrag")},_onMarkerDragEnd:function(e){e.target.setOpacity(1),this._fireEdit()},_onTouchStart:function(e){if(L.Edit.SimpleShape.prototype._onMarkerDragStart.call(this,e),typeof this._getCorners=="function"){var t=this._getCorners(),o=e.target,a=o._cornerIndex;o.setOpacity(0),this._oppositeCorner=t[(a+2)%4],this._toggleCornerMarkers(0,a)}this._shape.fire("editstart")},_onTouchMove:function(e){var t=this._map.mouseEventToLayerPoint(e.originalEvent.touches[0]),o=this._map.layerPointToLatLng(t);return e.target===this._moveMarker?this._move(o):this._resize(o),this._shape.redraw(),!1},_onTouchEnd:function(e){e.target.setOpacity(1),this.updateMarkers(),this._fireEdit()},_move:function(){},_resize:function(){}}),L.Edit=L.Edit||{},L.Edit.Rectangle=L.Edit.SimpleShape.extend({_createMoveMarker:function(){var e=this._shape.getBounds(),t=e.getCenter();this._moveMarker=this._createMarker(t,this.options.moveIcon)},_createResizeMarker:function(){var e=this._getCorners();this._resizeMarkers=[];for(var t=0,o=e.length;t<o;t++)this._resizeMarkers.push(this._createMarker(e[t],this.options.resizeIcon)),this._resizeMarkers[t]._cornerIndex=t},_onMarkerDragStart:function(e){L.Edit.SimpleShape.prototype._onMarkerDragStart.call(this,e);var t=this._getCorners(),o=e.target,a=o._cornerIndex;this._oppositeCorner=t[(a+2)%4],this._toggleCornerMarkers(0,a)},_onMarkerDragEnd:function(e){var t,o,a=e.target;a===this._moveMarker&&(t=this._shape.getBounds(),o=t.getCenter(),a.setLatLng(o)),this._toggleCornerMarkers(1),this._repositionCornerMarkers(),L.Edit.SimpleShape.prototype._onMarkerDragEnd.call(this,e)},_move:function(e){for(var t,o=this._shape._defaultShape?this._shape._defaultShape():this._shape.getLatLngs(),a=this._shape.getBounds(),l=a.getCenter(),s=[],c=0,h=o.length;c<h;c++)t=[o[c].lat-l.lat,o[c].lng-l.lng],s.push([e.lat+t[0],e.lng+t[1]]);this._shape.setLatLngs(s),this._repositionCornerMarkers(),this._map.fire(L.Draw.Event.EDITMOVE,{layer:this._shape})},_resize:function(e){var t;this._shape.setBounds(L.latLngBounds(e,this._oppositeCorner)),t=this._shape.getBounds(),this._moveMarker.setLatLng(t.getCenter()),this._map.fire(L.Draw.Event.EDITRESIZE,{layer:this._shape})},_getCorners:function(){var e=this._shape.getBounds();return[e.getNorthWest(),e.getNorthEast(),e.getSouthEast(),e.getSouthWest()]},_toggleCornerMarkers:function(e){for(var t=0,o=this._resizeMarkers.length;t<o;t++)this._resizeMarkers[t].setOpacity(e)},_repositionCornerMarkers:function(){for(var e=this._getCorners(),t=0,o=this._resizeMarkers.length;t<o;t++)this._resizeMarkers[t].setLatLng(e[t])}}),L.Rectangle.addInitHook(function(){L.Edit.Rectangle&&(this.editing=new L.Edit.Rectangle(this),this.options.editable&&this.editing.enable())}),L.Edit=L.Edit||{},L.Edit.CircleMarker=L.Edit.SimpleShape.extend({_createMoveMarker:function(){var e=this._shape.getLatLng();this._moveMarker=this._createMarker(e,this.options.moveIcon)},_createResizeMarker:function(){this._resizeMarkers=[]},_move:function(e){if(this._resizeMarkers.length){var t=this._getResizeMarkerPoint(e);this._resizeMarkers[0].setLatLng(t)}this._shape.setLatLng(e),this._map.fire(L.Draw.Event.EDITMOVE,{layer:this._shape})}}),L.CircleMarker.addInitHook(function(){L.Edit.CircleMarker&&(this.editing=new L.Edit.CircleMarker(this),this.options.editable&&this.editing.enable()),this.on("add",function(){this.editing&&this.editing.enabled()&&this.editing.addHooks()}),this.on("remove",function(){this.editing&&this.editing.enabled()&&this.editing.removeHooks()})}),L.Edit=L.Edit||{},L.Edit.Circle=L.Edit.CircleMarker.extend({_createResizeMarker:function(){var e=this._shape.getLatLng(),t=this._getResizeMarkerPoint(e);this._resizeMarkers=[],this._resizeMarkers.push(this._createMarker(t,this.options.resizeIcon))},_getResizeMarkerPoint:function(e){var t=this._shape._radius*Math.cos(Math.PI/4),o=this._map.project(e);return this._map.unproject([o.x+t,o.y-t])},_resize:function(e){var t=this._moveMarker.getLatLng();L.GeometryUtil.isVersion07x()?radius=t.distanceTo(e):radius=this._map.distance(t,e),this._shape.setRadius(radius),this._map.editTooltip&&this._map._editTooltip.updateContent({text:L.drawLocal.edit.handlers.edit.tooltip.subtext+"<br />"+L.drawLocal.edit.handlers.edit.tooltip.text,subtext:L.drawLocal.draw.handlers.circle.radius+": "+L.GeometryUtil.readableDistance(radius,!0,this.options.feet,this.options.nautic)}),this._shape.setRadius(radius),this._map.fire(L.Draw.Event.EDITRESIZE,{layer:this._shape})}}),L.Circle.addInitHook(function(){L.Edit.Circle&&(this.editing=new L.Edit.Circle(this),this.options.editable&&this.editing.enable())}),L.Map.mergeOptions({touchExtend:!0}),L.Map.TouchExtend=L.Handler.extend({initialize:function(e){this._map=e,this._container=e._container,this._pane=e._panes.overlayPane},addHooks:function(){L.DomEvent.on(this._container,"touchstart",this._onTouchStart,this),L.DomEvent.on(this._container,"touchend",this._onTouchEnd,this),L.DomEvent.on(this._container,"touchmove",this._onTouchMove,this),this._detectIE()?(L.DomEvent.on(this._container,"MSPointerDown",this._onTouchStart,this),L.DomEvent.on(this._container,"MSPointerUp",this._onTouchEnd,this),L.DomEvent.on(this._container,"MSPointerMove",this._onTouchMove,this),L.DomEvent.on(this._container,"MSPointerCancel",this._onTouchCancel,this)):(L.DomEvent.on(this._container,"touchcancel",this._onTouchCancel,this),L.DomEvent.on(this._container,"touchleave",this._onTouchLeave,this))},removeHooks:function(){L.DomEvent.off(this._container,"touchstart",this._onTouchStart,this),L.DomEvent.off(this._container,"touchend",this._onTouchEnd,this),L.DomEvent.off(this._container,"touchmove",this._onTouchMove,this),this._detectIE()?(L.DomEvent.off(this._container,"MSPointerDown",this._onTouchStart,this),L.DomEvent.off(this._container,"MSPointerUp",this._onTouchEnd,this),L.DomEvent.off(this._container,"MSPointerMove",this._onTouchMove,this),L.DomEvent.off(this._container,"MSPointerCancel",this._onTouchCancel,this)):(L.DomEvent.off(this._container,"touchcancel",this._onTouchCancel,this),L.DomEvent.off(this._container,"touchleave",this._onTouchLeave,this))},_touchEvent:function(e,t){var o={};if(e.touches!==void 0){if(!e.touches.length)return;o=e.touches[0]}else if(e.pointerType!=="touch"||(o=e,!this._filterClick(e)))return;var a=this._map.mouseEventToContainerPoint(o),l=this._map.mouseEventToLayerPoint(o),s=this._map.layerPointToLatLng(l);this._map.fire(t,{latlng:s,layerPoint:l,containerPoint:a,pageX:o.pageX,pageY:o.pageY,originalEvent:e})},_filterClick:function(e){var t=e.timeStamp||e.originalEvent.timeStamp,o=L.DomEvent._lastClick&&t-L.DomEvent._lastClick;return o&&o>100&&o<500||e.target._simulatedClick&&!e._simulated?(L.DomEvent.stop(e),!1):(L.DomEvent._lastClick=t,!0)},_onTouchStart:function(e){this._map._loaded&&this._touchEvent(e,"touchstart")},_onTouchEnd:function(e){this._map._loaded&&this._touchEvent(e,"touchend")},_onTouchCancel:function(e){if(this._map._loaded){var t="touchcancel";this._detectIE()&&(t="pointercancel"),this._touchEvent(e,t)}},_onTouchLeave:function(e){this._map._loaded&&this._touchEvent(e,"touchleave")},_onTouchMove:function(e){this._map._loaded&&this._touchEvent(e,"touchmove")},_detectIE:function(){var e=d.navigator.userAgent,t=e.indexOf("MSIE ");if(t>0)return parseInt(e.substring(t+5,e.indexOf(".",t)),10);if(e.indexOf("Trident/")>0){var o=e.indexOf("rv:");return parseInt(e.substring(o+3,e.indexOf(".",o)),10)}var a=e.indexOf("Edge/");return a>0&&parseInt(e.substring(a+5,e.indexOf(".",a)),10)}}),L.Map.addInitHook("addHandler","touchExtend",L.Map.TouchExtend),L.Marker.Touch=L.Marker.extend({_initInteraction:function(){return this.addInteractiveTarget?L.Marker.prototype._initInteraction.apply(this):this._initInteractionLegacy()},_initInteractionLegacy:function(){if(this.options.clickable){var e=this._icon,t=["dblclick","mousedown","mouseover","mouseout","contextmenu","touchstart","touchend","touchmove"];this._detectIE?t.concat(["MSPointerDown","MSPointerUp","MSPointerMove","MSPointerCancel"]):t.concat(["touchcancel"]),L.DomUtil.addClass(e,"leaflet-clickable"),L.DomEvent.on(e,"click",this._onMouseClick,this),L.DomEvent.on(e,"keypress",this._onKeyPress,this);for(var o=0;o<t.length;o++)L.DomEvent.on(e,t[o],this._fireMouseEvent,this);L.Handler.MarkerDrag&&(this.dragging=new L.Handler.MarkerDrag(this),this.options.draggable&&this.dragging.enable())}},_detectIE:function(){var e=d.navigator.userAgent,t=e.indexOf("MSIE ");if(t>0)return parseInt(e.substring(t+5,e.indexOf(".",t)),10);if(e.indexOf("Trident/")>0){var o=e.indexOf("rv:");return parseInt(e.substring(o+3,e.indexOf(".",o)),10)}var a=e.indexOf("Edge/");return a>0&&parseInt(e.substring(a+5,e.indexOf(".",a)),10)}}),L.LatLngUtil={cloneLatLngs:function(e){for(var t=[],o=0,a=e.length;o<a;o++)Array.isArray(e[o])?t.push(L.LatLngUtil.cloneLatLngs(e[o])):t.push(this.cloneLatLng(e[o]));return t},cloneLatLng:function(e){return L.latLng(e.lat,e.lng)}},(function(){var e={km:2,ha:2,m:0,mi:2,ac:2,yd:0,ft:0,nm:2};L.GeometryUtil=L.extend(L.GeometryUtil||{},{geodesicArea:function(t){var o,a,l=t.length,s=0,c=Math.PI/180;if(l>2){for(var h=0;h<l;h++)o=t[h],a=t[(h+1)%l],s+=(a.lng-o.lng)*c*(2+Math.sin(o.lat*c)+Math.sin(a.lat*c));s=6378137*s*6378137/2}return Math.abs(s)},formattedNumber:function(t,o){var a=parseFloat(t).toFixed(o),l=L.drawLocal.format&&L.drawLocal.format.numeric,s=l&&l.delimiters,c=s&&s.thousands,h=s&&s.decimal;if(c||h){var g=a.split(".");a=c?g[0].replace(/(\d)(?=(\d{3})+(?!\d))/g,"$1"+c):g[0],h=h||".",g.length>1&&(a=a+h+g[1])}return a},readableArea:function(t,o,c){var l,s,c=L.Util.extend({},e,c);return o?(s=["ha","m"],type=typeof o,type==="string"?s=[o]:type!=="boolean"&&(s=o),l=t>=1e6&&s.indexOf("km")!==-1?L.GeometryUtil.formattedNumber(1e-6*t,c.km)+" km\xB2":t>=1e4&&s.indexOf("ha")!==-1?L.GeometryUtil.formattedNumber(1e-4*t,c.ha)+" ha":L.GeometryUtil.formattedNumber(t,c.m)+" m\xB2"):(t/=.836127,l=t>=3097600?L.GeometryUtil.formattedNumber(t/3097600,c.mi)+" mi\xB2":t>=4840?L.GeometryUtil.formattedNumber(t/4840,c.ac)+" acres":L.GeometryUtil.formattedNumber(t,c.yd)+" yd\xB2"),l},readableDistance:function(t,o,a,l,h){var c,h=L.Util.extend({},e,h);switch(o?typeof o=="string"?o:"metric":a?"feet":l?"nauticalMile":"yards"){case"metric":c=t>1e3?L.GeometryUtil.formattedNumber(t/1e3,h.km)+" km":L.GeometryUtil.formattedNumber(t,h.m)+" m";break;case"feet":t*=3.28083,c=L.GeometryUtil.formattedNumber(t,h.ft)+" ft";break;case"nauticalMile":t*=.53996,c=L.GeometryUtil.formattedNumber(t/1e3,h.nm)+" nm";break;default:t*=1.09361,c=t>1760?L.GeometryUtil.formattedNumber(t/1760,h.mi)+" miles":L.GeometryUtil.formattedNumber(t,h.yd)+" yd"}return c},isVersion07x:function(){var t=L.version.split(".");return parseInt(t[0],10)===0&&parseInt(t[1],10)===7}})})(),L.Util.extend(L.LineUtil,{segmentsIntersect:function(e,t,o,a){return this._checkCounterclockwise(e,o,a)!==this._checkCounterclockwise(t,o,a)&&this._checkCounterclockwise(e,t,o)!==this._checkCounterclockwise(e,t,a)},_checkCounterclockwise:function(e,t,o){return(o.y-e.y)*(t.x-e.x)>(t.y-e.y)*(o.x-e.x)}}),L.Polyline.include({intersects:function(){var e,t,o,a=this._getProjectedPoints(),l=a?a.length:0;if(this._tooFewPointsForIntersection())return!1;for(e=l-1;e>=3;e--)if(t=a[e-1],o=a[e],this._lineSegmentsIntersectsRange(t,o,e-2))return!0;return!1},newLatLngIntersects:function(e,t){return!!this._map&&this.newPointIntersects(this._map.latLngToLayerPoint(e),t)},newPointIntersects:function(e,t){var o=this._getProjectedPoints(),a=o?o.length:0,l=o?o[a-1]:null,s=a-2;return!this._tooFewPointsForIntersection(1)&&this._lineSegmentsIntersectsRange(l,e,s,t?1:0)},_tooFewPointsForIntersection:function(e){var t=this._getProjectedPoints(),o=t?t.length:0;return o+=e||0,!t||o<=3},_lineSegmentsIntersectsRange:function(e,t,o,a){var l,s,c=this._getProjectedPoints();a=a||0;for(var h=o;h>a;h--)if(l=c[h-1],s=c[h],L.LineUtil.segmentsIntersect(e,t,l,s))return!0;return!1},_getProjectedPoints:function(){if(!this._defaultShape)return this._originalPoints;for(var e=[],t=this._defaultShape(),o=0;o<t.length;o++)e.push(this._map.latLngToLayerPoint(t[o]));return e}}),L.Polygon.include({intersects:function(){var e,t,o,a,l=this._getProjectedPoints();return!this._tooFewPointsForIntersection()&&(!!L.Polyline.prototype.intersects.call(this)||(e=l.length,t=l[0],o=l[e-1],a=e-2,this._lineSegmentsIntersectsRange(o,t,a,1)))}}),L.Control.Draw=L.Control.extend({options:{position:"topleft",draw:{},edit:!1},initialize:function(e){if(L.version<"0.7")throw new Error("Leaflet.draw 0.2.3+ requires Leaflet 0.7.0+. Download latest from https://github.com/Leaflet/Leaflet/");L.Control.prototype.initialize.call(this,e);var t;this._toolbars={},L.DrawToolbar&&this.options.draw&&(t=new L.DrawToolbar(this.options.draw),this._toolbars[L.DrawToolbar.TYPE]=t,this._toolbars[L.DrawToolbar.TYPE].on("enable",this._toolbarEnabled,this)),L.EditToolbar&&this.options.edit&&(t=new L.EditToolbar(this.options.edit),this._toolbars[L.EditToolbar.TYPE]=t,this._toolbars[L.EditToolbar.TYPE].on("enable",this._toolbarEnabled,this)),L.toolbar=this},onAdd:function(e){var t,o=L.DomUtil.create("div","leaflet-draw"),a=!1;for(var l in this._toolbars)this._toolbars.hasOwnProperty(l)&&(t=this._toolbars[l].addToolbar(e))&&(a||(L.DomUtil.hasClass(t,"leaflet-draw-toolbar-top")||L.DomUtil.addClass(t.childNodes[0],"leaflet-draw-toolbar-top"),a=!0),o.appendChild(t));return o},onRemove:function(){for(var e in this._toolbars)this._toolbars.hasOwnProperty(e)&&this._toolbars[e].removeToolbar()},setDrawingOptions:function(e){for(var t in this._toolbars)this._toolbars[t]instanceof L.DrawToolbar&&this._toolbars[t].setOptions(e)},_toolbarEnabled:function(e){var t=e.target;for(var o in this._toolbars)this._toolbars[o]!==t&&this._toolbars[o].disable()}}),L.Map.mergeOptions({drawControlTooltips:!0,drawControl:!1}),L.Map.addInitHook(function(){this.options.drawControl&&(this.drawControl=new L.Control.Draw,this.addControl(this.drawControl))}),L.Toolbar=L.Class.extend({initialize:function(e){L.setOptions(this,e),this._modes={},this._actionButtons=[],this._activeMode=null;var t=L.version.split(".");parseInt(t[0],10)===1&&parseInt(t[1],10)>=2?L.Toolbar.include(L.Evented.prototype):L.Toolbar.include(L.Mixin.Events)},enabled:function(){return this._activeMode!==null},disable:function(){this.enabled()&&this._activeMode.handler.disable()},addToolbar:function(e){var t,o=L.DomUtil.create("div","leaflet-draw-section"),a=0,l=this._toolbarClass||"",s=this.getModeHandlers(e);for(this._toolbarContainer=L.DomUtil.create("div","leaflet-draw-toolbar leaflet-bar"),this._map=e,t=0;t<s.length;t++)s[t].enabled&&this._initModeHandler(s[t].handler,this._toolbarContainer,a++,l,s[t].title);if(a)return this._lastButtonIndex=--a,this._actionsContainer=L.DomUtil.create("ul","leaflet-draw-actions"),o.appendChild(this._toolbarContainer),o.appendChild(this._actionsContainer),o},removeToolbar:function(){for(var e in this._modes)this._modes.hasOwnProperty(e)&&(this._disposeButton(this._modes[e].button,this._modes[e].handler.enable,this._modes[e].handler),this._modes[e].handler.disable(),this._modes[e].handler.off("enabled",this._handlerActivated,this).off("disabled",this._handlerDeactivated,this));this._modes={};for(var t=0,o=this._actionButtons.length;t<o;t++)this._disposeButton(this._actionButtons[t].button,this._actionButtons[t].callback,this);this._actionButtons=[],this._actionsContainer=null},_initModeHandler:function(e,t,o,a,l){var s=e.type;this._modes[s]={},this._modes[s].handler=e,this._modes[s].button=this._createButton({type:s,title:l,className:a+"-"+s,container:t,callback:this._modes[s].handler.enable,context:this._modes[s].handler}),this._modes[s].buttonIndex=o,this._modes[s].handler.on("enabled",this._handlerActivated,this).on("disabled",this._handlerDeactivated,this)},_detectIOS:function(){return/iPad|iPhone|iPod/.test(navigator.userAgent)&&!d.MSStream},_createButton:function(e){var t=L.DomUtil.create("a",e.className||"",e.container),o=L.DomUtil.create("span","sr-only",e.container);t.href="#",t.appendChild(o),e.title&&(t.title=e.title,o.innerHTML=e.title),e.text&&(t.innerHTML=e.text,o.innerHTML=e.text);var a=this._detectIOS()?"touchstart":"click";return L.DomEvent.on(t,"click",L.DomEvent.stopPropagation).on(t,"mousedown",L.DomEvent.stopPropagation).on(t,"dblclick",L.DomEvent.stopPropagation).on(t,"touchstart",L.DomEvent.stopPropagation).on(t,"click",L.DomEvent.preventDefault).on(t,a,e.callback,e.context),t},_disposeButton:function(e,t){var o=this._detectIOS()?"touchstart":"click";L.DomEvent.off(e,"click",L.DomEvent.stopPropagation).off(e,"mousedown",L.DomEvent.stopPropagation).off(e,"dblclick",L.DomEvent.stopPropagation).off(e,"touchstart",L.DomEvent.stopPropagation).off(e,"click",L.DomEvent.preventDefault).off(e,o,t)},_handlerActivated:function(e){this.disable(),this._activeMode=this._modes[e.handler],L.DomUtil.addClass(this._activeMode.button,"leaflet-draw-toolbar-button-enabled"),this._showActionsToolbar(),this.fire("enable")},_handlerDeactivated:function(){this._hideActionsToolbar(),L.DomUtil.removeClass(this._activeMode.button,"leaflet-draw-toolbar-button-enabled"),this._activeMode=null,this.fire("disable")},_createActions:function(e){var t,o,a,l,s=this._actionsContainer,c=this.getActions(e),h=c.length;for(o=0,a=this._actionButtons.length;o<a;o++)this._disposeButton(this._actionButtons[o].button,this._actionButtons[o].callback);for(this._actionButtons=[];s.firstChild;)s.removeChild(s.firstChild);for(var g=0;g<h;g++)"enabled"in c[g]&&!c[g].enabled||(t=L.DomUtil.create("li","",s),l=this._createButton({title:c[g].title,text:c[g].text,container:t,callback:c[g].callback,context:c[g].context}),this._actionButtons.push({button:l,callback:c[g].callback}))},_showActionsToolbar:function(){var e=this._activeMode.buttonIndex,t=this._lastButtonIndex,o=this._activeMode.button.offsetTop-1;this._createActions(this._activeMode.handler),this._actionsContainer.style.top=o+"px",e===0&&(L.DomUtil.addClass(this._toolbarContainer,"leaflet-draw-toolbar-notop"),L.DomUtil.addClass(this._actionsContainer,"leaflet-draw-actions-top")),e===t&&(L.DomUtil.addClass(this._toolbarContainer,"leaflet-draw-toolbar-nobottom"),L.DomUtil.addClass(this._actionsContainer,"leaflet-draw-actions-bottom")),this._actionsContainer.style.display="block",this._map.fire(L.Draw.Event.TOOLBAROPENED)},_hideActionsToolbar:function(){this._actionsContainer.style.display="none",L.DomUtil.removeClass(this._toolbarContainer,"leaflet-draw-toolbar-notop"),L.DomUtil.removeClass(this._toolbarContainer,"leaflet-draw-toolbar-nobottom"),L.DomUtil.removeClass(this._actionsContainer,"leaflet-draw-actions-top"),L.DomUtil.removeClass(this._actionsContainer,"leaflet-draw-actions-bottom"),this._map.fire(L.Draw.Event.TOOLBARCLOSED)}}),L.Draw=L.Draw||{},L.Draw.Tooltip=L.Class.extend({initialize:function(e){this._map=e,this._popupPane=e._panes.popupPane,this._visible=!1,this._container=e.options.drawControlTooltips?L.DomUtil.create("div","leaflet-draw-tooltip",this._popupPane):null,this._singleLineLabel=!1,this._map.on("mouseout",this._onMouseOut,this)},dispose:function(){this._map.off("mouseout",this._onMouseOut,this),this._container&&(this._popupPane.removeChild(this._container),this._container=null)},updateContent:function(e){return this._container?(e.subtext=e.subtext||"",e.subtext.length!==0||this._singleLineLabel?e.subtext.length>0&&this._singleLineLabel&&(L.DomUtil.removeClass(this._container,"leaflet-draw-tooltip-single"),this._singleLineLabel=!1):(L.DomUtil.addClass(this._container,"leaflet-draw-tooltip-single"),this._singleLineLabel=!0),this._container.innerHTML=(e.subtext.length>0?'<span class="leaflet-draw-tooltip-subtext">'+e.subtext+"</span><br />":"")+"<span>"+e.text+"</span>",e.text||e.subtext?(this._visible=!0,this._container.style.visibility="inherit"):(this._visible=!1,this._container.style.visibility="hidden"),this):this},updatePosition:function(e){var t=this._map.latLngToLayerPoint(e),o=this._container;return this._container&&(this._visible&&(o.style.visibility="inherit"),L.DomUtil.setPosition(o,t)),this},showAsError:function(){return this._container&&L.DomUtil.addClass(this._container,"leaflet-error-draw-tooltip"),this},removeError:function(){return this._container&&L.DomUtil.removeClass(this._container,"leaflet-error-draw-tooltip"),this},_onMouseOut:function(){this._container&&(this._container.style.visibility="hidden")}}),L.DrawToolbar=L.Toolbar.extend({statics:{TYPE:"draw"},options:{polyline:{},polygon:{},rectangle:{},circle:{},marker:{},circlemarker:{}},initialize:function(e){for(var t in this.options)this.options.hasOwnProperty(t)&&e[t]&&(e[t]=L.extend({},this.options[t],e[t]));this._toolbarClass="leaflet-draw-draw",L.Toolbar.prototype.initialize.call(this,e)},getModeHandlers:function(e){return[{enabled:this.options.polyline,handler:new L.Draw.Polyline(e,this.options.polyline),title:L.drawLocal.draw.toolbar.buttons.polyline},{enabled:this.options.polygon,handler:new L.Draw.Polygon(e,this.options.polygon),title:L.drawLocal.draw.toolbar.buttons.polygon},{enabled:this.options.rectangle,handler:new L.Draw.Rectangle(e,this.options.rectangle),title:L.drawLocal.draw.toolbar.buttons.rectangle},{enabled:this.options.circle,handler:new L.Draw.Circle(e,this.options.circle),title:L.drawLocal.draw.toolbar.buttons.circle},{enabled:this.options.marker,handler:new L.Draw.Marker(e,this.options.marker),title:L.drawLocal.draw.toolbar.buttons.marker},{enabled:this.options.circlemarker,handler:new L.Draw.CircleMarker(e,this.options.circlemarker),title:L.drawLocal.draw.toolbar.buttons.circlemarker}]},getActions:function(e){return[{enabled:e.completeShape,title:L.drawLocal.draw.toolbar.finish.title,text:L.drawLocal.draw.toolbar.finish.text,callback:e.completeShape,context:e},{enabled:e.deleteLastVertex,title:L.drawLocal.draw.toolbar.undo.title,text:L.drawLocal.draw.toolbar.undo.text,callback:e.deleteLastVertex,context:e},{title:L.drawLocal.draw.toolbar.actions.title,text:L.drawLocal.draw.toolbar.actions.text,callback:this.disable,context:this}]},setOptions:function(e){L.setOptions(this,e);for(var t in this._modes)this._modes.hasOwnProperty(t)&&e.hasOwnProperty(t)&&this._modes[t].handler.setOptions(e[t])}}),L.EditToolbar=L.Toolbar.extend({statics:{TYPE:"edit"},options:{edit:{selectedPathOptions:{dashArray:"10, 10",fill:!0,fillColor:"#fe57a1",fillOpacity:.1,maintainColor:!1}},remove:{},poly:null,featureGroup:null},initialize:function(e){e.edit&&(e.edit.selectedPathOptions===void 0&&(e.edit.selectedPathOptions=this.options.edit.selectedPathOptions),e.edit.selectedPathOptions=L.extend({},this.options.edit.selectedPathOptions,e.edit.selectedPathOptions)),e.remove&&(e.remove=L.extend({},this.options.remove,e.remove)),e.poly&&(e.poly=L.extend({},this.options.poly,e.poly)),this._toolbarClass="leaflet-draw-edit",L.Toolbar.prototype.initialize.call(this,e),this._selectedFeatureCount=0},getModeHandlers:function(e){var t=this.options.featureGroup;return[{enabled:this.options.edit,handler:new L.EditToolbar.Edit(e,{featureGroup:t,selectedPathOptions:this.options.edit.selectedPathOptions,poly:this.options.poly}),title:L.drawLocal.edit.toolbar.buttons.edit},{enabled:this.options.remove,handler:new L.EditToolbar.Delete(e,{featureGroup:t}),title:L.drawLocal.edit.toolbar.buttons.remove}]},getActions:function(e){var t=[{title:L.drawLocal.edit.toolbar.actions.save.title,text:L.drawLocal.edit.toolbar.actions.save.text,callback:this._save,context:this},{title:L.drawLocal.edit.toolbar.actions.cancel.title,text:L.drawLocal.edit.toolbar.actions.cancel.text,callback:this.disable,context:this}];return e.removeAllLayers&&t.push({title:L.drawLocal.edit.toolbar.actions.clearAll.title,text:L.drawLocal.edit.toolbar.actions.clearAll.text,callback:this._clearAllLayers,context:this}),t},addToolbar:function(e){var t=L.Toolbar.prototype.addToolbar.call(this,e);return this._checkDisabled(),this.options.featureGroup.on("layeradd layerremove",this._checkDisabled,this),t},removeToolbar:function(){this.options.featureGroup.off("layeradd layerremove",this._checkDisabled,this),L.Toolbar.prototype.removeToolbar.call(this)},disable:function(){this.enabled()&&(this._activeMode.handler.revertLayers(),L.Toolbar.prototype.disable.call(this))},_save:function(){this._activeMode.handler.save(),this._activeMode&&this._activeMode.handler.disable()},_clearAllLayers:function(){this._activeMode.handler.removeAllLayers(),this._activeMode&&this._activeMode.handler.disable()},_checkDisabled:function(){var e,t=this.options.featureGroup,o=t.getLayers().length!==0;this.options.edit&&(e=this._modes[L.EditToolbar.Edit.TYPE].button,o?L.DomUtil.removeClass(e,"leaflet-disabled"):L.DomUtil.addClass(e,"leaflet-disabled"),e.setAttribute("title",o?L.drawLocal.edit.toolbar.buttons.edit:L.drawLocal.edit.toolbar.buttons.editDisabled)),this.options.remove&&(e=this._modes[L.EditToolbar.Delete.TYPE].button,o?L.DomUtil.removeClass(e,"leaflet-disabled"):L.DomUtil.addClass(e,"leaflet-disabled"),e.setAttribute("title",o?L.drawLocal.edit.toolbar.buttons.remove:L.drawLocal.edit.toolbar.buttons.removeDisabled))}}),L.EditToolbar.Edit=L.Handler.extend({statics:{TYPE:"edit"},initialize:function(e,t){if(L.Handler.prototype.initialize.call(this,e),L.setOptions(this,t),this._featureGroup=t.featureGroup,!(this._featureGroup instanceof L.FeatureGroup))throw new Error("options.featureGroup must be a L.FeatureGroup");this._uneditedLayerProps={},this.type=L.EditToolbar.Edit.TYPE;var o=L.version.split(".");parseInt(o[0],10)===1&&parseInt(o[1],10)>=2?L.EditToolbar.Edit.include(L.Evented.prototype):L.EditToolbar.Edit.include(L.Mixin.Events)},enable:function(){!this._enabled&&this._hasAvailableLayers()&&(this.fire("enabled",{handler:this.type}),this._map.fire(L.Draw.Event.EDITSTART,{handler:this.type}),L.Handler.prototype.enable.call(this),this._featureGroup.on("layeradd",this._enableLayerEdit,this).on("layerremove",this._disableLayerEdit,this))},disable:function(){this._enabled&&(this._featureGroup.off("layeradd",this._enableLayerEdit,this).off("layerremove",this._disableLayerEdit,this),L.Handler.prototype.disable.call(this),this._map.fire(L.Draw.Event.EDITSTOP,{handler:this.type}),this.fire("disabled",{handler:this.type}))},addHooks:function(){var e=this._map;e&&(e.getContainer().focus(),this._featureGroup.eachLayer(this._enableLayerEdit,this),this._tooltip=new L.Draw.Tooltip(this._map),this._tooltip.updateContent({text:L.drawLocal.edit.handlers.edit.tooltip.text,subtext:L.drawLocal.edit.handlers.edit.tooltip.subtext}),e._editTooltip=this._tooltip,this._updateTooltip(),this._map.on("mousemove",this._onMouseMove,this).on("touchmove",this._onMouseMove,this).on("MSPointerMove",this._onMouseMove,this).on(L.Draw.Event.EDITVERTEX,this._updateTooltip,this))},removeHooks:function(){this._map&&(this._featureGroup.eachLayer(this._disableLayerEdit,this),this._uneditedLayerProps={},this._tooltip.dispose(),this._tooltip=null,this._map.off("mousemove",this._onMouseMove,this).off("touchmove",this._onMouseMove,this).off("MSPointerMove",this._onMouseMove,this).off(L.Draw.Event.EDITVERTEX,this._updateTooltip,this))},revertLayers:function(){this._featureGroup.eachLayer(function(e){this._revertLayer(e)},this)},save:function(){var e=new L.LayerGroup;this._featureGroup.eachLayer(function(t){t.edited&&(e.addLayer(t),t.edited=!1)}),this._map.fire(L.Draw.Event.EDITED,{layers:e})},_backupLayer:function(e){var t=L.Util.stamp(e);this._uneditedLayerProps[t]||(e instanceof L.Polyline||e instanceof L.Polygon||e instanceof L.Rectangle?this._uneditedLayerProps[t]={latlngs:L.LatLngUtil.cloneLatLngs(e.getLatLngs())}:e instanceof L.Circle?this._uneditedLayerProps[t]={latlng:L.LatLngUtil.cloneLatLng(e.getLatLng()),radius:e.getRadius()}:(e instanceof L.Marker||e instanceof L.CircleMarker)&&(this._uneditedLayerProps[t]={latlng:L.LatLngUtil.cloneLatLng(e.getLatLng())}))},_getTooltipText:function(){return{text:L.drawLocal.edit.handlers.edit.tooltip.text,subtext:L.drawLocal.edit.handlers.edit.tooltip.subtext}},_updateTooltip:function(){this._tooltip.updateContent(this._getTooltipText())},_revertLayer:function(e){var t=L.Util.stamp(e);e.edited=!1,this._uneditedLayerProps.hasOwnProperty(t)&&(e instanceof L.Polyline||e instanceof L.Polygon||e instanceof L.Rectangle?e.setLatLngs(this._uneditedLayerProps[t].latlngs):e instanceof L.Circle?(e.setLatLng(this._uneditedLayerProps[t].latlng),e.setRadius(this._uneditedLayerProps[t].radius)):(e instanceof L.Marker||e instanceof L.CircleMarker)&&e.setLatLng(this._uneditedLayerProps[t].latlng),e.fire("revert-edited",{layer:e}))},_enableLayerEdit:function(e){var t,o,a=e.layer||e.target||e;this._backupLayer(a),this.options.poly&&(o=L.Util.extend({},this.options.poly),a.options.poly=o),this.options.selectedPathOptions&&(t=L.Util.extend({},this.options.selectedPathOptions),t.maintainColor&&(t.color=a.options.color,t.fillColor=a.options.fillColor),a.options.original=L.extend({},a.options),a.options.editing=t),a instanceof L.Marker?(a.editing&&a.editing.enable(),a.dragging.enable(),a.on("dragend",this._onMarkerDragEnd).on("touchmove",this._onTouchMove,this).on("MSPointerMove",this._onTouchMove,this).on("touchend",this._onMarkerDragEnd,this).on("MSPointerUp",this._onMarkerDragEnd,this)):a.editing.enable()},_disableLayerEdit:function(e){var t=e.layer||e.target||e;t.edited=!1,t.editing&&t.editing.disable(),delete t.options.editing,delete t.options.original,this._selectedPathOptions&&(t instanceof L.Marker?this._toggleMarkerHighlight(t):(t.setStyle(t.options.previousOptions),delete t.options.previousOptions)),t instanceof L.Marker?(t.dragging.disable(),t.off("dragend",this._onMarkerDragEnd,this).off("touchmove",this._onTouchMove,this).off("MSPointerMove",this._onTouchMove,this).off("touchend",this._onMarkerDragEnd,this).off("MSPointerUp",this._onMarkerDragEnd,this)):t.editing.disable()},_onMouseMove:function(e){this._tooltip.updatePosition(e.latlng)},_onMarkerDragEnd:function(e){var t=e.target;t.edited=!0,this._map.fire(L.Draw.Event.EDITMOVE,{layer:t})},_onTouchMove:function(e){var t=e.originalEvent.changedTouches[0],o=this._map.mouseEventToLayerPoint(t),a=this._map.layerPointToLatLng(o);e.target.setLatLng(a)},_hasAvailableLayers:function(){return this._featureGroup.getLayers().length!==0}}),L.EditToolbar.Delete=L.Handler.extend({statics:{TYPE:"remove"},initialize:function(e,t){if(L.Handler.prototype.initialize.call(this,e),L.Util.setOptions(this,t),this._deletableLayers=this.options.featureGroup,!(this._deletableLayers instanceof L.FeatureGroup))throw new Error("options.featureGroup must be a L.FeatureGroup");this.type=L.EditToolbar.Delete.TYPE;var o=L.version.split(".");parseInt(o[0],10)===1&&parseInt(o[1],10)>=2?L.EditToolbar.Delete.include(L.Evented.prototype):L.EditToolbar.Delete.include(L.Mixin.Events)},enable:function(){!this._enabled&&this._hasAvailableLayers()&&(this.fire("enabled",{handler:this.type}),this._map.fire(L.Draw.Event.DELETESTART,{handler:this.type}),L.Handler.prototype.enable.call(this),this._deletableLayers.on("layeradd",this._enableLayerDelete,this).on("layerremove",this._disableLayerDelete,this))},disable:function(){this._enabled&&(this._deletableLayers.off("layeradd",this._enableLayerDelete,this).off("layerremove",this._disableLayerDelete,this),L.Handler.prototype.disable.call(this),this._map.fire(L.Draw.Event.DELETESTOP,{handler:this.type}),this.fire("disabled",{handler:this.type}))},addHooks:function(){var e=this._map;e&&(e.getContainer().focus(),this._deletableLayers.eachLayer(this._enableLayerDelete,this),this._deletedLayers=new L.LayerGroup,this._tooltip=new L.Draw.Tooltip(this._map),this._tooltip.updateContent({text:L.drawLocal.edit.handlers.remove.tooltip.text}),this._map.on("mousemove",this._onMouseMove,this))},removeHooks:function(){this._map&&(this._deletableLayers.eachLayer(this._disableLayerDelete,this),this._deletedLayers=null,this._tooltip.dispose(),this._tooltip=null,this._map.off("mousemove",this._onMouseMove,this))},revertLayers:function(){this._deletedLayers.eachLayer(function(e){this._deletableLayers.addLayer(e),e.fire("revert-deleted",{layer:e})},this)},save:function(){this._map.fire(L.Draw.Event.DELETED,{layers:this._deletedLayers})},removeAllLayers:function(){this._deletableLayers.eachLayer(function(e){this._removeLayer({layer:e})},this),this.save()},_enableLayerDelete:function(e){(e.layer||e.target||e).on("click",this._removeLayer,this)},_disableLayerDelete:function(e){var t=e.layer||e.target||e;t.off("click",this._removeLayer,this),this._deletedLayers.removeLayer(t)},_removeLayer:function(e){var t=e.layer||e.target||e;this._deletableLayers.removeLayer(t),this._deletedLayers.addLayer(t),t.fire("deleted")},_onMouseMove:function(e){this._tooltip.updatePosition(e.latlng)},_hasAvailableLayers:function(){return this._deletableLayers.getLayers().length!==0}})})(window,document);var oe=H(ie());var ne=class d{constructor(){this.initialState={center:oe.latLng(12.3714,-1.5197),zoom:13,bounds:null,activeBasemap:"osm",visibleLayers:["parcels","zones"],filters:{},selectedParcelIds:[],hoveredParcelId:null,isFullscreen:!1,sidebarOpen:!0,legendOpen:!0,controlPanelOpen:!0,activeTool:null,drawingMode:!1,loading:!1,loadingProgress:0,visibleParcelsCount:0,totalParcelsCount:0};this._state=T(this.initialState);this.stateSubject=new _e(this.initialState);this.state$=this.stateSubject.asObservable();this.history=[];this.historyIndex=-1;this.maxHistorySize=50;this.state=this._state.asReadonly();this.hasSelection=y(()=>this._state().selectedParcelIds.length>0);this.selectionCount=y(()=>this._state().selectedParcelIds.length);this.hasFilters=y(()=>{let i=this._state().filters;return Object.keys(i).length>0});this.isLoading=y(()=>this._state().loading);this.canUndo=y(()=>this.historyIndex>0);this.canRedo=y(()=>this.historyIndex<this.history.length-1);this.restoreState(),this.stateSubject.subscribe(i=>{this.saveState(i)})}updateState(i,n){let r=this._state(),e=i(r),t=D(D({},r),e);this._state.set(t),this.stateSubject.next(t),n&&this.recordAction({type:n,payload:e,timestamp:new Date})}setCenter(i){this.updateState(n=>({center:i}),"SET_CENTER")}setZoom(i){this.updateState(n=>({zoom:i}),"SET_ZOOM")}setBounds(i){this.updateState(n=>({bounds:i}),"SET_BOUNDS")}setViewport(i,n,r){this.updateState(e=>({center:i,zoom:n,bounds:r}),"SET_VIEWPORT")}setBasemap(i){this.updateState(n=>({activeBasemap:i}),"SET_BASEMAP")}toggleLayer(i){this.updateState(n=>({visibleLayers:n.visibleLayers.includes(i)?n.visibleLayers.filter(e=>e!==i):[...n.visibleLayers,i]}),"TOGGLE_LAYER")}showLayer(i){this.updateState(n=>n.visibleLayers.includes(i)?{}:{visibleLayers:[...n.visibleLayers,i]},"SHOW_LAYER")}hideLayer(i){this.updateState(n=>({visibleLayers:n.visibleLayers.filter(r=>r!==i)}),"HIDE_LAYER")}setFilters(i){this.updateState(n=>({filters:D(D({},n.filters),i)}),"SET_FILTERS")}clearFilters(){this.updateState(i=>({filters:{}}),"CLEAR_FILTERS")}selectParcel(i,n=!1){this.updateState(r=>n?{selectedParcelIds:r.selectedParcelIds.includes(i)?r.selectedParcelIds.filter(t=>t!==i):[...r.selectedParcelIds,i]}:{selectedParcelIds:[i]},"SELECT_PARCEL")}selectMultipleParcels(i){this.updateState(n=>({selectedParcelIds:[...new Set([...n.selectedParcelIds,...i])]}),"SELECT_MULTIPLE")}deselectParcel(i){this.updateState(n=>({selectedParcelIds:n.selectedParcelIds.filter(r=>r!==i)}),"DESELECT_PARCEL")}clearSelection(){this.updateState(i=>({selectedParcelIds:[]}),"CLEAR_SELECTION")}setHoveredParcel(i){this.updateState(n=>({hoveredParcelId:i}))}toggleFullscreen(){this.updateState(i=>({isFullscreen:!i.isFullscreen}),"TOGGLE_FULLSCREEN")}setFullscreen(i){this.updateState(n=>({isFullscreen:i}),"SET_FULLSCREEN")}toggleSidebar(){this.updateState(i=>({sidebarOpen:!i.sidebarOpen}),"TOGGLE_SIDEBAR")}toggleLegend(){this.updateState(i=>({legendOpen:!i.legendOpen}),"TOGGLE_LEGEND")}toggleControlPanel(){this.updateState(i=>({controlPanelOpen:!i.controlPanelOpen}),"TOGGLE_CONTROL_PANEL")}setActiveTool(i){this.updateState(n=>({activeTool:i}),"SET_ACTIVE_TOOL")}setDrawingMode(i){this.updateState(n=>({drawingMode:i}),"SET_DRAWING_MODE")}setLoading(i,n=0){this.updateState(r=>({loading:i,loadingProgress:n}))}updateLoadingProgress(i){this.updateState(n=>({loadingProgress:i}))}updateStats(i,n){this.updateState(r=>({visibleParcelsCount:i,totalParcelsCount:n}))}recordAction(i){this.historyIndex<this.history.length-1&&this.history.splice(this.historyIndex+1),this.history.push(i),this.historyIndex++,this.history.length>this.maxHistorySize&&(this.history.shift(),this.historyIndex--)}undo(){this.canUndo()&&(this.historyIndex--,console.log("Undo:",this.history[this.historyIndex]))}redo(){this.canRedo()&&(this.historyIndex++,console.log("Redo:",this.history[this.historyIndex]))}getHistory(){return[...this.history]}saveState(i){try{let n={center:{lat:i.center.lat,lng:i.center.lng},zoom:i.zoom,activeBasemap:i.activeBasemap,visibleLayers:i.visibleLayers,filters:i.filters,sidebarOpen:i.sidebarOpen,legendOpen:i.legendOpen,controlPanelOpen:i.controlPanelOpen};localStorage.setItem("map_state",JSON.stringify(n))}catch(n){console.warn("Failed to save map state:",n)}}restoreState(){try{let i=localStorage.getItem("map_state");if(i){let n=JSON.parse(i);this.updateState(r=>({center:oe.latLng(n.center.lat,n.center.lng),zoom:n.zoom,activeBasemap:n.activeBasemap,visibleLayers:n.visibleLayers,filters:n.filters,sidebarOpen:n.sidebarOpen,legendOpen:n.legendOpen,controlPanelOpen:n.controlPanelOpen}))}}catch(i){console.warn("Failed to restore map state:",i)}}getStateAsUrlParams(){let i=this._state(),n=new URLSearchParams;return n.set("lat",i.center.lat.toFixed(6)),n.set("lng",i.center.lng.toFixed(6)),n.set("zoom",i.zoom.toString()),n.set("basemap",i.activeBasemap),i.filters.category&&n.set("category",i.filters.category),i.filters.status&&n.set("status",i.filters.status),i.filters.zone&&n.set("zone",i.filters.zone),i.selectedParcelIds.length>0&&n.set("selected",i.selectedParcelIds.join(",")),n}restoreStateFromUrl(i){let n={},r=i.get("lat"),e=i.get("lng"),t=i.get("zoom");r&&e&&(n.center=oe.latLng(parseFloat(r),parseFloat(e))),t&&(n.zoom=parseInt(t,10));let o=i.get("basemap");o&&(n.activeBasemap=o);let a={};i.get("category")&&(a.category=i.get("category")),i.get("status")&&(a.status=i.get("status")),i.get("zone")&&(a.zone=i.get("zone")),Object.keys(a).length>0&&(n.filters=a);let l=i.get("selected");l&&(n.selectedParcelIds=l.split(",")),Object.keys(n).length>0&&this.updateState(()=>n,"RESTORE_FROM_URL")}reset(){this._state.set(this.initialState),this.stateSubject.next(this.initialState),this.history.length=0,this.historyIndex=-1,localStorage.removeItem("map_state")}static{this.\u0275fac=function(n){return new(n||d)}}static{this.\u0275prov=q({token:d,factory:d.\u0275fac,providedIn:"root"})}};var z=H(ie());var ae=class d{constructor(){this.viewportChangeSubject=new Z;this.currentBounds=null;this.currentZoom=13;this.DEBOUNCE_MS=300;this.LOAD_MARGIN=.5;this.viewportChange$=this.viewportChangeSubject.pipe(Y(this.DEBOUNCE_MS),ve((i,n)=>this.boundsEqual(i,n)))}updateViewport(i,n){this.currentBounds=i,this.currentZoom=n;let r=this.expandBounds(i,this.LOAD_MARGIN);this.viewportChangeSubject.next(r)}getCurrentBounds(){return this.currentBounds}getCurrentZoom(){return this.currentZoom}getExpandedBounds(i=this.LOAD_MARGIN){return this.currentBounds?this.expandBounds(this.currentBounds,i):null}getBboxParams(i){let n=i||this.currentBounds;return n?`${n.getSouthWest().lng},${n.getSouthWest().lat},${n.getNorthEast().lng},${n.getNorthEast().lat}`:""}isInViewport(i){return this.currentBounds?this.currentBounds.contains(i):!1}intersectsViewport(i){return this.currentBounds?this.currentBounds.intersects(i):!1}getDetailLevel(){return this.currentZoom<12?"low":this.currentZoom<15?"medium":"high"}shouldUseClustering(){return this.currentZoom<14}getSimplificationTolerance(){return this.currentZoom<10?.01:this.currentZoom<12?.005:this.currentZoom<14?.001:1e-4}expandBounds(i,n){let r=i.getSouthWest(),e=i.getNorthEast(),t=(e.lat-r.lat)*n,o=(e.lng-r.lng)*n;return z.latLngBounds(z.latLng(r.lat-t,r.lng-o),z.latLng(e.lat+t,e.lng+o))}boundsEqual(i,n){let e=i.getSouthWest(),t=i.getNorthEast(),o=n.getSouthWest(),a=n.getNorthEast();return Math.abs(e.lat-o.lat)<1e-4&&Math.abs(e.lng-o.lng)<1e-4&&Math.abs(t.lat-a.lat)<1e-4&&Math.abs(t.lng-a.lng)<1e-4}getOptimalPageSize(){switch(this.getDetailLevel()){case"low":return 100;case"medium":return 500;case"high":return 1e3}}getTiles(i,n=4){let r=i.getSouthWest(),e=i.getNorthEast(),t=(e.lat-r.lat)/Math.sqrt(n),o=(e.lng-r.lng)/Math.sqrt(n),a=[],l=Math.sqrt(n);for(let s=0;s<l;s++)for(let c=0;c<l;c++){let h=z.latLng(r.lat+s*t,r.lng+c*o),g=z.latLng(r.lat+(s+1)*t,r.lng+(c+1)*o);a.push(z.latLngBounds(h,g))}return a}reset(){this.currentBounds=null,this.currentZoom=13}static{this.\u0275fac=function(n){return new(n||d)}}static{this.\u0275prov=q({token:d,factory:d.\u0275fac,providedIn:"root"})}};var et=(d,i)=>i.name,tt=(d,i)=>i.id;function it(d,i){if(d&1&&(p(0,"mat-icon"),f(1),u()),d&2){let n=v().$implicit;m(),I(n.icon)}}function ot(d,i){if(d&1&&(p(0,"span",14),f(1),u()),d&2){let n=v().$implicit;m(),F("(",n.count,")")}}function nt(d,i){if(d&1){let n=G();p(0,"div",10),M("click",function(){let e=x(n).$implicit,t=v(3);return C(t.toggleItem(e))}),p(1,"mat-checkbox",11),M("change",function(e){let t=x(n).$implicit,o=v(3);return C(o.onItemToggle(t,e.checked))}),u(),p(2,"div",12),E(3,it,2,1,"mat-icon"),u(),p(4,"span",13),f(5),u(),E(6,ot,2,1,"span",14),u()}if(d&2){let n=i.$implicit;m(),R("checked",n.visible),m(),Ce("background-color",n.color),m(),S(n.icon?3:-1),m(2),I(n.label),m(),S(n.count!==void 0?6:-1)}}function at(d,i){d&1&&U(0,"mat-divider")}function rt(d,i){if(d&1){let n=G();p(0,"div",2)(1,"div",6)(2,"h4"),f(3),u(),p(4,"button",7),M("click",function(){let e=x(n).$implicit,t=v(2);return C(t.toggleCategory(e))}),p(5,"mat-icon"),f(6),u()()(),p(7,"div",8),he(8,nt,7,6,"div",9,tt),u(),E(10,at,1,0,"mat-divider"),u()}if(d&2){let n=i.$implicit,r=i.$index,e=i.$count,t=v(2);m(3),I(n.name),m(3),I(t.allVisible(n)?"visibility":"visibility_off"),m(2),pe(n.items),m(2),S(r!==e-1?10:-1)}}function st(d,i){if(d&1){let n=G();p(0,"mat-card-content"),he(1,rt,11,3,"div",2,et),p(3,"div",3)(4,"button",4),M("click",function(){x(n);let e=v();return C(e.showAll())}),p(5,"mat-icon"),f(6,"visibility"),u(),f(7," Tout afficher "),u(),p(8,"button",5),M("click",function(){x(n);let e=v();return C(e.hideAll())}),p(9,"mat-icon"),f(10,"visibility_off"),u(),f(11," Tout masquer "),u()()()}if(d&2){let n=v();m(),pe(n.categories)}}var re=class d{constructor(){this.categories=[{name:"Statut des parcelles",items:[{id:"available",label:"Disponible",color:"#4caf50",icon:"check_circle",visible:!0,count:0},{id:"occupied",label:"Occup\xE9",color:"#2196f3",icon:"home",visible:!0,count:0},{id:"disputed",label:"Contest\xE9",color:"#f44336",icon:"warning",visible:!0,count:0},{id:"reserved",label:"R\xE9serv\xE9",color:"#ff9800",icon:"lock",visible:!0,count:0}]},{name:"Cat\xE9gories",items:[{id:"residential",label:"R\xE9sidentiel",color:"#3887be",visible:!0,count:0},{id:"commercial",label:"Commercial",color:"#bc3de3",visible:!0,count:0},{id:"industrial",label:"Industriel",color:"#ff8100",visible:!0,count:0},{id:"agricultural",label:"Agricole",color:"#8fa900",visible:!0,count:0}]}];this.itemVisibilityChanged=new de;this.categoryVisibilityChanged=new de;this.minimized=T(!1)}toggleMinimize(){this.minimized.update(i=>!i)}toggleItem(i){i.visible=!i.visible,this.itemVisibilityChanged.emit({itemId:i.id,visible:i.visible})}onItemToggle(i,n){i.visible=n,this.itemVisibilityChanged.emit({itemId:i.id,visible:i.visible})}toggleCategory(i){let n=this.allVisible(i);i.items.forEach(r=>{r.visible=!n}),this.categoryVisibilityChanged.emit({categoryName:i.name,visible:!n})}allVisible(i){return i.items.every(n=>n.visible)}showAll(){this.categories.forEach(i=>{i.items.forEach(n=>{n.visible=!0})}),this.itemVisibilityChanged.emit({itemId:"all",visible:!0})}hideAll(){this.categories.forEach(i=>{i.items.forEach(n=>{n.visible=!1})}),this.itemVisibilityChanged.emit({itemId:"all",visible:!1})}updateCounts(i){this.categories.forEach(n=>{n.items.forEach(r=>{i[r.id]!==void 0&&(r.count=i[r.id])})})}static{this.\u0275fac=function(n){return new(n||d)}}static{this.\u0275cmp=W({type:d,selectors:[["app-map-legend"]],inputs:{categories:"categories"},outputs:{itemVisibilityChanged:"itemVisibilityChanged",categoryVisibilityChanged:"categoryVisibilityChanged"},decls:10,vars:4,consts:[[1,"legend-card"],["mat-icon-button","","matTooltip","R\xE9duire/Agrandir",3,"click"],[1,"legend-category"],[1,"legend-actions"],["mat-button","","matTooltip","Afficher tout",3,"click"],["mat-button","","matTooltip","Tout masquer",3,"click"],[1,"category-header"],["mat-icon-button","","matTooltip","Tout afficher/masquer",3,"click"],[1,"legend-items"],[1,"legend-item"],[1,"legend-item",3,"click"],[3,"change","checked"],[1,"item-marker"],[1,"item-label"],[1,"item-count"]],template:function(n,r){n&1&&(p(0,"mat-card",0)(1,"mat-card-header")(2,"mat-card-title")(3,"mat-icon"),f(4,"layers"),u(),f(5," L\xE9gende "),u(),p(6,"button",1),M("click",function(){return r.toggleMinimize()}),p(7,"mat-icon"),f(8),u()()(),E(9,st,12,0,"mat-card-content"),u()),n&2&&(N("minimized",r.minimized()),m(8),I(r.minimized()?"expand_more":"expand_less"),m(),S(r.minimized()?-1:9))},dependencies:[J,Te,ke,Se,De,Ee,He,Ve,Q,K,X,Ie,Oe,te,ee,Fe,Ne],styles:[".legend-card[_ngcontent-%COMP%]{position:absolute;bottom:24px;right:24px;max-width:300px;z-index:1000;box-shadow:0 4px 12px #0003;transition:all .3s ease}.legend-card.minimized[_ngcontent-%COMP%]   mat-card-header[_ngcontent-%COMP%]{border-bottom:none;padding-bottom:16px}@media(max-width:768px){.legend-card[_ngcontent-%COMP%]{bottom:80px;right:12px;max-width:calc(100% - 24px)}}mat-card-header[_ngcontent-%COMP%]{display:flex;justify-content:space-between;align-items:center;padding:16px;border-bottom:1px solid rgba(0,0,0,.1)}mat-card-header[_ngcontent-%COMP%]   mat-card-title[_ngcontent-%COMP%]{display:flex;align-items:center;gap:8px;margin:0;font-size:16px;font-weight:600}mat-card-header[_ngcontent-%COMP%]   mat-card-title[_ngcontent-%COMP%]   mat-icon[_ngcontent-%COMP%]{font-size:20px;width:20px;height:20px}mat-card-content[_ngcontent-%COMP%]{padding:16px;max-height:400px;overflow-y:auto}.legend-category[_ngcontent-%COMP%]{margin-bottom:16px}.legend-category[_ngcontent-%COMP%]:last-child{margin-bottom:0}.legend-category[_ngcontent-%COMP%]   .category-header[_ngcontent-%COMP%]{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}.legend-category[_ngcontent-%COMP%]   .category-header[_ngcontent-%COMP%]   h4[_ngcontent-%COMP%]{margin:0;font-size:14px;font-weight:600;color:#000000b3}.legend-category[_ngcontent-%COMP%]   .category-header[_ngcontent-%COMP%]   button[_ngcontent-%COMP%]{width:32px;height:32px}.legend-category[_ngcontent-%COMP%]   .category-header[_ngcontent-%COMP%]   button[_ngcontent-%COMP%]   mat-icon[_ngcontent-%COMP%]{font-size:18px;width:18px;height:18px}.legend-items[_ngcontent-%COMP%]{display:flex;flex-direction:column;gap:8px}.legend-item[_ngcontent-%COMP%]{display:flex;align-items:center;gap:8px;padding:8px;border-radius:4px;cursor:pointer;transition:background-color .2s}.legend-item[_ngcontent-%COMP%]:hover{background-color:#0000000a}.legend-item[_ngcontent-%COMP%]   mat-checkbox[_ngcontent-%COMP%]     .mdc-checkbox{padding:0}.legend-item[_ngcontent-%COMP%]   .item-marker[_ngcontent-%COMP%]{width:24px;height:24px;border-radius:4px;display:flex;align-items:center;justify-content:center;border:1px solid rgba(0,0,0,.1)}.legend-item[_ngcontent-%COMP%]   .item-marker[_ngcontent-%COMP%]   mat-icon[_ngcontent-%COMP%]{font-size:16px;width:16px;height:16px;color:#fff}.legend-item[_ngcontent-%COMP%]   .item-label[_ngcontent-%COMP%]{flex:1;font-size:14px;color:#000000de}.legend-item[_ngcontent-%COMP%]   .item-count[_ngcontent-%COMP%]{font-size:12px;color:#00000080}mat-divider[_ngcontent-%COMP%]{margin:12px 0}.legend-actions[_ngcontent-%COMP%]{display:flex;gap:8px;margin-top:16px;padding-top:16px;border-top:1px solid rgba(0,0,0,.1)}.legend-actions[_ngcontent-%COMP%]   button[_ngcontent-%COMP%]{flex:1;font-size:12px}.legend-actions[_ngcontent-%COMP%]   button[_ngcontent-%COMP%]   mat-icon[_ngcontent-%COMP%]{font-size:16px;width:16px;height:16px;margin-right:4px}"],changeDetection:0})}};var ge=H(ie());function Ye(d,i=.001){return d&&(d.type==="Polygon"?j(D({},d),{coordinates:d.coordinates.map(n=>me(n,i))}):d.type==="MultiPolygon"?j(D({},d),{coordinates:d.coordinates.map(n=>n.map(r=>me(r,i)))}):d.type==="LineString"?j(D({},d),{coordinates:me(d.coordinates,i)}):d)}function me(d,i){if(d.length<=3)return d;let n=[d[0]],r=d[0];for(let e=1;e<d.length-1;e++){let t=d[e];lt(r,t)>i&&(n.push(t),r=t)}return n.push(d[d.length-1]),n}function lt(d,i){let n=i[0]-d[0],r=i[1]-d[1];return Math.sqrt(n*n+r*r)}function B(d){return d<1e4?`${Math.round(d)} m\xB2`:`${(d/1e4).toFixed(2)} ha`}var se={available:"#4caf50",occupied:"#2196f3",disputed:"#f44336",reserved:"#ff9800",Habitation:"#3887be",residential:"#3887be",Commerce:"#bc3de3",commercial:"#bc3de3",Industriel:"#ff8100",industrial:"#ff8100",Agricole:"#8fa900",agricultural:"#8fa900","mixed-use":"#99008a","public-space":"#007d79",CTOM:"#e91e63",Gendarmerie:"#ff5722",Police:"#795548",CSPS:"#4caf50",CMA:"#ff9800",CEEP:"#9c27b0","Ecole primaire":"#00bcd4","Ecole secondaire":"#009688","\xC9cole primaire":"#00bcd4","\xC9cole secondaire":"#009688",Sante:"#e91e63",Sant\u00E9:"#e91e63",Hopital:"#d32f2f",H\u00F4pital:"#d32f2f",Forage:"#03a9f4",Route:"#757575",Voirie:"#616161",Mosquee:"#673ab7",Mosqu\u00E9e:"#673ab7","Eglise catholique":"#9c27b0","\xC9glise catholique":"#9c27b0",Eglise:"#9c27b0",\u00C9glise:"#9c27b0",Culte:"#7b1fa2",Cimetiere:"#607d8b",Cimeti\u00E8re:"#607d8b",Marche:"#ff6f00",March\u00E9:"#ff6f00",EV:"#8bc34a",RF:"#cddc39","Espace vert":"#8bc34a","Reserve fonciere":"#cddc39","R\xE9serve fonci\xE8re":"#cddc39"};function ct(d){let i=0;for(let t=0;t<d.length;t++){let o=d.charCodeAt(t);i=(i<<5)-i+o,i=i&i}let n=Math.abs(i%360),r=60+Math.abs(i%20),e=45+Math.abs(i%15);return`hsl(${n}, ${r}%, ${e}%)`}function w(d){if(!d)return"#9e9e9e";let i=d.trim(),n=Object.entries(se).find(([r])=>r.toLowerCase()===i.toLowerCase())?.[1];return n||ct(i)}var dt=["mapContainer"];function ht(d,i){if(d&1&&U(0,"mat-progress-bar",2),d&2){let n=v();R("value",n.loadingProgress())}}function pt(d,i){if(d&1&&(p(0,"span",17)(1,"mat-icon"),f(2,"check_circle"),u(),f(3),u()),d&2){let n=v(2);m(3),F(" ",n.selectedCount()," s\xE9lectionn\xE9e(s) ")}}function ut(d,i){if(d&1){let n=G();p(0,"div",4)(1,"div",7)(2,"button",8),M("click",function(){x(n);let e=v();return C(e.toggleFullscreen())}),p(3,"mat-icon"),f(4),u()(),p(5,"button",9),M("click",function(){x(n);let e=v();return C(e.refresh())}),p(6,"mat-icon"),f(7,"refresh"),u()()(),p(8,"div",10)(9,"div",11)(10,"button",12),M("click",function(){x(n);let e=v();return C(e.changeBasemap("osm"))}),p(11,"mat-icon"),f(12,"map"),u()(),p(13,"button",13),M("click",function(){x(n);let e=v();return C(e.changeBasemap("satellite"))}),p(14,"mat-icon"),f(15,"satellite"),u()()()(),p(16,"div",14)(17,"div",15)(18,"span",16)(19,"mat-icon"),f(20,"visibility"),u(),f(21),u(),E(22,pt,4,1,"span",17),p(23,"span",16)(24,"mat-icon"),f(25,"inventory"),u(),f(26),u()()()()}if(d&2){let n=v();m(2),R("matTooltip",n.isFullscreen()?"Quitter le plein \xE9cran":"Plein \xE9cran"),m(2),I(n.isFullscreen()?"fullscreen_exit":"fullscreen"),m(),R("disabled",n.loading()),m(5),N("active",n.mapState().activeBasemap==="osm"),m(3),N("active",n.mapState().activeBasemap==="satellite"),m(8),F(" ",n.visibleCount()," parcelles visibles "),m(),S(n.selectedCount()>0?22:-1),m(4),F(" ",n.totalCount()," total ")}}function mt(d,i){d&1&&(p(0,"div",5),U(1,"mat-spinner",18),p(2,"p"),f(3,"Chargement de la carte..."),u()())}function gt(d,i){if(d&1){let n=G();p(0,"app-map-legend",19),M("itemVisibilityChanged",function(e){x(n);let t=v();return C(t.onLegendItemVisibilityChanged(e))}),u()}if(d&2){let n=v();R("categories",n.legendCategories())}}var qe=class d{constructor(){this.mapService=O(Ze);this.parcelService=O(je);this.mapStateService=O(ne);this.viewportService=O(ae);this.route=O(we);this.router=O(Pe);this.snackBar=O(Ge);this.destroy$=new Z;this.map=null;this.baseLayers={};this.parcelLayer=null;this.clusterGroup=null;this.drawnItems=null;this.loadedParcelsCache=new Map;this.currentlyVisibleIds=new Set;this.mapState=this.mapStateService.state;this.loading=y(()=>this.mapState().loading);this.loadingProgress=y(()=>this.mapState().loadingProgress);this.isFullscreen=y(()=>this.mapState().isFullscreen);this.selectedCount=y(()=>this.mapState().selectedParcelIds.length);this.visibleCount=y(()=>this.mapState().visibleParcelsCount);this.totalCount=y(()=>this.mapState().totalParcelsCount);this.showControls=T(!0);this.mapReady=T(!1);this.showLegend=T(!0);this.legendCategories=T([{name:"Statut des parcelles",items:[{id:"available",label:"Disponible",color:"#4caf50",icon:"check_circle",visible:!0,count:0},{id:"occupied",label:"Occup\xE9",color:"#2196f3",icon:"home",visible:!0,count:0},{id:"disputed",label:"Contest\xE9",color:"#f44336",icon:"warning",visible:!0,count:0},{id:"reserved",label:"R\xE9serv\xE9",color:"#ff9800",icon:"lock",visible:!0,count:0}]},{name:"Cat\xE9gories",items:[{id:"residential",label:"R\xE9sidentiel",color:"#3887be",visible:!0,count:0},{id:"commercial",label:"Commercial",color:"#bc3de3",visible:!0,count:0},{id:"industrial",label:"Industriel",color:"#ff8100",visible:!0,count:0},{id:"agricultural",label:"Agricole",color:"#8fa900",visible:!0,count:0},{id:"Habitation",label:"Habitation",color:"#3887be",visible:!0,count:0},{id:"CTOM",label:"CTOM",color:"#bc3de3",visible:!0,count:0},{id:"Gendarmerie",label:"Gendarmerie",color:"#ff8100",visible:!0,count:0},{id:"CSPS",label:"CSPS",color:"#8fa900",visible:!0,count:0},{id:"Ecole primaire",label:"\xC9cole primaire",color:"#00bcd4",visible:!0,count:0},{id:"Sante",label:"Sant\xE9",color:"#e91e63",visible:!0,count:0}]}]);this.categoryColors=new Map;this.DEFAULT_CENTER=[12.3714,-1.5197];this.DEFAULT_ZOOM=13;this.MAX_ZOOM=20;this.MIN_ZOOM=8}ngOnInit(){this.initCategoryColors();let i=new URLSearchParams(window.location.search);this.mapStateService.restoreStateFromUrl(i),window.addEventListener("parcel-view",(n=>{let r=n.detail;r&&this.viewParcelDetails(r)})),window.addEventListener("parcel-report",(n=>{let r=n.detail;if(r){let e,t;if(typeof r=="string")try{let o=JSON.parse(r);e=o.id,t=o.reportType||"parcel-simple"}catch(o){e=r,t="parcel-simple"}else e=r.id||r,t=r.reportType||"parcel-simple";e&&this.router.navigate(["/reports/generator"],{queryParams:{parcelId:e,reportType:t}})}})),this.viewportService.viewportChange$.pipe(Y(500),ce(n=>this.loadParcelsInViewport(n)),be(this.destroy$)).subscribe({next:()=>{},error:n=>{console.error("Error loading parcels:",n),this.snackBar.open("Erreur lors du chargement des parcelles","Fermer",{duration:3e3})}})}ngAfterViewInit(){setTimeout(()=>{this.initMap()},0)}ngOnDestroy(){this.destroy$.next(),this.destroy$.complete(),this.map&&(this.map.remove(),this.map=null),this.loadedParcelsCache.clear(),this.currentlyVisibleIds.clear()}initMap(){try{let i=this.mapState();this.map=b.map(this.mapContainer.nativeElement,{center:i.center,zoom:i.zoom,maxZoom:this.MAX_ZOOM,minZoom:this.MIN_ZOOM,zoomControl:!1,attributionControl:!0}),this.initBaseLayers(),this.initDataLayers(),this.setupMapEvents(),this.mapReady.set(!0),this.loadInitialData()}catch(i){console.error("Error initializing map:",i),this.snackBar.open("Erreur lors de l'initialisation de la carte","Fermer",{duration:5e3})}}initBaseLayers(){if(!this.map)return;this.baseLayers.osm=b.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{attribution:"\xA9 OpenStreetMap contributors",maxZoom:19}),this.baseLayers.satellite=b.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",{attribution:"\xA9 ESRI",maxZoom:19});let i=this.mapState().activeBasemap;this.baseLayers[i].addTo(this.map)}initDataLayers(){this.map&&(typeof b.markerClusterGroup>"u"?(console.error("Le plugin leaflet.markercluster n'est pas charg\xE9 correctement"),this.parcelLayer=b.layerGroup().addTo(this.map),this.clusterGroup=null):(this.parcelLayer=b.layerGroup().addTo(this.map),this.clusterGroup=b.markerClusterGroup({maxClusterRadius:50,spiderfyOnMaxZoom:!0,showCoverageOnHover:!1,zoomToBoundsOnClick:!0})),this.drawnItems=new b.FeatureGroup,this.map.addLayer(this.drawnItems))}setupMapEvents(){this.map&&(this.map.on("moveend",()=>{this.onMapMoveEnd()}),this.map.on("zoomend",()=>{this.onMapZoomEnd()}),this.map.on("click",i=>{this.onMapClick(i)}),document.addEventListener("fullscreenchange",()=>{this.onFullscreenChange()}))}onMapMoveEnd(){if(!this.map)return;let i=this.map.getBounds(),n=this.map.getZoom(),r=this.map.getCenter();this.mapStateService.setViewport(r,n,i),this.viewportService.updateViewport(i,n),this.syncUrlWithState()}onMapZoomEnd(){if(!this.map)return;let i=this.map.getZoom();this.viewportService.shouldUseClustering()?this.enableClustering():this.disableClustering(),this.updateGeometrySimplification()}onMapClick(i){this.mapState().activeTool===null&&this.mapStateService.clearSelection()}onFullscreenChange(){let i=!!document.fullscreenElement;this.mapStateService.setFullscreen(i),setTimeout(()=>{this.map?.invalidateSize()},100)}loadInitialData(){if(!this.map)return;let i=this.map.getBounds();this.viewportService.updateViewport(i,this.map.getZoom())}loadParcelsInViewport(i){this.mapStateService.setLoading(!0,0);let n=this.viewportService.getBboxParams(i),r=this.mapState().filters,e=this.viewportService.getDetailLevel();return this.parcelService.getParcelsGeoJSON(n).pipe(Le(t=>(console.error("Error loading parcels:",t),this.mapStateService.setLoading(!1),le({type:"FeatureCollection",features:[]}))),ce(t=>(this.addParcelsToMap(t),this.mapStateService.setLoading(!1),le(t))))}addParcelsToMap(i){if(!this.map||!this.parcelLayer)return;let n=this.viewportService.getSimplificationTolerance(),r=new Set;i.features.forEach(e=>{let t=e.properties.id||e.id;if(r.add(t),this.loadedParcelsCache.has(t)){let a=this.loadedParcelsCache.get(t);this.parcelLayer.hasLayer(a)||this.parcelLayer.addLayer(a);return}n>1e-4&&(e.geometry=Ye(e.geometry,n));let o=b.geoJSON(e,{style:a=>this.getParcelStyle(a),onEachFeature:(a,l)=>{this.bindParcelInteractions(a,l)}}).getLayers()[0];this.loadedParcelsCache.set(t,o),this.parcelLayer.addLayer(o)}),this.currentlyVisibleIds.forEach(e=>{if(!r.has(e)){let t=this.loadedParcelsCache.get(e);t&&this.parcelLayer.hasLayer(t)&&this.parcelLayer.removeLayer(t)}}),this.currentlyVisibleIds=r,this.mapStateService.updateStats(r.size,i.totalCount||r.size),this.updateLegendCounts(i)}getParcelStyle(i){let n=i.properties,r=n.status,e=n.category,t=this.mapState().selectedParcelIds.includes(n.id),o=this.mapState().hoveredParcelId===n.id,a;return e?a=w(e):r&&se[r]?a=se[r]:a="#9e9e9e",{fillColor:a,fillOpacity:t?.7:o?.5:.3,color:t?"#000":a,weight:t?3:o?2:1}}bindParcelInteractions(i,n){let r=i.properties,e=this.createParcelPopup(r);n.bindPopup(e),n.on("click",t=>{b.DomEvent.stopPropagation(t),this.onParcelClick(r.id,t.originalEvent.shiftKey)}),n.on("mouseover",()=>{this.mapStateService.setHoveredParcel(r.id),this.updateLayerStyle(n)}),n.on("mouseout",()=>{this.mapStateService.setHoveredParcel(null),this.updateLayerStyle(n)})}createParcelPopup(i){let n=i.category||"N/A",r=i.category?w(i.category):"#9e9e9e";return`
      <div class="parcel-popup" style="min-width: 250px;">
        <h3 style="margin: 0 0 12px 0; color: #333; font-size: 16px; font-weight: 600;">
          \u{1F4CD} ${i.reference||"N/A"}
        </h3>
        <div style="margin-bottom: 8px;">
          <strong style="color: #666;">Adresse:</strong> 
          <span style="color: #333;">${i.address||"Non renseign\xE9e"}</span>
        </div>
        <div style="margin-bottom: 8px;">
          <strong style="color: #666;">Superficie:</strong> 
          <span style="color: #333;">${i.area?B(i.area):"N/A"}</span>
        </div>
        <div style="margin-bottom: 8px;">
          <strong style="color: #666;">Cat\xE9gorie:</strong> 
          <span style="display: inline-block; background: ${r}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px;">
            ${n}
          </span>
        </div>
        <div style="margin-bottom: 12px;">
          <strong style="color: #666;">Statut:</strong> 
          <span style="color: #333;">${this.getStatusLabel(i.status)}</span>
        </div>
        <div style="display: flex; gap: 8px; flex-direction: column;">
          <button 
            onclick="window.dispatchEvent(new CustomEvent('parcel-view', { detail: '${i.id}' }))"
            style="width: 100%; padding: 8px 16px; background: #2196f3; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: 500; transition: background 0.2s;"
            onmouseover="this.style.background='#1976d2'"
            onmouseout="this.style.background='#2196f3'">
            \u{1F441}\uFE0F Voir les d\xE9tails
          </button>
          <button
            onclick="window.dispatchEvent(new CustomEvent('parcel-report', { detail: JSON.stringify({ id: '${i.id}', reportType: 'parcel-with-layers' }) }))"
            style="width: 100%; padding: 8px 16px; background: #4caf50; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: 500; transition: background 0.2s;"
            onmouseover="this.style.background='#388e3c'"
            onmouseout="this.style.background='#4caf50'">
            \u{1F4CB} Rapport avec couches
          </button>
          <button
            onclick="window.dispatchEvent(new CustomEvent('parcel-report', { detail: JSON.stringify({ id: '${i.id}', reportType: 'parcel-simple' }) }))"
            style="width: 100%; padding: 8px 16px; background: #ff9800; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: 500; transition: background 0.2s;"
            onmouseover="this.style.background='#f57c00'"
            onmouseout="this.style.background='#ff9800'">
            \u{1F4CB} Rapport simple
          </button>
        </div>
      </div>
    `}viewParcelDetails(i){this.router.navigate(["/parcels",i])}printParcelReport(i,n=!0){let r=n?"G\xE9n\xE9ration du rapport avec carte et couches...":"G\xE9n\xE9ration du rapport...";this.snackBar.open(r,"",{duration:2e3}),this.parcelService.getParcelById(i).subscribe({next:e=>{if(n)this.router.navigate(["/reports/generator"],{queryParams:{parcelId:i,reportType:"parcel-with-layers"}});else{let t=this.generateParcelReportWithMap(e),o=window.open("","_blank","width=900,height=700");o&&(o.document.write(t),o.document.close(),setTimeout(()=>{o.print()},1e3))}this.snackBar.open("Rapport g\xE9n\xE9r\xE9 avec succ\xE8s !","OK",{duration:2e3})},error:e=>{console.error("Error fetching parcel details:",e),this.snackBar.open("Erreur lors de la r\xE9cup\xE9ration des d\xE9tails","Fermer",{duration:3e3})}})}getVisibleParcelsData(){let i=[];console.log("\u{1F50D} R\xE9cup\xE9ration des parcelles visibles..."),this.parcelLayer?this.parcelLayer.eachLayer(r=>{if(r.feature&&r.feature.properties){let e=r.feature.properties,t=r.feature.geometry,o=null;if(t&&t.type&&t.coordinates)switch(t.type){case"Point":o=t.coordinates;break;case"Polygon":if(t.coordinates&&t.coordinates[0]){let s=t.coordinates[0];if(s.length>0){let c=0,h=0,g=0;for(let _=0;_<s.length-1;_++){let[P,k]=s[_],[$,V]=s[_+1],A=P*V-$*k;c+=(P+$)*A,h+=(k+V)*A,g+=A}if(g!==0){let _=g/2;o=[c/(6*_),h/(6*_)]}else{let _=0,P=0;for(let k of s)_+=k[0],P+=k[1];o=[_/s.length,P/s.length]}}}break;case"MultiPolygon":if(t.coordinates&&t.coordinates[0]&&t.coordinates[0][0]){let s=t.coordinates[0][0];if(s.length>0){let c=0,h=0,g=0;for(let _=0;_<s.length-1;_++){let[P,k]=s[_],[$,V]=s[_+1],A=P*V-$*k;c+=(P+$)*A,h+=(k+V)*A,g+=A}if(g!==0){let _=g/2;o=[c/(6*_),h/(6*_)]}else{let _=0,P=0;for(let k of s)_+=k[0],P+=k[1];o=[_/s.length,P/s.length]}}}break;case"LineString":if(t.coordinates&&t.coordinates.length>0){let s=Math.floor(t.coordinates.length/2);o=t.coordinates[s]}break;default:if(t.coordinates&&Array.isArray(t.coordinates)&&t.coordinates.length>0)if(t.coordinates[0]&&Array.isArray(t.coordinates[0])){let s=Math.floor(t.coordinates.length/2);o=t.coordinates[s]}else o=t.coordinates;break}(!o||!Array.isArray(o)||o.length<2)&&(e.coordinates_lat&&e.coordinates_lng?o=[e.coordinates_lng,e.coordinates_lat]:e.latitude&&e.longitude?o=[e.longitude,e.latitude]:e.coordinates&&e.coordinates.lat&&e.coordinates.lng&&(o=[e.coordinates.lng,e.coordinates.lat]));let a=t;t&&t.type==="MultiPolygon"?t.coordinates&&t.coordinates.length>0&&(a={type:"Polygon",coordinates:t.coordinates[0]}):t&&t.type==="Polygon"&&t.coordinates&&t.coordinates[0]&&t.coordinates[0].length>50&&(a={type:"Polygon",coordinates:[t.coordinates[0].filter((c,h)=>h%5===0)]});let l={id:e.id,reference:e.reference||e.reference_cadastrale,category:e.category,coordinates:o,geometry:a};i.push(l),console.log(`  \u2713 Parcelle: ${l.reference}, Type: ${a?.type||"Unknown"}, Coords: ${o?"Oui":"Non"}`)}}):console.warn("\u26A0\uFE0F parcelLayer est null ou undefined"),console.log(`\u2705 Total parcelles r\xE9cup\xE9r\xE9es: ${i.length}`);let n=i.slice(0,20);return console.log(`\u{1F4CA} Nombre de parcelles limit\xE9es pour le rapport: ${n.length}`),n}captureMapAsImage(){return new Promise(i=>{i("")})}generateStaticMap(i){return fe(this,null,function*(){return new Promise(n=>{try{let r=0,e=0;if(i.coordinates&&(r=i.coordinates.lat||i.coordinates.latitude||0,e=i.coordinates.lng||i.coordinates.longitude||0),r===0&&e===0&&(r=i.coordinates_lat||0,e=i.coordinates_lng||0),r===0&&e===0&&(r=i.latitude||0,e=i.longitude||0),console.log("Parcel coordinates for map:",{lat:r,lng:e}),r===0&&e===0){n("");return}let t=16,o=w(i.category),a=`
          <!DOCTYPE html>
          <html>
          <head>
            <meta charset="utf-8">
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"><\/script>
            <style>
              body { margin: 0; padding: 0; }
              #map { width: 100%; height: 100%; }
            </style>
          </head>
          <body>
            <div id="map"></div>
            <script>
              var map = L.map('map', {
                center: [${r}, ${e}],
                zoom: ${t},
                zoomControl: false,
                attributionControl: false
              });

              L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19
              }).addTo(map);

              L.circleMarker([${r}, ${e}], {
                radius: 12,
                fillColor: '${o}',
                fillOpacity: 0.8,
                color: '#000',
                weight: 3
              }).addTo(map).bindPopup('\u{1F4CD} Parcelle');
            <\/script>
          </body>
          </html>
        `,l="data:text/html;charset=utf-8,"+encodeURIComponent(a);console.log("Map iframe generated successfully"),n(l)}catch(r){console.error("Error generating static map:",r),n("")}})})}generateParcelReportWithMap(i){let n=0,r=0;i.coordinates&&(n=i.coordinates.lat||i.coordinates.latitude||0,r=i.coordinates.lng||i.coordinates.longitude||0),n===0&&r===0&&(n=i.coordinates_lat||0,r=i.coordinates_lng||0),n===0&&r===0&&(n=i.latitude||0,r=i.longitude||0);let e=n!==0&&r!==0,t=i.category?w(i.category):"#9e9e9e";return this.generateParcelReport(i,null,n,r,e,t)}generateParcelReportWithMapAndLayers(i,n){let r=0,e=0;i.coordinates&&(r=i.coordinates.lat||i.coordinates.latitude||0,e=i.coordinates.lng||i.coordinates.longitude||0),r===0&&e===0&&(r=i.coordinates_lat||0,e=i.coordinates_lng||0),r===0&&e===0&&(r=i.latitude||0,e=i.longitude||0);let t=r!==0&&e!==0,o=i.category?w(i.category):"#9e9e9e",a=n.filter(l=>l.geometry&&l.geometry.type&&l.geometry.coordinates);return this.generateParcelReportWithStaticMapAndLayers(i,r,e,t,o,a)}generateParcelReportWithMapImageAndLayers(i,n,r){return""}generateParcelReportWithStaticMapAndLayers(i,n=0,r=0,e=!1,t="#9e9e9e",o=[]){let a=new Date().toLocaleDateString("fr-FR",{year:"numeric",month:"long",day:"numeric"}),l=i.category?w(i.category):"#9e9e9e",s=o.slice(0,10);return`
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Rapport de Parcelle - ${i.reference_cadastrale||i.reference}</title>
        <style>
          * { margin: 0; padding: 0; box-sizing: border-box; }
          body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 40px;
            line-height: 1.6;
            color: #333;
          }
          .header {
            text-align: center;
            border-bottom: 3px solid #2196f3;
            padding-bottom: 20px;
            margin-bottom: 30px;
          }
          .header h1 {
            color: #2196f3;
            font-size: 28px;
            margin-bottom: 10px;
          }
          .header .subtitle {
            color: #666;
            font-size: 14px;
          }
          .section {
            margin-bottom: 30px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
            border-left: 4px solid #2196f3;
          }
          .section h2 {
            color: #2196f3;
            font-size: 20px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
          }
          .info-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
          }
          .info-item {
            display: flex;
            flex-direction: column;
          }
          .info-item .label {
            font-weight: 600;
            color: #666;
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 5px;
          }
          .info-item .value {
            color: #333;
            font-size: 16px;
          }
          .badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            color: white;
            font-weight: 500;
            font-size: 14px;
          }
          .map-placeholder {
            text-align: center;
            padding: 40px;
            background: #f0f0f0;
            border: 2px dashed #ccc;
            border-radius: 8px;
            margin: 20px 0;
          }
          .map-placeholder h3 {
            color: #666;
            margin-bottom: 15px;
          }
          .map-legend {
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-top: 15px;
          }
          .map-legend h3 {
            font-size: 14px;
            margin-bottom: 10px;
            color: #333;
          }
          .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
            font-size: 12px;
          }
          .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 4px;
            border: 2px solid #333;
          }
          .footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
            text-align: center;
            color: #999;
            font-size: 12px;
          }
          @media print {
            body { padding: 20px; }
            .no-print { display: none; }
          }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>\u{1F4CB} RAPPORT DE PARCELLE</h1>
          <div class="subtitle">
            Syst\xE8me d'Information Urbaine (SIU)<br>
            G\xE9n\xE9r\xE9 le ${a}
          </div>
        </div>

        <div class="section">
          <h2>\u{1F4CD} Informations G\xE9n\xE9rales</h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">R\xE9f\xE9rence cadastrale</span>
              <span class="value">${i.reference_cadastrale||i.reference||"N/A"}</span>
            </div>
            <div class="info-item">
              <span class="label">Adresse</span>
              <span class="value">${i.address||"Non renseign\xE9e"}</span>
            </div>
            <div class="info-item">
              <span class="label">Superficie</span>
              <span class="value">${i.area?B(i.area):"N/A"}</span>
            </div>
            <div class="info-item">
              <span class="label">Zone</span>
              <span class="value">${i.zone||"N/A"}</span>
            </div>
            <div class="info-item">
              <span class="label">Cat\xE9gorie</span>
              <span class="badge" style="background: ${l};">
                ${i.category||"N/A"}
              </span>
            </div>
            <div class="info-item">
              <span class="label">Statut</span>
              <span class="value">${this.getStatusLabel(i.status)}</span>
            </div>
          </div>
        </div>

        ${i.description?`
        <div class="section">
          <h2>\u{1F4DD} Description</h2>
          <p>${i.description}</p>
        </div>
        `:""}

        ${e?`
        <div class="section">
          <h2>\u{1F5FA}\uFE0F Carte G\xE9ographique avec Couches des Parcelles</h2>
          <div class="map-placeholder">
            <h3>\u{1F4CD} Carte des parcelles visibles</h3>
            <p>La parcelle s\xE9lectionn\xE9e est situ\xE9e aux coordonn\xE9es : ${n.toFixed(6)}, ${r.toFixed(6)}</p>
            <p>Cette carte affiche la parcelle principale en \xE9vidence ainsi que ${s.length} autres parcelles visibles dans le p\xE9rim\xE8tre.</p>
            <p><strong>Les couches de parcelles sont visibles sur la carte interactive dans l'application.</strong></p>
          </div>
          <div class="map-legend">
            <h3>\u{1F3A8} L\xE9gende</h3>
            <div class="legend-item">
              <div class="legend-color" style="background: ${t}; border-color: #000; border-width: 3px;"></div>
              <span><strong>Parcelle s\xE9lectionn\xE9e:</strong> ${i.reference_cadastrale||i.reference}</span>
            </div>
            <div class="legend-item">
              <div class="legend-color" style="background: rgba(128,128,128,0.4); border-color: #666;"></div>
              <span>Autres parcelles visibles (${s.length} parcelles affich\xE9es)</span>
            </div>
          </div>
          <p style="margin-top: 10px; color: #666; font-size: 12px;">
            \u{1F4CD} Pour voir la carte interactive avec toutes les couches, veuillez consulter l'application SIU.
          </p>
        </div>
        `:""}

        ${i.coordinates||i.coordinates_lat||i.latitude?`
        <div class="section">
          <h2>\u{1F4D0} Coordonn\xE9es GPS</h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">Latitude</span>
              <span class="value">${i.coordinates?.lat||i.coordinates_lat||i.latitude||"N/A"}</span>
            </div>
            <div class="info-item">
              <span class="label">Longitude</span>
              <span class="value">${i.coordinates?.lng||i.coordinates_lng||i.longitude||"N/A"}</span>
            </div>
          </div>
        </div>
        `:""}

        <div class="section">
          <h2>\u{1F4CA} Liste des Parcelles Visibles</h2>
          <p>Total des parcelles visibles dans le p\xE9rim\xE8tre : ${o.length}</p>
          <div style="max-height: 300px; overflow-y: auto; margin-top: 15px;">
            <table style="width: 100%; border-collapse: collapse;">
              <thead>
                <tr style="background: #e3f2fd;">
                  <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">R\xE9f\xE9rence</th>
                  <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Cat\xE9gorie</th>
                  <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Superficie</th>
                </tr>
              </thead>
              <tbody>
                ${s.map(c=>`
                  <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">${c.reference||"N/A"}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">
                      <span class="badge" style="background: ${c.color||"#9e9e9e"};">${c.category||"N/A"}</span>
                    </td>
                    <td style="border: 1px solid #ddd; padding: 8px;">${c.area?B(c.area):"N/A"}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>
        </div>

        <div class="footer">
          <p>Ce document a \xE9t\xE9 g\xE9n\xE9r\xE9 automatiquement par le Syst\xE8me d'Information Urbaine (SIU)</p>
          <p>Pour plus d'informations, consultez la plateforme en ligne</p>
        </div>
      </body>
      </html>
    `}generateParcelReportWithLayers(i,n=0,r=0,e=!1,t="#9e9e9e",o=[]){let a=new Date().toLocaleDateString("fr-FR",{year:"numeric",month:"long",day:"numeric"}),l=i.category?w(i.category):"#9e9e9e",s=o.map(c=>({id:c.id,reference:c.reference,category:c.category,coordinates:c.coordinates,geometry:c.geometry,color:c.category?w(c.category):"#9e9e9e"}));return`
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Rapport de Parcelle - ${i.reference_cadastrale||i.reference}</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"><\/script>
        <style>
          * { margin: 0; padding: 0; box-sizing: border-box; }
          body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 40px;
            line-height: 1.6;
            color: #333;
          }
          .header {
            text-align: center;
            border-bottom: 3px solid #2196f3;
            padding-bottom: 20px;
            margin-bottom: 30px;
          }
          .header h1 {
            color: #2196f3;
            font-size: 28px;
            margin-bottom: 10px;
          }
          .header .subtitle {
            color: #666;
            font-size: 14px;
          }
          .section {
            margin-bottom: 30px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
            border-left: 4px solid #2196f3;
          }
          .section h2 {
            color: #2196f3;
            font-size: 20px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
          }
          .info-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
          }
          .info-item {
            display: flex;
            flex-direction: column;
          }
          .info-item .label {
            font-weight: 600;
            color: #666;
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 5px;
          }
          .info-item .value {
            color: #333;
            font-size: 16px;
          }
          .badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            color: white;
            font-weight: 500;
            font-size: 14px;
          }
          .map-legend {
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-top: 15px;
          }
          .map-legend h3 {
            font-size: 14px;
            margin-bottom: 10px;
            color: #333;
          }
          .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
            font-size: 12px;
          }
          .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 4px;
            border: 2px solid #333;
          }
          .footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
            text-align: center;
            color: #999;
            font-size: 12px;
          }
          @media print {
            body { padding: 20px; }
            .no-print { display: none; }
          }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>\u{1F4CB} RAPPORT DE PARCELLE</h1>
          <div class="subtitle">
            Syst\xE8me d'Information Urbaine (SIU)<br>
            G\xE9n\xE9r\xE9 le ${a}
          </div>
        </div>

        <div class="section">
          <h2>\u{1F4CD} Informations G\xE9n\xE9rales</h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">R\xE9f\xE9rence cadastrale</span>
              <span class="value">${i.reference_cadastrale||i.reference||"N/A"}</span>
            </div>
            <div class="info-item">
              <span class="label">Adresse</span>
              <span class="value">${i.address||"Non renseign\xE9e"}</span>
            </div>
            <div class="info-item">
              <span class="label">Superficie</span>
              <span class="value">${i.area?B(i.area):"N/A"}</span>
            </div>
            <div class="info-item">
              <span class="label">Zone</span>
              <span class="value">${i.zone||"N/A"}</span>
            </div>
            <div class="info-item">
              <span class="label">Cat\xE9gorie</span>
              <span class="badge" style="background: ${l};">
                ${i.category||"N/A"}
              </span>
            </div>
            <div class="info-item">
              <span class="label">Statut</span>
              <span class="value">${this.getStatusLabel(i.status)}</span>
            </div>
          </div>
        </div>

        ${i.description?`
        <div class="section">
          <h2>\u{1F4DD} Description</h2>
          <p>${i.description}</p>
        </div>
        `:""}

        ${e?`
        <div class="section">
          <h2>\u{1F5FA}\uFE0F Carte G\xE9ographique avec Couches des Parcelles</h2>
          <div id="map-container" style="text-align: center; margin: 20px 0;">
            <div id="print-map" style="width: 100%; height: 600px; margin: 0 auto; border: 2px solid #2196f3; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></div>
            <div class="map-legend">
              <h3>\u{1F3A8} L\xE9gende</h3>
              <div class="legend-item">
                <div class="legend-color" style="background: ${t}; border-color: #000; border-width: 3px;"></div>
                <span><strong>Parcelle s\xE9lectionn\xE9e:</strong> ${i.reference_cadastrale||i.reference}</span>
              </div>
              <div class="legend-item">
                <div class="legend-color" style="background: rgba(128,128,128,0.4); border-color: #666;"></div>
                <span>Autres parcelles visibles (${o.length} parcelles affich\xE9es)</span>
              </div>
            </div>
            <p style="margin-top: 10px; color: #666; font-size: 12px;">
              \u{1F4CD} La carte affiche la parcelle s\xE9lectionn\xE9e en \xE9vidence ainsi que toutes les parcelles visibles dans le p\xE9rim\xE8tre
            </p>
          </div>
        </div>
        <script>
          // Donn\xE9es des parcelles
          const parcelsData = ${JSON.stringify(s)};
          const mainParcelId = '${i.id}';

          // Variables pour le suivi de l'\xE9tat
          let mapInitialized = false;

          console.log('\u{1F4CA} Parcelles \xE0 afficher:', parcelsData.length);
          console.log('\u{1F3AF} Parcelle principale:', mainParcelId);

          // Fonction pour attendre que Leaflet soit charg\xE9
          function waitForLeafletAndInitMap() {
            if (typeof L !== 'undefined' && typeof L.map !== 'undefined' && !mapInitialized) {
              // Leaflet est charg\xE9, initialisons la carte
              initMap();
            } else if (!mapInitialized) {
              // Leaflet n'est pas encore charg\xE9, attendons un peu plus
              setTimeout(waitForLeafletAndInitMap, 200);
            }
          }

          // Fonction d'initialisation de la carte
          function initMap() {
            try {
              // V\xE9rifier que l'\xE9l\xE9ment de la carte existe
              const mapElement = document.getElementById('print-map');
              if (!mapElement) {
                console.error('\u274C \xC9l\xE9ment de la carte introuvable');
                return;
              }

              // S'assurer que la carte a des dimensions
              mapElement.style.width = '100%';
              mapElement.style.height = '600px';

              var map = L.map('print-map', {
                center: [${n}, ${r}],
                zoom: 15,
                zoomControl: true,
                scrollWheelZoom: false,
                dragging: false,  // D\xE9sactiver le drag pour impression
                touchZoom: false,
                doubleClickZoom: false,
                boxZoom: false,
                keyboard: false,
                attributionControl: false  // D\xE9sactiver pour impression
              });

              L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '\xA9 OpenStreetMap contributors',
                maxZoom: 19
              }).addTo(map);

              var layersAdded = 0;
              var mainParcelAdded = false;

              // Ajouter les parcelles visibles comme couches (limiter \xE0 10 pour performance)
              const parcelsToAdd = parcelsData.slice(0, 10);
              console.log('\u{1F4CA} Parcelles \xE0 ajouter \xE0 la carte:', parcelsToAdd.length);

              parcelsToAdd.forEach(function(parcelData) {
                if (!parcelData.geometry) {
                  console.warn('\u26A0\uFE0F Parcelle sans g\xE9om\xE9trie:', parcelData.id);
                  return;
                }

                const isMainParcel = parcelData.id === mainParcelId;

                // Fonction pour convertir les coordonn\xE9es GeoJSON en format Leaflet
                function convertCoordinates(coords) {
                  if (!coords || !Array.isArray(coords)) return [];

                  // Si c'est un tableau de coordonn\xE9es simples [lng, lat]
                  if (coords.length >= 2 && typeof coords[0] === 'number' && typeof coords[1] === 'number') {
                    return [coords[1], coords[0]]; // [lat, lng]
                  }

                  // Si c'est un tableau de tableaux de coordonn\xE9es
                  return coords.map(function(coord) {
                    if (Array.isArray(coord)) {
                      if (coord.length >= 2 && typeof coord[0] === 'number' && typeof coord[1] === 'number') {
                        return [coord[1], coord[0]]; // [lat, lng]
                      } else if (Array.isArray(coord[0])) {
                        // Cas de polygones ou multipolygones - traiter r\xE9cursivement
                        return convertCoordinates(coord);
                      }
                    }
                    return coord;
                  });
                }

                try {
                  if (parcelData.geometry.type === 'Point') {
                    // Afficher comme marqueur
                    const markerOptions = {
                      radius: isMainParcel ? 15 : 8,
                      fillColor: isMainParcel ? '${t}' : parcelData.color,
                      fillOpacity: isMainParcel ? 0.9 : 0.6,
                      color: isMainParcel ? '#000' : '#666',
                      weight: isMainParcel ? 3 : 2
                    };

                    // Utiliser les coordonn\xE9es du point directement
                    const pointCoords = convertCoordinates(parcelData.geometry.coordinates);
                    if (pointCoords && pointCoords.length >= 2) {
                      L.circleMarker(pointCoords, markerOptions)
                        .addTo(map)
                        .bindPopup('\u{1F4CD} ' + parcelData.reference + (isMainParcel ? ' <strong>(S\xE9lectionn\xE9e)</strong>' : ''));

                      layersAdded++;
                      if (isMainParcel) mainParcelAdded = true;
                      console.log('\u2705 Marqueur ajout\xE9:', parcelData.reference, isMainParcel ? '(Principale)' : '');
                    }

                  } else if (parcelData.geometry.type === 'Polygon') {
                    // Afficher comme polygone
                    const polygonCoords = convertCoordinates(parcelData.geometry.coordinates[0]);

                    if (polygonCoords && polygonCoords.length > 0) {
                      const polygonOptions = {
                        fillColor: isMainParcel ? '${t}' : parcelData.color,
                        fillOpacity: isMainParcel ? 0.5 : 0.3,
                        color: isMainParcel ? '#000' : '#666',
                        weight: isMainParcel ? 3 : 1
                      };

                      L.polygon(polygonCoords, polygonOptions)
                        .addTo(map)
                        .bindPopup('\u{1F4CD} ' + parcelData.reference + (isMainParcel ? ' <strong>(S\xE9lectionn\xE9e)</strong>' : ''));

                      layersAdded++;
                      if (isMainParcel) mainParcelAdded = true;
                      console.log('\u2705 Polygone ajout\xE9:', parcelData.reference, isMainParcel ? '(Principale)' : '');
                    }

                  } else if (parcelData.geometry.type === 'MultiPolygon') {
                    // Afficher comme multi-polygone
                    parcelData.geometry.coordinates.forEach(function(polygonCoords) {
                      const convertedCoords = convertCoordinates(polygonCoords[0]);

                      if (convertedCoords && convertedCoords.length > 0) {
                        const polygonOptions = {
                          fillColor: isMainParcel ? '${t}' : parcelData.color,
                          fillOpacity: isMainParcel ? 0.5 : 0.3,
                          color: isMainParcel ? '#000' : '#666',
                          weight: isMainParcel ? 3 : 1
                        };

                        L.polygon(convertedCoords, polygonOptions)
                          .addTo(map)
                          .bindPopup('\u{1F4CD} ' + parcelData.reference + (isMainParcel ? ' <strong>(S\xE9lectionn\xE9e)</strong>' : ''));

                        layersAdded++;
                        if (isMainParcel) mainParcelAdded = true;
                      }
                    });

                    console.log('\u2705 MultiPolygone ajout\xE9:', parcelData.reference, isMainParcel ? '(Principale)' : '');
                  } else {
                    // Pour d'autres types de g\xE9om\xE9trie, essayer de cr\xE9er un layer g\xE9n\xE9rique
                    const layer = L.geoJSON(parcelData.geometry, {
                      pointToLayer: function(feature, latlng) {
                        const markerOptions = {
                          radius: isMainParcel ? 15 : 8,
                          fillColor: isMainParcel ? '${t}' : parcelData.color,
                          fillOpacity: isMainParcel ? 0.9 : 0.6,
                          color: isMainParcel ? '#000' : '#666',
                          weight: isMainParcel ? 3 : 2
                        };
                        return L.circleMarker(latlng, markerOptions);
                      },
                      style: function(feature) {
                        return {
                          fillColor: isMainParcel ? '${t}' : parcelData.color,
                          fillOpacity: isMainParcel ? 0.5 : 0.3,
                          color: isMainParcel ? '#000' : '#666',
                          weight: isMainParcel ? 3 : 1
                        };
                      }
                    }).addTo(map);

                    layer.bindPopup('\u{1F4CD} ' + parcelData.reference + (isMainParcel ? ' <strong>(S\xE9lectionn\xE9e)</strong>' : ''));

                    layersAdded++;
                    if (isMainParcel) mainParcelAdded = true;
                    console.log('\u2705 G\xE9om\xE9trie g\xE9n\xE9rique ajout\xE9e:', parcelData.reference, isMainParcel ? '(Principale)' : '');
                  }
                } catch (e) {
                  console.error('\u274C Erreur lors de l'ajout de la parcelle:', parcelData.id, e);
                }
              });

              // Si la parcelle principale n'a pas \xE9t\xE9 ajout\xE9e, ajouter un marqueur de secours
              if (!mainParcelAdded && ${n} !== 0 && ${r} !== 0) {
                console.log('\u26A0\uFE0F Ajout du marqueur de secours pour la parcelle principale');
                L.circleMarker([${n}, ${r}], {
                  radius: 15,
                  fillColor: '${t}',
                  fillOpacity: 0.9,
                  color: '#000',
                  weight: 3
                }).addTo(map)
                  .bindPopup('<strong>\u{1F4CD} Parcelle principale</strong><br>${i.reference_cadastrale||i.reference}')
                  .openPopup();
                layersAdded++;
              }

              console.log('\u2705 Total de couches ajout\xE9es:', layersAdded);

              // Forcer le redimensionnement
              setTimeout(function() {
                map.invalidateSize();
                mapInitialized = true;

                // Centrer la carte sur la zone d'int\xE9r\xEAt
                if (layersAdded > 0) {
                  // Cr\xE9er un groupe de couches pour ajuster la vue
                  const group = new L.featureGroup([]);

                  // Ajouter toutes les couches au groupe
                  map.eachLayer(function(layer) {
                    if (layer instanceof L.Marker || layer instanceof L.Polygon || layer instanceof L.Circle) {
                      group.addLayer(layer);
                    }
                  });

                  // Ajuster la vue sur le groupe
                  if (group.getLayers().length > 0) {
                    map.fitBounds(group.getBounds().pad(0.1));
                  }
                }
              }, 100);
            } catch (e) {
              console.error('\u274C Erreur lors de l'initialisation de la carte:', e);
              const mapElement = document.getElementById('print-map');
              if (mapElement) {
                mapElement.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;background:#f5f5f5;"><p>Carte non disponible - Erreur: ' + e.message + '</p></div>';
              }
            }
          }

          // D\xE9marrer le processus d'attente et d'initialisation
          setTimeout(waitForLeafletAndInitMap, 500);
        <\/script>
        `:""}

        ${i.coordinates||i.coordinates_lat||i.latitude?`
        <div class="section">
          <h2>\u{1F4D0} Coordonn\xE9es GPS</h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">Latitude</span>
              <span class="value">${i.coordinates?.lat||i.coordinates_lat||i.latitude||"N/A"}</span>
            </div>
            <div class="info-item">
              <span class="label">Longitude</span>
              <span class="value">${i.coordinates?.lng||i.coordinates_lng||i.longitude||"N/A"}</span>
            </div>
          </div>
        </div>
        `:""}

        <div class="footer">
          <p>Ce document a \xE9t\xE9 g\xE9n\xE9r\xE9 automatiquement par le Syst\xE8me d'Information Urbaine (SIU)</p>
          <p>Pour plus d'informations, consultez la plateforme en ligne</p>
        </div>
      </body>
      </html>
    `}generateParcelReport(i,n=null,r=0,e=0,t=!1,o="#9e9e9e"){let a=new Date().toLocaleDateString("fr-FR",{year:"numeric",month:"long",day:"numeric"}),l=i.category?w(i.category):"#9e9e9e";return`
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Rapport de Parcelle - ${i.reference_cadastrale||i.reference}</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"><\/script>
        <style>
          * { margin: 0; padding: 0; box-sizing: border-box; }
          body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 40px;
            line-height: 1.6;
            color: #333;
          }
          .header {
            text-align: center;
            border-bottom: 3px solid #2196f3;
            padding-bottom: 20px;
            margin-bottom: 30px;
          }
          .header h1 {
            color: #2196f3;
            font-size: 28px;
            margin-bottom: 10px;
          }
          .header .subtitle {
            color: #666;
            font-size: 14px;
          }
          .section {
            margin-bottom: 30px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
            border-left: 4px solid #2196f3;
          }
          .section h2 {
            color: #2196f3;
            font-size: 20px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
          }
          .info-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
          }
          .info-item {
            display: flex;
            flex-direction: column;
          }
          .info-item .label {
            font-weight: 600;
            color: #666;
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 5px;
          }
          .info-item .value {
            color: #333;
            font-size: 16px;
          }
          .badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            color: white;
            font-weight: 500;
            font-size: 14px;
          }
          .footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
            text-align: center;
            color: #999;
            font-size: 12px;
          }
          @media print {
            body { padding: 20px; }
            .no-print { display: none; }
          }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>\u{1F4CB} RAPPORT DE PARCELLE</h1>
          <div class="subtitle">
            Syst\xE8me d'Information Urbaine (SIU)<br>
            G\xE9n\xE9r\xE9 le ${a}
          </div>
        </div>

        <div class="section">
          <h2>\u{1F4CD} Informations G\xE9n\xE9rales</h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">R\xE9f\xE9rence cadastrale</span>
              <span class="value">${i.reference_cadastrale||i.reference||"N/A"}</span>
            </div>
            <div class="info-item">
              <span class="label">Adresse</span>
              <span class="value">${i.address||"Non renseign\xE9e"}</span>
            </div>
            <div class="info-item">
              <span class="label">Superficie</span>
              <span class="value">${i.area?B(i.area):"N/A"}</span>
            </div>
            <div class="info-item">
              <span class="label">Zone</span>
              <span class="value">${i.zone||"N/A"}</span>
            </div>
            <div class="info-item">
              <span class="label">Cat\xE9gorie</span>
              <span class="badge" style="background: ${l};">
                ${i.category||"N/A"}
              </span>
            </div>
            <div class="info-item">
              <span class="label">Statut</span>
              <span class="value">${this.getStatusLabel(i.status)}</span>
            </div>
          </div>
        </div>

        ${i.description?`
        <div class="section">
          <h2>\u{1F4DD} Description</h2>
          <p>${i.description}</p>
        </div>
        `:""}

        ${t?`
        <div class="section">
          <h2>\u{1F5FA}\uFE0F Localisation G\xE9ographique</h2>
          <div id="map-container" style="text-align: center; margin: 20px 0;">
            <div id="print-map" style="width: 800px; height: 600px; margin: 0 auto; border: 2px solid #2196f3; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></div>
            <p style="margin-top: 10px; color: #666; font-size: 12px;">
              \u{1F4CD} La parcelle est indiqu\xE9e sur la carte avec un marqueur color\xE9
            </p>
          </div>
        </div>
        <script>
          // Initialiser la carte apr\xE8s le chargement de Leaflet
          document.addEventListener('DOMContentLoaded', function() {
            if (typeof L !== 'undefined') {
              try {
                var map = L.map('print-map', {
                  center: [${r}, ${e}],
                  zoom: 16,
                  zoomControl: false,
                  scrollWheelZoom: false,
                  dragging: false
                });
                
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                  attribution: '\xA9 OpenStreetMap',
                  maxZoom: 19
                }).addTo(map);
                
                L.circleMarker([${r}, ${e}], {
                  radius: 15,
                  fillColor: '${o}',
                  fillOpacity: 0.8,
                  color: '#000',
                  weight: 3
                }).addTo(map).bindPopup('\u{1F4CD} Parcelle ${i.reference_cadastrale||i.reference}');
                
                // Forcer le redimensionnement
                setTimeout(function() {
                  map.invalidateSize();
                }, 100);
              } catch (e) {
                console.error('Error initializing map:', e);
                document.getElementById('print-map').innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;background:#f5f5f5;"><p>Carte non disponible</p></div>';
              }
            }
          });
        <\/script>
        `:""}

        ${i.coordinates||i.coordinates_lat||i.latitude?`
        <div class="section">
          <h2>\u{1F4D0} Coordonn\xE9es GPS</h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">Latitude</span>
              <span class="value">${i.coordinates?.lat||i.coordinates_lat||i.latitude||"N/A"}</span>
            </div>
            <div class="info-item">
              <span class="label">Longitude</span>
              <span class="value">${i.coordinates?.lng||i.coordinates_lng||i.longitude||"N/A"}</span>
            </div>
          </div>
        </div>
        `:""}

        <div class="footer">
          <p>Ce document a \xE9t\xE9 g\xE9n\xE9r\xE9 automatiquement par le Syst\xE8me d'Information Urbaine (SIU)</p>
          <p>Pour plus d'informations, consultez la plateforme en ligne</p>
        </div>
      </body>
      </html>
    `}onParcelClick(i,n){this.mapStateService.selectParcel(i,n),this.updateAllLayerStyles()}updateLayerStyle(i){let n=i.feature;if(n){let r=this.getParcelStyle(n);i.setStyle(r)}}updateAllLayerStyles(){this.loadedParcelsCache.forEach(i=>{i.setStyle&&this.updateLayerStyle(i)})}enableClustering(){!this.map||!this.clusterGroup||!this.parcelLayer||(this.parcelLayer.eachLayer(i=>{this.clusterGroup.addLayer(i)}),this.parcelLayer.clearLayers(),this.map.addLayer(this.clusterGroup))}disableClustering(){!this.map||!this.clusterGroup||!this.parcelLayer||(this.clusterGroup.eachLayer(i=>{this.parcelLayer.addLayer(i)}),this.clusterGroup.clearLayers(),this.map.removeLayer(this.clusterGroup))}updateGeometrySimplification(){if(this.map){let i=this.map.getBounds();this.viewportService.updateViewport(i,this.map.getZoom())}}syncUrlWithState(){let i=this.mapStateService.getStateAsUrlParams(),n=this.router.createUrlTree([],{relativeTo:this.route,queryParams:{}}).toString();window.history.replaceState({},"",n)}toggleFullscreen(){document.fullscreenElement?document.exitFullscreen():this.mapContainer.nativeElement.requestFullscreen()}changeBasemap(i){if(!this.map)return;let n=this.mapState().activeBasemap;this.baseLayers[n]&&this.map.removeLayer(this.baseLayers[n]),this.baseLayers[i]&&this.baseLayers[i].addTo(this.map),this.mapStateService.setBasemap(i)}getStatusLabel(i){return{available:"Disponible",occupied:"Occup\xE9",disputed:"Contest\xE9",reserved:"R\xE9serv\xE9"}[i]||i}refresh(){if(this.loadedParcelsCache.clear(),this.currentlyVisibleIds.clear(),this.map){let i=this.map.getBounds();this.viewportService.updateViewport(i,this.map.getZoom())}}initCategoryColors(){this.legendCategories().forEach(i=>{i.items.forEach(n=>{this.categoryColors.set(n.id,w(n.id))})})}onLegendItemVisibilityChanged(i){this.loadedParcelsCache.forEach((n,r)=>{let e=n.feature;if(e){let t=e.properties,o=t.status,a=t.category;(i.itemId===o||i.itemId===a)&&(i.visible?this.parcelLayer?.hasLayer(n)||this.parcelLayer?.addLayer(n):this.parcelLayer?.removeLayer(n))}}),i.itemId==="all"&&this.loadedParcelsCache.forEach(n=>{i.visible?this.parcelLayer?.hasLayer(n)||this.parcelLayer?.addLayer(n):this.parcelLayer?.removeLayer(n)})}updateLegendCounts(i){let n={},r=new Set;i.features.forEach(o=>{let a=o.properties.status,l=o.properties.category;a&&(n[a]=(n[a]||0)+1),l&&(n[l]=(n[l]||0)+1,r.add(l))});let e=Array.from(r).sort((o,a)=>(n[a]||0)-(n[o]||0)).map(o=>({id:o,label:o,color:w(o),visible:!0,count:n[o]||0})),t=[{name:"Statut des parcelles",items:[{id:"available",label:"Disponible",color:"#4caf50",icon:"check_circle",visible:!0,count:n.available||0},{id:"occupied",label:"Occup\xE9",color:"#2196f3",icon:"home",visible:!0,count:n.occupied||0},{id:"disputed",label:"Contest\xE9",color:"#f44336",icon:"warning",visible:!0,count:n.disputed||0},{id:"reserved",label:"R\xE9serv\xE9",color:"#ff9800",icon:"lock",visible:!0,count:n.reserved||0}]},{name:"Cat\xE9gories",items:e}];this.legendCategories.set(t)}static{this.\u0275fac=function(n){return new(n||d)}}static{this.\u0275cmp=W({type:d,selectors:[["app-map-view"]],viewQuery:function(n,r){if(n&1&&ye(dt,7),n&2){let e;Me(e=xe())&&(r.mapContainer=e.first)}},decls:7,vars:6,consts:[["mapContainer",""],[1,"map-view-container"],["mode","determinate",1,"loading-bar",3,"value"],[1,"map-container"],[1,"map-controls"],[1,"loading-overlay"],[3,"categories"],[1,"controls-top-left"],["mat-mini-fab","","color","primary",1,"control-button",3,"click","matTooltip"],["mat-mini-fab","","color","primary","matTooltip","Actualiser",1,"control-button",3,"click","disabled"],[1,"controls-top-right"],[1,"basemap-selector"],["mat-mini-fab","","color","primary","matTooltip","OpenStreetMap",1,"control-button",3,"click"],["mat-mini-fab","","color","primary","matTooltip","Satellite",1,"control-button",3,"click"],[1,"controls-bottom"],[1,"map-stats"],[1,"stat-item"],[1,"stat-item","selected"],["diameter","60"],[3,"itemVisibilityChanged","categories"]],template:function(n,r){n&1&&(p(0,"div",1),E(1,ht,1,1,"mat-progress-bar",2),U(2,"div",3,0),E(4,ut,27,10,"div",4),E(5,mt,4,0,"div",5),E(6,gt,1,1,"app-map-legend",6),u()),n&2&&(N("fullscreen",r.isFullscreen()),m(),S(r.loading()?1:-1),m(3),S(r.showControls()?4:-1),m(),S(r.loading()&&!r.mapReady()?5:-1),m(),S(r.showLegend()&&r.mapReady()?6:-1))},dependencies:[J,$e,Be,X,ze,Q,K,te,ee,Ue,Re,Ae,re],styles:[".map-view-container[_ngcontent-%COMP%]{position:relative;width:100%;height:100vh;overflow:hidden}.map-view-container.fullscreen[_ngcontent-%COMP%]{position:fixed;inset:0;z-index:9999}.map-container[_ngcontent-%COMP%]{width:100%;height:100%;position:relative;z-index:1}.map-container   [_nghost-%COMP%]     .leaflet-container{font-family:inherit}.map-container   [_nghost-%COMP%]     .leaflet-popup-content{margin:0;padding:0}.map-container   [_nghost-%COMP%]     .parcel-popup{padding:1rem;min-width:250px}.map-container   [_nghost-%COMP%]     .parcel-popup h3{margin:0 0 .75rem;font-size:1.1rem;font-weight:500;color:#333}.map-container   [_nghost-%COMP%]     .parcel-popup p{margin:.5rem 0;font-size:.9rem;color:#666}.map-container   [_nghost-%COMP%]     .parcel-popup p strong{color:#333;font-weight:500}.map-container   [_nghost-%COMP%]     .parcel-popup button{margin-top:1rem;padding:.5rem 1rem;background-color:#673ab7;color:#fff;border:none;border-radius:4px;cursor:pointer;font-size:.9rem;font-weight:500;transition:background-color .2s}.map-container   [_nghost-%COMP%]     .parcel-popup button:hover{background-color:#5e35b1}.map-container   [_nghost-%COMP%]     .marker-cluster{background-color:#673ab799;border:2px solid rgba(103,58,183,.8)}.map-container   [_nghost-%COMP%]     .marker-cluster div{background-color:#673ab7cc;color:#fff;font-weight:600}.map-container   [_nghost-%COMP%]     .marker-cluster-small{background-color:#4caf5099}.map-container   [_nghost-%COMP%]     .marker-cluster-small div{background-color:#4caf50cc}.map-container   [_nghost-%COMP%]     .marker-cluster-medium{background-color:#ff980099}.map-container   [_nghost-%COMP%]     .marker-cluster-medium div{background-color:#ff9800cc}.map-container   [_nghost-%COMP%]     .marker-cluster-large{background-color:#f4433699}.map-container   [_nghost-%COMP%]     .marker-cluster-large div{background-color:#f44336cc}.loading-bar[_ngcontent-%COMP%]{position:absolute;top:0;left:0;right:0;z-index:1000}.map-controls[_ngcontent-%COMP%]{position:absolute;inset:0;pointer-events:none;z-index:400;padding:1rem}.map-controls[_ngcontent-%COMP%] > *[_ngcontent-%COMP%]{pointer-events:auto}.controls-top-left[_ngcontent-%COMP%]{position:absolute;top:1rem;left:1rem;display:flex;flex-direction:column;gap:.5rem}.controls-top-right[_ngcontent-%COMP%]{position:absolute;top:1rem;right:1rem;display:flex;flex-direction:column;gap:.5rem}.controls-bottom[_ngcontent-%COMP%]{position:absolute;bottom:1rem;left:50%;transform:translate(-50%)}.control-button[_ngcontent-%COMP%]{box-shadow:0 2px 4px #0003!important;transition:all .2s ease}.control-button[_ngcontent-%COMP%]:hover:not(:disabled){box-shadow:0 4px 8px #0000004d!important;transform:translateY(-2px)}.control-button[_ngcontent-%COMP%]:disabled{opacity:.5;cursor:not-allowed}.control-button.active[_ngcontent-%COMP%]{background-color:#5e35b1!important}.control-button[_ngcontent-%COMP%]   mat-icon[_ngcontent-%COMP%]{color:#fff}.basemap-selector[_ngcontent-%COMP%]{display:flex;flex-direction:column;gap:.5rem}.map-stats[_ngcontent-%COMP%]{background:#fffffff2;-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);padding:.75rem 1.5rem;border-radius:24px;box-shadow:0 2px 8px #00000026;display:flex;gap:1.5rem;align-items:center}.map-stats[_ngcontent-%COMP%]   .stat-item[_ngcontent-%COMP%]{display:flex;align-items:center;gap:.5rem;font-size:.9rem;font-weight:500;color:#333}.map-stats[_ngcontent-%COMP%]   .stat-item[_ngcontent-%COMP%]   mat-icon[_ngcontent-%COMP%]{font-size:18px;width:18px;height:18px;color:#673ab7}.map-stats[_ngcontent-%COMP%]   .stat-item.selected[_ngcontent-%COMP%]{color:#673ab7;font-weight:600}.map-stats[_ngcontent-%COMP%]   .stat-item.selected[_ngcontent-%COMP%]   mat-icon[_ngcontent-%COMP%]{color:#673ab7}.loading-overlay[_ngcontent-%COMP%]{position:absolute;inset:0;background:#ffffffe6;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:1001;gap:1rem}.loading-overlay[_ngcontent-%COMP%]   p[_ngcontent-%COMP%]{margin:0;font-size:1rem;color:#666}@media(max-width:768px){.map-controls[_ngcontent-%COMP%]{padding:.5rem}.controls-top-left[_ngcontent-%COMP%], .controls-top-right[_ngcontent-%COMP%]{top:.5rem}.controls-top-left[_ngcontent-%COMP%]{left:.5rem}.controls-top-right[_ngcontent-%COMP%]{right:.5rem}.controls-bottom[_ngcontent-%COMP%]{bottom:.5rem;left:.5rem;right:.5rem;transform:none}.map-stats[_ngcontent-%COMP%]{padding:.5rem 1rem;flex-direction:column;gap:.5rem;align-items:flex-start;width:100%}.map-stats[_ngcontent-%COMP%]   .stat-item[_ngcontent-%COMP%]{font-size:.85rem}.control-button[_ngcontent-%COMP%]{width:40px!important;height:40px!important}.control-button[_ngcontent-%COMP%]   mat-icon[_ngcontent-%COMP%]{font-size:20px;width:20px;height:20px}}@media(prefers-color-scheme:dark){.map-stats[_ngcontent-%COMP%]{background:#212121f2;color:#ffffffde}.map-stats[_ngcontent-%COMP%]   .stat-item[_ngcontent-%COMP%]{color:#ffffffde}.map-stats[_ngcontent-%COMP%]   .stat-item[_ngcontent-%COMP%]   mat-icon[_ngcontent-%COMP%]{color:#b39ddb}.map-stats[_ngcontent-%COMP%]   .stat-item.selected[_ngcontent-%COMP%]{color:#b39ddb}.map-stats[_ngcontent-%COMP%]   .stat-item.selected[_ngcontent-%COMP%]   mat-icon[_ngcontent-%COMP%]{color:#b39ddb}.loading-overlay[_ngcontent-%COMP%]{background:#212121e6}.loading-overlay[_ngcontent-%COMP%]   p[_ngcontent-%COMP%]{color:#ffffffde}[_nghost-%COMP%]     .parcel-popup{background-color:#2a2a2a}[_nghost-%COMP%]     .parcel-popup h3{color:#ffffffde}[_nghost-%COMP%]     .parcel-popup p{color:#fff9}[_nghost-%COMP%]     .parcel-popup p strong{color:#ffffffde}[_nghost-%COMP%]     .parcel-popup button{background-color:#7e57c2}[_nghost-%COMP%]     .parcel-popup button:hover{background-color:#9575cd}}@media print{.map-controls[_ngcontent-%COMP%], .loading-bar[_ngcontent-%COMP%], .loading-overlay[_ngcontent-%COMP%]{display:none!important}.map-view-container[_ngcontent-%COMP%]{height:100%;page-break-inside:avoid}}@keyframes _ngcontent-%COMP%_fadeIn{0%{opacity:0}to{opacity:1}}.control-button[_ngcontent-%COMP%], .map-stats[_ngcontent-%COMP%]{animation:_ngcontent-%COMP%_fadeIn .3s ease-in}[_ngcontent-%COMP%]:focus-visible{outline:2px solid #673ab7;outline-offset:2px}.map-container[_ngcontent-%COMP%]{will-change:transform}@media(hover:none)and (pointer:coarse){.control-button[_ngcontent-%COMP%]{min-width:48px!important;min-height:48px!important}}"],changeDetection:0})}};export{qe as MapViewComponent};
