import "leaflet-easybutton";
import React from "react";
import { Col, Row, Container } from "react-bootstrap";
import { useHistory, withRouter } from "react-router-dom";
import "./App.css";
import "leaflet-easybutton";
import axios from "axios";
import file from "./file.json";
import blueIconpng from "./blueIcon.png";
import redIconpng from "./redIcon.png";

// import JSON from "json";
// import * as L from "leaflet/dist/leaflet";

let police_tweets;
let pyrosvestiki_tweets;

// This line takes leaflet from the index.html declaration
let L = window.L;

let LeafletMap = (props) => {
  let history = useHistory();
  let [mapState, setMapState] = React.useState();

  React.useEffect(() => {
    const home = {
      lat: 38.505,
      lng: 23.91,
      zoom: 6.5,
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

    const Google_Satellite = L.tileLayer(
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

    const HumanitarianMap = L.tileLayer(
      "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png",
      {
        maxZoom: 20,
        maxNativeZoom: 19,
        attribution:
          "© OpenStreetMap Contributors. Tiles courtesy of Humanitarian OpenStreetMap Teams",
      }
    );
    const WaterColorMap = L.tileLayer(
      // "http://c.tile.stamen.com/watercolor/${z}/${x}/${y}.jpg",
      "https://stamen-tiles.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.png",
      {
        maxZoom: 20,
        maxNativeZoom: 19,
        attribution:
          'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>',
      }
    );

    const TonerMap = L.tileLayer(
      // "http://c.tile.stamen.com/watercolor/${z}/${x}/${y}.jpg",
      "https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png",
      {
        maxZoom: 20,
        maxNativeZoom: 19,
        attribution:
          'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.',
      }
    );

    let map = new L.map("mapid", { zoomControl: false, cursor: true });
    map.setView([home.lat, home.lng], home.zoom, false);

    OpenStreetMap.addTo(map);

    const basemaps = {
      OpenStreetMap: OpenStreetMap,
      HumanitarianMap: HumanitarianMap,
      "Toner Map": TonerMap,
      OpenTopoMap: OpenTopoMap,
      "Water Color Map": WaterColorMap,
      "Google Satellite": Google_Satellite,
    };
    var blueIcon = L.icon({
        iconUrl: blueIconpng,
        shadowUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
        iconSize:[40, 40],
        iconAnchor:  [0, 0],
        shadowAnchor: [-8,0]
    });

    var redIcon = L.icon({
        iconUrl: redIconpng,
        shadowUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
        iconSize:[40, 40],
        iconAnchor:  [0, 0],
        shadowAnchor: [-8,0]
    });

    // let a = L.geoJSON(file, {
    //     pointToLayer: function(feature, latlng) {
    //         return blueIcon(latlng);
    //     }
    // }        
    // );
    // a.addTo(map);

    L.geoJson(file, {
        pointToLayer: function (feature, latlng) {
            return L.marker(latlng, {icon: redIcon});
        }}, { 
        onEachFeature: function (feature, layer) {
        layer.bindPopup(feature.properties.text);
        }
    }).addTo(map);

    // axios.get("/GetLayer_Police").then(function (response) {
    //     console.log(response.data);
    //     police_tweets = L.geoJSON(response.data,{
    //         style: {fillColor: "#1111d8"}
    //     });

    //     police_tweets.addTo(map);

    //     axios.get("/GetLayer_Pyrosvestiki").then(function (response) {
    //         console.log(response.data);
    //         pyrosvestiki_tweets = L.geoJSON(response.data, {
    //             style: {fillColor: "#ca1c20"}
    //         });

    //         pyrosvestiki_tweets.addTo(map);
    //         const overlaymaps = {
    //             "Tweets: Hellenic Fire Department": pyrosvestiki_tweets,
    //             "Tweets: Hellenic Police": police_tweets
    //         };
    //         L.control.layers(basemaps,overlaymaps).addTo(map);
    //     });
    // });

    L.control.zoom({ position: "topleft" }).addTo(map);

    // map.setMaxBounds(map.getBounds());

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
    let marker = L.marker([38.2, 23.23])
      .bindPopup(
        `<blockquote class="twitter-tweet" data-theme="dark"><p lang="el" dir="ltr">❗Περισσότερα από 67 κιλά κάνναβης κατασχέθηκαν από αστυνομικούς της Διεύθυνσης Αστυνομίας Ορεστιάδας σε παρέβρια περιοχή του Έβρου.<br>👉<a href="https://t.co/K4MkPuiAVI">https://t.co/K4MkPuiAVI</a> <a href="https://t.co/zVLMGR2VCC">pic.twitter.com/zVLMGR2VCC</a></p>&mdash; Ελληνική Αστυνομία (@hellenicpolice) <a href="https://twitter.com/hellenicpolice/status/1494387434112655362?ref_src=twsrc%5Etfw">February 17, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> `
      )
      .addTo(map);

    let position = new Position();
    map.addControl(position);
    map.addEventListener("mousemove", (event) => {
      let lat = Math.round(event.latlng.lat * 100000) / 100000;
      let lng = Math.round(event.latlng.lng * 100000) / 100000;
      position.updateHTML(lat, lng);
    });
    L.control
      .scale({
        metric: true,
        imperial: true,
        position: "bottomleft",
        maxWidth: 100,
      })
      .addTo(map);

    setMapState(map);
  }, []);

  return (
    <div id="mapMainContainer" style={{ position: "relative" }}>
      <div id="mapid"></div>
    </div>
  );
};

export default LeafletMap;
