import "leaflet-easybutton";
import React from "react";
import { Col, Row, Container } from "react-bootstrap";
import {useHistory} from "react-router-dom";
import "./App.css";
import "leaflet-easybutton";
// import * as L from "leaflet/dist/leaflet";

// This line takes leaflet from the index.html declaration
let L = window.L;

let LeafletMap = (props) => {
    let history = useHistory();
    let [mapState, setMapState] = React.useState();

    React.useEffect(() => {
        const home = {
            lat: 38.505,
            lng: 23.91,
            zoom: 6
        };
        const OpenStreetMap = L.tileLayer(
            "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            {
                maxZoom: 20,
                maxNativeZoom: 19,
                attribution:
                '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            }
            );
            
        const Google_Terrain = L.tileLayer(
            "http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            {
                maxZoom: 20,
                maxNativeZoom: 19,
                subdomains: ["mt0", "mt1", "mt2", "mt3"],
            }
            );
            
        const OpenTopoMap = L.tileLayer(
            "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
            {
                maxZoom: 20,
                maxNativeZoom: 19,
                attribution:
                'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
            }
            );
                
        let map = new L.map("mapid", {zoomControl: false, cursor: true});
        map.setView([home.lat, home.lng], home.zoom, false);
        
        OpenStreetMap.addTo(map);

        const basemaps = {
            OpenStreetMap: OpenStreetMap,
            "Google Terrain": Google_Terrain,
            OpenTopoMap: OpenTopoMap,
        };
        L.control.layers(basemaps).addTo(map);
        L.control.zoom({ position: "topleft" }).addTo(map);
        
        L.easyButton(
            "fa-home",
            function (btn, map) {
                map.setView([home.lat, home.lng], home.zoom);
            },
            "Initial View"
        ).addTo(map);
            
            
            let Position = L.Control.extend({
                _container: null,
                options: {
                    position: "bottomleft",
                },
                
                onAdd: function (map) {
                    var latlng = L.DomUtil.create("div", "mouseposition");
                    this._latlng = latlng;
                    return latlng;
                },
                
                updateHTML: function (lat, lng) {
                    this._latlng.innerHTML = "lat: " + lat + " lon: " + lng;
                    this._latlng.style.border = "2px solid #777";
                    this._latlng.style.borderTop = "none";
                    this._latlng.style.background = "rgba(255,255,255,0.5)";
                    this._latlng.style.padding = "0px 5px 0px";
                    this._latlng.style.left = "-3%";
                    this._latlng.style.marginTop = "-2.5%";
                },
            });
            
            let position = new Position();
            map.addControl(position);   
            map.addEventListener("mousemove", (event) => {
                let lat = Math.round(event.latlng.lat * 100000) / 100000;
                let lng = Math.round(event.latlng.lng * 100000) / 100000;
                position.updateHTML(lat, lng);
            });
            L.control.scale({metric: true, imperial: true, position: "bottomleft",maxWidth: 100}).addTo(map);
            
            setMapState(map);
        }, []);
        
        return(
        <div id="mapMainContainer" style={{ position: "relative" }}>
            <div id="mapid"></div>
        </div>
    );
}

export default LeafletMap;